#!/usr/bin/env python3
"""
HTML to PDF converter using Playwright
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


def html_to_pdf(html_path: str, pdf_path: str) -> None:
    """Convert HTML file to PDF using Playwright"""
    html_file = Path(html_path)
    if not html_file.exists():
        print(f"Error: HTML file not found: {html_path}")
        sys.exit(1)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load HTML file
        page.goto(f"file://{html_file.absolute()}")

        # Wait for page to be ready
        page.wait_for_load_state("networkidle")

        # Add CSS to ensure Japanese fonts are used
        page.add_style_tag(
            content="""
            * {
                font-family: "Hiragino Kaku Gothic ProN", "Hiragino Sans", "Yu Gothic", "Meiryo", sans-serif !important;
            }
        """
        )

        # Generate PDF
        page.pdf(
            path=pdf_path,
            format="A4",
            margin={
                "top": "20mm",
                "right": "20mm",
                "bottom": "20mm",
                "left": "20mm",
            },
            print_background=True,
        )

        browser.close()
        print(f"Successfully converted {html_path} to {pdf_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: html_to_pdf.py <input.html> <output.pdf>")
        sys.exit(1)

    html_to_pdf(sys.argv[1], sys.argv[2])
