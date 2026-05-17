# AGENTS.md

## Code Fence Rules

- In `.qmd` files, write static highlighted code blocks with Pandoc attribute
  class syntax: use an opening fence like ` ```{.bash}` rather than
  ` ```bash`.
- In `.qmd` files, add filenames as Pandoc attributes on the same opening
  fence, for example ` ```{.bash filename="script.sh"}`.
- Use ` ```{bash}`, ` ```{python}`, and similar non-class braces only for
  intentionally executable Quarto cells. For documentation examples that
  should not execute, use a static class fence such as ` ```{.python}` or wrap
  the example in a larger Markdown/text code block.
- Use ` ```{mermaid}` for Mermaid diagrams that Quarto should render. Use a
  static Markdown/text block when showing Mermaid source as copyable source
  code.
- Use raw attribute fences such as ` ```{=html}` only when the block is meant
  to pass raw output-format content through Quarto/Pandoc.
- For shell examples in `.qmd`, prefer ` ```{.bash}`. Avoid `shell` or
  `{.shell}` when Bash highlighting is intended. Use `sh` only when the
  example is specifically POSIX `sh`.
- In plain `.md` files that target CommonMark, GitHub, or Zenn, use normal
  Markdown info strings such as ` ```bash`, ` ```python`, or Zenn's
  ` ```bash:script.sh` filename form. Do not use Pandoc-only forms such as
  ` ```{.bash}` there unless the file is intentionally processed by Pandoc.
