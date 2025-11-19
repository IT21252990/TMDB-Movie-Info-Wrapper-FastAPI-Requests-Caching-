🎬 TMDB Movie Info Wrapper (FastAPI, Requests, Caching)

This project is a high-performance, validated API wrapper built with Python and FastAPI. It integrates with The Movie Database (TMDB) API to fetch structured movie information, providing a clean, consistent interface while utilizing in-memory caching to boost response speed and reduce external API load.

✨ Features

Robust Structure: Built on FastAPI and Pydantic for automatic data validation, documentation, and serialization.

External API Integration: Uses the requests library to securely communicate with the TMDB API.

In-Memory Caching: Implements functools.lru_cache within the external client layer to cache results for common movie lookups and search queries, ensuring near-instant responses for repeated requests.

Performance Demonstration: Explicitly measures and reports API call latency in the response body to demonstrate the speed difference between a cache miss (external API call) and a cache hit (in-memory retrieval).

Two Core Endpoints:

/movies/{movie_id}: Retrieves detailed information for a single movie ID.

/search: Searches for movies by title query.

⚙️ Prerequisites

Before you begin, ensure you have the following installed:

Python 3.8+

TMDB API Key: Obtain a free API key (v3 or v4) from The Movie Database website.

🚀 Installation and Setup

1. Clone the repository

git clone <your-repo-link>
cd tmdb-movie-wrapper


2. Create and Activate Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies.

python3 -m venv venv
source venv/bin/activate  # On Linux/macOS
# .\venv\Scripts\activate  # On Windows


3. Install Dependencies

Install all required Python packages:

pip install fastapi uvicorn requests pydantic python-dotenv


4. Configuration (.env file)

Create a file named .env in the root directory of the project and add your TMDB API key.

# .env file content
TMDB_API_KEY="YOUR_API_KEY_HERE" 


▶️ Running the Application

Start the FastAPI server using Uvicorn. The --reload flag is helpful for development.

uvicorn main:app --reload


The application will now be running at http://127.0.0.1:8000.

📖 API Usage and Endpoints

Access the interactive documentation (Swagger UI) at: http://127.0.0.1:8000/docs

1. Get Movie Details (Cached)

Retrieves detailed information for a movie using its unique TMDB ID.

Endpoint: GET /movies/{movie_id}

Example (The Avengers, ID 24428):

[http://127.0.0.1:8000/movies/24428](http://127.0.0.1:8000/movies/24428)


Response Model (MovieDetailsResponse):
The response now includes the duration_ms field to demonstrate caching.

{
  "movie_id": 24428,
  "title": "The Avengers",
  "release_date": "2012-04-25",
  "rating": 7.7,
  "summary": "Nick Fury is the director of S.H.I.E.L.D....",
  "duration_ms": 350.15  // Cache Miss (first time)
}


2. Search Movies by Name (Cached)

Searches the TMDB catalog for movies matching the given query.

Endpoint: GET /search

Query Parameter: query (string, required)

Example (Searching for 'Matrix'):

[http://127.0.0.1:8000/search?query=Matrix](http://127.0.0.1:8000/search?query=Matrix)


Response Model (SearchResponse):

{
  "query": "Matrix",
  "total_results": 7,
  "results": [
    // ... results list
  ],
  "duration_ms": 1.28 // Cache Hit (subsequent request)
}


🧪 Testing and Caching Verification

The easiest way to verify caching is by observing the duration_ms field in the response JSON or the network tab of your browser's developer tools.

Test Scenario

Action

Expected duration_ms Value

Cache Status

Cache Miss

First request to /movies/24428

High (e.g., 100ms - 500ms)

External API Call

Cache Hit

Second request to /movies/24428

Very Low (e.g., 0.5ms - 5ms)

In-Memory Cache

Cache Miss (Search)

First request to /search?query=Dune

High (e.g., 100ms - 500ms)

External API Call

Cache Hit (Search)

Second request to /search?query=Dune

Very Low (e.g., 0.5ms - 5ms)

In-Memory Cache

The significant drop in milliseconds clearly demonstrates the speed benefit of the lru_cache functionality.