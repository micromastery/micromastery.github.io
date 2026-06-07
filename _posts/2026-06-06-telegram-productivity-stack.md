---
title: "Building a Self-Hosted Productivity Stack"
date: 2026-06-06
categories: [Self-Hosting, Homelab Series]
tags: [homelab, n8n, memos, linkwarden, automation, self-hosting]
description: "Memos for thoughts, Linkwarden for bookmarks, n8n to glue it all together — building a personal productivity system on a home server."
image: /assets/BannerImages/2026-06-06-telegram-productivity-stack.png
---

> **Part 6** of the [Homelab Series](/categories/homelab-series/) — capturing thoughts, saving links, and automating workflows with self-hosted tools.

## The Problem with "I'll Remember That Later"

I have ideas at the worst times. Walking to the kitchen, half-asleep at 2 AM, in the middle of debugging something completely unrelated. The thought shows up, sticks around for 30 seconds, and vanishes.

Before the home server, my system was: text myself on WhatsApp. Or open Google Keep. Or just tell myself I'll remember. I had thoughts scattered across different apps and zero habit of reviewing any of them.

The bookmark problem was similar. I'd find an interesting article, think "I'll read this later," and save it to Pocket. Pocket shut down (or got absorbed into Firefox — same thing). My browser bookmarks became a graveyard of links I'd never visit again. No tags, no search, no way to resurface anything useful.

What I needed was dead simple: one place to send thoughts, one place to save links, and something that would remind me they exist.

## Choosing the Tools

My criteria for any service on this server:

1. **Lightweight** — this is a laptop, not a rack server
2. **API-friendly** — if I can't automate it, I won't use it
3. **Self-hosted** — the whole point of this project

For notes, I landed on **Memos**. It's a single container, stores everything in SQLite, has a clean API, and supports tags. No folders, no hierarchy, no notebooks to organize. You just write and tag. That's it.

For bookmarks, **Linkwarden**. It's heavier (needs PostgreSQL + Meilisearch for search), but it actually archives pages, extracts metadata, and has solid tagging. It replaced Pocket without the "some company will shut this down" anxiety.

For automation, **n8n**. This is where it gets interesting.

## Why n8n

n8n is a low-code workflow automation tool — think Zapier but self-hosted. You connect triggers to actions with a visual editor, and for anything the built-in nodes can't do, there's a Code node where you write JavaScript.

I didn't evaluate alternatives much. I'd seen n8n mentioned in self-hosting communities, it had community workflow templates I could learn from, and — honestly — I could describe what I wanted to an AI and get a working workflow outline in minutes. The visual editor makes it easy to debug: you can see exactly where data flows, what each node receives, and where things break.

It also has trigger nodes for Telegram, webhooks, cron schedules, and dozens of other sources — so you can wire up inputs and notifications however you want.

## Connecting It All Together

Each service has an API, but I'm not going to open three web UIs every time I have a thought. The whole point of n8n is to create workflows that let me interact with these services from wherever I already am.

I started with Telegram bots as the input layer — it was already on my phone, BotFather makes bot creation trivial, and n8n has a built-in Telegram trigger node. Two bots: one for Memos, one for Linkwarden, because the interactions are completely different and I didn't want command conflicts.

*(The delivery mechanism isn't the point though — you could swap Telegram for ntfy, Discord, a CLI tool, or anything with a webhook. What matters is the workflow pattern underneath.)*

## Capturing Thoughts with Memos

This is my most-used workflow. It understands several commands:

```
/idea <text>     — Save an idea (my favorite)
/todo <text>     — Save a todo item
/code <text>     — Save a code snippet
/project <text>  — Save a project note
/remind 5m <text> — Remind me in 5 minutes
/search <query>  — Search my memos
/recent          — Show last 5 entries
/random          — Resurface a random thought
/tags            — List all tags
```

Or just type anything without a command — it saves as a general thought.

The `/idea` command is the one I use most. Whenever a thought hits — a blog topic, a feature for the server, something I want to try — I type `/idea` and move on. On weekends I sit down, pull up all my `#idea` memos, and actually work through them. It's the difference between "I had a great idea last week but forgot" and having a backlog of things I genuinely want to build.

### How It Works

The workflow is straightforward:

1. **Telegram Trigger** — receives the message
2. **Parse Message** (Code node) — detects commands, extracts arguments, determines the action
3. **Route Action** (Switch node) — sends to the right handler based on action type
4. **Save/Search/etc.** (HTTP Request) — calls the Memos API
5. **Reply** — confirms back to Telegram with a preview

The save action is simple — POST to the Memos API with the content and a tag appended:

```javascript
// Simplified from the actual workflow
if (command === '/idea' && args) {
  return [{ json: { action: 'save', content: args, tag: 'idea', chatId } }];
}

// Default: plain text without any command
if (text.trim().length > 0) {
  return [{ json: { action: 'save', content: text, tag: 'thought', chatId } }];
}
```

The confirmation message uses emoji per tag type — 💡 for ideas, ✅ for todos, 💭 for thoughts — so I can tell at a glance what got saved without opening the app.

### The Reminder System

`/remind 30m close social media` — this one is niche but useful. When I catch myself scrolling, I set a 30-minute reminder to stop. I have a custom notification sound for it so I know it's not a regular message.

The implementation is two workflows:

1. **Save**: When you use `/remind`, it parses the delay (supports `m`/`h`/`d`), calculates the target time, and saves a memo with `#reminder #pending` tags plus metadata (due time, chat ID, reminder text).

2. **Cron**: A separate workflow runs every 5 minutes, fetches all memos with `#pending`, checks if any are due, sends the reminder to Telegram, and removes the `#pending` tag.

Five-minute polling means your reminder might be up to 5 minutes late. That's fine for "remind me in 30 minutes to stop doomscrolling." If I needed precision, I'd use a different approach — but this works and it was simple to build.

## Saving Links with Linkwarden

Different workflow, optimized for one thing: saving links fast.

**Send a URL** → Bot saves it to Linkwarden, replies with "✅ Saved: [url]"

**Reply to the saved message with tags** → Bot categorizes the link (e.g., reply with `docker automation` and it adds both tags)

**Commands:**
```
/tags   — List all existing tags
/title  — Rename a saved link (reply to the saved message)
```

The reply-to-categorize pattern is key. I never tag links at the moment I save them — I'm usually saving them because I'm busy and want to read later. But when I have a minute, I scroll through recent saves and reply with tags. Two separate actions, zero friction for either one.

The detection logic handles multiple URL formats — plain URLs, text links, URLs with trailing punctuation — because people (me) paste links in messy ways:

```javascript
// Check Telegram entities first (most reliable)
for (const entity of entities) {
  if (entity.type === 'url') {
    const url = text.substring(entity.offset, entity.offset + entity.length);
    return [{ json: { action: 'save', url, chatId } }];
  }
  if (entity.type === 'text_link') {
    return [{ json: { action: 'save', url: entity.url, chatId } }];
  }
}
// Fallback: regex match
const match = text.match(/https?:\/\/[^\s<>"']+/);
```

## The Weekly Digest

This one's newer — I just added it this week, so the verdict is still out.

Every Sunday, a cron-triggered workflow:
1. Fetches all memos from the last 7 days
2. Sends them to Ollama (gemma3:4b running locally — more on Ollama in the next post)
3. Gets back a structured summary
4. Sends it to me on Telegram

The prompt is opinionated about format:

```
- Group memos by theme/tag
- List any unchecked todos
- One sentence on what the focus was for the week
- NO motivational quotes
- NO action items (todos already cover that)
- NO follow-up questions
```

I had to be very specific about what *not* to include because small models love adding "inspirational" filler. With temperature 0.4 and a 512 token limit, it stays factual.

Whether this is actually useful or just a novelty — ask me in a month.

## The Pixel Watch Integration

This one's a fun detour. I have a Pixel Watch that I forget to wear after charging. The Home Assistant app on the watch reports battery level and charging status to my Home Assistant instance every 30 minutes. HA forwards that to an n8n webhook, and the logic is simple:

- **Charging + battery > 80%** → "Put your watch on"
- **Not charging + battery ≤ 20%** → "Charge your watch"
- **Quiet hours (11 PM - 7 AM)** → No notifications

The webhook is internal-only. The reverse proxy blocks it from the public internet:

```nginx
# In the n8n server block
include /etc/nginx/snippets/internal_webhooks.conf;
```

```nginx
# snippets/internal_webhooks.conf
location /webhook/pixel-watch-status {
    return 403;
}
```

The watch → HA → n8n path only works on the internal Docker network. No one outside can trigger it.

## What Didn't Work

Not everything stuck:

**Jellyfin** — I set up a media server but realized I don't actually have media to serve. Downloaded it, configured it, deleted it the same week.

**Water drink reminders** — I built a recurring reminder workflow. It just became spam. After a day I muted it, after a week I deleted it. Notifications that fire on a schedule without context become noise instantly.

The lesson: automation works when it's triggered by *your* action (sending a message, saving a link) or by *relevant context* (watch is charged, memo is due). Automation that interrupts you on a timer is just a fancier alarm clock.

## The Docker Setup

All three services are simple Docker Compose stacks:

**Memos** — single container, one volume:
```yaml
services:
  memos:
    image: neosmemo/memos:stable
    container_name: memos
    restart: always
    expose:
      - "5230"
    volumes:
      - memos-data:/var/opt/memos
    networks:
      - homeserver
```

**n8n** — with Browserless Chrome for web scraping workflows:
```yaml
services:
  n8n:
    image: n8nio/n8n:latest
    container_name: n8n
    restart: always
    expose:
      - "5678"
    volumes:
      - n8n-data:/home/node/.n8n
    environment:
      - N8N_HOST=homeworkflows.mavsankar.com
      - N8N_PROTOCOL=https
      - WEBHOOK_URL=https://homeworkflows.mavsankar.com/
    networks:
      - homeserver
```

**Linkwarden** — the heaviest of the three (Postgres + Meilisearch + app):
```yaml
services:
  linkwarden:
    image: ghcr.io/linkwarden/linkwarden:latest
    container_name: linkwarden
    restart: always
    depends_on:
      - linkwarden-db
      - linkwarden-meilisearch
    # ... env vars from .env file
```

They all join the shared `homeserver` network and get a subdomain through the reverse proxy (covered in Post 3).

## Tips

**Start with one bot.** I built the Memos bot first, used it for a week, and only then added Linkwarden. If you build three integrations at once, you won't know which ones you actually use.

**Use the Code node liberally.** n8n's built-in nodes are great for simple API calls, but the moment you need conditional logic or string parsing, the Code node (JavaScript) is faster and more readable than chaining 5 IF nodes together.

**Block internal webhooks.** If a workflow only needs to be triggered from inside your network (cron jobs, Home Assistant, internal services), make sure it's not accessible from the internet. A simple nginx `return 403` on the webhook path does the job.

## What's Next

This series covered the infrastructure — Cloudflare, Docker, Nginx, Gitea, MeshCentral — and now the first real services. But Memos, Linkwarden, and n8n are just the beginning. There's also local AI (Ollama running on that MX130 GPU), a PDF toolkit, file sharing, ebook library, smart home control, and more.

Rather than writing a separate post for each service, I maintain a **[live services page](/posts/my-homeserver-services/)** that dynamically loads everything currently running on the server — with descriptions, what I use each one for, and documentation links. It updates automatically whenever I add or remove something.

Keep checking that page, or better yet — if you've followed this series and set up n8n yourself, create a workflow that checks the page periodically and notifies you when something new shows up. That's the kind of automation a homelab enables.

---

*All the code and configurations for my home server are open source: [github.com/mavsankar/homeserver](https://github.com/mavsankar/homeserver)*
