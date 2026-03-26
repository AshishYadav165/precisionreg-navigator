from src.retrieval import RetrievalService
from src.agents import classify_product, assess_product

class RegulatoryPipeline:
    def __init__(self):
        self.retrieval = RetrievalService()

    def run(self, product_input: dict):
        classification = classify_product(product_input)

        retrieval_query = " ".join([
            product_input.get("disease", ""),
            product_input.get("platform", ""),
            product_input.get("specimen_type", ""),
            " ".join(product_input.get("biomarkers", [])),
            product_input.get("intended_use", ""),
            "FDA oncology IVD companion diagnostic tumor profiling analytical validation precision medicine"
        ])

        guidance_hits = self.retrieval.search_guidance(retrieval_query, k=5)

        biomarker = product_input.get("biomarkers", [""])[0] if product_input.get("biomarkers") else ""
        precedent_hits = self.retrieval.search_precedents(
            disease=product_input.get("disease", ""),
            platform=product_input.get("platform", ""),
            biomarker=biomarker
        )

        assessment = assess_product(
            product_input,
            guidance_hits=guidance_hits,
            precedent_hits=precedent_hits
        )

        return {
            "classification": classification,
            "guidance_hits": guidance_hits,
            "precedent_hits": precedent_hits,
            "assessment": assessment,
        }
