"""Exercise the Mermaid refresh hook across an awaited render disconnect.

Run after rendering the target slide:
    uv run quarto render slides/2026-10-15-terminal-night-3-tmux.qmd --to revealjs
    PLAYWRIGHT_CHROME=/path/to/chrome uv run python tests/mermaid_reveal_refresh_disconnect.py

If PLAYWRIGHT_CHROME is unset, Playwright's installed Chromium is used.
"""

import os
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "_site/slides/2026-10-15-terminal-night-3-tmux.html"

SETUP = r"""
() => {
  const realMermaid = window.mermaid;
  const api = realMermaid.mermaidAPI;
  const originalRender = api.render.bind(api);
  let release;
  const gate = new Promise((resolve) => { release = resolve; });
  const probe = {
    source: "graph TD; A-->B",
    calls: 0,
    renderSettled: false,
    release: () => release()
  };

  // Mermaid's API object is frozen, so intercept access through its root.
  const delayedApi = {
    render: async (...args) => {
      probe.calls++;
      const result = await originalRender(...args);
      probe.renderSettled = true;
      await gate;
      return result;
    }
  };
  window.mermaid = new Proxy(realMermaid, {
    get(target, key, receiver) {
      if (key === "mermaidAPI") return delayedApi;
      return Reflect.get(target, key, receiver);
    }
  });

  const diagram = [...document.querySelectorAll(".presentation-diagram")].at(-1);
  const svg = diagram.querySelector("svg.mermaid-js");
  probe.parent = svg.parentElement;
  probe.pre = document.createElement("pre");
  probe.pre.className = "mermaid-js";
  probe.pre.textContent = probe.source;
  window.__mermaidDisconnectProbe = probe;
  probe.parent.append(probe.pre);
}
"""


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args: object) -> None:
        pass


def main() -> None:
    if not HTML.is_file():
        raise FileNotFoundError(f"Render the target slide first: {HTML}")

    handler = partial(QuietHandler, directory=str(ROOT / "_site"))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as playwright:
            launch = {"headless": True}
            if chrome := os.environ.get("PLAYWRIGHT_CHROME"):
                launch["executable_path"] = chrome
            browser = playwright.chromium.launch(**launch)
            try:
                page = browser.new_page(viewport={"width": 390, "height": 844})
                errors: list[str] = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.on(
                    "console",
                    lambda message: (
                        errors.append(message.text) if message.type == "error" else None
                    ),
                )
                page.route("https://**", lambda route: route.abort())
                url = (
                    f"http://127.0.0.1:{server.server_port}"
                    "/slides/2026-10-15-terminal-night-3-tmux.html"
                )
                page.goto(url, wait_until="load")
                page.wait_for_function(
                    "document.querySelectorAll('svg.mermaid-js').length === 5"
                )
                page.evaluate(SETUP)
                page.wait_for_function("window.__mermaidDisconnectProbe?.renderSettled")

                before = page.evaluate(
                    "() => ({"
                    "text: __mermaidDisconnectProbe.pre.textContent,"
                    "connected: __mermaidDisconnectProbe.pre.isConnected,"
                    "calls: __mermaidDisconnectProbe.calls"
                    "})"
                )
                if before != {"text": "", "connected": True, "calls": 1}:
                    raise AssertionError(
                        f"Render did not reach the cleared-pre window: {before}"
                    )

                page.evaluate(
                    "() => {"
                    "__mermaidDisconnectProbe.pre.remove();"
                    "__mermaidDisconnectProbe.release();"
                    "}"
                )
                page.wait_for_function(
                    "() => __mermaidDisconnectProbe.pre.textContent"
                    " === __mermaidDisconnectProbe.source"
                )
                detached = page.evaluate(
                    "() => !__mermaidDisconnectProbe.pre.isConnected"
                )
                if not detached:
                    raise AssertionError(
                        "Source was restored without disconnecting the pre"
                    )

                page.evaluate(
                    "() => __mermaidDisconnectProbe.parent.append("
                    "__mermaidDisconnectProbe.pre)"
                )
                page.wait_for_function(
                    "document.querySelectorAll('svg.mermaid-js').length === 6"
                    " && document.querySelectorAll('pre.mermaid-js').length === 0"
                )
                calls = page.evaluate("() => __mermaidDisconnectProbe.calls")
                if calls != 2 or errors:
                    raise AssertionError(
                        f"Reconnect failed: calls={calls}, errors={errors}"
                    )
                print(
                    "PASS: cleared source restored after disconnect; reconnect rendered SVG"
                )
            finally:
                browser.close()
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()
