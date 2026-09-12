# Why Multi-Agent?
uma-chan
2026-07-14

## 1. The Question

Why multi-agent?

The question looks simple until the role names start piling up. Planner,
implementer, reviewer, approver, operator: after a few labels, a system
can look serious before it has proved that the extra machinery helps.
More names do not make the work better. Sometimes they only make it
slower.

I still think about multi-agent systems because some responsibilities
are a bad fit for one uninterrupted agent context. The pressure point is
not whether one agent is smart enough. It is whether one running
conversation can carry planning, execution, review, approval, memory,
and reporting without blurring them.

The short version:

> Multi-agent is not mainly about parallelism. It is about separating
> responsibilities.

This first post starts with that pressure. The next posts cover [tmux as
the surviving execution
substrate](https://i9wa4.github.io/2026-07-14-tmux-survives-visible-form-disappears.md), [the
two state machines behind agent
work](https://i9wa4.github.io/2026-07-14-two-state-machines-for-agent-work.md), and [the
company-like shape of a personal agent
workstation](https://i9wa4.github.io/2026-07-14-company-inside-personal-computer.md).

## 2. One Agent Looks Too Capable

A strong single agent can do a lot. It can plan, research, implement,
test, summarize, and report. For short tasks, that is often enough, and
adding roles would only add ceremony.

The trouble starts when the task gets longer and the same conversation
has to carry too many roles:

- planner;
- implementer;
- reviewer;
- approver;
- coordinator;
- operator.

Put those roles in the same context, the same transcript, and the same
desire to finish, and failure becomes harder to see. The actor who did
the work says it is done. The transcript keeps stale assumptions nearby.
Review drifts toward implementation convenience. The agent’s
intermediate reasoning becomes something the agent is tempted to defend.

This is not mainly a capability problem. It is a role-fit problem.

## 3. Keep Context Small

The first reason is smaller context, but not in the vague sense that
shorter is always better. The useful reduction is more specific: each
role should receive the context it can act on and less of everything
else.

The weakness of the one-human, one-agent model often appears as
context-window pressure, lower judgment quality over long tasks, one
narrow viewpoint, and unclear human intervention points.

Operationally, the same weakness appears in another form. Agents lose
track of early instructions and checklists. They miss project guidance
or available skills. After compaction, they can continue with the wrong
shape of work. The underlying issue is not that the agent never saw the
instruction. It is that the right context is not reliably supplied at
the moment when a role needs it.

Splitting roles makes each job smaller. The planner shapes the work. The
implementer focuses on the change. The reviewer sees the diff and
evidence. The approver stops risky actions. The coordinator sees routes
and open obligations. The operator focuses on state, exceptions, and
reporting to the human.

This is not “more agents are magically smarter.” It is “each role
receives less irrelevant context.”

## 4. Separate Implementer From Reviewer

The second reason is separating the implementer from the reviewer. A
task can look finished from inside the implementation path and still be
weak when judged from the requirement.

A setup where the implementer is the only judge of completion has an
obvious weak point. The same actor that made the change picks the
evidence, runs the tests, and says the work is done.

Human software teams already know why that is weak. A pull request
approved only by its author is not much of a review. The same issue
exists with agents.

A second agent does not automatically create objectivity. Two instances
of the same model with the same prompt and the same context can share
blind spots. So the separation is not merely giving the reviewer a
different name.

The useful separation changes what the reviewer sees.

The reviewer should receive the change, the evidence, the validation
command, and the artifact. It should not need the implementer’s whole
implementation transcript. The reviewer checks whether the result
reaches the requirement, not whether the implementer’s reasoning sounded
plausible. That can decorrelate the review enough to matter even when
the underlying model family is the same.

## 5. Approval Is a Different State

The third reason is approval. Caution by the implementer is not a
procedure.

Deletion, deployment, credential changes, production-data writes, public
posting, public comments, and branch publication are not the same kind
of act as editing a draft file. An implementer being technically able to
perform the action does not mean the action should proceed.

What is needed here is a different state transition.

Routine work flows. Risky work pauses. The reason for the pause, the
required approval, the approver, and the rejected path are recorded.
That is more stable when represented as a role and a harness rule than
as something every implementer must remember from the prompt.

In a multi-agent setup, the approver can be separate from the
implementer. The role that can execute is not automatically the role
that decides whether a risky boundary should be crossed. That looks
organizational because the risk is organizational: execution and
authorization are different responsibilities.

## 6. Move Conversation and Checklists Outside Chat

The fourth reason is memory outside one conversation.

Agent-to-agent conversation, checklists, artifacts, and reply
obligations should live outside any one agent’s private transcript. If
the system depends on one conversation log, agents are hard to replace,
compaction becomes dangerous, and humans end up inferring open work from
terminal scrollback.

At minimum, these things should be external:

- who asked whom to do what;
- which reply is required;
- which artifact is evidence;
- what counts as completion.

Once this layer exists, agents become more replaceable. Claude Code and
Codex can both read the same mail, artifact, and checklist. The model’s
personality still matters, but continuity moves out of the model
client’s transcript and into the record of work.

## 7. Parallelism Is a Side Effect

Multi-agent systems are often sold as parallelism. Parallelism does
help: divide research, compare options, overlap implementation and
review, or ask multiple reviewers for different perspectives.

But treating parallelism as the main reason leads to bad design. It
optimizes for motion before the system can say what counts as done.

The first-order need is role separation, reply obligations, review,
approval, and artifact records. Without those, adding agents only makes
progress look faster while making it harder to know what is complete,
what is unverified, and who is waiting on whom.

Parallelism works after responsibility is legible.

## 8. Multi-Agent Is a Small Organization

That is why multi-agent design is closer to organization design than to
a trick for running more prompts. The resemblance is not decorative; it
appears at the points where attention, authority, and evidence have to
move between roles.

There are planners, implementers, reviewers, approvers, coordinators,
and operators.

This is not because human companies are aesthetically interesting. It is
because human organizations have spent a long time handling finite
attention, separation of duties, approval, handoff, audit, and exception
handling. Long agent tasks converge on similar problems.

Use one agent when one agent is enough.

Reach for multi-agent structure when these questions start shaping the
work:

- Should someone other than the implementer inspect the evidence?
- Should risky actions enter a separate approval state?
- Should work memory outlive the chat transcript?
- Should open requests be machine-inspectable?
- Should the human avoid reading every pane?
- Should the model or CLI be replaceable midstream?

If several answers are yes, multi-agent is not decoration. It is the
structure that lets work run longer without losing its obligations.

## 9. What The Next Pieces Cover

Putting this question first changes the rest of the series. The later
pieces are not separate tool notes; they answer what has to exist once
responsibilities are split.

The next post, [“tmux Survives, But Its Visible Form
Disappears”](https://i9wa4.github.io/2026-07-14-tmux-survives-visible-form-disappears.md), is
about the execution substrate that can carry multiple agents. The
terminal does not disappear, but it should stop being the object the
human directly watches.

The following post, [“Two State Machines for Agent
Work”](https://i9wa4.github.io/2026-07-14-two-state-machines-for-agent-work.md), is about
separating operating state from task meaning. Message delivery and task
acceptance are different events.

The final post, [“A Company Inside the Personal
Computer”](https://i9wa4.github.io/2026-07-14-company-inside-personal-computer.md), is about
why this structure starts to look like a small organization inside a
personal workstation.

The point of multi-agent work is not a dramatic swarm.

It is taking responsibilities that are incompatible inside one long
chat, externalizing them, naming them, recording them, and making them
reviewable.

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fen%2Fblog%2F2026-07-14-why-multi-agent.html&text=Why%20Multi-Agent%3F%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=Why%20Multi-Agent%3F%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fen%2Fblog%2F2026-07-14-why-multi-agent.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fen%2Fblog%2F2026-07-14-why-multi-agent.html&title=Why%20Multi-Agent%3F%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
