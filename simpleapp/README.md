## Using Postgres as a backend database
We further make our app more advanced. Find this exercise under the simpleapp folder. In most real-life scenarios, there is a backend database interacting with the application. Instead of a Python list in the above simplified example, we employed Docker to set up a PostgreSQL container, connecting it to our FastAPI application. The following command initiated the PostgreSQL container:

```
docker run --name mypostgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres
```
#### SQLAlchemy Model 
The SQLAlchemy Model is a Python class that defines the structrue of the data we would like to interact with the application. SQLAlchemy models often serve as a Python representation of database tables, and you can use SQLAlchemy to create, modify, and query those tables. SQLAlchemy models are a tool to interact with database tables in a more Pythonic and object-oriented way. When you define an SQLAlchemy model, you're essentially specifying how the data in that model should be stored and retrieved from a database table. In our FastAPI application, we established a model for the items table using Python's object-oriented programming principles. This model, located in the models.py file, was defined with attributes like id, name, and description.

#### Connecting Database to FastAPI
We integrated the database with our FastAPI application, ensuring seamless interaction. The database connection settings and sessions were established in the ```simpleapp/app/database.py``` file. Our FastAPI application then utilized these settings to fetch all items stored in the backend database. To populate the database, we introduced a ```migrate_data_to_database()``` function. This function read data from a Python list and inserted it into the PostgreSQL database. This crucial step facilitated the availability of item data in our application.

#### Providing Item Details
Lastly, we created hyperlinks for each item, allowing users to access more detailed information about individual items. This user-friendly interface enhancement enhances the usability and functionality of our FastAPI application.

In summary, this FastAPI exercise demonstrates the integration of a PostgreSQL database into a FastAPI application, showcasing how to create a database model, populate it with data, and connect it to your API. The implementation includes a user-friendly interface with hyperlinks to access additional item details, making it a practical foundation for more complex web applications.