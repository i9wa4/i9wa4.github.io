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

    # Calculate the web path (relative to _site/)
    # Example: /path/to/_site/resume/index.html -> /resume
    abs_path = html_file.absolute()
    path_str = str(abs_path)

    # Find _site in the path and extract everything after it
    if "_site" in path_str:
        site_index = path_str.index("_site")
        relative_path = path_str[site_index + 6 :]  # +6 to skip "_site/"
        web_dir = "/" + str(Path(relative_path).parent)
    else:
        # Fallback: just use the parent directory name
        web_dir = "/" + html_file.parent.name

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load HTML file
        page.goto(f"file://{html_file.absolute()}")

        # Wait for page to be ready
        page.wait_for_load_state("networkidle")

        # Rewrite file:// links and relative links to https://i9wa4.github.io/
        page.evaluate(
            """
            (webDir) => {
                // Fix file:// links
                const fileLinks = document.querySelectorAll('a[href^="file://"]');
                fileLinks.forEach(link => {
                    const url = new URL(link.href);
                    // Extract path after _site/
                    const match = url.pathname.match(/\\/_site\\/(.+)/);
                    if (match) {
                        link.href = `https://i9wa4.github.io/${match[1]}`;
                    }
                });

                // Fix relative links (e.g., "05-genda.qmd#...")
                const allLinks = document.querySelectorAll('a[href]');
                allLinks.forEach(link => {
                    const href = link.getAttribute('href');
                    // Skip if already absolute URL (http://, https://, //, #, mailto:, etc)
                    if (href && !href.match(/^(https?:\\/\\/|\\/\\/|#|mailto:)/)) {
                        // Convert .qmd to .html
                        let newHref = href.replace(/\\.qmd(#|$)/, '.html$1');
                        // Make it absolute URL using the web directory path
                        link.href = `https://i9wa4.github.io${webDir}/${newHref}`;
                    }
                });
            }
        """,
            web_dir,
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
