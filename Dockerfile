# Step 1: Start with an official box that already has Python 3.9 installed.
# The "-slim" version is a smaller, more efficient base.
FROM python:3.9-slim

# Step 2: Set the working directory inside the box to a folder named /app.
# All our next commands will happen inside this folder.
WORKDIR /app

# Step 3: Copy our dependencies from our computer into the /app folder in the box.
COPY requirements.txt .

# Step 4: Run the pip command inside the box to install all the Python libraries.
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy all the other files from our computer (main.py, database.py, etc.)
# into the /app folder in the box.
COPY . .

# Step 6: Tell Docker that the application inside the box uses port 8000.
EXPOSE 8000

# Step 7: This is the final command to run when the container starts.
# It tells Uvicorn to run our app and listen for connections from anywhere ("0.0.0.0").
# This is crucial for Docker to connect to it from the outside.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]