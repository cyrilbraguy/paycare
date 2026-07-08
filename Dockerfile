# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./etl.py /app/etl.py
COPY /data /app/data

# Install the Python dependencies
RUN pip install -r requirements.txt


# Run the application
CMD python /app/etl.py
