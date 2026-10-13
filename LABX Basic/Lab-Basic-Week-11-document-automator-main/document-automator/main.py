# document-automator/main.py

import sys
import os
import datetime

# Add the src directory to the Python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from pdf_processor import PDFProcessor
from word_processor import WordProcessor
from utils import ensure_directory_exists, setup_logging

logger = setup_logging(__name__)


def main():
    """Main entry point for the document automation application."""

    documents_dir = os.path.join(BASE_DIR, "documents")
    ensure_directory_exists(documents_dir)

    # Input and output file paths
    input_pdf_path = os.path.join(
        documents_dir, "input_article.pdf"
    )
    output_docx_path = os.path.join(
        documents_dir, "output_report.docx"
    )
    merged_pdf_output_path = os.path.join(
        documents_dir, "merged_output.pdf"
    )
    dummy_pdf1 = os.path.join(
        documents_dir, "dummy_doc1.pdf"
    )
    dummy_pdf2 = os.path.join(
        documents_dir, "dummy_doc2.pdf"
    )

    # Check the required input PDF
    if not os.path.exists(input_pdf_path):
        logger.critical(
            f"Required input PDF not found: {input_pdf_path}"
        )
        logger.info(
            "Please place input_article.pdf in the documents folder."
        )
        return

    pdf_proc = PDFProcessor()
    word_proc = WordProcessor()

    logger.info("--- Starting Document Automation Workflow ---")

    # Task 1: Extract PDF text and create a Word report
    logger.info("Task 1: Extracting PDF text and creating Word report.")

    extracted_text = pdf_proc.extract_text_from_pdf(input_pdf_path)

    if extracted_text and extracted_text.strip():
        doc = word_proc.create_document()

        word_proc.add_heading(
            doc, "Automated Document Report", level=1
        )

        word_proc.add_paragraph(
            doc,
            "This report was automatically generated "
            "from PDF content and structured data.",
            bold=True,
            font_size=12
        )

        word_proc.add_paragraph(
            doc,
            "--- Extracted Content from PDF ---",
            italic=True,
            font_size=10,
            align="center"
        )

        word_proc.add_paragraph(doc, extracted_text)

        word_proc.add_heading(doc, "Summary Data", level=2)

        # Count pages using the page-end marker
        total_pages = sum(
            1 for line in extracted_text.splitlines()
            if line.startswith("--- Page ") and line.endswith(" End ---")
        )

        table_data = [
            ["Metric", "Value", "Notes"],
            [
                "Total Pages Processed",
                str(total_pages),
                "From Input PDF"
            ],
            ["Document Type", "PDF/Word Hybrid", ""],
            [
                "Generated Date",
                datetime.date.today().isoformat(),
                ""
            ]
        ]

        word_proc.add_table(
            doc,
            table_data,
            include_header=True,
            header_bold=True,
            col_widths=[1.5, 1.5, 3.0]
        )

        if word_proc.save_document(doc, output_docx_path):
            logger.info("Word report generated successfully.")
        else:
            logger.error("Failed to save the Word report.")

    else:
        logger.error(
            "Could not extract text from PDF. "
            "Skipping Word document generation."
        )

    # Task 2: Merge multiple PDFs
    dummy_pdfs_exist = (
        os.path.exists(dummy_pdf1)
        and os.path.exists(dummy_pdf2)
    )

    if dummy_pdfs_exist:
        logger.info("Task 2: Merging dummy PDF files.")

        pdfs_to_merge = [dummy_pdf1, dummy_pdf2]

        if pdf_proc.merge_pdfs(
            pdfs_to_merge, merged_pdf_output_path
        ):
            logger.info("PDF merge completed successfully.")
        else:
            logger.error("Failed to merge PDF files.")

    else:
        logger.warning(
            "Dummy PDFs not found. Skipping PDF merge task."
        )

    logger.info("--- Document Automation Workflow Completed ---")


if __name__ == "__main__":
    main()