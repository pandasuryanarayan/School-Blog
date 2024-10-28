# School-Blog

A simple school blog post website created using **MongoDB**, **FastAPI**, and **Pydantic**.

## Getting Started

To get started with this project, follow these steps:

1. **Download and Extract** the ZIP file of this project provided.
2. **Open** the project folder in your preferred editor (e.g., VS Code) or in a terminal.

## Prerequisites

Ensure you have the following installed on your system:

- **Python** (version 3.8 or later)
- **MongoDB** (running on localhost)

## Installation

1. **Activate the virtual environment in the root of the folder**:
    ```bash
    source myenv/bin/activate
    ```
2. **Run the application** with Uvicorn:
    ```bash
    uvicorn main:app --reload
    ```

## Accessing the Website

Once the server is running, navigate to:
- [http://127.0.0.1:8000/static/index.html](http://127.0.0.1:8000/static/index.html)

## Demo

Here are some screenshots of the application in action:

![Create Post](Demo-Videos/Create_Post.webm)
*Creating a new blog post*

![Delete Post](Demo-Videos/Delete_Post.webm)
*Deleting a blog post*

## Additional Information

The application uses **FastAPI** to create a RESTful API, **Pydantic** for data validation, and **MongoDB** as the backend database. FastAPI serves the HTML file at `/static/index.html`.

---

**Note**: Ensure that MongoDB is running on `localhost` (default port 27017) for successful database connections.
