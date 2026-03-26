from src.models import MemoOutput

def generate_memo(product_input, classification, assessment, guidance_hits, precedent_hits=None):
    citations = []
    for g in guidance_hits[:5]:
        title = g.get("title", "")
        section = g.get("section", "")
        citations.append(f"{title} - {section}")

    precedent_names = []
    seen = set()
    if precedent_hits:
        for p in precedent_hits[:10]:
            label = f"{p.trade_name} ({p.submission_number})"
            if label not in seen:
                seen.add(label)
                precedent_names.append(label)

    product_assessment = classification.rationale
    if precedent_names:
        product_assessment += "\n\nRelevant FDA precedents considered: " + ", ".join(precedent_names[:5])

    return MemoOutput(
        title="FDA Regulatory Assessment Memo",
        executive_summary=assessment.summary,
        product_assessment=product_assessment,
        evidence_gaps=assessment.evidence_gaps,
        recommended_actions=assessment.next_steps,
        citations=list(dict.fromkeys(citations + precedent_names)),
    )
