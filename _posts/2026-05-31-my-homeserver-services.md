---
title: "My Homeserver — Live Services Dashboard"
date: 2026-05-31
categories: [Self-Hosting, Homelab Series]
tags: [homelab, self-hosting, docker, home-server, services, dashboard]
description: "A live screenshot of my homeserver dashboard showing all the services I self-host."
image: /assets/BannerImages/2026-05-31-my-homeserver-services.png
---

> This page shows a **live screenshot** of my homeserver dashboard. What you see below is always up to date with what's actually running.

## Dashboard

<div style="position:relative; text-align:center; background:#1a1a2e; border-radius:8px; min-height:400px; display:flex; align-items:center; justify-content:center; overflow:hidden;">
  <p style="position:absolute; color:#888; font-style:italic; z-index:0;">Loading live screenshot...</p>
  <img src="https://homeworkflows.mavsankar.com/webhook/homepage-screenshot" alt="Homepage Dashboard" style="position:relative; max-width:100%; border-radius:8px; z-index:1;">
</div>

_Live screenshot of my homeserver dashboard_

---

## What's Running

The dashboard above is powered by [Homepage](https://gethomepage.dev/) and shows all my self-hosted services at a glance. I keep adding and removing services, so rather than listing them here, the screenshot above is always the source of truth — what you see is exactly what's running right now.

The services are grouped into categories like apps, monitoring, developer tools, and AI — all running as Docker containers behind a reverse proxy.

---

## Why Self-Host?

A few reasons I run all of this instead of using cloud services:

- **Privacy** — My notes, bookmarks, and automations stay on hardware I control
- **Cost** — After the initial setup, it's just electricity.
- **Learning** — Docker, networking, reverse proxies, CI/CD — this is a playground for everything.

---

## The Hardware

This entire stack runs on a 2019 Lenovo Flex 5 with a broken screen:

- **CPU:** Intel i7-8550U (4 cores / 8 threads)
- **RAM:** 16 GB DDR4
- **Storage:** 512 GB NVMe SSD
- **GPU:** NVIDIA MX130 (used for Ollama inference)
- **OS:** Ubuntu Server 22.04

No rack. No enterprise hardware. Just a laptop with the lid closed, running 24/7.

---

## The Series

This post is part of the **Homelab Series** where I document building this entire setup from scratch. Check out all the posts in the series [here](/categories/homelab-series/).

---

*This page updates automatically — the screenshot always reflects the current state of the server.*
