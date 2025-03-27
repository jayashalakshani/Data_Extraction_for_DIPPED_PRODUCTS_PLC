import streamlit as st
import pdfplumber
import requests
import tempfile
import ollama
import re
import pandas as pd
from io import StringIO

def extract_structured_table(pdf_url, page_number):
    """Extracts a structured table from a PDF page and formats it as Markdown."""
    response = requests.get(pdf_url)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(response.content)
        pdf_path = tmp.name

    with pdfplumber.open(pdf_path) as pdf:
        if page_number > len(pdf.pages):
            return None
        page = pdf.pages[page_number - 1]
        text = page.extract_text()

    prompt = f"""<|begin_of_text|>
    <|start_header_id|>system<|end_header_id|>
    You are a financial data expert. Convert this complex table into a clean markdown format with:
    1. SINGLE header row: Metric | 06-month (Rs. '000) | 03-month (Rs. '000) |
    2. ONE row per metric with all corresponding values
    3. Negative values in parentheses
    4. Remove duplicate headers
    5. Preserve exact values from source
    6. Extract only data related to the year 2024
    7. Extract all relevant metrics, including revenue, expenses, profits, tax, and dividends
    8. Reject any data from previous years
    9. Always get correct numerical value
    
    Rules:
    1. Include ALL metrics from the source table for the year 2024 only
    2. Preserve exact numerical formatting
    3. Maintain original metric names
    4. Include final metrics like EPS and Dividends

    Example format:
    | Metric | 06-month (Rs. '000) | 03-month (Rs. '000) |
    |---|---|---|
    | Revenue from contracts (2024) | 40,463,469 | 21,277,143 |
    
    <|start_header_id|>user<|end_header_id|>
    Source text:
    {text}
    <|eot_id|>
    """

    response = ollama.chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': prompt}],
        options={'temperature': 0.0}
    )
    return response['message']['content']

# Streamlit UI
st.title("🚀 Financial Data Extraction for DIPPED PRODUCTS PLC 2024")

url = st.text_input("Enter PDF URL")
page = st.number_input("Enter Page Number", min_value=1, step=1)

if url and page:
    if st.button("Generate Report"):
        with st.spinner("Processing complex table structure..."):
            try:
                result = extract_structured_table(url, page)
                
                table_pattern = (
                    r'(\|.*\|.*\|.*\|\n)'
                    r'(\|[-| ]+\|[-| ]+\|[-| ]+\|\n)'
                    r'((\|.*\|.*\|.*\|\n)+)'
                )
                
                table_match = re.search(table_pattern, result, re.DOTALL)
                
                if table_match:
                    full_table = f"{table_match.group(1)}{table_match.group(2)}{table_match.group(3)}"
                    st.markdown(full_table)
                    st.success("Data Structured Correctly")

                    # Save as Markdown
                    md_filename = "structured_table.md"
                    with open(md_filename, "w") as md_file:
                        md_file.write(full_table)
                    st.download_button("Download as Markdown", full_table, file_name=md_filename)
                    
                    # Convert to CSV
                    data = []
                    for line in full_table.split("\n")[2:]:
                        if '|' in line:
                            data.append([col.strip() for col in line.split('|')[1:-1]])
                    
                    df = pd.DataFrame(data, columns=["Metric", "06-month (Rs. '000)", "03-month (Rs. '000)"])
                    csv_buffer = StringIO()
                    df.to_csv(csv_buffer, index=False)
                    st.download_button("Download as CSV", csv_buffer.getvalue(), file_name="structured_table.csv", mime="text/csv")
                else:
                    st.error("Format mismatch. Raw response:")
                    st.text(result)
            except Exception as e:
                st.error(f"Error: {str(e)}")





























