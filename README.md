# Puryfi-Chaster-Linker

Puryfi plugin to link [Chaster](https://chaster.app/) & [Puryfi](https://pury.fi/).
atm, project is in development it'll evolve when i'll have time and ideas

## Features
- Add duration to a Chaster Lock when user views a censored object

## Requirements

- Puryfi 0.8.6.0 or higher
- Docker or UV
- Chaster Extension for access token

## Run

### using Docker

```bash
cd server
docker build -t puryfi-chaster-linker .
docker run -p 8090:8090 puryfi-chaster-linker
```

### using UV

```bash
cd server
uv run uvicorn main:app --host [IP_ADDRESS] --port 8090
```

## How to use

1. Get your Chaster API token ([Chaster Applications](https://chaster.app/developers/applications) -> Tokens)
2. Get your Chaster Lock ID (Edit your lock -> Id is after /locks in URL)
3. Run the plugin
4. Open Puryfi -> Plugins -> Register new plugin -> WebSocket (default url: ws://localhost:8090)
5. Set the configuration in the plugin