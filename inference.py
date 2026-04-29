import json
import argparse
import time
import re
from src.retrieval import retrieve_context, generate_rationale

def extract_is_codes(text):
    # Senior Engineer Fix: If text is a list, join it into one string
    if isinstance(text, list):
        text = " ".join([str(i) for i in text])
    
    if not text:
        return []

    pattern = r"IS\s?\d+(?::\d+)?"
    codes = re.findall(pattern, text)
    return list(set(codes))

def run_inference(input_path, output_path):
    with open(input_path, 'r') as f:
        data = json.load(f)

    results = []
    print(f"🧐 Processing {len(data)} queries for BIS compliance...")

    for item in data:
        query = item['query']
        query_id = item['id']
        
        start_time = time.time()
        
        # RAG Pipeline
        context = retrieve_context(query)
        ai_response = generate_rationale(query, context)
        
        # We provide the full rationale for manual scoring 
        # but extract codes for automated scoring
        found_codes = extract_is_codes(ai_response)
        
        latency = time.time() - start_time
        
        results.append({
            "id": query_id,
            "retrieved_standards": found_codes if found_codes else ["None Found"],
            "rationale": ai_response, # Extra field for the manual relevance score
            "latency_seconds": round(latency, 3)
        })
        
        print(f"  ✅ {query_id} processed in {latency:.2f}s")

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=4)
    
    print(f"\n🏁 Finished! Results saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    
    run_inference(args.input, args.output)