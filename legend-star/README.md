# Legend Star

Legend Star is a Discord bot monitoring and analytics platform.

## Project structure

- `/backend`: FastAPI backend
  - `main.py` - API implementation
  - `requirements.txt` - dependencies
  - `.env.example` - environment example

- `/frontend`: React + Vite + Tailwind frontend
  - `src` - React app
  - `public` - static assets
  - `package.json` - dependencies

- `discord_bot.py`: sample integration script for Discord

## Backend setup

1. Create `.env` in `/backend`:

```
MONGO_URL=mongodb+srv://<user>:<pass>@cluster0.xxxx.mongodb.net/legend_star?retryWrites=true&w=majority
API_KEY=your-api-key
PORT=8000
```

2. Install Python dependencies:

```bash
cd legend-star/backend
python -m pip install -r requirements.txt
```

3. Run API:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT --reload
```

## Frontend setup

1. Set env vars in `legend-star/frontend/.env`:

```bash
VITE_BACKEND_URL=http://localhost:8000
VITE_API_KEY=your-api-key
```

2. Install and run:

```bash
cd legend-star/frontend
npm install
npm run dev
```

3. Open web app at `http://localhost:5173`.

## Discord bot integration

1. Create `.env` in root or same folder as `discord_bot.py`:

```
DISCORD_TOKEN=your-bot-token
API_KEY=your-api-key
BACKEND_URL=http://localhost:8000
```

2. Run bot:

```bash
python discord_bot.py
```

## API endpoints

- `POST /log` - secure to ingest log entries (`x-api-key` header required)
- `GET /logs` - list latest logs
- `GET /analytics` - summary metrics
- `GET /errors` - error-only logs
- `GET /users` - user activity breakdown
- `GET /ws` - WebSocket live log feed
- `POST /control` - queue control actions (`send_message`, `get_status`)
- `GET /control` - poll pending control actions (bot polling)
- `POST /control/ack` - acknowledge processed action

## Deployment

### Backend (Railway)

- Set `MONGO_URL`, `API_KEY`, `PORT` in Railway env.
- Deploy from repo and set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel)

- Connect to repository and set env `VITE_BACKEND_URL`, `VITE_API_KEY`.
- Build command: `npm run build`; publish directory: `dist`.

## Extra features

- human time formatting in front-end
- search + filters
- auto refresh live logs
- color-coded display and JSON pretty view
- pagination support via `limit` + `skip` query
