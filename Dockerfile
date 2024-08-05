# Use a base Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt

# Copy the application code
COPY . .

# Copy the .env file
COPY .env ./

# Expose port 5000 for Flask
EXPOSE 5000

# Command to run the application
CMD ["python", "main.py"]
