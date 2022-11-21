# syntax = docker/dockerfile:experimental
# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8

EXPOSE 5000

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser
USER appuser

# Keeps Python from generating .pyc files in the container
# Turns off buffering for easier container logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:${PATH}"

# Install pip requirements
COPY requirements.txt .
RUN --mount=type=cache,target=/home/appuser/.cache/pip,uid=5678 python -m pip install --user -r requirements.txt
RUN python -c "import classla; classla.download('sl')"
# WORKDIR /app
COPY . /app

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "128",  "app.main:app"]
