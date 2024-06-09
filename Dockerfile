FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY app /app
COPY requirements.txt /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt


EXPOSE 8000

# Run app/main.py when the container launches
CMD ["python", "web_app.py"]

