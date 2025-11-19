# 🎬 TMDB Movie Info Wrapper

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**A high-performance, validated API wrapper for The Movie Database (TMDB)**

[Features](#-features) • [Installation](#-installation-and-setup) • [Usage](#-api-usage) • [Documentation](#-api-endpoints) • [Testing](#-testing-and-caching-verification)

</div>

---

## 📋 Overview

This project is a high-performance, validated API wrapper built with Python and FastAPI. It integrates with The Movie Database (TMDB) API to fetch structured movie information, providing a clean, consistent interface while utilizing in-memory caching to boost response speed and reduce external API load.

---

## ✨ Features

1. Robust Structure: Built on FastAPI and Pydantic for automatic data validation, documentation, and serialization.

2. External API Integration: Uses the requests library to securely communicate with the TMDB API.

3. In-Memory Caching: Implements functools.lru_cache within the external client layer to cache results for common movie lookups and search queries, ensuring near-instant responses for repeated requests.

4. Performance Demonstration: Explicitly measures and reports API call latency in the response body to demonstrate the speed difference between a cache miss (external API call) and a cache hit (in-memory retrieval).

5. Two Core Endpoints:
```bash
/movies/{movie_id}: Retrieves detailed information for a single movie ID.

/search: Searches for movies by title query.
```

---

## ⚙️ Prerequisites

Before you begin, ensure you have the following:

- 🐍 **Python 3.8+** installed on your system
- 🔑 **TMDB API Key**: Get your free API key from [The Movie Database](https://www.themoviedb.org/settings/api)

---

## 🚀 Installation and Setup

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-link>
cd tmdb-movie-wrapper
```

### 2️⃣ Create Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies.

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
\venv\Scripts\activate  # On Windows
```

### 3️⃣ Install Dependencies

Install all required Python packages:

```bash
pip install fastapi uvicorn requests pydantic python-dotenv
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the root directory:

```bash
# .env file content
TMDB_API_KEY="YOUR_API_KEY_HERE"
```

> ⚠️ **Important**: Never commit your `.env` file to version control. Add it to your `.gitignore`.

---

## ▶️ Running the Application

Start the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload
```

The application will now be running at:

- 🌐 **API Server**: http://127.0.0.1:8000
- 📖 **Interactive Docs**: http://127.0.0.1:8000/docs

---

## 📖 API Endpoints

### 🎥 Get Movie Details (Cached)

Retrieves detailed information for a movie using its unique TMDB ID.

**Endpoint**: `GET /movies/{movie_id}`

**Example Request**:
```bash
curl http://127.0.0.1:8000/movies/24428
```

**Response Model** (`MovieDetailsResponse`):
```json
{
  "movie_id": 24428,
  "title": "The Avengers",
  "release_date": "2012-04-25",
  "rating": 7.7,
  "summary": "Nick Fury is the director of S.H.I.E.L.D....",
  "duration_ms": 350.15
}
```

---

### 🔍 Search Movies by Name (Cached)

Searches the TMDB catalog for movies matching the given query.

**Endpoint**: `GET /search`

**Query Parameters**:
- `query` (string, required): Search term

**Example Request**:
```bash
curl http://127.0.0.1:8000/search?query=Matrix
```

**Response Model** (`SearchResponse`):
```json
{
  "query": "Matrix",
  "total_results": 7,
  "results": [
    {
      "movie_id": 603,
      "title": "The Matrix",
      "release_date": "1999-03-30",
      "rating": 8.2
    }
  ],
  "duration_ms": 1.28
}
```

---

## 🧪 Testing and Caching Verification

The easiest way to verify caching is by observing the `duration_ms` field in the response JSON.

### Performance Comparison

| Test Scenario | Action | Expected `duration_ms` | Cache Status |
|--------------|--------|----------------------|--------------|
| 🔴 **Cache Miss** | First request to `/movies/24428` | 100ms - 500ms | External API Call |
| 🟢 **Cache Hit** | Second request to `/movies/24428` | 0.5ms - 5ms | In-Memory Cache |
| 🔴 **Cache Miss** | First request to `/search?query=Dune` | 100ms - 500ms | External API Call |
| 🟢 **Cache Hit** | Second request to `/search?query=Dune` | 0.5ms - 5ms | In-Memory Cache |

### Visual Performance Demonstration

```
First Request (Cache Miss):  ████████████████████ 350ms
Second Request (Cache Hit):  █ 2ms

Speed Improvement: ~175x faster! 🚀
```

---

## 📁 Project Structure

```
tmdb-movie-wrapper/
├── main.py              # FastAPI application entry point
├── movie_client.py      # Core Logic and TMDB API Client
├── .env                 # Environment variables (not in git)
├── .gitignore           # Git ignore file
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── venv/                # Virtual environment (not in git)
```

---

## 🛠️ Tech Stack

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast web framework
- **[Pydantic](https://docs.pydantic.dev/)** - Data validation using Python type hints
- **[Uvicorn](https://www.uvicorn.org/)** - Lightning-fast ASGI server
- **[Requests](https://requests.readthedocs.io/)** - HTTP library for Python
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** - Environment variable management

---

## 📝 Requirements

Create a `requirements.txt` file:

```txt
annotated-doc==0.0.4
annotated-types==0.7.0
anyio==4.11.0
certifi==2025.11.12
charset-normalizer==3.4.4
click==8.3.1
colorama==0.4.6
fastapi==0.121.3
h11==0.16.0
idna==3.11
pydantic==2.12.4
pydantic_core==2.41.5
python-dotenv==1.2.1
requests==2.32.5
sniffio==1.3.1
starlette==0.50.0
typing-inspection==0.4.2
typing_extensions==4.15.0
urllib3==2.5.0
uvicorn==0.38.0
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [The Movie Database (TMDB)](https://www.themoviedb.org/) for providing the API
- [FastAPI](https://fastapi.tiangolo.com/) for the amazing web framework

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ and Python

</div>