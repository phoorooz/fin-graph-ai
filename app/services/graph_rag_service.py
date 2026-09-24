from app.services.llm_service import LLMService
from app.services.neo4j_service import Neo4jService
from app.services.retrieval_service import RetrievalService


class GraphRAGService:
    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.neo4j_service = Neo4jService()
        self.llm_service = LLMService()

    def answer(
        self,
        question: str,
        company_name: str = "Microsoft",
        limit: int = 5,
    ):
        # --------------------------------------------------
        # 1. Vector retrieval
        # --------------------------------------------------

        documents = self.retrieval_service.retrieve(
            query=question,
            limit=limit,
        )

        document_context = "\n\n".join(
            [
                (
                    f"[Document Source {index + 1} | "
                    f"Chunk {document['chunk_id']}]\n"
                    f"{document['text']}"
                )
                for index, document in enumerate(documents)
            ]
        )

        # --------------------------------------------------
        # 2. Graph retrieval
        # --------------------------------------------------

        graph_data = self.neo4j_service.get_financial_graph(
            company_name
        )

        graph_context = f"""
Company:
{graph_data['company']}

Financial metrics:
{graph_data['financial_metrics']}

Business relationships:
{graph_data['business_relationships']}
"""

        # --------------------------------------------------
        # 3. Combine vector + graph context
        # --------------------------------------------------

        prompt = f"""
You are a financial research assistant.

Answer the user's question using ONLY the provided
financial document context and knowledge graph context.

Rules:
- Do not invent financial facts.
- If the available context is insufficient, say so.
- Use the document sources to support factual claims.
- Cite document sources using [Source 1], [Source 2], etc.
- Use the knowledge graph to understand relationships
  between companies, metrics, segments, products, and periods.
- Clearly distinguish information retrieved from documents
  from relationships retrieved from the knowledge graph.
- Keep the answer concise and easy to understand.

User question:
{question}

Financial document context:
{document_context}

Knowledge graph context:
{graph_context}

Provide the final answer with citations.
"""

        # --------------------------------------------------
        # 4. Generate answer
        # --------------------------------------------------

        answer = self.llm_service.generate(prompt)

        # --------------------------------------------------
        # 5. Return result
        # --------------------------------------------------

        return {
            "question": question,
            "answer": answer,
            "documents": documents,
            "graph": graph_data,
        }

    def close(self):
        self.neo4j_service.close()