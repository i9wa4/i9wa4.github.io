---
name: generate-trends
description: |
  Generate daily tech trend digest articles for the auto/ directory.
  Creates EN and JA trend summaries with checkbox-based feedback.
  Use when user asks to generate trends, create a tech digest, or
  wants to see what's trending in tech today.
---

# Generate Tech Trend Digest

## 1. Workflow

Execute these steps in order:

### 1.1. Step 1: Update preferences from feedback

Run `uv run python bin/parse-feedback.py` to scan existing articles for checked
items and update `auto/.preferences.yaml`.

### 1.2. Step 2: Read preferences

Read `auto/.preferences.yaml` to understand user interests. If `topics: {}` is
empty, skip personalization entirely -- generate 100% diverse content.

### 1.3. Step 3: Get today's date

Use today's date in YYYY-MM-DD format for filenames and front matter.

### 1.4. Step 4: Search for current trends

Use WebSearch to find today's trending tech topics from these sources:

**For EN article:**

- Hacker News top stories and discussions
- GitHub trending repositories (all languages)
- Reddit r/programming, r/technology, r/machinelearning

**For JA article:**

- Zenn trending articles
- Qiita trending articles
- Plus the same HN/GitHub sources above

### 1.5. Step 5: Generate EN article

Create `auto/YYYY-MM-DD-en-tech-trends.qmd` with this exact structure:

```text
---
title: "Tech Trends (EN) - YYYY-MM-DD"
author: uma-chan
categories:
  - "auto"
  - "tech-trends"
  - "en"
date: YYYY-MM-DD
date-modified: last-modified
description: |
  Daily tech trend digest - Hacker News, GitHub Trending, Reddit
image: "/assets/common/icon_hhkb3_large.jpg"
---

## Picks For You

(Items matching user preferences. Max 50% of total items.
Skip this section entirely if preferences are empty.)

- [ ] **Title** - 2-3 sentence summary [tag1, tag2]

## Discover

(Diverse items from various tech domains. Min 50% of total items.)

- [ ] **Title** - 2-3 sentence summary [tag1, tag2]

## Highlights

Brief 2-3 sentence deep-dive on the top 3 most notable items.
```

### 1.6. Step 6: Generate JA article

Create `auto/YYYY-MM-DD-ja-tech-trends.qmd` with the same structure but:

- Title: `"Tech Trends (JA) - YYYY-MM-DD"`
- Category: `"ja"` instead of `"en"`
- Description in Japanese
- Article body in Japanese
- Include Zenn/Qiita trending content

### 1.7. Step 7: Update category buttons

Run `uv run python bin/update-categories.py auto`.

## 2. Content Rules

- Total 8-12 items per article
- If preferences exist: max 50% personalized, min 50% diverse
- If preferences empty: 100% diverse
- Each item MUST end with tags in square brackets: `[tag1, tag2]`
- Tags: lowercase, hyphenated (e.g., `machine-learning`, `web-development`)
- Do NOT invent or fabricate trends -- only include real, verifiable items
- Skip generating if the file for today already exists

## 3. Tag Guidelines

Use consistent tag names across articles:

- Languages: `rust`, `python`, `go`, `typescript`, `java`
- Domains: `ai`, `machine-learning`, `web-development`, `devops`, `databases`
- Tools: `kubernetes`, `docker`, `terraform`, `neovim`, `git`
- Platforms: `github`, `aws`, `gcp`, `azure`, `databricks`
