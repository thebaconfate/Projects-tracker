FROM python:3.12

WORKDIR /app

# Install Poetry
RUN pip install pipx
RUN pipx install poetry

ENV PATH="/root/.local/bin:${PATH}"

# Copy the poetry.lock and pyproject.toml
COPY poetry.lock pyproject.toml ./

RUN poetry install

COPY . /app

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the application
CMD ["poetry", "run", "main"]
