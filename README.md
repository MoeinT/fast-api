# Creating a Fast API application
 FastAPI applications are created by importing the necessary modules and using Python functions and decorators to define routes and their corresponding functions. A route is a URL pattern that maps to a Python function, which handles the logic for that route. Here's an example: 

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
```
## How to access the service
 When you access the root URL ("/"), the read_root function will be executed, and it will return a JSON response with the message "Hello, FastAPI!". In order to access the URL, run the ```uvicorn main:app``` command and go to ```http://127.0.0.1:8000``` in the browser. Here's a quick note on the port number: The ```uvicorn``` server uses 8000 as the default port. Port numbers are used to differentiate services running on a single machine or IP address. Using port numbers, there could be different services running on a single machine, each accessible through its own port. If you'd like the application to be accessible through a different port, you can specify it while running the uvicorn command: ```uvicorn main:app --port 8888```. 
## Handling Path Parameters
Path parameters allow you to have dynamic parts in your path URL. They're denoted by {}. Here's an example: 

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```
In the above function, the item_id parameter will be input by the user. For example, when the ```http://127.0.0.1:8000/items/42``` path is requested, the value 42 gets printed out. 
## Query Parameters
Query parameters are key-value pairs added to the end of the URL after the **?** symbol. They are optional inputs by the user for filtering, sorting and passing additional information to the url. Here's an example: 

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/")
def read_item(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```
For example, we can use the ```http://127.0.0.1:8888/items/?skip=2&limit=222``` url to pass the skip and limit parameters to the request. 

## Request Bodies & Response Models
Many APIs require the client to send a request body. FastAPI makes it easy to validate and handle request data using the Pydantic model. Fast API also allows you to use response models, which define the structure of the response returned by the API route; this not only allows with the documentation, but also ensures the returned data matches the expected format. Here's an example of a POST application, that requies a response body, and an additional parameter to define the response model: 

```
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None

class ItemResponse(BaseModel):
    item_id: int
    item: Item

@app.post("/items/", response_model=ItemResponse)
def create_item(item: Item):
    return {"item_id": 1, "item": item}
```
In the above application, a request body is expected from the user; this has a json format with two fields, name and description of type str. We've defined a class Item, which inherits from the BaseModel. We've also used the BaseModel class to specify the structure of the returned response by the API. This will be a json with two fields, item_id of type int, and item of type Item. 