import os

from fastapi import FastAPI

from app.services.neo4j_service import Neo4jService


app = FastAPI(
    title="FinGraph AI",
    description="Financial Research Assistant using RAG and Knowledge Graphs",
    version="0.1.0",
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/neo4j")
def neo4j_health():
    service = Neo4jService()

    try:
        result = service.verify_connection()

        return {
            "status": "ok",
            "neo4j": result,
        }
    finally:
        service.close()


@app.post("/graph/sample")
def create_sample_graph():
    service = Neo4jService()

    try:
        return service.create_sample_graph()
    finally:
        service.close()
        

@app.post("/graph/financial")
def create_financial_data():
    service = Neo4jService()

    try:
        return service.create_financial_data()
    finally:
        service.close()

@app.get("/graph/financial/{company_name}")
def get_company_financials(company_name: str):
    service = Neo4jService()

    try:
        return service.get_company_financials(company_name)
    finally:
        service.close()        