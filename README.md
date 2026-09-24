# FinGraph AI



A small financial research assistant built with **RAG, Neo4j, Qdrant, and a local LLM**.



The goal of this project is to experiment with **GraphRAG** and understand how vector search and knowledge graphs can work together when answering questions about financial documents.



## How it works



```text

Financial Document

      │

      ├──► Qdrant ──► Semantic Search

      │

      └──► Neo4j ───► Relationships

                        │

                        ▼

                      GraphRAG

                        │

                        ▼

                   Qwen3 8B

                        │

                        ▼

                   Final Answer

```



The system combines:



* **Qdrant** for document embeddings and semantic search

* **Neo4j** for financial relationships and knowledge graphs

* **Ollama + Qwen3 8B** for local LLM inference

* **FastAPI** for the API

* **Docker Compose** for running everything together



\## Example



The assistant can answer questions like:



> Why did Microsoft's revenue increase in 2025?



It retrieves relevant parts of the annual report, combines them with information from the knowledge graph, and generates an answer with source references.



## Project Structure



```text

app/

├── api/

└── services/

   ├── embedding\_service.py

   ├── retrieval\_service.py

   ├── vector\_store\_service.py

   ├── neo4j\_service.py

   ├── llm\_service.py

   ├── rag\_service.py

   └── graph\_rag\_service.py



scripts/

data/

docker-compose.yml

Dockerfile

requirements.txt

```



## Run



```bash

git clone https://github.com/phoorooz/fin-graph-ai.git

cd fin-graph-ai



docker compose up -d --build

```



API:



```text

http://localhost:8000

```



Swagger:



```text

http://localhost:8000/docs

```



## Status



This is a **v0.1 portfolio project**. The main goal is to demonstrate the architecture and the integration of RAG, vector search, knowledge graphs, and LLMs rather than build a production-ready financial platform.



## Author



**Ali Forouzan**



AI Engineer & Backend Software Engineer



GitHub: https://github.com/phoorooz



