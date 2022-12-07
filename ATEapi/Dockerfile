# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# RUN apk add --no-cache gcc musl-dev
RUN pip install gunicorn

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app


ADD https://kt-cloud.ijs.si/index.php/s/T4qtSKxbxgqr6c5/download/pytorch_model.bin ./model/term_extractor/

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "-t 0", "--bind", "0.0.0.0:5000", "main:app"]
