import time # <--- NEW: Import time for timing the request
from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from movie_client import MovieAPIClient
import uvicorn
from typing import List, Optional

# --- 1. Pydantic Data Models (Request/Response Validation) ---

class MovieDetailsResponse(BaseModel):
    """
    Defines the structured response format for our public API (for single movie details).
    """
    movie_id: int = Field(..., description="The unique identifier of the movie.")
    title: str = Field(..., description="The official title of the movie.")
    release_date: Optional[str] = Field(None, description="The release date (YYYY-MM-DD format), or null if unavailable.")
    rating: float = Field(..., description="The average TMDB user rating.")
    summary: str = Field(..., description="A short summary or overview of the plot.")
    # NEW FIELD for demonstrating performance
    duration_ms: float = Field(..., description="Time taken to retrieve this result (Cache Hit: < 5ms, Cache Miss: > 100ms).")

class MovieSearchResult(BaseModel):
    """
    Defines the condensed structure for a single result in a search list.
    """
    movie_id: int = Field(..., description="The unique identifier of the movie.")
    title: str = Field(..., description="The official title of the movie.")
    release_date: Optional[str] = Field(None, description="The release date (YYYY-MM-DD format), or null if unavailable.")

class SearchResponse(BaseModel):
    """
    Defines the structured response for the movie search endpoint.
    """
    query: str = Field(..., description="The search term used.")
    total_results: int = Field(..., description="Total number of results found by the external API.")
    results: List[MovieSearchResult] = Field(..., description="A list of movies matching the search query.")
    # NEW FIELD for demonstrating performance
    duration_ms: float = Field(..., description="Time taken to retrieve this search result (Cache Hit: < 5ms, Cache Miss: > 100ms).")


# --- 2. FastAPI Application Setup ---

app = FastAPI(
    title="TMDB Movie Info Wrapper (with Caching)",
    description="A FastAPI wrapper to fetch validated movie details from TMDB, now featuring a search endpoint and ** automatic in-memory caching ** for client requests.",
    version="1.1.0"
)

# Initialize the external client globally
try:
    tmdb_client = MovieAPIClient()
    print("TMDB Client initialized. Caching enabled.")
except ValueError as e:
    # If the API key is missing, raise an error during startup
    print(f"FATAL: {e}")
    tmdb_client = None

# --- 3. API Endpoints ---

@app.get("/")
async def root():
    """Simple root endpoint to confirm API is running."""
    return {"message": "Movie Info Wrapper API is running. Go to /docs for interactive documentation."}

@app.get(
    "/movies/{movie_id}", 
    response_model=MovieDetailsResponse,
    summary="Get details for a specific movie",
    description="Fetches and validates core movie details by TMDB ID. **Results are cached in-memory for fast repeated access.**"
)
async def get_movie(
    movie_id: int = Path(..., description="The TMDB ID of the movie to fetch (e.g., 24428 for The Avengers).", ge=1)
):
    """
    Fetches movie details from the external client and maps them to our Pydantic model.
    """
    if not tmdb_client:
        raise HTTPException(
            status_code=503, 
            detail="External API Client failed to initialize. Check environment variables."
        )

    # NEW: Start timing the client call
    start_time = time.perf_counter()
    
    # 1. Fetch data from external client (caching handled inside movie_client)
    movie_data = tmdb_client.get_movie_details(movie_id)
    
    # NEW: Stop timing the client call
    end_time = time.perf_counter()
    duration_ms = round((end_time - start_time) * 1000, 2)

    # 2. Handle client errors/missing data
    if movie_data is None:
        raise HTTPException(status_code=404, detail=f"Movie with ID {movie_id} not found.")
    
    if isinstance(movie_data, dict) and 'error' in movie_data:
        # Handle specific error structure returned by the client (e.g., API key issue)
        raise HTTPException(
            status_code=500, 
            detail=f"External API Error: {movie_data.get('message', 'Check client logs.')}"
        )

    # 3. Validate and transform data for our public response structure
    try:
        # Map TMDB response keys to our desired output keys
        validated_response = MovieDetailsResponse(
            movie_id=movie_data.get("id"),
            title=movie_data.get("title"),
            release_date=movie_data.get("release_date"),
            rating=movie_data.get("vote_average"),
            summary=movie_data.get("overview"),
            duration_ms=duration_ms # Include timing
        )
        return validated_response
        
    except Exception as e:
        print(f"Validation/Mapping Error: {e}")
        # If mapping or validation fails (e.g., a required field is missing in TMDB response)
        raise HTTPException(
            status_code=500, 
            detail="Error processing external data structure. Internal service error."
        )

@app.get(
    "/search", 
    response_model=SearchResponse,
    summary="Search for movies by name",
    description="Searches TMDB for movies matching the query. **Results are cached in-memory for fast repeated access.**"
)
async def search_movie(
    query: str = Query(..., description="The movie title or partial title to search for.", min_length=2)
):
    """
    Searches for movies using the external client and returns a list of matching titles.
    """
    if not tmdb_client:
        raise HTTPException(
            status_code=503, 
            detail="External API Client failed to initialize. Check environment variables."
        )

    # NEW: Start timing the client call
    start_time = time.perf_counter()

    # 1. Fetch data from external client (caching handled inside movie_client)
    search_data = tmdb_client.search_movies(query)

    # NEW: Stop timing the client call
    end_time = time.perf_counter()
    duration_ms = round((end_time - start_time) * 1000, 2)

    # 2. Handle client errors/missing data
    if isinstance(search_data, dict) and 'error' in search_data:
        raise HTTPException(
            status_code=500, 
            detail=f"External API Error: {search_data.get('message', 'Check client logs.')}"
        )
    
    if not search_data or 'results' not in search_data:
         # Treat empty results as a successful search but no match
        return SearchResponse(query=query, total_results=0, results=[], duration_ms=duration_ms)

    # 3. Validate and transform results
    try:
        results_list = []
        for item in search_data.get("results", []):
            # We use the condensed MovieSearchResult model here
            results_list.append(MovieSearchResult(
                movie_id=item.get("id"),
                title=item.get("title"),
                release_date=item.get("release_date")
            ))

        validated_response = SearchResponse(
            query=query,
            total_results=search_data.get("total_results", len(results_list)),
            results=results_list,
            duration_ms=duration_ms # Include timing
        )
        return validated_response
        
    except Exception as e:
        print(f"Search Validation/Mapping Error: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Error processing external search results. Internal service error."
        )

# --- 4. Main Execution (for direct run) ---

if __name__ == "__main__":
    # To run the app directly without the CLI command:
    # uvicorn main:app --reload
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)