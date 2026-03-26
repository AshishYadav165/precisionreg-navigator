import json
from anthropic import Anthropic
from src.models import ProductClassification, RegulatoryAssessment
from src.prompts import CLASSIFIER_PROMPT, ASSESSMENT_PROMPT
from src.config import ANTHROPIC_API_KEY

client = Anthropic(api_key=ANTHROPIC_API_KEY)

def call_llm(prompt: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1200,
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()

def clean_json_response(raw: str) -> str:
    raw = raw.strip()

    if raw.startswith("```json"):
        raw = raw[len("```json"):].strip()
    elif raw.startswith("```"):
        raw = raw[len("```"):].strip()

    if raw.endswith("```"):
        raw = raw[:-3].strip()

    return raw

def extract_json_object(raw: str) -> str:
    raw = clean_json_response(raw)
    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1 and end > start:
        return raw[start:end+1]
    return raw

def safe_json_loads(raw: str) -> dict:
    cleaned = extract_json_object(raw)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        print("\nRAW MODEL OUTPUT:\n", raw)
        print("\nCLEANED JSON CANDIDATE:\n", cleaned)
        raise

def normalize_classification_payload(parsed: dict) -> dict:
    rationale = parsed.get("rationale", "")

    if isinstance(rationale, dict):
        if "summary" in rationale:
            parsed["rationale"] = str(rationale["summary"])
        else:
            parsed["rationale"] = json.dumps(rationale, ensure_ascii=False)
    elif isinstance(rationale, list):
        parsed["rationale"] = " ".join(str(x) for x in rationale)
    elif rationale is None:
        parsed["rationale"] = ""
    else:
        parsed["rationale"] = str(rationale)

    return parsed

def normalize_assessment_payload(parsed: dict) -> dict:
    for field in ["evidence_gaps", "key_risks", "next_steps"]:
        value = parsed.get(field, [])
        if isinstance(value, str):
            parsed[field] = [value]
        elif value is None:
            parsed[field] = []
        elif not isinstance(value, list):
            parsed[field] = [str(value)]

    summary = parsed.get("summary", "")
    if isinstance(summary, dict):
        parsed["summary"] = str(summary.get("summary", json.dumps(summary, ensure_ascii=False)))
    elif summary is None:
        parsed["summary"] = ""
    else:
        parsed["summary"] = str(summary)

    probable_route = parsed.get("probable_route", "")
    if probable_route is None:
        parsed["probable_route"] = ""
    else:
        parsed["probable_route"] = str(probable_route)

    return parsed

def classify_product(product_dict: dict) -> ProductClassification:
    prompt = f"{CLASSIFIER_PROMPT}\n\nProduct:\n{json.dumps(product_dict, indent=2)}"
    raw = call_llm(prompt)
    parsed = safe_json_loads(raw)
    parsed = normalize_classification_payload(parsed)
    return ProductClassification(**parsed)

def assess_product(product_dict: dict, guidance_hits: list, precedent_hits: list) -> RegulatoryAssessment:
    precedent_payload = []
    for p in precedent_hits:
        precedent_payload.append({
            "trade_name": p.trade_name,
            "sponsor": p.sponsor,
            "disease_use": p.disease_use,
            "biomarker": p.biomarker,
            "platform": p.platform,
            "specimen_type": p.specimen_type,
            "route": p.route,
            "submission_number": p.submission_number,
            "cdx_flag": p.cdx_flag,
        })

    compact_guidance = []
    for g in guidance_hits[:4]:
        compact_guidance.append({
            "title": g["title"],
            "section": g["section"],
            "text": g["text"][:700]
        })

    prompt = (
        f"{ASSESSMENT_PROMPT}\n\n"
        f"IMPORTANT: Keep summary under 120 words. "
        f"Each list must contain at most 5 short items. "
        f"Return valid JSON only.\n\n"
        f"Product:\n{json.dumps(product_dict, indent=2)}\n\n"
        f"Guidance:\n{json.dumps(compact_guidance, indent=2)}\n\n"
        f"Precedents:\n{json.dumps(precedent_payload[:5], indent=2)}"
    )

    raw = call_llm(prompt)
    parsed = safe_json_loads(raw)
    parsed = normalize_assessment_payload(parsed)
    return RegulatoryAssessment(**parsed)
