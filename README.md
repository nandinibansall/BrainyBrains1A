**📝 PDF Heading Extractor**

This tool extracts the main title and hierarchical headings (H1, H2, H3, ...) from PDF documents and outputs a clean JSON representation containing:
The main title (extracted from the top of page 1).
Structured headings with levels and corresponding page numbers.

**🚀 Approach**

PDF Parsing with PyMuPDF (fitz):
Each page of the PDF is parsed to identify text blocks, lines, and font sizes.
Headings are heuristically determined based on font size, position on the page, and text quality (e.g., ignoring numeric-only or irrelevant content).

*Main Title Extraction:*
Extracted from the top 30% of the first page using the largest font size text lines.
Multiple lines with the same max font are joined to form the full title.

*Heading Detection:*
All text lines are filtered using custom logic (is_heading_candidate).
The most common font size is assumed to be body text, and larger fonts are treated as headings.
The top 4 heading font sizes are mapped to H1–H4 levels.

*Output Format:*

{
  "title": "Main Document Title",
  
  "outline": [
  
    {"level": "H1", "text": "Heading Text", "page": 1},
    {"level": "H2", "text": "Subheading Text", "page": 2},
    ...
    
  ]
}

**🛠️ Libraries Used**

PyMuPDF (fitz) – For parsing and analyzing PDFs.
Built-in libraries: os, json, collections.Counter

**📦 Directory Structure**

/app

│
├── input/           ← Folder containing the input PDF files
├── output/          ← JSON outputs go here after processing
├── extract.py       ← Main Python script
└── README.md        ← Documentation (this file)

**🧪 Expected Execution**

*The solution runs as follows:*

1. All .pdf files in /app/input/ are scanned.
2. For each PDF, a .json file is generated in /app/output/.
3. Each JSON contains the extracted title and a structured outline of headings.

No additional input is required — this will run in a pre-dockerized or CLI-based execution environment.
