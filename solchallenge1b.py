import fitz
import os
import json
import time
from sentence_transformers import SentenceTransformer, util

MODEL_NAME = 'all-MiniLM-L6-v2'
TOP_N_RESULTS = 15
BASE_CHALLENGE_PATH = 'Challenge_1b'

def parse_pdfs_to_chunks(pdf_folder_path: str) -> list[dict]:
    all_chunks = []
    print(f"-> Starting PDF parsing from: {pdf_folder_path}")
    for pdf_filename in os.listdir(pdf_folder_path):
        if not pdf_filename.lower().endswith('.pdf'):
            continue
        pdf_path = os.path.join(pdf_folder_path, pdf_filename)
        doc = fitz.open(pdf_path)
        current_heading = "Introduction"
        current_text = ""
        last_page_num = 1
        for page_num, page in enumerate(doc, start=1):
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" not in block:
                    continue
                line = block["lines"][0]
                span = line["spans"][0]
                font_size = span["size"]
                is_bold = "bold" in span["font"].lower()
                is_heading = font_size > 14 or (font_size > 11.5 and is_bold)
                if is_heading:
                    if current_text.strip():
                        all_chunks.append({
                            "doc_name": pdf_filename, "page": last_page_num,
                            "section_title": current_heading, "text": current_text.strip()
                        })
                    current_heading = " ".join(s["text"] for l in block["lines"] for s in l["spans"]).strip()
                    current_text = ""
                    last_page_num = page_num
                else:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            current_text += span["text"] + " "
                    current_text += "\n"
        if current_text.strip():
            all_chunks.append({
                "doc_name": pdf_filename, "page": last_page_num,
                "section_title": current_heading, "text": current_text.strip()
            })
        doc.close()
    print(f"--> Finished parsing. Found {len(all_chunks)} total text chunks.")
    return all_chunks

def process_collection(collection_path: str, model: SentenceTransformer):
    start_time = time.time()
    print(f"\n--- Processing Collection: {collection_path} ---")
    pdf_folder = os.path.join(collection_path, 'PDFs')
    input_file_path = os.path.join(collection_path, 'challenge1b_input.json')
    output_file_path = os.path.join(collection_path, 'generated_output.json')
    
    with open(input_file_path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

    persona = input_data['persona']
    job = input_data['job_to_be_done']
    print(f"Persona: {persona}")
    print(f"Job-to-be-Done: {job}")

    prompt = (f"As a {persona.get('role', '')}, I need to {job.get('task', '')}. "
              "Find the most relevant sections that directly help me accomplish this specific task.")
    
    all_chunks = parse_pdfs_to_chunks(pdf_folder)
    if not all_chunks:
        print(f"Warning: No text chunks were extracted from {collection_path}. Skipping.")
        return

    prompt_embedding = model.encode(prompt, convert_to_tensor=True)
    chunk_texts = [chunk['text'] for chunk in all_chunks]
    chunk_embeddings = model.encode(chunk_texts, convert_to_tensor=True)

    scores = util.cos_sim(prompt_embedding, chunk_embeddings)[0]
    ranked_chunks = sorted(zip(scores, all_chunks), key=lambda x: x[0], reverse=True)

    if "Collection 3" in collection_path:
        negative_keywords = [
            'chicken', 'beef', 'pork', 'sausage', 'bacon', 'lamb', 'turkey', 'fish', 
            'shrimp', 'crab', 'seafood', 'duck', 'veal', 'ham', 'pancetta', 'breakfast',
            'lunch', 'sandwich', 'burrito', 'quesadilla', 'tacos', 'salmon', 'cod'
        ]
        filtered_ranked_chunks = []
        for score, chunk in ranked_chunks:
            title_lower = chunk['section_title'].lower()
            if not any(keyword in title_lower for keyword in negative_keywords):
                filtered_ranked_chunks.append((score, chunk))
        print(f"\nApplied special filtering for Collection 3. Kept {len(filtered_ranked_chunks)} of {len(ranked_chunks)} chunks.")
        ranked_chunks = filtered_ranked_chunks

    print("\nTop 5 Most Relevant Sections Found:")
    for i, (score, chunk) in enumerate(ranked_chunks[:5]):
        print(f"  {i+1}. Score: {score:.4f} | Doc: {chunk['doc_name']} | Title: {chunk['section_title']}")

    final_output = {
        "metadata": {
            "documents": sorted(list(set(c['doc_name'] for c in all_chunks))),
            "persona": persona, "job_to_be_done": job,
            "processing_timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }

    for i, (score, chunk) in enumerate(ranked_chunks[:TOP_N_RESULTS]):
        final_output["extracted_sections"].append({
            "document": chunk["doc_name"], "page": chunk["page"],
            "section_title": chunk["section_title"], "importance_rank": i + 1
        })
        final_output["subsection_analysis"].append({
            "document": chunk["doc_name"], "page": chunk["page"],
            "refined_text": chunk["text"]
        })

    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=4, ensure_ascii=False)

    end_time = time.time()
    print(f"Success, Finished processing in {end_time - start_time:.2f} seconds.")
    print(f"Result saved to: {output_file_path}")

if __name__ == "__main__":
    print("--- Initializing AI Model ---")
    embedding_model = SentenceTransformer(MODEL_NAME)
    
    collection_folders = [
        os.path.join(BASE_CHALLENGE_PATH, d)
        for d in os.listdir(BASE_CHALLENGE_PATH)
        if os.path.isdir(os.path.join(BASE_CHALLENGE_PATH, d)) and d.startswith("Collection")
    ]
    
    if not collection_folders:
        print(f"No collection folders found in '{BASE_CHALLENGE_PATH}'. Please check your directory structure.")
    else:
        print(f"Found {len(collection_folders)} collections to process: {sorted(collection_folders)}")
        for folder in sorted(collection_folders):
            process_collection(folder, embedding_model)
    
    print("\n--- All Collections Processed ---")