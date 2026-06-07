---
title: "What's Running on My Homeserver — Live Services"
date: 2026-05-31
categories: [Self-Hosting, Homelab Series]
tags: [homelab, self-hosting, docker, home-server, services, dashboard]
description: "A live view of all the services running on my homeserver, dynamically loaded from the actual configuration."
image: /assets/BannerImages/2026-05-31-my-homeserver-services.png
pin: true
---

> Part of the [Homelab Series](/categories/homelab-series/) — a live reference page for all services running on my home server.

> This page is **dynamic** — the services listed below are loaded live from my homeserver's configuration. What you see is what's actually running.

## Dashboard

<div style="position:relative; text-align:center; background:#1a1a2e; border-radius:8px; min-height:400px; display:flex; align-items:center; justify-content:center; overflow:hidden;">
  <p style="position:absolute; color:#888; font-style:italic; z-index:0;">Loading live screenshot...</p>
  <img id="dashboard-screenshot" src="https://homeworkflows.mavsankar.com/webhook/homepage-screenshot" alt="Homepage Dashboard" style="position:relative; max-width:100%; border-radius:8px; z-index:1;">
</div>

<p id="screenshot-timestamp" style="color:#666; font-size:0.8em; text-align:center;">_Live screenshot of my homeserver dashboard_</p>

<script>
document.getElementById('dashboard-screenshot').addEventListener('load', function() {
  const ts = new Date().toLocaleString();
  document.getElementById('screenshot-timestamp').innerHTML = '<em>Live screenshot of my homeserver dashboard — loaded ' + ts + '</em>';
});
</script>

---

## Services

<div id="services-container" style="margin-top:1rem;">
  <p style="color:#888; font-style:italic;">Loading services...</p>
</div>

<script src="/assets/js/services-loader.js"></script>

---

## The Hardware

This entire stack runs on a 2019 Lenovo Flex 5 with a broken screen:

- **CPU:** Intel i7-8550U (4 cores / 8 threads)
- **RAM:** 16 GB DDR4
- **Storage:** 512 GB NVMe SSD
- **GPU:** NVIDIA MX130 (used for Ollama inference)
- **OS:** Windows 11 + Docker Desktop (WSL2)

No rack. No enterprise hardware. Just a laptop with the lid closed, running 24/7.

---

## The Series

This post is part of the **Homelab Series** where I document building this entire setup from scratch. To know how the journey started, read [Part 1 — From Broken Laptop to Home Server](/posts/from-broken-laptop-to-home-server/). Check out all the posts in the series [here](/categories/homelab-series/).

---

*This page updates automatically — the screenshot always reflects the current state of the server.*
