import json
import fitz  # PyMuPDF
import pandas as pd
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    """Extract text and tables from PDF file."""
    doc = fitz.open(pdf_path)
    content = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        
        # Extract tables using PyMuPDF's table extraction
        tables = page.find_tables()
        table_data = []
        
        for table in tables:
            table_data.append(table.extract())
        
        content.append({
            'text': text,
            'tables': table_data,
            'page_number': page_num + 1
        })
    
    return content

def create_jsonl_entry(content, page_num, file_path):
    """Create a JSONL entry with the required structure."""
    return {
        "Primary Topic": "Data Product Catalog",  # Default value, can be modified based on content
        "Sub-Topic": "Data",  # Default value, can be modified based on content
        "Keywords": "Data",  # Default value, can be modified based on content
        "Description": content['text'],
        "rawContent": content['text'],
        "enhancedContext": "Data Product Catalog",  # Default value, can be modified based on content
        "presentationContext": "Data Product Catalog",  # Default value, can be modified based on content
        "metadata": {
            "chunkId": page_num,
            "pageNumber": page_num,
            "fileUrl": str(file_path),
            "groupNames": ["bank", "data product"]
        }
    }

def process_pdf_to_jsonl(pdf_path, output_path):
    """Process PDF file and convert to JSONL format."""
    content = extract_text_from_pdf(pdf_path)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for page_content in content:
            json_entry = create_jsonl_entry(
                page_content,
                page_content['page_number'],
                Path(pdf_path).absolute()
            )
            f.write(json.dumps(json_entry) + '\n')

if __name__ == "__main__":
    input_pdf = "sample-tables.pdf"
    output_jsonl = "output.jsonl"
    
    process_pdf_to_jsonl(input_pdf, output_jsonl)
    print(f"Conversion complete. Output saved to {output_jsonl}") 