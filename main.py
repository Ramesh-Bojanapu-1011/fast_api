from typing import Optional

from fastapi import FastAPI, Request  
from googlesearch import search
from pydantic import BaseModel
from youtube_search import YoutubeSearch

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


"""
This function is used to search google for a given query and return the top 3 results.

Args:
    query (str): The search query to be made.

Returns:
    list: A list of the top 3 search results.
"""


@app.post("/find/person/wiki_url")
async def find_wiki_url(request: Request):
    actor_info = await request.json()
    name = actor_info.get("name")
    craft = actor_info.get("craft")
    # Process the received item (e.g., save it to a database)
    query = f"Get Wiki URL for Telugu {craft} {name}"
    result = search_google(query)
    response = {"status": True, "data": result[:3]}
    return response


def search_google(query: str):
    """
    Searches Google for the given query and returns the top 4 results.

    Args:
        query (str): The search query to be made.

    Returns:
        list: A list of the top 4 search results.
    """
    try:
        search_results = search(query, num_results=4)
        results = list(search_results)
        return results
    except Exception:
        return []


# This is a Pydantic model class named `SearchQuery` that inherits from the `BaseModel` class.
# The model has two attributes:
# 1. `search_text`: A required string attribute that stores the text to be searched.
# 2. `num_results`: An optional integer attribute that represents the number of search results to return.
# The default value of `num_results` is set to 3 if not provided.
class SearchQuery(BaseModel):
    search_text: str
    num_results: Optional[int] = 3


@app.post("/find/youtube/videos")
async def youtube_search(search_query: SearchQuery):
    query = search_query.search_text
    num_results = search_query.num_results
    results = YoutubeSearch(query, max_results=num_results)
    return results
