from sqlalchemy import or_
from src.embeddings import Embedder
from src.vectorstore import LocalVectorStore
from src.db import get_session, FDAPrecedent
from src.config import EMBEDDING_MODEL, VECTORSTORE_INDEX, VECTORSTORE_METADATA, SQLITE_PATH

class RetrievalService:
    def __init__(self):
        self.embedder = Embedder(EMBEDDING_MODEL)
        self.vectorstore = LocalVectorStore.load(
            VECTORSTORE_INDEX,
            VECTORSTORE_METADATA
        )
        self.session = get_session(SQLITE_PATH)

    def search_guidance(self, query: str, k: int = 5):
        qv = self.embedder.embed_query(query)
        return self.vectorstore.search(qv, k=k)

    def _dedupe_precedents(self, rows):
        seen = set()
        unique = []
        for r in rows:
            key = (r.trade_name, r.submission_number)
            if key not in seen:
                seen.add(key)
                unique.append(r)
        return unique

    def search_precedents(self, disease: str = "", platform: str = "", biomarker: str = ""):
        query = self.session.query(FDAPrecedent)

        if disease:
            query = query.filter(FDAPrecedent.disease_use.ilike(f"%{disease}%"))

        if platform:
            if "NGS" in platform.upper():
                query = query.filter(
                    or_(
                        FDAPrecedent.platform.ilike("%NGS%"),
                        FDAPrecedent.platform.ilike("%Tumor Profiling%"),
                        FDAPrecedent.platform.ilike("%Liquid biopsy%")
                    )
                )
            elif "LIQUID" in platform.upper():
                query = query.filter(
                    or_(
                        FDAPrecedent.platform.ilike("%Liquid biopsy%"),
                        FDAPrecedent.platform.ilike("%NGS%")
                    )
                )
            else:
                query = query.filter(FDAPrecedent.platform.ilike(f"%{platform}%"))

        if biomarker and biomarker.lower() != "multiple biomarkers":
            query = query.filter(
                or_(
                    FDAPrecedent.biomarker.ilike(f"%{biomarker}%"),
                    FDAPrecedent.biomarker.ilike("%Multiple biomarkers%")
                )
            )

        results = self._dedupe_precedents(query.limit(15).all())
        if results:
            return results[:10]

        fallback = self.session.query(FDAPrecedent)

        if disease:
            fallback = fallback.filter(FDAPrecedent.disease_use.ilike(f"%{disease}%"))

        fallback_results = self._dedupe_precedents(fallback.limit(15).all())
        if fallback_results:
            return fallback_results[:10]

        return self._dedupe_precedents(self.session.query(FDAPrecedent).limit(15).all())[:10]
