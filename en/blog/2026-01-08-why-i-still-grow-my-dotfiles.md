# Why I Still Grow My Dotfiles in the Age of AI Coding Agents
uma-chan
2026-01-08

## 1. What Claude Code’s Evolution Tells Us

Boris Cherny, the creator of Claude Code, announced the 2.1.0 release
with a massive list of shipped features.

<blockquote class="twitter-tweet">

<p lang="en" dir="ltr">

Claude Code 2.1.0 is officially out! claude update to get it We
shipped: - Shift+enter for newlines, w/ zero setup - Add hooks directly
to agents & skills frontmatter - Skills: forked context, hot reload,
custom agent support, invoke with / - Agents no longer stop when you
deny <a href="https://t.co/p29WlcdwoR">https://t.co/p29WlcdwoR</a>
</p>

— Boris Cherny (@bcherny)
<a href="https://twitter.com/bcherny/status/2009072293826453669?ref_src=twsrc%5Etfw">January
2026</a>
</blockquote>

<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Background agent execution, `/teleport` for handing off CLI sessions to
web/mobile, subagent hooks, mobile notifications for long-running tasks
— the list goes on.

My first reaction was:

**“You can only do this in a terminal” will not be true for much
longer.**

## 2. Feature Comparisons Are Becoming Meaningless

### 2.1. The Current Advantage

As of early 2026, the terminal + Claude Code combination still has some
advantages. With tmux, you can run unlimited parallel agents in the same
directory on different tasks.

But looking at the development roadmap, this gap is closing.

### 2.2. Convergence Is Inevitable

Claude Code’s VS Code extension uses the same configuration files as the
terminal version:

``` text
.claude/
  CLAUDE.md
  rules/
  skills/
  agents/
  commands/
```

**Claude Code’s features are interface-agnostic.** The configuration
you’re carefully building works everywhere.

So why choose the terminal at all?

## 3. What Remains: The Ability to Build Your Environment

### 3.1. The Real Value of Terminal Environments

The real value of a terminal environment is not something you can
compare in a feature matrix.

**The real value is that you can define your entire development
environment in text files and manage it with Git.**

### 3.2. Unix Philosophy

The Claude Code documentation itself says it:

> ## Why developers love Claude Code
>
> - **Works in your terminal:** Not another chat window. Not another
>   IDE. Claude Code meets you where you already work, with the tools
>   you already love.
>
> - **Unix philosophy:** Claude Code is composable and scriptable.
>
> — [Claude Code Overview](https://code.claude.com/docs/en/overview)

In a terminal environment, you can combine AI agents with shell scripts
and other CLI tools to build a development environment that is uniquely
yours.

### 3.3. Every Layer Is Replaceable

In a terminal environment, every tool is swappable:

| Layer                | Options                            | Swappable? |
|----------------------|------------------------------------|------------|
| Terminal emulator    | Ghostty, WezTerm, iTerm2, Kitty    | Yes        |
| Terminal multiplexer | tmux, zellij, screen               | Yes        |
| Shell                | zsh, bash, fish                    | Yes        |
| Text editor          | Neovim, Vim, Emacs, Helix          | Yes        |
| AI coding agent      | Claude Code, Codex CLI, Gemini CLI | Yes        |

Each layer evolves independently.

I’ve switched my terminal emulator from Alacritty to Ghostty to WezTerm
recently, and my development experience hasn’t changed at all. My tmux,
Vim, and Zsh keybindings are tuned to work together across all of them.

## 4. The Case for Dotfiles

### 4.1. What Are Dotfiles?

Dotfiles is the culture of managing your home directory configuration
files with Git.

A typical structure looks like this:

``` text
dotfiles/
  .config/
    claude/      # AI coding agent config
    tmux/        # Terminal multiplexer config
    wezterm/     # Terminal emulator config
    nvim/        # Text editor config
  .zshrc         # Shell config
  bin/           # Custom scripts
```

### 4.2. Why Grow Your Dotfiles?

#### 4.2.1. Reproducibility

`git clone` and a few commands give you the same environment on any new
machine.

The confidence that you can always reproduce your setup motivates you to
invest in making it better.

#### 4.2.2. Evolution History

Every configuration change is tracked in Git.

You can always trace why you made a change and easily revert to a
previous state.

#### 4.2.3. Accumulated Knowledge

Dotfiles are a concrete expression of “how I want to work.”

Configuration refined over years becomes an asset you can’t get anywhere
else.

#### 4.2.4. Sharing and Learning

You can learn from others’ dotfiles and share your own.

Since dotfiles are text files, you can feed them to an AI and ask “What
does this configuration do?” or “How can I adopt this in my setup?” The
barrier to understanding someone else’s complex configuration has
dropped dramatically.

Here’s a post from the Japanese developer community that captures this
well. A developer recommends learning Claude Code configuration by
reading another developer’s dotfiles — configuration knowledge that was
common among dotfiles enthusiasts but hadn’t spread to the wider
community.

<blockquote class="twitter-tweet">

<p lang="ja" dir="ltr">

ryoppippiからclaude
codeの設定を学ぶといいので、みんなryoppippiのdotfilesも見ような<a href="https://t.co/RduDuxgLml">https://t.co/RduDuxgLml</a>
<a href="https://t.co/NJMD3hNyFP">https://t.co/NJMD3hNyFP</a>
</p>

— yasunori🫖@loglass🐳 (@YKirin0418)
<a href="https://twitter.com/YKirin0418/status/1977585870787301738?ref_src=twsrc%5Etfw">October
13, 2025</a>
</blockquote>

<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

The information gap is real. Dotfiles users share and learn from each
other, while everyone else misses out.

### 4.3. Claude Code Config + Surrounding Tools = Your Ultimate Environment

Claude Code configuration alone works in IDEs too. But…

``` text
dotfiles/
  .config/
    claude/         # <- Works in IDEs too
      CLAUDE.md
      rules/
      agents/
      commands/

    tmux/           # <- Terminal-only
      tmux.conf

    wezterm/        # <- Terminal-only
      wezterm.lua

  .zshrc            # <- Terminal-only

  bin/              # <- Terminal-only
```

Claude Code config is a **point**. Your entire dotfiles are a
**surface**.

The integration with surrounding tools lets AI blend into your entire
development workflow.

## 5. Getting Started with Dotfiles

Dotfiles aren’t built in a day. You grow them gradually, picking up new
ideas as you go.

Start small — perhaps with your Claude Code configuration — and expand
from there.

Some resources to get started:

- [Getting Started with Dotfiles - Dries
  Vints](https://www.driesvints.com/blog/getting-started-with-dotfiles/)
- [GitHub does dotfiles](https://dotfiles.github.io/)

## 6. Summary

### 6.1. Features Will Converge

As Claude Code’s `/teleport` and background execution show, the feature
gap between terminal and IDE is disappearing.

### 6.2. What Remains Is “Environment Building”

The value of a terminal environment is that it is programmable,
composable, swappable, and portable. An environment defined entirely in
text files and managed with Git will not lose its shine even after AI
agent features converge.

### 6.3. Grow Your Dotfiles

Claude Code config works in IDEs too. But…

- Workflow automation with scripts
- Integration with custom tools and bleeding-edge CLIs
- Unified keybindings across multiple tools

These are only possible in an environment you build yourself.

### 6.4. And Most Importantly

**Dotfiles are fun. I highly recommend it. Let your setup reflect how
you live and work.**

That’s all I wanted to say.

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fen%2Fblog%2F2026-01-08-why-i-still-grow-my-dotfiles.html&text=Why%20I%20Still%20Grow%20My%20Dotfiles%20in%20the%20Age%20of%20AI%20Coding%20Agents%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=Why%20I%20Still%20Grow%20My%20Dotfiles%20in%20the%20Age%20of%20AI%20Coding%20Agents%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fen%2Fblog%2F2026-01-08-why-i-still-grow-my-dotfiles.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fen%2Fblog%2F2026-01-08-why-i-still-grow-my-dotfiles.html&title=Why%20I%20Still%20Grow%20My%20Dotfiles%20in%20the%20Age%20of%20AI%20Coding%20Agents%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
