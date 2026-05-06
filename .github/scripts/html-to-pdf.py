"""
HTML to PDF converter using Playwright
"""

import os
import shutil
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
        executable_path = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH")
        if executable_path and not Path(executable_path).exists():
            executable_path = shutil.which(executable_path) or executable_path

        launch_options = {}
        if executable_path:
            launch_options["executable_path"] = executable_path

        browser = p.chromium.launch(**launch_options)
        page = browser.new_page(viewport={"width": 1440, "height": 1200})

        # Load HTML file
        page.goto(f"file://{html_file.absolute()}")

        # Wait for page to be ready
        page.wait_for_load_state("load", timeout=60000)

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

        # Keep resume PDFs within the public 1-2 page target without removing content.
        page.add_style_tag(
            content="""
@media print {
  body {
    font-size: 85% !important;
    line-height: 1.18 !important;
  }

  p,
  li {
    line-height: 1.18 !important;
  }

  h1,
  h2,
  h3 {
    margin-top: 0.45rem !important;
    margin-bottom: 0.25rem !important;
  }

  ul {
    margin-top: 0.15rem !important;
    margin-bottom: 0.25rem !important;
  }
}
"""
        )

        # Generate PDF
        page.pdf(
            path=pdf_path,
            format="A4",
            scale=0.85,
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
