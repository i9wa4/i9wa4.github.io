# AGENTS.md

## English Blog Descriptions

- For `en/blog/*.qmd` frontmatter, write `description` as concise social or
  LinkedIn promotional copy: a strong hook, the practical value, and optional
  relevant hashtags. Match existing English blog examples; do not turn the
  field into a long abstract.

## Code Fence Rules

- In `.qmd` files, write static highlighted code blocks with Pandoc attribute
  class syntax: use an opening fence like ` ```{.bash}` rather than
  ` ```bash`.
- When adding filenames in `.qmd` files, write them as Pandoc attributes on
  the same opening fence, for example ` ```{.bash filename="script.sh"}`.
- Add filenames only when the filename carries useful meaning for the reader or
  maps to a real file. Avoid decorative `.txt` filename attributes such as
  `filename="prompt.txt"` on prompt/example snippets.
- In public `.qmd` surfaces, keep filename attributes repo-relative or
  filename-only. Do not use machine-local absolute paths.
- Use ` ```{bash}`, ` ```{python}`, and similar non-class braces only for
  intentionally executable Quarto cells. For documentation examples that
  should not execute, use a static class fence such as ` ```{.python}` or wrap
  the example in a larger Markdown/text code block.
- Use ` ```{mermaid}` for Mermaid diagrams that Quarto should render. Use a
  static Markdown/text block when showing Mermaid source as copyable source
  code.
- After adding or editing renderable Mermaid diagrams in `.qmd`, verify that
  Quarto renders them correctly. Do not leave Quarto cell-option lines such as
  `#| label:` inside Mermaid source that is emitted to HTML.
- Use raw attribute fences such as ` ```{=html}` only when the block is meant
  to pass raw output-format content through Quarto/Pandoc.
- For shell examples in `.qmd`, prefer ` ```{.bash}`. Avoid `shell` or
  `{.shell}` when Bash highlighting is intended. Use `sh` only when the
  example is specifically POSIX `sh`.
- Use ` ```{.text}` in `.qmd` only for genuinely plain text, output, logs,
  terminal transcripts, directory trees, config-ish samples, or
  language-neutral content. If a block is primarily an executable shell command
  for the reader to run, use ` ```{.bash}` instead.
- For prompt-like shell invocations or reader-run commands with no meaningful
  filename, prefer unnamed ` ```{.bash}` blocks. Keep `.text` for logs, command
  output, directory trees, config-ish samples, and language-neutral content.
- In plain `.md` files that target CommonMark, GitHub, or Zenn, use normal
  Markdown info strings such as ` ```bash`, ` ```python`, or Zenn's
  ` ```bash:script.sh` filename form. Do not use Pandoc-only forms such as
  ` ```{.bash}` there unless the file is intentionally processed by Pandoc.

## Quarto Verification

- In this repository, run Quarto through uv. Use `uv run quarto ...` for render
  or verification commands instead of assuming `quarto` is directly available
  on `PATH`.
