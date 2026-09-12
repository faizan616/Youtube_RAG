from sentence_transformers import CrossEncoder


class DocumentReranker:

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    ):
        self.model = CrossEncoder(
            model_name
        )

    def rerank(
        self,
        query: str,
        documents: list,
        top_k: int = 4
    ):

        if not documents:
            return []

        # -----------------------------------------------
        # Create query-document pairs
        # -----------------------------------------------

        pairs = [
            (
                query,
                document.page_content
            )
            for document in documents
        ]

        # -----------------------------------------------
        # Calculate relevance scores
        # -----------------------------------------------

        scores = self.model.predict(
            pairs
        )

        # -----------------------------------------------
        # Attach score to metadata
        # -----------------------------------------------

        scored_documents = []

        for document, score in zip(
            documents,
            scores
        ):

            # Make sure metadata exists
            if document.metadata is None:
                document.metadata = {}

            document.metadata[
                "rerank_score"
            ] = float(score)

            scored_documents.append(
                document
            )

        # -----------------------------------------------
        # Sort by rerank score
        # -----------------------------------------------

        scored_documents.sort(
            key=lambda document: document.metadata[
                "rerank_score"
            ],
            reverse=True
        )

        # -----------------------------------------------
        # Return top documents
        # -----------------------------------------------

        return scored_documents[:top_k]