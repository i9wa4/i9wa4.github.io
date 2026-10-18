(() => {
  const source = document.querySelector(".voice-diagram pre.mermaid")?.textContent;
  if (!source) return;

  let state = "idle";
  let attempts = 0;
  let current;
  const observer = new MutationObserver(schedule);

  function schedule() {
    const host = document.querySelector(".voice-diagram");
    if (!host) return;
    if (state === "done" && !host.contains(current)) {
      state = "idle";
      attempts = 0;
    }
    if (state !== "idle") return;
    const original = host.querySelector("svg.mermaid-js") ||
      (current && host.querySelector("pre.mermaid"));
    if (!original) return;
    state = "running";
    observer.disconnect();
    void render(original, host);
  }

  async function render(original, host) {
    let workspace;
    attempts += 1;
    try {
      await document.fonts.ready;
      if (!host.contains(original) ||
          document.querySelector(".voice-diagram") !== host || !document.body) {
        throw new Error("Voice diagram is unavailable");
      }

      workspace = document.createElement("div");
      workspace.style.cssText = "position:fixed;left:-10000px;top:0;visibility:hidden;width:1500px";
      const diagram = document.createElement("div");
      diagram.className = "mermaid";
      diagram.textContent = source;
      workspace.append(diagram);
      document.body.append(workspace);

      await mermaid.run({ nodes: [diagram] });
      const resized = diagram.querySelector("svg");
      if (!resized || !host.contains(original) ||
          document.querySelector(".voice-diagram") !== host) {
        throw new Error("Voice diagram changed during render");
      }
      resized.classList.add("mermaid-js");
      original.replaceWith(resized);
      current = resized;
      state = "done";
    } catch (error) {
      if (attempts < 2) {
        state = "idle";
        setTimeout(schedule, 50);
      } else {
        state = "failed";
        console.error("Could not size voice diagram", error);
      }
    } finally {
      workspace?.remove();
      if (state !== "failed") {
        observer.observe(document, { childList: true, subtree: true });
        queueMicrotask(schedule);
      }
    }
  }

  observer.observe(document, { childList: true, subtree: true });
  window.addEventListener("load", schedule, { once: true });
  schedule();
})();
