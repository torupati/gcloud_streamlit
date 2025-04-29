FROM python:3.12 AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    POETRY_HOME="/opt/poetry" \
    PATH="${POETRY_HOME}/bin:${PATH}"

RUN curl -sSL https://install.python-poetry.org | python - && \
    chmod +x ${POETRY_HOME}/bin/poetry


RUN ${POETRY_HOME}/bin/poetry config virtualenvs.create false

WORKDIR /app

# Install dependencies
COPY pyproject.toml poetry.lock /app/
RUN ${POETRY_HOME}/bin/poetry install --no-interaction --without dev --no-ansi --no-root -vvv

# Lightweight image
FROM python:3.12-slim

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING="UTF-8"

# Copy necessary files from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/streamlit /usr/local/bin/

# working directory
# Create a non-root user
#RUN addgroup --system streamlit && adduser --system --ingroup streamlit streamlit
WORKDIR /app

# Copy application code
COPY . /app/

# Expose the port
EXPOSE 8501
# Run the application
CMD ["streamlit", "run", "app.py", "--server.port", "8501"]
# docker build --no-cache -t streamlit-app .
# docker run -rm -p 8501:8501 --name my-streamlit-app streamlit-app:latest
