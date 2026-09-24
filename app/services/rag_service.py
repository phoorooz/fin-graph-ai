from app.services.llm_service import LLMService
from app.services.retrieval_service import RetrievalService


class RAGService:
    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.llm_service = LLMService()

    def answer(
        self,
        question: str,
        limit: int = 5,
    ):
        documents = self.retrieval_service.retrieve(
            query=question,
            limit=limit,
        )

        context = "\n\n".join(
            [
                (
                    f"[Source {index + 1} | "
                    f"Microsoft 2025 Annual Report | "
                    f"Chunk {document['chunk_id']}]\n"
                    f"{document['text']}"
                )
                for index, document in enumerate(documents)
            ]
        )

        prompt = f"""
You are a financial research assistant.

Answer the user's question using ONLY the provided financial document context.

Important rules:
- Do not invent financial facts.
- If the context does not contain enough information, say so.
- Cite the relevant source numbers in your answer using [Source 1], [Source 2], etc.
- Only cite sources that actually support the statement.
- Keep the answer clear and concise.

User question:
{question}

Financial document context:
{context}

Provide the answer with citations.
"""

        answer = self.llm_service.generate(prompt)

        sources = []

        for index, document in enumerate(documents, start=1):
            sources.append(
                {
                    "source": index,
                    "document": document["document"],
                    "chunk_id": document["chunk_id"],
                    "score": document["score"],
                }
            )

        return {
            "question": question,
            "answer": answer,
            "sources": sources,
        }