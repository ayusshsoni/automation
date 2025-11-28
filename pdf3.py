import os
import PyPDF2
from tqdm import tqdm
from multiprocessing import Pool

# Gujarati name to search
SEARCH_NAME = "નાંઢા જાગ્રુતિબેન"

# Folder containing your PDF files
PDF_FOLDER = r"C:\Users\ayush\pdfs"

# Output file
OUTPUT_FILE = r"C:\Users\ayush\pdfs\extracted_results1.txt"


def extract_from_pdf(pdf_path):
    """Reads a PDF and returns all lines containing the Gujarati name."""
    matched_lines = []

    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = ""

            # Extract all pages' text
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

            # Line-by-line search to preserve address/details
            for line in text.split("\n"):
                if SEARCH_NAME in line:
                    matched_lines.append(f"{os.path.basename(pdf_path)} → {line}")

    except Exception as e:
        matched_lines.append(f"Error processing {pdf_path}: {e}")

    return matched_lines


def main():
    # Collect all PDFs
    pdf_paths = [
        os.path.join(PDF_FOLDER, file)
        for file in os.listdir(PDF_FOLDER)
        if file.lower().endswith(".pdf")
    ]

    if not pdf_paths:
        print("No PDF files found in the folder!")
        return

    print(f"Found {len(pdf_paths)} PDF files. Running 15 parallel processes...\n")

    all_results = []

    # 15 parallel workers
    with Pool(15) as pool:
        for result in tqdm(
            pool.imap_unordered(extract_from_pdf, pdf_paths),
            total=len(pdf_paths),
            desc="Processing PDFs",
        ):
            all_results.extend(result)

    # Save results
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for line in all_results:
            out.write(line + "\n")

    print(f"\n✔ Done! Found {len(all_results)} matching lines.")
    print(f"✔ Saved results to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
