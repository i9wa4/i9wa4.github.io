# Agent Skills as Reusable Operating Knowledge
uma-chan
2026-05-26

## 1. The Prompt Is Not the Whole Interface

A short prompt is not automatically a weak prompt.

A short prompt becomes weak when it depends on context that the agent
does not have:

- which source of truth to read first
- which workflow to follow
- which constraints are non-negotiable
- which checks should prove the work
- which residual risks should be reported instead of hidden

If those details live only in the prompt, every task starts with a long
preamble. If they are omitted, the agent fills gaps by inference.

Agent Skills are useful because they move recurring process knowledge
out of the one-off prompt and into a reusable package. The prompt can
stay focused on the current task while the skill carries the operating
knowledge that should be reused every time.

The agent remains probabilistic. The starting materials become more
consistent.

[OpenAI’s skills
documentation](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)
describes skills as reusable, shareable workflows that help ChatGPT
perform a specific task more consistently, and says skills can include
instructions, examples, code, and supporting resources. For daily
engineering work, “more consistently” carries the practical value.
Skills reduce variance by providing the same process knowledge, but the
agent still interprets the task probabilistically.

My working definition is simple: Agent Skills are reusable operating
knowledge for AI agents. In shorthand: Skills = reusable operating
knowledge.

A skill is a small package that tells an agent when a workflow applies,
how to proceed, what to avoid, and how to prove the result.

## 2. Package Contents and Routing Metadata

The [Agent Skills specification](https://agentskills.io/specification)
defines a skill as a directory that contains at least a `SKILL.md` file.
That file has YAML frontmatter followed by Markdown instructions.

A skill needs two frontmatter fields:

| Field | Routing role |
|----|----|
| `name` | The stable identifier. It must follow the naming rules and match the directory name. |
| `description` | The discoverability surface. It should say what the skill does and when to use it. |

The body is where the work instructions live. Optional `references/`,
`scripts/`, and `assets/` directories can hold supporting material.

This shape supports progressive disclosure, which becomes the main
design constraint later in the article. The specification says the
`name` and `description` metadata are loaded first, the full `SKILL.md`
body is loaded when a skill is activated, and resources are loaded only
as needed.

The frontmatter is routing metadata.

A small skill can look like this:

<div class="code-with-filename">

**skills/scoped-code-change/SKILL.md**

``` yaml
---
name: scoped-code-change
description: |
  USE FOR: Implementing a bounded code change from an issue or ticket,
  including source-of-truth discovery, implementation, checks, and residual-risk reporting.
  DO NOT USE FOR: Incident response, production operations, or broad architecture redesigns.
license: MIT
---

# Scoped Code Change

## Workflow

1. Read the issue or ticket and extract the goal, constraints, acceptance criteria, and requested evidence.
2. Discover relevant Agent Skills and source-of-truth documents before editing.
3. Make a short plan only when the change is ambiguous, risky, or multi-step.
4. Implement the smallest scoped change that satisfies the ticket.
5. Run the nearest test, lint, render, or validation check.
6. Report changed files, checks, residual risks, and anything intentionally left out.
```

</div>

This operating procedure gives the agent a repeatable starting point.

## 3. `name` and `description` Drive Selection

Many first drafts spend most of their effort on the body. The body only
helps after the skill has been selected.

The `name` and `description` decide whether the skill is discoverable in
the first place.

The Agent Skills specification requires `name` to follow strict naming
rules and to match the parent directory. The same document says
`description` should explain both what the skill does and when to use
it, and should include keywords that help agents identify relevant
tasks.

That means vague descriptions are costly:

<div class="code-with-filename">

**skills/code/SKILL.md**

``` yaml
description: Helps with code.
```

</div>

A better description gives the agent routing material:

<div class="code-with-filename">

**skills/scoped-code-change/SKILL.md**

``` yaml
description: |
  USE FOR: Implementing a bounded code change from an issue or ticket,
  including source-of-truth discovery, implementation, checks, and residual-risk reporting.
  DO NOT USE FOR: Incident response, production operations, or broad architecture redesigns.
```

</div>

`USE FOR` and `DO NOT USE FOR` are not required fields in the Agent
Skills specification. They are a convention inside the `description`
text. I like the convention because it makes scope visible to both
humans and agents, and because evaluation tools can reason about trigger
precision more easily when positive and negative scope are explicit.

The general rule is simple: if the description cannot route the task,
the detailed body may never matter.

## 4. One-Shot Prompting Needs Two Halves

People often describe one-shot prompting as if the prompt itself has to
contain everything.

For agentic engineering work, I think the better model is:

> good ticket + relevant Agent Skills = useful short prompt

The ticket or issue should carry the task-specific facts:

| Ticket content | Example |
|----|----|
| Goal | What should change |
| Scope | Which files, behavior, or user path matters |
| Constraints | What must not change |
| Acceptance criteria | What must be true when the work is done |
| Verification | Which checks, screenshots, tests, or examples matter |
| Residual-risk policy | What uncertainty should be reported instead of hidden |

The Agent Skill should carry the reusable process:

| Skill content | Example                                                  |
|---------------|----------------------------------------------------------|
| Discovery     | How to find source-of-truth context before acting        |
| Workflow      | The usual order of operations                            |
| Constraints   | General safety and style boundaries                      |
| Validation    | Which check surfaces are normally trusted                |
| Reporting     | What evidence and residual risk should appear at handoff |

That split makes the one-shot prompt smaller:

``` bash
$skill-description-index

Implement issue 123.
```

That prompt works only when the issue and relevant Agent Skills are
good. If the ticket is vague, the skill cannot invent acceptance
criteria. If the skill catalog is noisy or stale, the prompt may
activate the wrong process.

One-shot prompting becomes easier because the reusable part is no longer
in the prompt.

## 5. The `$skill-description-index` Pattern

The Agent Skills specification’s progressive-disclosure model creates a
useful tension. Loading only compact metadata at startup keeps context
small, but sometimes the compressed catalog is not enough.

`$skill-description-index` is how I fill that catalog-recovery gap in my
local workflow.

It is not an Agent Skills spec field, an official command, or portable
metadata. It is a local, repository-specific utility skill example: a
way to ask the agent to recover the available skill catalog and
source-of-truth descriptions before it chooses how to work.

The concrete local package is named `skill-description-index`. Its job
is narrow: recover full skill descriptions from disk when the active
catalog is missing, truncated, compressed by autocompaction, or
otherwise unclear. It should not replace the repo’s source of truth, and
it should not be used as a general-purpose rewrite trigger.

A minimal local version can be created by copy-pasting a small
`SKILL.md` and adapting the paths to your own skill tree:

<div class="code-with-filename">

**skills/skill-description-index/SKILL.md**

``` markdown
---
name: skill-description-index
license: MIT
description: |
  USE FOR: Recover full skill descriptions from disk. Use when descriptions are missing, truncated, or unclear, including after autocompaction.
  DO NOT USE FOR: unrelated tasks, broad rewrites outside the request, generated runtime outputs, or replacing repo-specific source of truth.
---

# Skill Description Index

Use this skill when the active skill catalog is too short to trust:
descriptions are missing, truncated, compressed by autocompaction, or unclear.

## Workflow

1. Inspect the relevant files, current repo conventions, and `git status`.
2. Read `references/preserved-guidance.md` before changing behavior or giving detailed instructions.
3. Recover full skill descriptions from the installed or repo-local `SKILL.md` files.
4. Make the smallest scoped change that satisfies the request.
5. Run the checks named in the preserved guidance or the nearest repo harness.
6. Report verification results and any remaining risk.

## References

- `references/preserved-guidance.md`
```

</div>

The preserved guidance is where the local, non-portable details belong.
My version records that the index script scans installed user-level
skill trees and prints a Markdown table:

<div class="code-with-filename">

**skills/skill-description-index/references/preserved-guidance.md**

``` markdown
# Preserved Guidance

Use this local skill when the active skill catalog is missing, truncated, or unclear.

If an index script is installed with this skill, run it from the available local skill tree:

- `bash ~/.codex/skills/skill-description-index/scripts/agent-skill-description-index.sh`
- `bash ~/.claude/skills/skill-description-index/scripts/agent-skill-description-index.sh`

The script should print a Markdown index with:

- skill root
- skill name
- home-relative `SKILL.md` path
- frontmatter `description`

Treat installed skill trees as generated output. Edit source skills in the repository or local source tree that owns them, not in generated installs.
```

</div>

Without that step, the agent may act from a partial memory of the
catalog. With the index step, the agent has a stronger opening move:

``` bash
$skill-description-index

Use the available skill catalog and source-of-truth skill descriptions,
then implement issue 123.
```

Success should be visible in the agent’s first actions. Instead of
relying only on the compressed catalog entry, it should read the skill
package, follow the preserved guidance, and recover a Markdown index
shaped like this:

> # Agent Skill Description Index
>
> Generated from installed user-level skill trees.
>
> | Skill Root | Skill | SKILL.md Path | Description |
> |----|----|----|----|
> | ~/.codex/skills | `github` | `~/.codex/skills/github/SKILL.md` | GitHub workflow guidance… |
> | ~/.codex/skills | `skill-description-index` | `~/.codex/skills/skill-description-index/SKILL.md` | Recover full skill descriptions from disk… |

After that, a good handoff should say which full skill descriptions were
used, which source files were read, and which checks proved the work.
Installed skill trees can be useful catalog evidence, but they are not
the editable source of truth. If the index output is empty, stale, or
does not lead back to an owning source tree, treat that as a signal to
fix the local skill roots or the preserved guidance.

The index step cannot guarantee the correct skill choice, but it makes
the failure mode more inspectable. If the wrong skill was selected, you
can improve the description, split overlapping skills, or add a
prompt-case evaluation.

The portable principle is broader than the exact token: before asking an
agent to act, let it recover the current operating knowledge that should
guide the work.

## 6. Put First-Step Knowledge in `SKILL.md`

A lot of prompts repeat the same development-order instructions: read
the issue, find the relevant docs, plan if needed, implement the change,
run tests, and report risks.

These are process instructions, not task facts. They belong in a
process-oriented Agent Skill.

For ordinary engineering tasks, the reusable workflow often looks like
this:

1.  Understand the ticket or issue.
2.  Discover relevant Agent Skills and source-of-truth documents.
3.  Plan only when the task needs a plan.
4.  Implement the smallest useful change.
5.  Run the nearest test, lint, render, or validation check.
6.  Report evidence and residual risks.

That workflow can live in `SKILL.md`. Then the prompt can stay short:
“Use the scoped code-change process and implement issue 123.”

The most useful `SKILL.md` is usually not the longest one. The body is
loaded when the skill is activated, so it should give the agent enough
structure to start correctly without forcing it to carry every possible
example. Long background belongs in `references/`.

A practical first version can be small:

| Section    | Useful content                                              |
|------------|-------------------------------------------------------------|
| Purpose    | The work this skill owns                                    |
| Workflow   | The usual order of operations                               |
| Validation | The minimum checks expected before reporting success        |
| Report     | The evidence and residual risk expected in the final answer |
| References | Links to deeper files that should be read only when needed  |

Copying a whole manual into `SKILL.md` creates a new problem. The skill
should be an entry point. It can point to a manual, a runbook, or a
script, but it should not become an unbounded archive.

When I decide whether something belongs in `SKILL.md`, I use this rule:

> If the agent needs it before taking the first safe step, keep it in
> `SKILL.md`. If the agent needs it only for a specific branch of the
> work, move it to `references/`.

That rule keeps the entry small while still preserving depth.

## 7. Progressive Disclosure and Language Choices

Progressive disclosure is the main design pressure behind Agent Skills.
It is context-budget architecture, not just a packaging nicety.

The specification describes a staged loading model:

| Stage | Loaded material | Design implication |
|----|----|----|
| Catalog | `name` and `description` | Keep routing clear and specific |
| Activation | Full `SKILL.md` | Keep the main workflow short and actionable |
| On demand | `references/`, `scripts/`, `assets/` | Split deeper detail into focused support files |

That model rewards small entry points and focused references.

For example:

``` text
skills/
  writing-rules/
    SKILL.md
    references/
      style-rules.md
      review-checklist.md
    scripts/
      check_style.sh
```

The `SKILL.md` should tell the agent when to read `style-rules.md`, not
paste the whole style guide into the main file.

Agent Skills also do not need English-only bodies. For Japanese-heavy
work, I prefer this split:

| Location | Practical guidance |
|----|----|
| `name` | Use lowercase ASCII, digits, and hyphens. This is the portable package name. |
| `description` | Prefer English for discovery when catalog tooling compares text directly. |
| Body | Use the language that makes the workflow clearest for the people and agents using it. |
| `references/` | Use the language of the source material. Japanese references are fine. |
| Evaluation prompt cases | Include Japanese request cases when real requests are Japanese. |

That English-description preference is operational, not a spec rule. I
keep `name` and `description` closer to English because they are the
catalog surface. Tools read them early, compare them often, and use them
for routing. The body and references can be much more local.

If you expect Japanese prompts, test Japanese prompt cases. Here, an
evaluation prompt case means a test input that should or should not
trigger a skill. In Waza trigger tests, make those cases explicit:

<div class="code-with-filename">

**evals/markdown/trigger_tests.yaml**

``` yaml
skill: markdown

should_trigger_prompts:
  - prompt: "Zenn の記事でコードブロックの書き方を確認して"
    reason: "A request about Markdown authoring"

should_not_trigger_prompts:
  - prompt: "Quarto のビルドエラーを直して"
    reason: "A build-debugging request, not Markdown authoring guidance"
```

</div>

``` bash
waza run evals/markdown/eval.yaml
```

A trigger test is not a static lint check. When `waza run` finds
`trigger_tests.yaml` next to the eval spec, it runs each prompt through
the configured executor and compares the recorded skill invocations with
the expected label: `should_trigger_prompts` should invoke `markdown`,
and `should_not_trigger_prompts` should not.

That run may involve GitHub Copilot, but not every Waza check or eval
path does. Waza’s normal project default is the `copilot-sdk` executor.
That is not just an internal label: Waza’s docs and source show this
path uses the GitHub Copilot SDK/CLI. With the default provider, local
runs need `copilot login`; token-based CI runs use `GITHUB_TOKEN`. A
custom Copilot SDK provider can use `COPILOT_BASE_URL` or
`COPILOT_PROVIDER_BASE_URL` and related provider environment variables,
which skips the default Copilot auth check. The agent/task model is
`config.model` or `--model`; `executor: mock` is local simulation and
does not need Copilot authentication. This is separate from
`waza check`, which checks compliance, token budget, and eval file
presence.

The grader side is also mixed. `skill_invocation` checks recorded
invocations deterministically, and the lightweight `trigger` grader
scores prompt/skill relevance heuristically. Only the `prompt` grader is
LLM-as-judge, controlled by `config.judge_model` or `--judge-model`.
When the result is wrong, improve the `description` trigger and
anti-trigger wording or the skill body.

Progressive disclosure also makes failures easier to fix. If the wrong
skill is selected, improve the description. If the right skill is
selected but the work goes off track, improve the workflow. If the
workflow is correct but lacks depth, improve the references.

## 8. Tooling Snapshot: Waza and `gh skill`

Agent Skills encode operating knowledge. Tooling helps because skills
are small packages that can drift.

This is a May 2026 snapshot. The tool surfaces below are real, but both
local versions and hosted documentation can change.

Official documentation exists for both tools, so I treat the hosted docs
and installed help as the first behavior sources. The repository source
checks below are implementation verification for the versions I checked
in May 2026, not a substitute for the docs.

I separate two concerns:

| Tool | Useful for | Do not treat it as |
|----|----|----|
| Waza | Skill readiness, checks, evals, graders, token and quality feedback | A guarantee that the agent will behave deterministically |
| `gh skill` | GitHub CLI packaging, search, preview, install, update, and publish validation | A trigger-quality evaluator |

The official [Waza
documentation](https://microsoft.github.io/waza/about/) is the primary
documentation source I use here. It describes a CLI platform for
creating, testing, and evaluating AI agent skills. The [Waza CLI
reference](https://microsoft.github.io/waza/reference/cli/) documents
`waza check`, `waza quality`, `waza run`, graders, token commands, and
related workflows.

GitHub CLI’s [`gh skill`](https://cli.github.com/manual/gh_skill)
command has a different role. The official manual says it installs and
manages agent skills from GitHub repositories. It also says this CLI
surface is in preview and subject to change. The same manual lists
`gh skills` as an alias and lists `install`, `preview`, `publish`,
`search`, and `update` as available commands. The
[`gh skill publish`](https://cli.github.com/manual/gh_skill_publish)
manual documents `--dry-run` as validation without publishing.

Use each tool for a different question:

- Use Waza to ask whether the skill is shaped well enough to use and
  evaluate.
- Use `gh skill publish --dry-run` to ask whether the repository is
  shaped well enough to publish.
- Use prompt cases and evals to ask whether the right skills are
  selected for real requests.

These are structural and behavioral checks, not trust checks. They do
not prove supply-chain integrity, script safety, reference safety, or
`allowed-tools` safety.

## 9. Waza Details I Verified

After checking the Waza docs and installed help, I verified
`waza --version`; the output was `waza version 0.33.0`. I also checked
the source of `microsoft/waza` at commit
[`23e9dbae6bd73f8a526b9c16cef0eb543ddaed96`](https://github.com/microsoft/waza/tree/23e9dbae6bd73f8a526b9c16cef0eb543ddaed96).

The most useful implementation references were:

- [`cmd/waza/cmd_check.go`](https://github.com/microsoft/waza/blob/23e9dbae6bd73f8a526b9c16cef0eb543ddaed96/cmd/waza/cmd_check.go)
- [`internal/checks/spec_checks.go`](https://github.com/microsoft/waza/blob/23e9dbae6bd73f8a526b9c16cef0eb543ddaed96/internal/checks/spec_checks.go)
- [`internal/checks/token_budget.go`](https://github.com/microsoft/waza/blob/23e9dbae6bd73f8a526b9c16cef0eb543ddaed96/internal/checks/token_budget.go)
- [`internal/checks/eval_suite.go`](https://github.com/microsoft/waza/blob/23e9dbae6bd73f8a526b9c16cef0eb543ddaed96/internal/checks/eval_suite.go)
- [`cmd/waza/cmd_run.go`](https://github.com/microsoft/waza/blob/23e9dbae6bd73f8a526b9c16cef0eb543ddaed96/cmd/waza/cmd_run.go)
- [`internal/execution/copilot.go`](https://github.com/microsoft/waza/blob/23e9dbae6bd73f8a526b9c16cef0eb543ddaed96/internal/execution/copilot.go)
- [`internal/execution/sdkclient.go`](https://github.com/microsoft/waza/blob/23e9dbae6bd73f8a526b9c16cef0eb543ddaed96/internal/execution/sdkclient.go)
- [`internal/execution/mock.go`](https://github.com/microsoft/waza/blob/23e9dbae6bd73f8a526b9c16cef0eb543ddaed96/internal/execution/mock.go)
- [`internal/graders/run.go`](https://github.com/microsoft/waza/blob/23e9dbae6bd73f8a526b9c16cef0eb543ddaed96/internal/graders/run.go)
- [`internal/graders/prompt_grader.go`](https://github.com/microsoft/waza/blob/23e9dbae6bd73f8a526b9c16cef0eb543ddaed96/internal/graders/prompt_grader.go)
- [`internal/graders/trigger_grader.go`](https://github.com/microsoft/waza/blob/23e9dbae6bd73f8a526b9c16cef0eb543ddaed96/internal/graders/trigger_grader.go)
- [`internal/graders/skill_invocation_grader.go`](https://github.com/microsoft/waza/blob/23e9dbae6bd73f8a526b9c16cef0eb543ddaed96/internal/graders/skill_invocation_grader.go)
- [`cmd/waza/cmd_quality.go`](https://github.com/microsoft/waza/blob/23e9dbae6bd73f8a526b9c16cef0eb543ddaed96/cmd/waza/cmd_quality.go)

The installed help says `waza check` runs compliance, token, and eval
checks. The implementation is more detailed than that summary. In the
checked source, `checkReadiness` loads `SKILL.md`, computes compliance,
runs MCP and link checks, checks token budget, detects evals, validates
eval and task schemas when present, and runs spec plus advisory checks.

The JSON `ready` field carries the gate. In the checked implementation,
readiness is true only when:

- compliance is at least `Medium-High`
- the token budget is not exceeded
- links pass when link results are available
- eval and task schemas have no validation errors
- spec checks pass

Eval absence is reported, but absence of eval coverage alone does not
necessarily make `ready` false. I confirmed that with an
installed-command probe against a local skill:

``` text
agent-skills-management true    Medium-High ok  false
```

Those columns were `name`, `ready`, `compliance.level`,
`tokenBudget.status`, and `eval.found`. This means `eval.found=false`
and `ready=true` can coexist.

I do not describe `waza check` as “the eval gate.” It is a readiness
check with eval visibility. Eval coverage is still useful, but the
current readiness flag is not “has eval.”

Waza also has a separate `waza quality` command. The checked help and
source describe it as an LLM-as-judge quality check across clarity,
completeness, trigger precision, scope coverage, and anti-patterns. It
requires Copilot authentication in the current implementation.

For trigger work, the distinction is:

| Mechanism | Check surface |
|----|----|
| `trigger` grader | A heuristic score between a prompt and skill trigger material |
| `skill_invocation` grader | Whether expected skills were invoked, including required and forbidden skills |
| `waza check` | Structural readiness and related validation, not a full real-task routing test |

So the practical loop is:

1.  Use `waza check` for structural readiness.
2.  Use prompt cases and graders for routing behavior.
3.  Use `waza quality` when you want LLM-judged feedback on the skill
    text.

## 10. `gh skill` Details I Verified

After checking the official GitHub CLI manual and installed help, I
checked `gh version 2.92.0`. I also checked the source of `cli/cli` at
commit
[`9a593ce81b593dee752cc11737d1a3ef768e52b3`](https://github.com/cli/cli/tree/9a593ce81b593dee752cc11737d1a3ef768e52b3).

The most useful implementation references were:

- [`pkg/cmd/skills/skills.go`](https://github.com/cli/cli/blob/9a593ce81b593dee752cc11737d1a3ef768e52b3/pkg/cmd/skills/skills.go)
- [`pkg/cmd/skills/publish/publish.go`](https://github.com/cli/cli/blob/9a593ce81b593dee752cc11737d1a3ef768e52b3/pkg/cmd/skills/publish/publish.go)
- [`internal/skills/discovery/discovery.go`](https://github.com/cli/cli/blob/9a593ce81b593dee752cc11737d1a3ef768e52b3/internal/skills/discovery/discovery.go)
- [`internal/skills/frontmatter/frontmatter.go`](https://github.com/cli/cli/blob/9a593ce81b593dee752cc11737d1a3ef768e52b3/internal/skills/frontmatter/frontmatter.go)
- [`skills/gh-skill/SKILL.md`](https://github.com/cli/cli/blob/9a593ce81b593dee752cc11737d1a3ef768e52b3/skills/gh-skill/SKILL.md)

The top-level command is a core GitHub CLI command named `gh skill`,
with `gh skills` as an alias. The manual and installed help list these
subcommands:

- `install`
- `preview`
- `publish`
- `search`
- `update`

For publishability, the validation path is:

``` bash
gh skill publish --dry-run
```

The official manual says `--dry-run` validates without publishing. The
checked source confirms the local validation path before the release
flow.

In the checked implementation, `gh skill publish` discovers skills using
conventions such as:

- `skills/*/SKILL.md`
- `skills/{scope}/*/SKILL.md`
- `*/SKILL.md`
- `plugins/{scope}/skills/*/SKILL.md`

Then it validates:

| Check | Meaning |
|----|----|
| Name | Present, strict Agent Skills naming, and matching directory name |
| Description | Required frontmatter field |
| `allowed-tools` | Must be a string, not an array |
| Install metadata | `metadata.github-*` should be stripped before publishing |
| License | Recommended; missing license is a warning |
| Body length | Long bodies can warn before publish |

I also ran a minimal local dry-run probe with a generated skill
directory. It produced a missing-remote warning but completed
validation:

``` text
warning     no git remote found. Create a GitHub repository with: gh repo create

Dry run complete. Use without --dry-run to publish.
```

Do not document a separate `gh skill validate` workflow. The documented
and implemented validation path is `gh skill publish --dry-run`.

## 11. Lifecycle, Evidence, and Risk Surface

This section has three layers: a cheap development loop, the evidence to
return after work, and risks that checks do not remove.

The practical lifecycle can stay short:

1.  Notice a repeated instruction, missing check, or recurring handoff
    mistake.
2.  Draft a small `SKILL.md` for one workflow.
3.  Use it on a real task.
4.  Run prompt cases and structural checks.
5.  Keep, revise, split, or retire the skill based on what happened.

Do not skip the last step. Old skills keep competing for attention, and
a stale skill can be worse than no skill because it gives the agent
confident but outdated process knowledge.

For validation, I use three layers:

1.  Try prompt cases that cover expected routing, adjacent workflows,
    and negative scope.
2.  Run Waza checks for structural readiness, quality, and eval
    visibility.
3.  Run `gh skill publish --dry-run` when the repository should be
    publishable through GitHub CLI.

For one skill:

``` bash
waza --no-update-check check skills/<name> --format json
```

For a repository that should be publishable through GitHub CLI:

``` bash
gh skill publish --dry-run
```

Neither command proves that the agent will choose the right skill for
every prompt. Prompt cases expose routing mistakes. A skill that looks
clear in isolation can still be hard for an agent to select when
adjacent skills have overlapping descriptions.

A small prompt-case table is enough to start:

| Prompt case | Expected skill | What to observe |
|----|----|----|
| “Implement issue 123” | `scoped-code-change` | Does the agent read the ticket and discover context before editing? |
| “Review this migration plan” | `plan-review` | Does it avoid the implementation workflow? |
| “Fix production now” | Not this skill | Does negative scope prevent unsafe activation? |
| “Write release notes for this diff” | `release-notes` | Does it route to writing rather than code change? |

Short prompts also increase the need for completion evidence. If the
skill owns a workflow, it should also own the handoff shape.

A useful final report should include:

- changed files
- checks that ran
- check results
- artifacts produced, such as screenshots or rendered output
- remaining blockers
- residual risks or unverified assumptions

For example:

<div class="code-with-filename">

**skills/scoped-code-change/SKILL.md**

``` markdown
## Report

Include:

- changed files
- verification commands and results
- behavior intentionally left unchanged
- residual risk, if any
```

</div>

A skill should not train an agent to pretend. For risky work, the skill
should say when to stop:

| Stop condition | Why it matters |
|----|----|
| Missing source of truth | Prevents implementation from guesswork |
| Denied command or hook | Prevents silent policy bypass |
| Production write operation | Requires explicit human approval in many workflows |
| Failing verification | Prevents “done” from meaning “untested” |
| Conflicting instructions | Forces the conflict into the open |

Use `BLOCKED` to keep uncertainty visible, not to avoid work.

The broader risk surface matters too:

| Risk | What to watch |
|----|----|
| Discovery failure | Overlapping descriptions, skill explosion, and routing ambiguity |
| Version drift | Stale skills, conflicting policies, and unclear version provenance |
| Security and trust | Malicious skills, poisoned references, unsafe scripts, exfiltration |
| Missing retirement path | Old skills keep competing with better current workflows |
| Over-centralized root prompt | One giant instruction surface becomes hard to audit and update |

Not everything should move into a skill:

| Content | Better home |
|----|----|
| This task’s specific goal | Prompt, issue, or ticket |
| Acceptance criteria | Issue or ticket |
| Long domain background | `references/` or external documentation |
| Project-wide style rules | Project docs, then referenced by the skill |
| Generated evidence | Task artifact, CI output, or final report |
| Secrets or personal credentials | Nowhere in the skill |

Future tooling may improve this with embedding retrieval, hierarchical
routing, evaluator feedback loops, and better audit trails for which
skill version was used. Those are useful directions, but they do not
remove the need for clear boundaries today.

## 12. Documented Behavior, Framing, and Summary

Separate documented behavior from interpretation.

Documented facts:

- Agent Skills use a `SKILL.md` file with required `name` and
  `description` frontmatter.
- The Agent Skills specification documents optional `scripts/`,
  `references/`, and `assets/` directories.
- The specification describes progressive disclosure: metadata first,
  full instructions on activation, resources as needed.
- [OpenAI’s skills
  documentation](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)
  describes skills as reusable workflows that can include instructions,
  examples, code, and supporting resources, and states that OpenAI
  skills follow the Agent Skills open standard.
- GitHub CLI documents `gh skill` as preview and documents
  `gh skill publish --dry-run` as validation without publishing.
- Waza documents skill checks, validators, graders, quality scoring, and
  evaluation workflows.

My framing:

- “Reusable operating knowledge” is a practical way to think about what
  should move from a repeated prompt into a skill.
- `$skill-description-index` is a local catalog-recovery pattern, not a
  spec field.
- A good ticket is the other half of a good one-shot prompt.
- Skills reduce repeated instructions and improve consistency, but they
  do not make probabilistic agents deterministic.
- Different tools check different layers. Waza readiness, Waza evals,
  and `gh skill publish --dry-run` should not be collapsed into one
  generic “validation” bucket.

Agent Skills are most useful when they are treated as reusable operating
knowledge. The short prompt becomes practical only when the surrounding
system is strong: a good issue or ticket on one side, and well-described
Agent Skills on the other.

The body-placement rule is the part I return to most often. If the agent
needs it before taking the first safe step, keep it in `SKILL.md`; if
the agent needs it only for a specific branch of the work, move it to
`references/`.

The value is repeated access to process knowledge every time an agent
starts work.

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fen%2Fblog%2F2026-05-26-agent-skills-reusable-operating-knowledge.html&text=Agent%20Skills%20as%20Reusable%20Operating%20Knowledge%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=Agent%20Skills%20as%20Reusable%20Operating%20Knowledge%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fen%2Fblog%2F2026-05-26-agent-skills-reusable-operating-knowledge.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fen%2Fblog%2F2026-05-26-agent-skills-reusable-operating-knowledge.html&title=Agent%20Skills%20as%20Reusable%20Operating%20Knowledge%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
