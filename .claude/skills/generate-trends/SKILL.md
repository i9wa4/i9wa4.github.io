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

### 1.3. Step 3: Fetch trending data

Run `uv run python bin/fetch-trends.py > /tmp/trends.json` to fetch real
articles from public APIs. Then read `/tmp/trends.json`.

The JSON has this structure:

```json
{
  "en": {
    "hackernews": [{"title": "...", "url": "...", "score": 193}],
    "devto": [{"title": "...", "url": "...", "reactions": 367, "tags": [...]}],
    "github": [{"title": "owner/repo", "url": "...", "description": "...", "stars": 5000}]
  },
  "ja": {
    "zenn": [{"title": "...", "url": "...", "likes": 114}],
    "qiita": [{"title": "...", "url": "...", "likes": 39, "tags": [...]}],
    "hatena": [{"title": "...", "url": "...", "bookmarks": 889}]
  }
}
```

Use this data as the sole source for article items. Do NOT use WebSearch.

**EN sources:** Hacker News, dev.to, GitHub Trending
**JA sources:** Zenn, Qiita, Hatena Bookmark

### 1.4. Step 4: Get today's date

Use today's date in YYYY-MM-DD format for filenames and front matter.

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
  Daily tech trend digest (EN) - Hacker News, GitHub Trending, Reddit
image: "/assets/common/icon_hhkb3_large.jpg"
---

## Picks For You

(Items matching user preferences. Max 50% of total items.
Skip this section entirely if preferences are empty.)

- [ ] **[Title](https://example.com/article)** - 2-3 sentence summary [tag1, tag2]

## AI & Machine Learning

(Group AI/ML related items here)

- [ ] **[Title](https://example.com/article)** - 2-3 sentence summary [tag1, tag2]

## Development & Tools

(Group developer tools, languages, frameworks here)

- [ ] **[Title](https://example.com/article)** - 2-3 sentence summary [tag1, tag2]

## Infrastructure & Security

(Group cloud, devops, security items here)

- [ ] **[Title](https://example.com/article)** - 2-3 sentence summary [tag1, tag2]

## Others

(Items that don't fit the above categories)

- [ ] **[Title](https://example.com/article)** - 2-3 sentence summary [tag1, tag2]

## Highlights

Brief 2-3 sentence deep-dive on the top 3 most notable items.
```

### 1.6. Step 6: Generate JA article

Create `auto/YYYY-MM-DD-ja-tech-trends.qmd` with the same structure but:

- Title: `"Tech Trends (JA) - YYYY-MM-DD"`
- Category: `"ja"` instead of `"en"`
- Description: `Daily tech trend digest (JA) - Zenn, Qiita, Hatena Bookmark`
- Article body in Japanese
- Use JA sources only (Zenn, Qiita, Hatena Bookmark)

### 1.7. Step 7: Update category buttons

Run `uv run python bin/update-categories.py auto`.

## 2. Content Rules

- Target ~30 items per article (use all fetched data)
- Group items loosely by category: AI & ML, Development & Tools,
  Infrastructure & Security, Others
- If preferences exist: max 50% personalized, min 50% diverse
- If preferences empty: 100% diverse (grouped by category)
- Every item MUST come from the fetched trends JSON data
- Every item MUST link to the actual source URL from the JSON data
- Format: `**[Article Title](https://actual-url-to-the-article)**`
- Each item MUST end with tags in square brackets: `[tag1, tag2]`
- Tags: lowercase, hyphenated (e.g., `machine-learning`, `web-development`)
- NEVER fabricate articles, URLs, or trends -- every item must be verifiable
- NEVER use vague summaries like "AI is trending" -- cite a specific article
- Skip generating if the file for today already exists

## 3. Tag Guidelines

Use consistent tag names across articles:

- Languages: `rust`, `python`, `go`, `typescript`, `java`
- Domains: `ai`, `machine-learning`, `web-development`, `devops`, `databases`
- Tools: `kubernetes`, `docker`, `terraform`, `neovim`, `git`
- Platforms: `github`, `aws`, `gcp`, `azure`, `databricks`
