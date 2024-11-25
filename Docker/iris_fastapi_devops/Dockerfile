# Stage 1: Build the FastAPI app
FROM python:3.9-slim AS build

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app code
COPY . .

# Stage 2: Production image
FROM python:3.9-slim AS final

# Set the working directory
WORKDIR /app

# Copy dependencies and app code from the build stage
COPY --from=build /app /app

# Expose the application port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
