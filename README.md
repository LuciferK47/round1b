📄 Adobe India Hackathon 2025 - Challenge 1B: Persona-Driven Document Intelligence


Overview
This solution is designed for Challenge 1B of the Adobe India Hackathon 2025. It builds an intelligent offline system that analyzes PDF documents and extracts the most relevant sections based on a specific user persona and their job-to-be-done.

The output is a ranked, structured JSON file containing the top extracted insights tailored to the persona’s intent. The system is efficient, offline-capable, and compliant with all hackathon constraints.

Key Features
🧠 Semantic Understanding of PDFs
Intelligent parsing that understands headings, sections, and text emphasis using font properties.

🎯 Persona-Centric Relevance Ranking
Dynamic prompt generation using persona and job-to-be-done context for more targeted extraction.

⚖️ Rule-Based Filtering
Applies keyword-based filtering to enhance accuracy in highly specific use cases (e.g., vegetarian-only constraints).

⚡ Fast & Lightweight
Processes each collection in <15 seconds using a model of only ~80MB. Entirely CPU-based.

🔌 Offline-Ready
Requires no internet after initial setup.

Methodology & Pipeline
The entire workflow is implemented in solchallenge1b.py and follows a modular pipeline:

a. Collection Discovery
Automatically scans the Challenge_1b/ folder for subfolders named:

Collection 1

Collection 2

Collection 3

...etc.

Each collection is processed sequentially without manual input.

b. Input Parsing
Parses challenge1b_input.json from each collection to extract:

persona

job_to_be_done

This input forms the core query for downstream semantic ranking.

c. PDF Chunking (Semantic Sectioning)
Uses PyMuPDF to:

Detect headings using font size & boldness.

Group surrounding paragraphs into logical chunks.

Produces clean, semantically relevant sections.

d. Semantic Embedding & Ranking
Embeds each chunk and prompt using:

Model: all-MiniLM-L6-v2 (from Sentence Transformers)

Computes cosine similarity between prompt and chunk embeddings. Ranks all chunks by descending similarity score.

e. Rule-Based Post-Filtering
Applied in specialized tasks (e.g., vegetarian food):

Filters out chunks with keywords like: chicken, pork, beef, breakfast, etc.

Ensures precision in sensitive contexts.

f. JSON Output Generation
For each collection:

Selects top 15 ranked chunks.

Saves structured output in: Challenge_1b/Collection {n}/generated_output.json

Output includes:

metadata

extracted_sections (with importance_rank)

subsection_analysis

🧰 Models & Libraries Used
Component

Tool / Model

Embeddings

all-MiniLM-L6-v2 (~80MB)

Transformer Framework

sentence-transformers, torch

PDF Parsing

PyMuPDF (fitz)

🔧 How to Run
Step 1: Install Dependencies
pip install sentence-transformers torch PyMuPDF

Step 2: Run the Script
Navigate to project root (Adobe-India-Hackathon25-main - Copy/) and run:

python Challenge_1b/solchallenge1b.py

That’s it! Output files will be saved automatically in each Collection folder.

✅ Constraint Compliance Checklist
Constraint

Status

Details

CPU-Only Execution

✅ Compliant

No GPU required

Model Size ≤ 1 GB

✅ Compliant

Model size: ~80MB

Runtime ≤ 60 seconds

✅ Compliant

Typically ~15s per collection

Offline Capability

✅ Compliant

No network calls after first run

📁 Folder Structure
Adobe-India-Hackathon25-main - Copy/
└── Challenge_1b/
    ├── Collection 1/
    │   ├── challenge1b_input.json
    │   └── *.pdf
    ├── Collection 2/
    │   ├── ...
    └── solchallenge1b.py

📌 Example Prompt
Persona: "Food Contractor"
Job: "Plan vegetarian dinner meals"

🔁 Semantic prompt generated dynamically:
"As a Food Contractor, I need to plan vegetarian dinner meals for a group..."

📣 Final Notes
This project demonstrates a hybrid AI + rule-based pipeline that is:

Modular

Efficient

Persona-aware

Offline-compliant

It’s designed to serve real-world document intelligence use-cases with high accuracy under strict performance constraints.

👨‍💻 Authors
Team Adobe Hackathon 2025
(Replace with actual names, GitHub links, or contact info)
