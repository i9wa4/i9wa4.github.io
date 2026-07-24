# From `jupyter execute` to Production
Mawatari Daiki
2026-02-13

## 1. Introduction

**Daiki Mawatari, GENDA**

AI agents × Databricks notebooks

<div class="notes">

Hello, I’m Daiki Mawatari from GENDA. Today I’ll demonstrate how AI
agents can autonomously execute Databricks notebooks via CLI, enabling
agentic development on Databricks.

</div>

------------------------------------------------------------------------

## 2. The Vision

**What you’ll take away:**

- AI agents executing Databricks notebooks from CLI
- Practical patterns from production
- Open source tool available today

<div class="notes">

To unlock full AI automation with Databricks notebooks, we need a
CLI-first approach that enables agents to execute code, receive results,
and iterate independently. Today you’ll learn how to enable AI agents to
execute Databricks notebooks from command line, practical patterns from
GENDA’s production data platform, and an open source tool you can use
today.

</div>

------------------------------------------------------------------------

## 3. The Solution

My Project: <https://github.com/i9wa4/jupyter-databricks-kernel>

- CLI notebook execution
- Remote execution on Databricks
- AI assistant integration
- Autonomous iteration

<div class="notes">

The solution is jupyter-databricks-kernel. It enables one-command
notebook execution via CLI, complete remote execution on Databricks
compute, seamless integration with AI coding assistants, and a natural
workflow for autonomous iteration.

</div>

------------------------------------------------------------------------

## 4. Demo Environment

My Project: <https://github.com/i9wa4/databricks-ai-starter> on GitHub
Codespaces

**Prompt:** \> Describe the schema of samples.nyctaxi.trips, then create
and execute a notebook with one histogram of trip distances.

<div class="notes">

For this demo, I’m using the databricks-ai-starter repository running on
GitHub Codespaces. I’ll give Claude Code this prompt: “Describe the
schema of samples.nyctaxi.trips, then create and execute a notebook with
one histogram of trip distances.” Claude Code will write and execute
notebooks autonomously, demonstrating the agentic workflow in action.

</div>

------------------------------------------------------------------------

## 5. CLI Execution Example

**For example:**

\$ jupyter execute demo_nyctaxi.ipynb –kernel_name=databricks

<div class="notes">

Let me show you an example of how this works. Here’s the command:
“jupyter execute”, then the notebook name “demo_nyctaxi.ipynb”, and the
kernel specification “–kernel_name=databricks”. Claude Code can execute
notebooks via CLI - you don’t need to type anything manually during
execution. So basically, it uploads your local files to the compute,
executes the notebook on Databricks, and brings back the results. No UI
clicks, no manual copying - just this one command and you’re done.

</div>

------------------------------------------------------------------------

## 6. Complete Remote Execution

**All code runs on Databricks, not locally**

- Databricks Runtime libraries available
- No local environment setup
- Independent agent iteration

<div class="notes">

The notebook is generating trip trend analysis and visualizations.
Execution runs on Databricks compute using Databricks Runtime libraries.
The key differentiator: All code runs on Databricks, not locally. You
can use any library pre-installed in Databricks Runtime without local
environment setup. Agents can iterate independently with kernel support.
Minimal human intervention required.

</div>

------------------------------------------------------------------------

## 7. Reviewing Results

Notebook execution completes with visualizations and analysis outputs.

<div class="notes">

The notebook completes with trip trend visualizations and analysis
results. You can open the generated notebook to review outputs, verify
data quality, and iterate on the analysis. This immediate feedback loop
enables rapid development - agents can execute, review, and refine
notebooks autonomously.

</div>

------------------------------------------------------------------------

## 8. Why This Matters

- **Credible:** Production use at GENDA
- **Useful:** Open source, available today
- **Timely:** Autonomous AI agents

<div class="notes">

Why credible: We use this for development at GENDA. Why useful: It’s
open source. You can try it today. Reproducible workflow for your own
projects. Why now: This enables agents to execute notebooks
autonomously, aligning with the AI Agents track theme.

</div>

------------------------------------------------------------------------

## 9. Development Workflow

**Dev = Production runtime**

Deploy via Databricks Asset Bundles

<div class="notes">

Development runs on Databricks compute, matching production runtime.
Notebooks can be deployed via Databricks Asset Bundles.

</div>

------------------------------------------------------------------------

## 10. Get Started

My Project: <https://github.com/i9wa4/jupyter-databricks-kernel>

Thank you.
