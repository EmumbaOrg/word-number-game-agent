# Word & Number Game Agent

This project is an interactive AI-powered game platform where users can play word and number guessing games with an LLM agent. It features a FastAPI backend and a Streamlit frontend.

---

## Note on Project Focus

This project was developed primarily as a LangGraph assignment, with an emphasis on demonstrating advanced agent orchestration, state management, and GenAI integration using LangGraph and related tools. As a result, certain backend engineering best practices—such as robust session management, advanced error handling, and production-grade API design—may not be fully implemented in this codebase.

While the core logic and agent flows are designed to showcase LangGraph capabilities, further enhancements in backend architecture, security, and scalability are recommended for production use.

---

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Running with Docker](#running-with-docker)
- [Running without Docker](#running-without-docker)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)

---

## Features

- **Word Guessing Game:** The AI asks questions to guess a word you select.
- **Number Guessing Game:** The AI tries to guess a number you think of between 1 and 50.
- **User Stats:** Track your game history and performance.
- **Modern UI:** Streamlit-based frontend for easy interaction.

---

## Project Structure

```
.
├── app/           # FastAPI backend
├── frontend/      # Streamlit frontend
├── requirements.txt
├── Dockerfile
├── Procfile
├── .env.example
└── ...
```

---

## Requirements

- **Python 3.13+**
- **Docker** (recommended for easy setup)
- **OpenAI API Key** (for LLM functionality)
- **LangSmith API Key** (for tracing, optional)

---

## Running with Docker

### 1. Install Docker

- **Windows/Mac:** Download and install Docker Desktop from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
- **Linux:** Follow instructions at [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)

Verify installation:

```sh
docker --version
```

### 2. Set Up Environment Variables

- Copy `.env.example` to `.env` and fill in your OpenAI and LangSmith keys:

```sh
cp .env.example .env
```

Edit `.env` and add your API keys.

### 3. Build and Run the Docker Container

```sh
docker build -t word-number-game-agent .
docker run -p 8000:8000 -p 8501:8501 --env-file .env word-number-game-agent
```

- **FastAPI backend:** http://localhost:8000
- **Streamlit frontend:** http://localhost:8501

### 4. Stopping the Container

Press `Ctrl+C` in the terminal, or run:

```sh
docker ps
docker stop <container_id>
```

---

## Running without Docker

### 1. Install Python and Dependencies

Make sure you have Python 3.13+ installed.

```sh
python --version
```

Install dependencies:

```sh
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Copy `.env.example` to `.env` and fill in your keys:

```sh
cp .env.example .env
```

### 3. Start the Backend (FastAPI)

```sh
fastapi dev
```

Or with Uvicorn:

```sh
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Start the Frontend (Streamlit)

```sh
cd frontend
streamlit run app.py
```

- **Backend:** http://localhost:8000
- **Frontend:** http://localhost:8501

---

## Environment Variables

Set these in your `.env` file:

```
OPENAI_API_KEY=sk-...
LANGSMITH_TRACING=True
LANGSMITH_API_KEY=lsv2_pt_...
LANGSMITH_PROJECT=your-project-name
```

---

## Troubleshooting

- **Docker build fails:** Make sure you have enough memory and disk space.
- **API key errors:** Double-check your `.env` file.
- **Port conflicts:** Ensure ports 8000 and 8501 are free.
- **Frontend not connecting to backend:** Both must be running; check URLs in frontend code.

---

## License

MIT

---

## Contact

For questions or issues, open a GitHub issue or contact the maintainer.
