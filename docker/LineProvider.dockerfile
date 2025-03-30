FROM python:3.10

# Install user settings in shell
SHELL ["/bin/bash", "-eo", "pipefail", "-c"]

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=2.1.1
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/app/poetry python3 && ln -s /app/poetry/bin/poetry /usr/local/bin/poetry

# Verify Poetry installation
RUN poetry --version

# Set environment variables for Poetry
ENV POETRY_HOME="/app/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1

# Set the working dir for poetry
WORKDIR /app

# Copy pyproject.toml and poetry.lock files
COPY ./pyproject.toml ./poetry.lock ./

# Install python dependencies using Poetry
RUN poetry install --no-root


# Copy the rest of the application code
COPY ./line_provider/ ./src

# Expose the app's port
EXPOSE 8080

# Go to project dir
WORKDIR /app/src

# Run the FastAPI app with uvicorn
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]


