from app.services.llm_service import LLMService
from app.services.neo4j_service import Neo4jService
from app.services.retrieval_service import RetrievalService


class GraphRAGService:
    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.neo4j_service = Neo4jService()
        self.llm_service = LLMService()

    def _retrieve_graph_data(
        self,
        question: str,
        company_name: str,
    ):
        question_lower = question.lower()

        # --------------------------------------------------
        # Financial metric questions
        # --------------------------------------------------

        if "revenue" in question_lower:
            return {
                "type": "financial_metric",
                "data": self.neo4j_service.get_metric(
                    company_name,
                    "Revenue",
                ),
            }

        if (
            "operating income" in question_lower
            or "operating profit" in question_lower
        ):
            return {
                "type": "financial_metric",
                "data": self.neo4j_service.get_metric(
                    company_name,
                    "Operating Income",
                ),
            }

        # --------------------------------------------------
        # Product relationship questions
        # --------------------------------------------------

        if "azure" in question_lower:
            return {
                "type": "product_relationship",
                "data": self.neo4j_service.get_product_relationships(
                    company_name,
                    "Azure",
                ),
            }

        # --------------------------------------------------
        # General graph retrieval
        # --------------------------------------------------

        return {
            "type": "general_financial",
            "data": self.neo4j_service.get_company_financials(
                company_name,
            ),
        }

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
        # 2. Targeted graph retrieval
        # --------------------------------------------------

        graph_result = self._retrieve_graph_data(
            question=question,
            company_name=company_name,
        )

        # --------------------------------------------------
        # 3. Build graph context
        # --------------------------------------------------

        graph_context = f"""
Graph retrieval type:
{graph_result['type']}

Graph data:
{graph_result['data']}
"""

        # --------------------------------------------------
        # 4. Combine vector + graph context
        # --------------------------------------------------

        prompt = f"""
You are a financial research assistant.

Answer the user's question using ONLY the provided
financial document context and knowledge graph context.

Rules:
- Do not invent financial facts.
- If the available context is insufficient, say so.
- Use the financial documents to support factual claims.
- Cite document sources using [Source 1], [Source 2], etc.
- Use the knowledge graph to understand structured
  financial facts and relationships.
- Clearly distinguish information retrieved from documents
  from information retrieved from the knowledge graph.
- If a graph value says "Surpassed $75 billion", do not
  present $75 billion as an exact value.
- Keep the answer concise and easy to understand.

User question:
{question}

Financial document context:
{document_context}

Knowledge graph context:
{graph_context}

Provide the answer with citations.
"""

        # --------------------------------------------------
        # 5. Generate answer
        # --------------------------------------------------

        answer = self.llm_service.generate(prompt)

        # --------------------------------------------------
        # 6. Return result
        # --------------------------------------------------

        return {
            "question": question,
            "answer": answer,
            "documents": documents,
            "graph": graph_result,
        }

    def close(self):
        self.neo4j_service.close()