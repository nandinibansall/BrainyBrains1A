import fitz  # PyMuPDF
import os
import json
from collections import Counter

def is_heading_candidate(text):
    t = text.strip()
    if len(t) < 3 or t.isspace() or t.replace('.', '').isdigit():
        return False
    if len(t.split()) < 2 and any(char.isdigit() for char in t):
        return False
    return True

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    font_infos = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if block["type"] != 0:
                continue
            for line in block["lines"]:
                line_text = "".join([span["text"] for span in line["spans"]]).strip()
                if not is_heading_candidate(line_text):
                    continue
                line_size = max([round(span["size"]) for span in line["spans"]])
                font_infos.append({
                    "size": line_size,
                    "text": line_text,
                    "y0": line["bbox"][1],
                    "x0": line["bbox"][0],
                    "page": page_num + 1
                })

    if not font_infos:
        return "Untitled", []

    # Title logic: get top headings on page 1 (upper 30% of page height)
    page1_headers = [f for f in font_infos if f["page"] == 1 and f["y0"] < doc.load_page(0).rect.height * 0.3]
    if page1_headers:
        max_size = max(f["size"] for f in page1_headers)
        top_title_lines = [f for f in page1_headers if f["size"] == max_size]
        top_title_lines = sorted(top_title_lines, key=lambda x: x["y0"])
        main_title = " ".join(f["text"] for f in top_title_lines)
    else:
        main_title = font_infos[0]["text"]

    # Heading level detection
    outline = []
    seen = set()
    all_fonts = [f["size"] for f in font_infos]

    size_counts = Counter(all_fonts)
    body_font = size_counts.most_common(1)[0][0]
    header_sizes = sorted(set(sz for sz in all_fonts if sz > body_font), reverse=True)
    if not header_sizes:
        header_sizes = sorted(set(all_fonts), reverse=True)[:4]

    font_to_level = {}
    for idx, size in enumerate(header_sizes[:4]):
        font_to_level[size] = f"H{idx+1}"

    for f in font_infos:
        if f["size"] not in font_to_level:
            continue
        key = (f["text"], f["page"])
        if key in seen:
            continue
        if sum(c.isdigit() for c in f["text"]) > len(f["text"]) // 2:
            continue
        outline.append({
            "level": font_to_level[f["size"]],
            "text": f["text"],
            "page": f["page"]
        })
        seen.add(key)

    doc.close()
    return main_title, outline

def main():
    input_folder = "/app/input"
    output_folder = "/app/output"
    os.makedirs(output_folder, exist_ok=True)
    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_folder, pdf_file)
        title, outline = extract_outline(pdf_path)
        result = {
            "title": title,
            "outline": outline
        }
        output_path = os.path.join(output_folder, os.path.splitext(pdf_file)[0] + '.json')
        with open(output_path, "w", encoding="utf-8") as out_f:
            json.dump(result, out_f, indent=2, ensure_ascii=False)
        print(f"✅ Processed {pdf_file} → {output_path}")

if __name__ == "__main__":
    main()