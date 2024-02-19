# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Flask and other dependencies
RUN pip3 install -r requirements.txt

# Expose the port that the Flask app runs on
EXPOSE 5000

# Define the command to run your Flask application
CMD ["python3", "app.py"]
