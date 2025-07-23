# 1. Import the FastAPI class
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
# Import our new database function
from database import create_db_and_tables, insert_result, get_all_results

# 2. Create an "instance" of the FastAPI class
# This 'app' object will be the main point of interaction for our API
app = FastAPI()

# --- THIS IS OUR SHOEBOX ---
# This function will run once when the application starts.
@app.on_event("startup")
def on_startup():
    print("Application is starting up...")
    create_db_and_tables()

# --- THIS IS OUR FORM TEMPLATE ---
# We're saying that every "TestResult" must have these fields.
class TestResult(BaseModel):
    test_name: str        # A box for text
    status: str           # A box for text (like "pass" or "fail")
    duration_ms: int      # A box for a whole number
    test_suite: str       # A box for text (like "smoke_tests")
    
    # This box is optional. A test that passes won't have an error message.
    error_message: Optional[str] = None

# 3. Define a "path operation decorator"
# @app.get("/") tells FastAPI that the function below is in charge of
# handling requests that go to the URL "/" using a GET operation.
@app.get("/")
def read_root():
    # 4. Return a dictionary, which FastAPI will automatically
    # convert to a JSON response.
    return {"message": "Hello QA dashboard"}

# 2. Add the new GET endpoint. It's common for the GET (all) and POST
# endpoints for a resource to share the same URL.
@app.get("/api/results")
def read_results():
    # This function is simple: just call our database function...
    results = get_all_results()
    # ...and return the data. FastAPI automatically converts the
    # list of dictionaries into a JSON array.
    return results

# --- THIS IS OUR MAILBOX ---
# @app.post("/api/results") means:
# "Create a mailbox at the address '/api/results' that accepts POST packages."
@app.post("/api/results", status_code=201)
def create_test_result(result: TestResult):
    # 'result: TestResult' means:
    # "When a package arrives, make sure it looks like our TestResult form."
    # FastAPI does this check for us automatically!

    # If the form is good, we add it to our database.
    print(f"Received new test result: {result.test_name}") # A useful print statement!
    insert_result(result)

    # Then we send back a "Got it!" message.
    return {"message": "Test result received and stored successfully."}
    