# Use the official Python image from the Docker Hub
FROM python:3.8.0

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /usr/src/app

# Install dependencies
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev pkg-config cmake \
    libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev \
    libboost-python-dev libboost-thread-dev && \
    apt-get clean

# Install MySQL client dependencies
RUN apt-get update && apt-get install -y default-libmysqlclient-dev

# Upgrade pip
RUN python -m pip install --upgrade pip

# Copy the requirements file into the container
COPY requirement.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirement.txt

# Copy the entire Django project into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "dashboard.wsgi:application"]
