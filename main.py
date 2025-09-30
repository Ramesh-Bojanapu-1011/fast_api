from typing import Optional, List
import logging
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from googlesearch import search
from pydantic import BaseModel, Field, field_validator
from youtube_search import YoutubeSearch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Search API Service",
    description="A FastAPI service for Google and YouTube search functionality",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {"message": "Hello World", "status": "active", "service": "Search API"}


@app.get("/hello/{name}", tags=["Health"])
async def say_hello(name: str):
    """Personalized greeting endpoint"""
    if not name or name.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name cannot be empty"
        )
    return {"message": f"Hello {name.strip()}", "status": "success"}


class ActorSearchRequest(BaseModel):
    """Request model for actor/craft search"""
    name: str = Field(..., min_length=1, max_length=100, description="Actor/person name")
    craft: str = Field(..., min_length=1, max_length=50, description="Craft/profession (e.g., actor, director)")
    
    @field_validator('name', 'craft')
    @classmethod
    def validate_not_empty(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Field cannot be empty or just whitespace')
        return v.strip()


class SearchResponse(BaseModel):
    """Response model for search results"""
    status: bool
    data: List[str]
    message: Optional[str] = None


@app.post("/find/person/wiki_url", response_model=SearchResponse, tags=["Search"])
async def find_wiki_url(request: ActorSearchRequest):
    """
    Find Wikipedia URLs for Telugu actors/crafts.
    
    This endpoint searches Google for Wikipedia URLs related to Telugu actors or crafts.
    
    Args:
        request: ActorSearchRequest containing name and craft
        
    Returns:
        SearchResponse with search results
    """
    try:
        logger.info(f"Searching for: {request.name} - {request.craft}")
        
        query = f"Get Wiki URL for Telugu {request.craft} {request.name}"
        result = search_google(query)
        
        if not result:
            return SearchResponse(
                status=False,
                data=[],
                message="No search results found"
            )
        
        return SearchResponse(
            status=True,
            data=result[:3],
            message=f"Found {len(result[:3])} results"
        )
        
    except Exception as e:
        logger.error(f"Error in find_wiki_url: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while searching. Please try again later."
        )


def search_google(query: str) -> List[str]:
    """
    Searches Google for the given query and returns the top 4 results.

    Args:
        query (str): The search query to be made.

    Returns:
        List[str]: A list of the top 4 search results.
    """
    try:
        logger.info(f"Performing Google search for: {query}")
        search_results = search(query, num_results=4)
        results = list(search_results)
        logger.info(f"Found {len(results)} search results")
        return results
    except Exception as e:
        logger.error(f"Error in Google search: {str(e)}")
        return []


class SearchQuery(BaseModel):
    """
    Pydantic model for YouTube search queries.
    
    Attributes:
        search_text: The text to search for on YouTube
        num_results: Number of results to return (1-50)
    """
    search_text: str = Field(..., min_length=1, max_length=200, description="Text to search for")
    num_results: Optional[int] = Field(default=3, ge=1, le=50, description="Number of results (1-50)")
    
    @field_validator('search_text')
    @classmethod
    def validate_search_text(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Search text cannot be empty')
        return v.strip()


class YouTubeSearchResponse(BaseModel):
    """Response model for YouTube search"""
    status: bool
    data: dict
    message: Optional[str] = None


@app.post("/find/youtube/videos", response_model=YouTubeSearchResponse, tags=["Search"])
async def youtube_search(search_query: SearchQuery):
    """
    Search for YouTube videos based on the provided query.
    
    This endpoint searches YouTube for videos matching the search text
    and returns the specified number of results.
    
    Args:
        search_query: SearchQuery containing search text and number of results
        
    Returns:
        YouTubeSearchResponse with search results
    """
    try:
        logger.info(f"YouTube search for: {search_query.search_text}")
        
        results = YoutubeSearch(
            search_query.search_text, 
            max_results=search_query.num_results
        ).to_dict()
        
        if not results:
            return YouTubeSearchResponse(
                status=False,
                data={},
                message="No YouTube videos found for the search query"
            )
        
        return YouTubeSearchResponse(
            status=True,
            data={"videos": results, "count": len(results)},
            message=f"Found {len(results)} YouTube videos"
        )
        
    except Exception as e:
        logger.error(f"Error in YouTube search: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while searching YouTube. Please try again later."
        )


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "service": "Search API",
        "version": "1.0.0",
        "endpoints": {
            "google_search": "/find/person/wiki_url",
            "youtube_search": "/find/youtube/videos"
        }
    }
