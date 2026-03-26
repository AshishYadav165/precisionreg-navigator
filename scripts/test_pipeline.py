from src.pipeline import RegulatoryPipeline

def main():
    pipeline = RegulatoryPipeline()

    product_input = {
        "disease": "NSCLC",
        "intended_use": "NGS-based tumor profiling assay intended to identify actionable genomic alterations in patients with advanced non-small cell lung cancer to support therapy selection.",
        "biomarkers": ["EGFR", "ALK", "ROS1", "KRAS"],
        "therapy_linked": True,
        "specimen_type": "FFPE tissue",
        "platform": "NGS targeted panel",
        "software_involved": True,
    }

    result = pipeline.run(product_input)

    print("\n=== CLASSIFICATION ===")
    print(result["classification"].model_dump())

    print("\n=== ASSESSMENT ===")
    print(result["assessment"].model_dump())

    print("\n=== GUIDANCE HITS ===")
    for hit in result["guidance_hits"][:3]:
        print(hit["title"], hit["section"])

    print("\n=== PRECEDENTS ===")
    for p in result["precedent_hits"][:5]:
        print(p.trade_name, "|", p.route, "|", p.platform)

if __name__ == "__main__":
    main()
