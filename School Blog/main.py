from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import pytz
import httpx  # Use httpx for making asynchronous HTTP requests

# MongoDB setup: Create an asynchronous MongoDB client and specify the database.
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.school_blog

# Pydantic model to define the structure of a blog post received from the frontend.
class BlogPost(BaseModel):
    id: str  # Unique ID for the blog post, generated by the frontend
    title: str  # Title of the blog post
    content: str  # Content of the blog post
    author: str  # Author of the blog post

# Pydantic model for the blog post data returned from the database,
# which includes the createdAt timestamp.
class BlogPostInDB(BlogPost):
    createdAt: str  # The timestamp when the post was created

# Create an instance of FastAPI
app = FastAPI()

# Serve static files (e.g., HTML, CSS) from the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")

async def get_user_timezone() -> str:
    """Fetch the user's timezone from the free IP API."""
    try:
        # Make an asynchronous HTTP GET request to the API
        async with httpx.AsyncClient() as client:
            response = await client.get("https://freeipapi.com/api/json/")
            response.raise_for_status()  # Raise an error for bad HTTP responses
            data = response.json()  # Parse the JSON response
            # Return the first timezone from the response or default to 'Asia/Kolkata'
            return data.get("timeZones", [None])[0] or "Asia/Kolkata"  
    except Exception as e:
        # Log the error and return the default timezone in case of failure
        print(f"Error fetching timezone: {e}")
        return "Asia/Kolkata"  # Default timezone

# Create a blog post
@app.post("/posts/", response_model=BlogPostInDB)
async def create_blog_post(post: BlogPost):
    post_data = post.dict()  # Convert the Pydantic model to a dictionary

    # Get the user's timezone using the asynchronous API call
    user_timezone = await get_user_timezone()

    # Attempt to set the timezone; default to Asia/Kolkata if invalid
    try:
        local_tz = pytz.timezone(user_timezone)
    except pytz.UnknownTimeZoneError:
        raise HTTPException(
            status_code=400, detail="Invalid timezone provided"
        )  # Return an error if the timezone is unknown

    # Get the current time in the user's timezone and format it
    post_data["createdAt"] = datetime.now(local_tz).strftime("%Y-%m-%d %H:%M:%S")
    
    # Insert the blog post into the MongoDB collection
    await db.posts.insert_one(post_data)
    
    # Return the created blog post data, including the createdAt timestamp
    return post_data

# Read all blog posts
@app.get("/posts/", response_model=List[BlogPostInDB])
async def read_blog_posts():
    posts = []
    # Query the database for all posts, excluding the MongoDB's default _id field
    async for post in db.posts.find({}, {"_id": 0}):  
        posts.append(BlogPostInDB(**post))  # Append each post to the list
    return posts  # Return the list of blog posts

# Delete a blog post by its ID
@app.delete("/posts/{post_id}", response_model=dict)
async def delete_blog_post(post_id: str):
    # Attempt to delete the post from the database using the given ID
    result = await db.posts.delete_one({"id": post_id})
    if result.deleted_count == 1:
        return {"message": "Post deleted successfully"}  # Confirmation message
    else:
        # Raise a 404 error if the post was not found
        raise HTTPException(status_code=404, detail="Post not found")