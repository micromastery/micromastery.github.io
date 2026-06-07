---
title: "What's Running on My Homeserver — Live Services"
date: 2026-05-31
categories: [Self-Hosting, Homelab Series]
tags: [homelab, self-hosting, docker, home-server, services, dashboard]
description: "A live view of all the services running on my homeserver, dynamically loaded from the actual configuration."
image: /assets/BannerImages/2026-05-31-my-homeserver-services.png
---

> This page is **dynamic** — the services listed below are loaded live from my homeserver's configuration. What you see is what's actually running.

## Dashboard

<div style="position:relative; text-align:center; background:#1a1a2e; border-radius:8px; min-height:400px; display:flex; align-items:center; justify-content:center; overflow:hidden;">
  <p style="position:absolute; color:#888; font-style:italic; z-index:0;">Loading live screenshot...</p>
  <img src="https://homeworkflows.mavsankar.com/webhook/homepage-screenshot" alt="Homepage Dashboard" style="position:relative; max-width:100%; border-radius:8px; z-index:1;">
</div>

_Live screenshot of my homeserver dashboard_

---

## Services

<div id="services-container" style="margin-top:1rem;">
  <p style="color:#888; font-style:italic;">Loading services...</p>
</div>

<script>
(async () => {
  const container = document.getElementById('services-container');
  try {
    const res = await fetch('https://homeworkflows.mavsankar.com/webhook/services');
    const data = await res.json();
    const services = data.services;

    // Group by category
    const grouped = {};
    services.forEach(s => {
      if (!grouped[s.category]) grouped[s.category] = [];
      grouped[s.category].push(s);
    });

    let html = '';
    for (const [category, items] of Object.entries(grouped)) {
      html += `<h3>${category}</h3>`;
      html += '<div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:1rem; margin-bottom:1.5rem;">';
      items.forEach(s => {
        const docsLink = s.docs ? `<a href="${s.docs}" target="_blank" rel="noopener" style="font-size:0.85em;">Docs ↗</a>` : '';
        const detailsHtml = s.details ? `<p style="margin:0.5rem 0; color:#ccc; font-size:0.85em;">${s.details}</p>` : '';
        html += `
          <div style="border:1px solid #333; border-radius:8px; padding:1rem; background:#1a1a2e;">
            <strong>${s.name}</strong>
            <p style="margin:0.4rem 0; color:#aaa; font-size:0.9em;">${s.description}</p>
            ${detailsHtml}
            ${docsLink}
          </div>`;
      });
      html += '</div>';
    }

    html += `<p style="color:#666; font-size:0.8em; margin-top:2rem;">Last updated: ${new Date(data.lastUpdated).toLocaleDateString()}</p>`;
    container.innerHTML = html;
  } catch (e) {
    container.innerHTML = '<p style="color:#cc6666;">Could not load services. The homeserver might be temporarily offline.</p>';
  }
})();
</script>

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

This post is part of the **Homelab Series** where I document building this entire setup from scratch. Check out all the posts in the series [here](/categories/homelab-series/).

---

*This page updates automatically — the screenshot always reflects the current state of the server.*
