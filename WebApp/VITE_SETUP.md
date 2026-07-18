# Vite Migration Setup Guide

Instructions for setting up the Vite dev environment on any machine with this repo.

## Prerequisites

- Python 3.9+ (for the backend)
- Node.js 18+ (for the frontend dev server)
- Git (to clone/pull the repo)

## 1. Clone & Backend Setup

```bash
git clone https://github.com/marbleperfume/juice-yaml-library.git
cd juice-yaml-library

# Create Python venv (use system Python or UE5's bundled interpreter)
python -m venv WebApp/.venv

# Install backend deps
WebApp/.venv/Scripts/python.exe -m pip install -r WebApp/backend/requirements.txt
```

## 2. Frontend Setup (Vite)

```bash
cd WebApp/frontend
npm install
```

This installs React, ReactDOM, Vite, and the React plugin into a local `node_modules/` folder.

## 3. Running in Dev Mode

**Terminal 1 — Backend** (from repo root):
```bash
WebApp\.venv\Scripts\python.exe -m uvicorn WebApp.backend.main:app --port 8400
```

**Terminal 2 — Frontend** (from `WebApp/frontend/`):
```bash
npm run dev
```

**Open** → http://localhost:5173

The Vite dev server proxies all `/api/*` requests to FastAPI on `:8400. Changes to `.jsx` files hot-reload instantly in the browser.

## 4. Production Build

```bash
cd WebApp/frontend
npm run build
```

This outputs bundled files to `WebApp/frontend/dist/`. FastAPI auto-detects and serves `dist/` over `public/` when it exists.

To revert to no-build mode, just delete the `dist/` folder.

## 5. Fallback (No Node Required)

If Node isn't available, the app still works without Vite:

```bash
WebApp\.venv\Scripts\python.exe -m uvicorn WebApp.backend.main:app --port 8400
```

Open http://127.0.0.1:8400 — serves the raw ESM files from `public/` directly.

---

## Files to Create in `WebApp/frontend/`

### `package.json`

```json
{
  "name": "juice-design-hub",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite --port 5173",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "vite": "^5.4.0",
    "@vitejs/plugin-react": "^4.3.0"
  }
}
```

### `vite.config.js`

```js
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  root: ".",
  build: {
    outDir: "dist",
    emptyOutDir: true,
  },
  server: {
    port: 5173,
    proxy: {
      "/api": "http://127.0.0.1:8400",
    },
  },
});
```

### `index.html` (Vite entry — goes in `WebApp/frontend/`, NOT inside `public/`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Juice Design Hub</title>
  <link rel="stylesheet" href="/src/styles.css" />
</head>
<body>
  <div id="root"></div>
  <script type="module" src="/src/main.jsx"></script>
</body>
</html>
```

---

## `.gitignore` Additions (add to repo root)

```
# Node / Vite
node_modules/
WebApp/frontend/dist/

# Python
__pycache__/
*.pyc
WebApp/.venv/
```

---

## Planned File Split (components.js → src/)

Once the scaffold is working, split the 27 KB `components.js` monolith:

```
WebApp/frontend/src/
├── main.jsx                    ← entry (createRoot, render <App/>)
├── api.js                      ← fetch helper (get/put/post)
├── styles.css                  ← moved from public/
├── App.jsx                     ← tabs/routing shell
└── components/
    ├── FileBrowser.jsx         ← sidebar file tree
    ├── AbilityFileEditor.jsx   ← schema-driven ability form
    ├── RawEditor.jsx           ← raw YAML editor
    ├── ValidationPanel.jsx     ← validator results display
    ├── GraphView.jsx           ← relationship graph
    └── TrackerPanel.jsx        ← finalization tracker
```

Target: ~3-8 KB per component file. LLMs only need to read the file relevant to the question.

---

## Architecture Recap

```
┌─────────────────────┐         ┌─────────────────────┐
│  Vite Dev Server    │         │  FastAPI (uvicorn)   │
│  localhost:5173     │────────▶│  localhost:8400      │
│                     │  proxy  │                      │
│  • Serves React UI  │ /api/*  │  • Serves JSON API   │
│  • Hot reloads JSX  │         │  • Reads/writes YAML │
│  • Source maps      │         │  • Runs validators   │
└─────────────────────┘         └─────────────────────┘
        ▲
        │
    Browser opens localhost:5173
```

Both servers bind to localhost only — no network exposure, no AWS service dependencies.
