import json
import os

DATA_DIR = "/Users/mekot/Desktop/TRANSFER/CLAUDE-HANDOFF/CODE/development/coaching tree/research/data"

def load_json(filename):
    with open(os.path.join(DATA_DIR, filename), 'r') as f:
        return json.load(f)

def verify_data():
    print("Loading data...")
    coaches = load_json('coaches.json')
    relationships = load_json('relationships.json')
    stints = load_json('stints.json')
    
    errors = []
    warnings = []

    print(f"Loaded {len(coaches)} coaches, {len(relationships)} relationships, {len(stints)} stints.")
    print("\n--- Running Checks ---\n")

    # 1. Check Coaches
    coach_ids = set(coaches.keys())
    for cid, data in coaches.items():
        if not data.get('name'):
            errors.append(f"Coach missing name: {cid}")
        if 'generation' not in data:
            errors.append(f"Coach missing generation: {cid}")
            
    # 2. Check Relationships
    for i, rel in enumerate(relationships):
        mentor_id = rel.get('mentor_id')
        protege_id = rel.get('protege_id')
        
        if mentor_id not in coach_ids:
            errors.append(f"Relationship [{i}] '{rel.get('id')}' has invalid mentor_id: {mentor_id}")
        if protege_id not in coach_ids:
            errors.append(f"Relationship [{i}] '{rel.get('id')}' has invalid protege_id: {protege_id}")
            
        ys = rel.get('year_start')
        ye = rel.get('year_end')
        if ys and ye and ys > ye:
            errors.append(f"Relationship '{rel.get('id')}' has year_start > year_end ({ys} > {ye})")

    # 3. Check Stints
    stint_ids = set()
    for i, stint in enumerate(stints):
        sid = stint.get('id')
        if not sid:
            errors.append(f"Stint [{i}] missing id")
        elif sid in stint_ids:
            errors.append(f"Duplicate stint id: {sid}")
        stint_ids.add(sid)
            
        coach_id = stint.get('coach_id')
        hc_id = stint.get('head_coach_id')
        
        if coach_id not in coach_ids:
            errors.append(f"Stint '{sid}' has invalid coach_id: {coach_id}")
            
        if hc_id and hc_id not in coach_ids:
            errors.append(f"Stint '{sid}' has invalid head_coach_id: {hc_id}")
            
        ys = stint.get('year_start')
        ye = stint.get('year_end')
        if ys and ye and ys > ye:
            errors.append(f"Stint '{sid}' has year_start > year_end ({ys} > {ye})")

    if not errors and not warnings:
        print("✅ All checks passed successfully! No errors or warnings found.")
    else:
        if errors:
            print(f"❌ Found {len(errors)} Errors:")
            for err in errors:
                print(f"  - {err}")
        if warnings:
            print(f"\n⚠️ Found {len(warnings)} Warnings:")
            for warn in warnings:
                print(f"  - {warn}")

if __name__ == '__main__':
    verify_data()
