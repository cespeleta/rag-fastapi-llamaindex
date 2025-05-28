# Local RAG System with FastAPI, LlamaIndex and ChromaDB

This project provides a complete, production-ready Retrieval Augmented Generation (RAG) system using FastAPI, LlamaIndex and ChromaDB. It uses FastAPI to expose an API that can answer questions based on the content of **PDF**'s documents that you can provide. The system is fully containerized with **Docker** and includes an automated **CI/CD pipeline** for testing and deployment.

The core of the project is a RAG pipeline build with **LlamaIndex**, using **HuggingFace** models for document embedding and LLM's, and **ChromaDB** as the local vector store.

## Project structure

```shell
.
├── .github/    # CI/CD github workflow
├── app/        # Main application source code
│ ├── api/      # API endpoints, schemas, and error handlers
│ ├── core/     # Core logic: configuration, exceptions, logging
│ ├── services/ # RAG service and its components (LLM, vector store)
│ └── main.py   # FastAPI application entrypoint
├── pdfs/       # Directory for PDF files
├── chromadb/   # Directory for ChromaDB database
├── templates/  # Jinja2 prompt templates
```

## Getting started

Follow these steps to set up and run the application on your local machine.

### 1. Clone the repository

```bash
git clone ...
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Edit the `.env` and add your `HF_TOKEN`.

### 3. Install dependencies

```bash
make setup
```

### 4. Add your documents

Place any PDF file you want to query into the `./pdfs` directory.

### 5. Run the application

The application will be available at `http://localhost:8000`. You can access the interactive documentation at `http://localhost:8000/docs`.


## Docker deployment

The simplest way to run the appication is with Docker.

### 1. Build the Docker Image

This command uses a multi-stage `Dockerfile` to build a production-ready image.

```bash
make build.docker
```

### 2. Run the Container

This command starts the container in detached mode.

```bash
make run.docker
```

### 3. Interact with the Container
You can interact with the docker container with the following commands:
* View logs: `make logs.docker`
* Stop and Remove: `make stop.docker`


## Usage

Interact with the API via the documentation at `http://localhost:8000/docs` or using a tool like `curl`.

### 1. Query the RAG System

We create a request with the following prompt: `Give me a list of the data sources used for pre-training the Llama models.`

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/query/query' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "prompt": "Give me a list of the data sources used for pre-training the Llama models."
}'
```

The answer we get is shown below.

```bash
app.services.rag_service - INFO - Executing async query: 'Give me a list of the data sources used for pre-training the Llama models.'
app.services.rag_service - INFO - Generated answer: '2.1 Pre-training Data
- English CommonCrawl [67%].
- C4 [15%].
- Github [4.5%].
- Wikipedia [4.5%].
- Books [4.5%].
- ArXiv [2.5%].
- StackExchange [2.0%].'
```

## Configuration

Application behaviour can be configured through the `config-local.yaml` and environment variables.
* `config-local.yaml`: Contains static configuration like api attributes, model names and RAG parameters.
* **Environment variables**: Used to store secrets.


## CI/CD Pipeline

This project includes a CI/CD pipeline defined in `.github/workflows/ci-cd.yaml`. It automatically trigers on pushes and pull requests to the `main` branch.

The pipeline consists of two main jobs:
1. `checks`: Perform linting, type checking, unit testing and Dockerfile validation. It also uploads the coverage report as a built artifact.
2. `build-and-publish`: On a successful push to `main`, this job builds the production Docker image and pushed it to a container registry.
