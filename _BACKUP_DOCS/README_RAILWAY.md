Railway deployment quickstart

1) Install Railway CLI (option A: npm):

```
npm install -g railway
```

Or use the installer (macOS/Linux):

```
curl -sL https://railway.app/install.sh | sh
```

2) Login and initialize

```
railway login
railway init
```

3) Deploy (local Docker build) or connect GitHub repo

```
railway up
```

Or connect the repository via the Railway web UI and enable automatic deploys from your GitHub branch.

Notes:
- This repo includes a Dockerfile (for Docker-based deploys) and a Procfile (for direct run).
- If you use `railway init` it may create `railway.toml`; use `railway.template.toml` as a reference.
