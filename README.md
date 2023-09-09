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
In the above function, the item_id parameter is a mandatory input into the url path. Depending on that input, a specific logic could be implemented inside the function. For example, when the ```http://127.0.0.1:8000/items/42``` path is requested, the value 42 gets printed out. 
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

@app.post("/items/{item_id}", response_model=ItemResponse)
def create_item(item: Item, item_id: int):
    return {"item_id": item_id, "item": item}
```
In the above application, a request body is expected from the user; this has a json format with two fields, name and description of type str. We've defined a class Item, which inherits from the BaseModel. We've also used the BaseModel class to specify the structure of the returned response by the API. This will be a json with two fields, item_id of type int, and item of type Item. 

## Multiple Routes
In most cases, the application might contain multiple pages, each corresponding to a route function. Let's consider the following example application with a **home page**, a **contact page**, and an **about page**. 

```
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/about", response_class=HTMLResponse)
async def read_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/contact", response_class=HTMLResponse)
async def read_contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})
```
Each route function returns an HTTP file provided under the ../templates directory. Here's the steps to the above code: 
- Created an object of the *Jinja2Templates* class and provided the path to the templates directory. 
- Created an app and provided *HTMLResponse* as the response class, which is a way to tell the route function that its rendering an HTML file. 
- Created an asynchronous function to define the logic for each route. Asynchronous functions in Python allow you to perform non-blocking operations, such as waiting for external resources like databases or APIs, without blocking the execution of the entire program. Using asynchronous functions can improve the scalability and responsiveness of your application. When you mark a function as async, it becomes capable of running concurrently with other tasks, which is particularly useful for I/O-bound operations like waiting for a database query or an HTTP request.
- Called the TemplateResponse method of the templates object and provided the name of the html file, as well as the context being returned, which is an object of the *Request* class in this case. This object will be automatically injected when the route is called. The context dictionary is a set of key-value pairs that we can provide to the template. These key-value pairs act as variables that the template can access and use while rendering the template. In this case, when we're passing an object of the Request class to the TemplateResponse method, we're making the details of the HTTP request available to be used in this template. Imagine a scenario where we'd like to display the user's IP address in the screen. We can add the following to our HTML body: ```<p>Your IP address: {{ request.client.host }}</p>```
## Advancing the Routes
In many real-life scenarios, we would like to display a list of items on the home page. In the below exercise we will display on the page page all items of a Python list. Within the home page template, we loop through the items and create a separate hyperlink for each item. This link will direct the user to a separate page corresponding to more details of that item. We need to make sure the items are made available to the home page template file through the method explained above. Here's how to loop through the items in HTML: 
```
<ul>
    {% for item in items %}
        <li>
            <a href="/item/{{item.id}}">{{item.name}}</a><br>
                {{item.description}}
        </li>
    {% endfor %}
</ul> 
```
Note that the item details, such as the id and the name are encapsulated within the link above. This mean that when the user clicks on the link, the the item_id parameter (see the codes below) is automatically populated in path. We would then have to define the route logic for each item, so that when the /item/item_id pattern is requested by the client, details of that item gets desplayed. Here's the final code: 
```
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="../templates")

# Define a list of items (for demonstration purposes)
items = [
    {"id": 1, "name": "Item 1", "description": "Description of Item 1"},
    {"id": 2, "name": "Item 2", "description": "Description of Item 2"},
    {"id": 3, "name": "Item 3", "description": "Description of Item 3"},
]

# Home page containing all items
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "items": items})

# Route logic for each item
@app.get("/item/{item_id}", response_class=HTMLResponse)
async def read_detail(request: Request, item_id: int):

    item = next((item for item in items if item["id"] == item_id), None)
    if item:
        return templates.TemplateResponse("index_details.html", {"request": request, "item": item})
    print(f"Item {item_id} not found!")
```
See the template details under the ```../templates``` directory to see how the item components are accessed in the ```index.html``` and ```index_details.html``` files. 

## Using Postgres as a backend database
In most real-life scenarios, there is a backend database interacting with the application. Instead of a Python list in the above simplified example, we employed Docker to set up a PostgreSQL container, connecting it to our FastAPI application. The following command initiated the PostgreSQL container:

```
docker run --name mypostgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres
```
### SQLAlchemy Model 
The SQLAlchemy Model is a Python class that defines the structrue of the data we would like to interact with the application. SQLAlchemy models often serve as a Python representation of database tables, and you can use SQLAlchemy to create, modify, and query those tables. SQLAlchemy models are a tool to interact with database tables in a more Pythonic and object-oriented way. When you define an SQLAlchemy model, you're essentially specifying how the data in that model should be stored and retrieved from a database table. In our FastAPI application, we established a model for the items table using Python's object-oriented programming principles. This model, located in the models.py file, was defined with attributes like id, name, and description.

### Connecting Database to FastAPI
We integrated the database with our FastAPI application, ensuring seamless interaction. The database connection settings and sessions were established in the ```simpleapp/app/database.py``` file. Our FastAPI application then utilized these settings to fetch all items stored in the backend database. To populate the database, we introduced a ```migrate_data_to_database()``` function. This function read data from a Python list and inserted it into the PostgreSQL database. This crucial step facilitated the availability of item data in our application.

### Providing Item Details
Lastly, we created hyperlinks for each item, allowing users to access more detailed information about individual items. This user-friendly interface enhancement enhances the usability and functionality of our FastAPI application.

In summary, this FastAPI exercise demonstrates the integration of a PostgreSQL database into a FastAPI application, showcasing how to create a database model, populate it with data, and connect it to your API. The implementation includes a user-friendly interface with hyperlinks to access additional item details, making it a practical foundation for more complex web applications.

