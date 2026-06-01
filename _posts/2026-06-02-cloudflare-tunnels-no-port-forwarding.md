---
title: "Cloudflare Tunnels — Public Access Without Port Forwarding"
date: 2026-06-02
categories: [Self-Hosting, Homelab Series]
tags: [homelab, cloudflare, networking, tunnels, reverse-proxy]
---

> **Part 2** of the [Homelab Series](/categories/homelab-series/) — exposing your home server to the internet without opening a single port.

## The Problem

My ISP router has a web gateway where I can configure firewall rules and other settings, but **port forwarding is restricted to business plans**. No amount of Googling or calling support changed that. Without port forwarding, nothing running on my laptop is reachable from outside my home network.

As a developer, I use Microsoft Dev Tunnels at work all the time — temporary public URLs for local services during development. I needed the same thing but permanent: custom domains, running as a daemon, and free. That led me to **Cloudflare Tunnels**.

## What is a Cloudflare Tunnel?

A Cloudflare Tunnel creates an outbound-only connection from your server to Cloudflare's edge network. Traffic flows like this:

```
User → Cloudflare Edge → Tunnel → Your Server
```

Your server **dials out** to Cloudflare — no inbound ports needed. Your ISP, firewall, NAT — none of it matters. If your machine can make HTTPS requests, it can serve traffic.

This is actually **more secure** than traditional port forwarding because:
- No ports exposed on your router
- No need for a static IP
- Cloudflare handles DDoS protection, SSL/TLS, and caching
- Traffic is encrypted end-to-end through the tunnel

## Prerequisites

- A domain managed by Cloudflare (free plan works)
- A Cloudflare account with Zero Trust enabled (also free for up to 50 users)
- `cloudflared` running on your server (Docker or native)

## Setting It Up

### 1. Create a Tunnel

Go to [Cloudflare Zero Trust Dashboard](https://one.dash.cloudflare.com/) → Networks → Tunnels → Create a tunnel.

Give it a name (e.g., `homeserver`), and Cloudflare generates a **tunnel token**. This token is what your server uses to authenticate.

<p align="center">
  <img src="../assets/CloudflareTunnel/create_a_tunnel.png" alt="Cloudflare dashboard showing tunnel creation and token generation">
  <br>
  <em>Creating a tunnel in Cloudflare Zero Trust — the generated token is all your server needs. (In the screenshot, the token is on the right side of the docker command)</em>
</p>

### 2. Run cloudflared

The simplest way — a single Docker container:

```yaml
services:
  cloudflared:
    image: cloudflare/cloudflared:latest
    container_name: cloudflared
    restart: always
    command: tunnel run
    environment:
      - TUNNEL_TOKEN=${CLOUDFLARE_TUNNEL_TOKEN}
    networks:
      - homeserver
```

Set your token in a `.env` file:

```
CLOUDFLARE_TUNNEL_TOKEN=eyJhIjoiYWJjZGVm...
```

That's it. `docker compose up -d` and the tunnel is live.

### 3. Add Public Hostnames

Back in the Cloudflare dashboard, add routes for each service. Each route maps a subdomain to an internal service:

| Public Hostname | Service | URL |
|----------------|---------|-----|
| `landing.yourdomain.com` | HTTP | `http://reverse-proxy:8000` |
| `books.yourdomain.com` | HTTP | `http://reverse-proxy:8000` |
| `ai.yourdomain.com` | HTTP | `http://reverse-proxy:8000` |

<p align="center">
  <img src="../assets/CloudflareTunnel/public_hostnames.png" alt="Cloudflare dashboard showing public hostname configuration">
  <br>
  <em>Each subdomain routes to the reverse proxy — Nginx handles the rest.</em>
</p>

Notice all routes point to the **reverse proxy**, not individual services. The reverse proxy (Nginx) handles routing based on the hostname. More on that in a later post.

## Architecture Overview

Here's how the full flow works:

```
Internet
    │
    ▼
Cloudflare Edge (SSL termination, DDoS protection)
    │
    ▼ (encrypted tunnel, outbound-only)
cloudflared container
    │
    ▼
reverse-proxy (Nginx, port 8000)
    │
    ├── landing.* → homepage:3000
    ├── books.* → kavita:5000
    ├── ai.* → open-webui:8080
    ├── pdf.* → stirling-pdf:8080
    └── ... (12+ services)
```

All containers sit on the same Docker network (`homeserver`), so Nginx can reach them by container name.

## Access Policies (Optional but Recommended)

For services that don't have their own authentication (like my homepage dashboard and dev tools), I use **Cloudflare Access policies**. These add a login gate before the tunnel even reaches your server:

- Go to Zero Trust → Access → Applications
- Add a Self-hosted application
- Set the domain (e.g., `landing.yourdomain.com`)
- Add a policy: allow emails matching your own email, one-time PIN verification

Now even if someone guesses your subdomain, they hit a Cloudflare login screen before reaching anything.

<p align="center">
  <img src="../assets/CloudflareTunnel/access_policies.png" alt="Cloudflare Access policy configuration">
  <br>
  <em>Cloudflare Access adds a login gate — one-time PIN to your email before anything loads.</em>
</p>

<p align="center">
  <img src="../assets/CloudflareTunnel/assign_policy.png" alt="Cloudflare Access policy assignment to an application">
  <br>
  <em>Assigning a Cloudflare Access policy to an application — ensures only authorized users can access the service.</em>
</p>

## What This Costs

- Cloudflare account: **Free**
- Tunnel: **Free** (unlimited bandwidth)
- Domain: ~$10/year
- Zero Trust (up to 50 users): **Free**

Total: the cost of a domain name.

## Before and After

**Before Cloudflare Tunnel:**
- Services only accessible on home WiFi

**After:**
- Every service accessible from anywhere with a clean URL
- SSL/TLS handled automatically
- No ports exposed, no static IP needed
- Takes 30 seconds to expose a new service

## What's Next

At this point I could access my services from anywhere — but I still needed a monitor to manage the server itself. In the next post, I'll cover how **MeshCentral** gave me full remote access to a screenless laptop, and why it's better than TeamViewer or AnyDesk for a homelab.

---

*All the code and configurations for my home server are open source: [github.com/mavsankar/homeserver](https://github.com/mavsankar/homeserver)*
