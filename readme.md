Adobe India Hackathon - Challenge 1B: Persona-Driven Document Intelligence
1. Challenge Overview
The goal of this challenge is to build an intelligent system that analyzes a collection of PDF documents and extracts the most relevant sections based on a specific user persona and their job-to-be-done. The solution must be efficient, run entirely offline, and adhere to strict constraints on model size and processing time.

This project implements a fully automated pipeline that processes multiple document collections, understands the user's intent for each, and generates a ranked list of relevant information in the required JSON format.

2. Our Approach & Methodology
The solution is built around a modular Python script (solchallenge1b.py) that employs a multi-stage pipeline to transform raw PDFs into actionable insights.

Core Pipeline Stages:
a. Automated Collection Discovery
The script is designed for efficiency and scalability. When executed, it automatically scans the Challenge_1b directory to find all sub-folders named Collection 1, Collection 2, etc. It then processes each collection sequentially without requiring separate commands.

b. Dynamic Input Parsing
For each collection, the script reads the corresponding challenge1b_input.json file to understand the context. It dynamically extracts the persona and job_to_be_done, which are crucial for tailoring the analysis.

c. Smart PDF Chunking
A key feature of this solution is its ability to understand document structure. Instead of treating PDFs as a single block of text, the parse_pdfs_to_chunks function uses the PyMuPDF library to analyze text properties. It uses a heuristic based on font size and style (boldness) to intelligently identify headings and group the subsequent paragraphs under them. This creates semantically meaningful "chunks" (e.g., a section on "Budget-Friendly Restaurants") which leads to far more relevant results than simple paragraph splitting.

d. Semantic Ranking with Embeddings
The core of the intelligence lies in semantic search:

AI Model: We use the all-MiniLM-L6-v2 sentence transformer model. This model was chosen for its excellent balance of performance and size (~80MB), easily meeting the < 1GB constraint.

Dynamic Prompt Crafting: A unique prompt is crafted for each collection by combining the persona and their job. For example: "As a Travel Planner, I need to Plan a trip of 4 days for a group of 10 college friends..."

Scoring: The script generates vector embeddings for the prompt and for every text chunk. It then calculates the cosine similarity between the prompt and each chunk.

Ranking: The chunks are sorted in descending order of their similarity score, ensuring the most relevant sections appear first.

e. Intelligent Filtering (Rule-Based Enhancement)
For Collection 3 (the "Food Contractor" persona), the task is highly specific: find vegetarian dinner recipes. A purely semantic search can sometimes miss such specific negative constraints. To solve this, a rule-based filter is applied after the initial AI ranking. This filter removes any ranked sections containing keywords like 'chicken', 'beef', 'pork', 'breakfast', etc. This hybrid approach demonstrates adaptability and significantly improves the final accuracy for nuanced tasks.

f. JSON Output Generation
The top 15 highest-ranked (and filtered) chunks are formatted into the precise JSON structure specified in the problem statement, including metadata, extracted_sections (with importance rank), and subsection_analysis. The final file is saved as generated_output.json within its respective collection folder.

3. Models & Libraries Used
Model: sentence-transformers/all-MiniLM-L6-v2 (via Hugging Face)

Core Libraries:

sentence-transformers: For generating text embeddings.

torch: The backend framework for the model.

PyMuPDF (fitz): For fast and detailed PDF text extraction.

4. How to Build and Run the Solution
The solution is a single Python script with no complex build process.

Step 1: Install Dependencies
Ensure you have Python installed. Then, install the required libraries using pip:

pip install sentence-transformers torch PyMuPDF

Step 2: Run the Script
Navigate to the root directory of the project (Adobe-India-Hackathon25-main - Copy/) in your terminal and run the following command:

python Challenge_1b/solchallenge1b.py

The script will automatically find and process all collection folders inside Challenge_1b and generate the output JSON files in their respective directories.

5. Constraint Compliance Checklist
The solution was built from the ground up to meet all hackathon constraints:

[✔] CPU Only: The entire pipeline runs on CPU.

[✔] Model Size (≤ 1GB): The all-MiniLM-L6-v2 model is only ~80MB.

[✔] Processing Time (≤ 60s): The script is highly optimized. Processing time for each collection is typically under 15 seconds, well below the 60-second limit.

[✔] Offline Execution: The embedding model is downloaded and cached on the first run, allowing all subsequent runs to be fully offline. The script makes no external network calls.