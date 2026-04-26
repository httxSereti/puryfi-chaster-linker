# Puryfi-Chaster-Linker

Puryfi plugin and Chaster extension to link [Chaster](https://chaster.app/) & [Puryfi](https://pury.fi/).
Atm, project is in development it'll evolve when i'll have time and ideas.
The code is messy, i'll clean it up when i'll have time, the goal is to increment and test features/bugs.
I'll make public this extension on Chaster extension when it'll be ready.

## Features

- ❄️ Lock & Enable Puryfi when your lock is frozen.
- 🔓 Unlock & Disable Puryfi when your lock is unfrozed.

## Requirements

- Puryfi 0.8.6.0 or higher
- Docker & Docker Compose
- Chaster Extension (+ public exposed endpoints for webhook)
- Public endpoint (can use ngrok, cloudflared, etc.)

## Run

**⚠ Fill the `.env` file first.**

```bash
git clone https://github.com/httxSereti/puryfi-chaster-linker.git
cd puryfi-chaster-linker
cp .env.example .env
docker compose up -d
```

## How to use

1. Copy .env.example as .env and fill it
2. Create a Chaster extension with a public reachable endpoints for webhook (i personally use ngrok)
```
Main page URL: http://localhost:5173/extension/main
Configuration page URL: http://localhost:5173/extension/configuration
Webhook URL: https://<your-public-domain>/api/webhooks/extensions/chaster
```
3. Run using Docker Compose
4. Open Puryfi -> Plugins -> Register new plugin -> WebSocket (default url: ws://localhost:8000)
5. Use the Chaster extension (open main page of the extension as wearer only) to generate a linking token
6. Link Chaster extension in the plugin settings (copy paste the token)
7. Enjoy!