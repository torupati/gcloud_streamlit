FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN bash -c "python3 -m venv .venv && source .venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt"

COPY app.py .
COPY pages .

EXPOSE 8501

CMD [".venv/bin/streamlit", "run", "app.py", "--server.port=8501"]
# necessary to set server port in Dockerfile...

#
# docker build --no-cache -t streamlit-app .
# docker run -rm -p 8501:8501 --name my-streamlit-app streamlit-app:latest