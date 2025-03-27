# Financial Data Extraction for DIPPED PRODUCTS PLC 2024

🚀 This project is a Streamlit-based application designed to extract and format financial data from PDF documents into Markdown and CSV formats. The primary focus is on processing data for the year 2024.

## Features

- Extracts structured tables from PDF documents
- Formats the extracted data into a clean Markdown format
- Provides options to download the data as Markdown or CSV
- Handles complex table structures and ensures accurate data extraction

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/jayashalakshani/financial-data-extraction.git
    cd financial-data-extraction
    ```

## Usage

1. Run the Streamlit application:
    ```bash
    streamlit run main.py
    ```

2. Enter the PDF URL and the page number to extract the table from.

3. Click on "Generate Report" to process and display the structured table.

4. Download the data as Markdown or CSV using the provided download buttons.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.

## Limitations

- **PDF Structure Dependency:** The accuracy of data extraction depends on the structure of the PDF. Highly complex or irregular tables may not be processed correctly.
- **Page Number Validation:** The script does not handle cases where the provided page number exceeds the number of pages in the PDF.
- **Network Dependency:** The script requires an internet connection to fetch the PDF from the provided URL.
- **Year-Specific Extraction:** The current implementation focuses on extracting data specifically for the year 2024. Data from other years will not be processed.
- **Error Handling:** Limited error handling for edge cases such as invalid URLs, network issues, or unsupported PDF formats.

Please feel free to reach out for any questions or support.
