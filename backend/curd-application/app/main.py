from fastapi import FastAPI
from routes.userroutes import user_router  # Import the user_router from the userroutes module.

app = FastAPI()       #application instance is created using FastAPI class.
app.include_router(user_router)  # Include the user_router in the main application.

@app.get("/")      #decorator is used to define the route for the root endpoint.
def read_root():    #function to handle GET requests to the root endpoint.
    return {"message": "Welcome to the FastAPI application!"}   #returns a JSON response with a welcome message.

