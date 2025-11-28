import os
import pdfplumber

# Folder that contains all PDF files
folder_path = r"C:\Users\ayush\pdfs"

# Gujarati name you want to search
target_name = "જાગૃતિ"

# Output file
output_file = r"C:\Users\ayush\extracted_results.txt"

results = []

for pdf_file in os.listdir(folder_path):
    if pdf_file.lower().endswith(".pdf"):
        pdf_path = os.path.join(folder_path, pdf_file)

        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if not text:
                    continue

                # Search line-by-line
                for line in text.split("\n"):
                    if target_name in line:
                        result = f"[{pdf_file} → Page {page_num}]  {line}"
                        print(result)
                        results.append(result)

# Save results to file
with open(output_file, "w", encoding="utf-8") as f:
    for entry in results:
        f.write(entry + "\n")

print("\nDone! Extracted results saved to:", output_file)
