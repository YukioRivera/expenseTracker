# # extra info
# # to reset the docker and apply changes use this command
# sudo docker-compose down
# sudo docker-compose build
# sudo docker-compose up

# Use an official Python runtime as the parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /home/dev/expenseTracker

# Copy the current directory contents into the container at /home/dev/expenseTracker
COPY . /home/dev/expenseTracker

# Install system dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    libssl-dev \
    libffi-dev

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Set the PYTHONPATH
ENV PYTHONPATH /home/dev/expenseTracker

# Set the FLASK_APP environment variable to point to the correct application factory
ENV FLASK_APP app:create_app

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
