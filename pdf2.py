import os
import pdfplumber
from tqdm import tqdm

# Folder containing all PDFs
folder_path = r"C:\Users\ayush\pdfs"

# Gujarati name to search
target_name = "જાગૃતિ"

# Output file
output_file = r"C:\Users\ayush\extracted_results.txt"

results = []

# Get list of PDFs
pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]

# Outer progress bar: PDF files
for pdf_file in tqdm(pdf_files, desc="Processing PDFs", unit="file"):
    pdf_path = os.path.join(folder_path, pdf_file)

    try:
        with pdfplumber.open(pdf_path) as pdf:

            # Inner progress bar: pages
            for page_num in tqdm(range(len(pdf.pages)), 
                                  desc=f"→ {pdf_file}", 
                                  leave=False,
                                  unit="page"):
                page = pdf.pages[page_num]
                text = page.extract_text()

                if not text:
                    continue

                for line in text.split("\n"):
                    if target_name in line:
                        result = f"[{pdf_file} → Page {page_num + 1}]  {line}"
                        print(result)
                        results.append(result)

    except Exception as e:
        print(f"Error reading {pdf_file}: {e}")

# Write to output file
with open(output_file, "w", encoding="utf-8") as f:
    for entry in results:
        f.write(entry + "\n")

print("\nDone! Extracted results saved to:", output_file)
