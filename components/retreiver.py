from rank_bm25 import BM25Okapi


class HybridRetriever:

    def __init__(
        self,
        vector_store,
        documents,
        dense_k: int = 8,
        keyword_k: int = 8
    ):

        self.vector_store = vector_store
        self.documents = documents

        self.dense_k = dense_k
        self.keyword_k = keyword_k

        # -----------------------------------------------
        # BM25
        # -----------------------------------------------

        tokenized_documents = [
            document.page_content.lower().split()
            for document in documents
        ]

        self.bm25 = BM25Okapi(
            tokenized_documents
        )

    def search(
        self,
        query: str
    ):

        # ===============================================
        # FAISS
        # ===============================================

        dense_documents = (
            self.vector_store.similarity_search(
                query,
                k=self.dense_k
            )
        )

        # ===============================================
        # BM25
        # ===============================================

        tokenized_query = (
            query.lower().split()
        )

        scores = self.bm25.get_scores(
            tokenized_query
        )

        ranked_indexes = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )

        keyword_documents = [
            self.documents[i]
            for i in ranked_indexes[
                :self.keyword_k
            ]
        ]

        # ===============================================
        # MERGE + DEDUPLICATE
        # ===============================================

        combined = (
            dense_documents
            + keyword_documents
        )

        unique_documents = {}

        for document in combined:

            chunk_id = document.metadata.get(
                "chunk_id"
            )

            # If chunk_id exists, use it
            if chunk_id is not None:

                if chunk_id not in unique_documents:

                    unique_documents[
                        chunk_id
                    ] = document

            else:

                # Fallback to document text
                key = document.page_content

                if key not in unique_documents:

                    unique_documents[
                        key
                    ] = document

        return list(
            unique_documents.values()
        )