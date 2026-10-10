# aroku-frontend

React + Vite frontend for the aroku support agent (Home + Chat).

    npm install
    npm run dev        # http://localhost:5173

Start your FastAPI backend on port 8000 first:

    uvicorn backend.app.main:app --reload --port 8000

If your backend uses another port, edit `target` in `vite.config.js`.
