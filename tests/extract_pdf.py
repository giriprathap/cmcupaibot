
import os
from pypdf import PdfReader

# Path to PDF
pdf_path = r"tests\2000 questions for training.pdf"
output_path = r"tests\extracted_questions.txt"

def extract_questions_from_pdf(pdf_path, output_path):
    print(f"Reading PDF: {pdf_path}")
    try:
        reader = PdfReader(pdf_path)
        questions = []
        
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                # Split by newlines and clean
                lines = text.split('\n')
                for line in lines:
                    line = line.strip()
                    # Filter out short lines
                    if len(line) < 10:
                        continue
                        
                    # Check if line looks like a question
                    # 1. Ends with question mark
                    if line.endswith("?"):
                        questions.append(line)
                    # 2. Starts with Question words (Common in this dataset)
                    elif line.lower().split(' ')[0] in ["what", "where", "who", "when", "why", "how", "is", "are", "can", "does", "do", "which"]:
                        questions.append(line)
                    # 3. Numbered questions (e.g. "1. What is...") handled later by cleanup but need to catch here
                    elif "?" in line: 
                         questions.append(line)


        # Post-processing to clean up numbering (e.g., "1. What is..." -> "What is...")
        cleaned_questions = []
        import re
        for q in questions:
            # Remove leading numbers/bullets
            q_clean = re.sub(r'^\d+[\.\)\s]+', '', q).strip()
            if q_clean and q_clean not in cleaned_questions:
                cleaned_questions.append(q_clean)
        
        print(f"Extracted {len(cleaned_questions)} unique questions.")
        
        with open(output_path, "w", encoding="utf-8") as f:
            for q in cleaned_questions:
                f.write(q + "\n")
                
        print(f"Saved to {output_path}")
        
    except Exception as e:
        print(f"Error reading PDF: {e}")

if __name__ == "__main__":
    if os.path.exists(pdf_path):
        extract_questions_from_pdf(pdf_path, output_path)
    else:
        print("PDF not found!")
