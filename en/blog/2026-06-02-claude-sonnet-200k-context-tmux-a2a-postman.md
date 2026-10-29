# Why Claude Sonnet 200k Still Needs a Workflow
uma-chan
2026-06-02

## 1. A Large Context Window Is Not a Workflow

Claude Sonnet 200k still matters because it is a practical operating
target. Here, Claude Sonnet 200k means a Claude Sonnet model with a
200k-token context window. A large context window gives the model room
to read and reason, but it does not manage roles, task state, compaction
recovery, or coordination. If a task only works by reaching for the
bigger or deeper model every time, the workflow is spending Claude Opus
where discipline should have been enough.

On 2026-06-02, my Claude Code `/model` menu labels Claude Sonnet 4.6 as
“Default (recommended)” and “Best for everyday tasks.” The same menu
labels Claude Opus 4.8 as “Opus (1M context)” and “Most capable for
complex work.” The [Claude Code model
guide](https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code)
gives the same shape: Claude Sonnet is the default for most coding work,
while Claude Opus is the deeper-reasoning choice for difficult
debugging, large refactors, and architecture decisions.

That is the model-choice argument for this article. Claude Sonnet is the
everyday path. Claude Opus is the deliberate high-capability and
high-context option. A good agent workflow should make Claude Sonnet
effective first, then reserve Claude Opus for turns where deeper
reasoning actually pays.

Do not confuse that with a simple usage-bucket story. I first saw a Team
`/usage` screen without a “Current week (Sonnet only)” meter, then later
saw that a Claude Sonnet-only meter can appear after all. A Max-plan
screenshot also showed one. The [Claude Code
changelog](https://code.claude.com/docs/en/changelog) says one release
hid a redundant Claude Sonnet-only bar for Pro and Enterprise plans. The
current [Max plan
page](https://support.claude.com/en/articles/11049741-what-is-the-max-plan)
and [Team plan
page](https://support.claude.com/en/articles/9266767-what-is-the-team-plan)
say some plans or seats have both all-model and Claude Sonnet-only
weekly limits. The safe conclusion is UI, plan, seat, version, and
account-state variability, not a confirmed bug and not a universal
accounting rule.

The reliable distinction is usage pressure. The model guide says Claude
Opus uses meaningfully more quota than Claude Sonnet and costs several
times more per turn. Anthropic’s API [pricing
page](https://platform.claude.com/docs/en/about-claude/pricing) also
shows higher Claude Opus rates than Claude Sonnet rates; Claude Code
subscription meters are not API invoices, but model choice still affects
how quickly work spends the available budget. The [usage limits
page](https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work)
adds the broader rule: usage depends on the model, conversation length,
features, and tools.

Context limits also vary by product surface and model. The current
[paid-plan context
page](https://support.claude.com/en/articles/8606394-how-large-is-the-context-window-on-paid-claude-plans)
describes 1M Claude Code paths for recent Claude Opus models and Claude
Sonnet 4.6 under plan and usage-credit conditions. The [API context
page](https://support.claude.com/en/articles/8606395-how-large-is-the-claude-api-s-context-window)
separates 1M-capable recent Claude Opus and Claude Sonnet 4.6
deployments from 200k-class models. So I treat Claude Sonnet 200k as the
everyday operating target, not as a universal limit for every Claude
Sonnet deployment.

My local `/usage` evidence points at the same failure mode:
subagent-heavy sessions and 150k-plus contexts create pressure. The fix
is not to treat Claude Opus as extra room for every task. The fix is to
make the everyday Claude Sonnet path cleaner.

For agentic coding, the failure mode is rarely “the model cannot fit the
file.” The failure mode is usually operational:

- The task owner is no longer obvious
- The current checklist is buried under old turns
- A reviewer request never gets answered
- Compaction summarizes away the detail that made the next step safe
- One agent becomes planner, implementer, reviewer, memory keeper, and
  user-facing reporter

That is why I do not try to solve long-running Claude work by stuffing
more text into Claude. I treat context as a workspace. The durable parts
of the workflow need a different home.

## 2. Practice One: Split the Work Across Agents

The first practice is to make each context window smaller on purpose.

A single capable agent can plan, edit, test, review, and report, but
that role stack gets heavy. The session fills with stale options,
partial checks, reviewer notes, user-facing phrasing, and implementation
details. A large context window makes that possible for longer. It does
not make it clean.

I prefer to split the work by responsibility:

| Responsibility       | Narrower context shape            |
|----------------------|-----------------------------------|
| receive user request | messenger or entry role           |
| plan and delegate    | orchestrator role                 |
| implement            | worker role                       |
| verify               | reviewer role                     |
| summarize to user    | messenger or orchestrator handoff |

This is not about pretending multiple agents are magically objective. A
reviewer can still miss things. An orchestrator can still delegate
poorly. The practical advantage is narrower working memory: each agent
receives the context needed for its role and carries less irrelevant
history forward.

The large window is still valuable here. It becomes room for a focused
role to inspect files, logs, and evidence deeply, not an invitation to
keep the whole organization inside one prompt.

## 3. Practice Two: Reground the Role After Compaction

Automatic compaction is useful because it keeps long sessions alive. It
is also risky because it changes what the agent has immediately
available.

The dangerous version is silent compaction:

1.  The agent is midway through a task.
2.  The runtime compacts the conversation.
3.  The agent continues from a summary.
4.  A small but important instruction no longer has the same force.

After compaction, I want the agent to ground itself again before acting:

- What role am I in?
- Who can I talk to?
- What task is currently open?
- What original checklist defines “done”?
- What evidence already exists outside the transcript?

If Claude Code exposes an after-compaction hook in your version, that
hook is a natural place to re-input the role. For one agent, the hook
can say: read this instruction file, recover this task artifact, and
continue from the current checklist.

The multi-agent case is harder. The same reminder cannot be injected
into every pane. A messenger, orchestrator, worker, and reviewer each
need a different role, a different contact list, and a different set of
safety rules. The hook needs a stable way to answer “which agent just
compacted?”

In a tmux-based setup, the practical answer is the pane title. A pane
titled `worker` should recover the worker role. A pane titled
`orchestrator` should recover the coordinator role. A pane titled
`messenger` should stay transport-only. The pane title is outside the
model context, visible to the harness, and simple enough to use as local
role identity.

## 4. Practice Three: Externalize the Task State

Long context helps reasoning. It is bad at being a task database.

A single long chat mixes different kinds of information:

| In the same context window | What the agent needs instead             |
|----------------------------|------------------------------------------|
| old decisions              | current decisions with evidence          |
| abandoned plans            | active checklist and owner               |
| command output             | verification summary and failing checks  |
| review comments            | open and resolved findings               |
| side discussion            | routable handoff to the responsible role |

The difference matters because the model does not experience its own
context as a structured queue. It sees a sequence. The operator sees a
long transcript. Neither of those is the same as “worker has one open
task, reviewer owes one approval, messenger should not implement, and
compaction just happened.”

The fix is not to make every prompt longer. The fix is to create small
durable surfaces outside the prompt:

- Messages for handoffs
- Reply-required slots for obligations
- Task artifacts for checklists and evidence
- Role boundaries for decomposition
- Recovery events for compaction

This gives the model a current working set instead of asking it to infer
the live task board from thousands of old tokens.

## 5. The Communication Problem

The three practices are tool-agnostic, but they create a concrete
systems problem.

If agents have separate roles, they need a way to hand work to each
other. If compaction changes the transcript, they need a way to recover
the right role. If task state lives outside chat, they need a way to
find the current checklist and prove that an obligation is closed.

A light implementation can handle part of this. An after-compaction hook
can read the current tmux pane title and map it to `roles/worker.md`,
`roles/reviewer.md`, or another role prompt. A shared Markdown file,
issue, or task board can hold the durable checklist.

That can be enough for one agent or a small manual setup. The harder
part is communication between agents:

- How does the planner send scoped work to the implementer?
- How does the implementer know a reply is required?
- How does the reviewer recover a missed request?
- How does the operator distinguish “waiting for someone else” from
  “forgotten”?
- How does compaction become an event that restores role and task state?

Any serious implementation has to answer those questions. Otherwise, the
workflow still depends on the transcript remembering obligations that
belong outside the transcript.

## 6. The Concrete Implementation: `tmux-a2a-postman`

My local implementation is
[`tmux-a2a-postman`](https://github.com/i9wa4/tmux-a2a-postman). I
introduced the mailbox layer in [a previous `tmux-a2a-postman`
post](https://i9wa4.github.io/2026-05-17-tmux-a2a-postman-markdown-mail-for-ai-agent-teams.md);
this article is about using it as the coordination layer around Claude’s
large but fallible working memory.

`tmux-a2a-postman` does not make Claude smarter. It does not increase
the context window. It does not replace Claude Code, Codex CLI, tmux, or
native subagents.

It adds the missing coordination surface:

- Roles are named in `postman.md`
- Allowed handoffs are defined as Mermaid edges
- Node identity uses tmux pane titles
- Messages are stored as Markdown mail
- Recipients claim mail with `pop`
- Required replies open exact input requests
- Status reports `pending`, `waiting`, `ready`, `stale`, queues, and
  dead letters
- Archived mail remains readable after pane history is gone

The simplest useful topology is small:

``` mermaid
graph LR
    messenger["messenger<br/>human-facing"]
    orchestrator["orchestrator<br/>task coordinator"]
    worker["worker<br/>implementation"]
    reviewer["reviewer<br/>verification"]

    messenger --- orchestrator
    orchestrator --- worker
    orchestrator --- reviewer

    class messenger entry
    class orchestrator,worker,reviewer role
    classDef entry fill:#dbeafe,stroke:#2563eb,color:#0f172a
    classDef role fill:#f8fafc,stroke:#64748b,color:#0f172a
```

One user request can become a smaller route:

``` text
messenger -> orchestrator: user request and constraints
orchestrator -> worker: scoped implementation request
worker -> orchestrator: DONE or BLOCKED with evidence
orchestrator -> reviewer: verify the result
reviewer -> orchestrator: APPROVED or NOT APPROVED
orchestrator -> messenger: final user-facing result
```

Each role sees a narrower job. The worker does not need to remember how
to talk to the human. The reviewer does not need the full implementation
transcript. The messenger does not need to inspect files. The
orchestrator holds the route, not every implementation detail.

For compaction recovery, the important behavior is not the PING text.
The important behavior is that compaction becomes a mailbox event. A
compacted pane gets a reason to read role instructions again, recover
the active task artifact, and continue from explicit state instead of
pane memory alone.

A minimal `postman.md` file can opt a skill catalog into ordinary PING
mail, compaction PING mail, or both:

<div class="code-with-filename">

**postman.md**

``` markdown
---
skill_path:
  - path: ~/.codex/skills
    inject:
      - ping
      - compaction_ping
    skills:
      - postman-session-operator
      - postman-send-message
      - postman-config-auditor
---

## `edges`

~~~mermaid
graph LR
    messenger --- orchestrator
    orchestrator --- worker
    orchestrator --- reviewer
    class messenger ui_node
~~~
```

</div>

The task-management part is equally important. A sender can create a
required reply:

``` bash
tmux-a2a-postman send-heredoc --to worker --reply-required <<'MESSAGE_BODY'
Task: update the article.

Original checklist:
- [ ] Keep the opening tool-agnostic.
- [ ] Preserve the Claude Sonnet/default versus Claude Opus/deliberate framing.
- [ ] Verify and report evidence.
MESSAGE_BODY
```

The receiver claims mail:

``` bash
tmux-a2a-postman pop
```

`pop` returns an archived Markdown body path. The agent must read that
body before acting. Pane history is not the source of truth.

When the work is done, the receiver closes the required input:

``` bash
tmux-a2a-postman send-heredoc \
  --to orchestrator \
  --fills-input-request-id <input-request-id> \
  --reply-to <message-id> <<'MESSAGE_BODY'
DONE: Article updated and verified.
Task artifact: <artifact-reference>
Original checklist: PASS
Evidence: rumdl, Vale, Harper, Quarto render
Remaining blockers: none
MESSAGE_BODY
```

That closes the transport slot. It still does not prove the work is
correct. For that, I keep a durable Markdown artifact with the original
checklist, progress, decisions, verification evidence, blockers, and
completion verdict. Mail carries obligations; the artifact carries
proof.

You can build a lighter version without `tmux-a2a-postman`. A hook plus
pane-title role prompts plus a shared Markdown checklist may be enough
for single-agent recovery. For multi-agent work, you still need routing,
reply-required state, archives, status, and missed-message recovery.
`tmux-a2a-postman` is my answer to that communication layer.

## 7. The Rule of Thumb

My rule for Claude Sonnet 200k work is simple:

> Put reasoning in context. Put obligations in mail. Put evidence in
> artifacts.

The context window is a powerful workspace. It is not a reliable memory
system, queue, review process, or project manager.

For long agent runs, I want three things around it:

1.  Multi-agent decomposition so each role has a smaller job.
2.  Compaction recovery so the agent restores role and state after the
    runtime rewrites the conversation.
3.  Durable task management so the checklist and evidence survive
    outside the model’s working memory.

`tmux-a2a-postman` is just the local implementation of that operating
model. It keeps Claude Sonnet useful for everyday work and makes Claude
Opus a deliberate choice instead of a rescue path for messy state.

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fen%2Fblog%2F2026-06-02-claude-sonnet-200k-context-tmux-a2a-postman.html&text=Why%20Claude%20Sonnet%20200k%20Still%20Needs%20a%20Workflow%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=Why%20Claude%20Sonnet%20200k%20Still%20Needs%20a%20Workflow%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fen%2Fblog%2F2026-06-02-claude-sonnet-200k-context-tmux-a2a-postman.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fen%2Fblog%2F2026-06-02-claude-sonnet-200k-context-tmux-a2a-postman.html&title=Why%20Claude%20Sonnet%20200k%20Still%20Needs%20a%20Workflow%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
