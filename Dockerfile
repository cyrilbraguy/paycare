# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory
WORKDIR /home

# Copy the current directory contents into the container at /app
COPY ./app /home/app
COPY /data /home/data
COPY ./requirements.txt /home/requirements.txt

# Install the Python dependencies
RUN pip install -r requirements.txt


# Run the application
CMD python /home/app/etl.py
