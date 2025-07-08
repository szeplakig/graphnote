# GraphNote

GraphNote is a simple note-taking application that demonstrates a small FastAPI backend with a React (Vite) + Tailwind frontend. Notes are stored in a SQLite database and can reference each other using UUIDs.

## Features

- Create, update and delete notes
- Notes are stored as markdown content
- Link notes together via UUID references
- Query incoming and outgoing links for a note

## Requirements

- Python 3.10+
- Node 18+

## Running the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Running the frontend

```bash
cd frontend
npm install
npm run dev
```

This repository contains only a minimal skeleton meant to be extended.
