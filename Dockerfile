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

ARG DB_HOST
ENV DB_HOST=$MYSQLHOST

ARG DB_PASSWORD
ENV DB_PASSWORD=$MYSQLPASSWORD

ARG DB_USER
ENV DB_USER=$MYSQLUSER

ARG DB_NAME
ENV DB_NAME=$MYSQLDB

ARG DB_PORT
ENV DB_PORT=$MYSQLPORT

ARG SECRET_KEY
ENV SECRET_KEY=$SECRET_KEY

ARG TOKEN_EXPIRATION
ENV TOKEN_EXPIRATION=$TOKEN_EXPIRATION

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the application
ENTRYPOINT ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000" ]