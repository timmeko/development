#!/usr/bin/env python3
"""
Coaching Tree Data Verification
Generates and runs verification queries via OpenAI API to fact-check
every coach in coaches.json against their stated HC stops and mentor connections.

Usage:
    # Set your API key
    export OPENAI_API_KEY="sk-..."

    # Run all verification queries
    python verify_coaches.py

    # Run a specific batch by number
    python verify_coaches.py --batch 1

    # Run a range of batches
    python verify_coaches.py --from 1 --to 5

    # List all batches without running them
    python verify_coaches.py --list

    # Use a different model (default: gpt-4o)
    python verify_coaches.py --model gpt-4o-mini

    # Generate a summary report from existing results
    python verify_coaches.py --report
"""

import os
import sys
import time
import json
import argparse
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not installed. Run: pip install openai")
    sys.exit(1)

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
OUTPUT_DIR = SCRIPT_DIR / "research" / "verification"

SYSTEM_PROMPT = """You are a college football coaching history expert helping verify a coaching tree database.

IMPORTANT RULES:
- Be precise about facts. If a claim is WRONG, say so clearly.
- If you're uncertain, say "UNCERTAIN" rather than guessing.
- Check each claimed HC stop carefully — was this person actually the HEAD COACH (not OC, DC, or interim)?
- Check mentor connections — did this person actually work on that staff during those years?
- Mark each verification with: CORRECT, WRONG, UNCERTAIN, or PARTIALLY CORRECT
- If something is wrong, provide the correct information.
- Pay special attention to:
  * Coaches listed as HC who were actually coordinators
  * Wrong schools (e.g., listing someone at School A when they were at School B)
  * Wrong years
  * Wrong mentor connections (worked under Coach X, not Coach Y)

OUTPUT FORMAT:
For each coach, provide a markdown section with verification results."""

# ── Batch size ────────────────────────────────────────────────────────────────
BATCH_SIZE = 8  # coaches per query (keeps prompt/response manageable)


def load_coaches():
    """Load coaches.json."""
    with open(DATA_DIR / "coaches.json") as f:
        return json.load(f)


def load_relationships():
    """Load relationships.json."""
    with open(DATA_DIR / "relationships.json") as f:
        return json.load(f)


def build_verification_batches(coaches, relationships):
    """Build verification queries from coaches.json data.

    Groups coaches into batches and creates a verification prompt for each.
    Only includes coaches with HC stops (the ones visible on the poster).
    """
    # Build relationship lookup: protege_id → list of {mentor, school, years, role}
    rel_lookup = {}
    for r in relationships:
        pid = r["protege_id"]
        mid = r["mentor_id"]
        mentor_name = coaches.get(mid, {}).get("name", mid)
        rel_lookup.setdefault(pid, []).append({
            "mentor": mentor_name,
            "school": r.get("school", "?"),
            "year_start": r.get("year_start", "?"),
            "year_end": r.get("year_end", "?"),
            "role": r.get("protege_role", "?"),
        })

    # Collect coaches to verify (those with HC stops)
    to_verify = []
    for cid, info in coaches.items():
        hc_schools = info.get("hc_schools", [])
        gen = info.get("generation", 99)
        if gen < 1 or gen > 3:
            continue  # skip Holtz and upstream
        if not hc_schools:
            continue  # skip non-HC coaches

        mentor_ctx = info.get("mentor_context", info.get("holtz_connection", ""))
        primary_mentor = info.get("mentor", "lou-holtz" if gen == 1 else "?")
        primary_mentor_name = coaches.get(primary_mentor, {}).get("name", primary_mentor)

        rels = rel_lookup.get(cid, [])

        to_verify.append({
            "id": cid,
            "name": info["name"],
            "generation": gen,
            "hc_schools": hc_schools,
            "mentor_context": mentor_ctx,
            "primary_mentor": primary_mentor_name,
            "relationships": rels,
            "notes": info.get("notes", ""),
        })

    # Sort by generation then name for consistent ordering
    to_verify.sort(key=lambda x: (x["generation"], x["name"]))

    # Build batches
    batches = []
    for i in range(0, len(to_verify), BATCH_SIZE):
        batch = to_verify[i:i + BATCH_SIZE]
        batch_num = len(batches) + 1
        filename = f"verify_{batch_num:02d}"

        # Build the prompt
        prompt_parts = [
            "I'm verifying data in a coaching tree database centered on Lou Holtz. "
            "For each coach below, please verify:\n"
            "1. Were they actually HEAD COACH at the listed schools? (not OC/DC/coordinator)\n"
            "2. Is the mentor connection accurate? Did they actually work under that coach at that school during those years?\n"
            "3. Are there any factual errors?\n\n"
            "For each coach, provide a verification section.\n\n"
        ]

        for coach in batch:
            prompt_parts.append(f"## {coach['name']} (Gen {coach['generation']})\n")
            prompt_parts.append(f"- **Claimed HC stops:** {', '.join(coach['hc_schools'])}\n")
            prompt_parts.append(f"- **Primary mentor:** {coach['primary_mentor']}\n")
            prompt_parts.append(f"- **Mentor context:** {coach['mentor_context']}\n")
            if coach["relationships"]:
                prompt_parts.append("- **All mentor connections:**\n")
                for rel in coach["relationships"]:
                    prompt_parts.append(
                        f"  - Under {rel['mentor']} at {rel['school']} "
                        f"({rel['year_start']}-{rel['year_end']}), role: {rel['role']}\n"
                    )
            if coach.get("notes"):
                prompt_parts.append(f"- **Notes:** {coach['notes']}\n")
            prompt_parts.append("\n")

        prompt_parts.append(
            "\nFor each coach, respond with:\n\n"
            "## [Coach Name]\n"
            "- **HC Stops:** CORRECT / WRONG (explain) / UNCERTAIN\n"
            "- **Mentor Connection:** CORRECT / WRONG (explain) / UNCERTAIN\n"
            "- **Other Issues:** Any additional facts that are wrong\n"
            "- **Corrections:** What the correct data should be (if anything is wrong)\n"
        )

        prompt = "".join(prompt_parts)
        coach_names = [c["name"] for c in batch]
        batches.append((filename, prompt, coach_names))

    return batches


def run_query(client, model, batch_num, total, filename, prompt):
    """Run a single verification query and save results."""
    output_path = OUTPUT_DIR / f"{filename}.md"

    print(f"\n{'=' * 60}")
    print(f"Batch {batch_num}/{total}: {filename}")
    print(f"{'=' * 60}")

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,  # Low temperature for factual verification
            max_tokens=4096,
        )

        content = response.choices[0].message.content

        with open(output_path, "w") as f:
            f.write(f"# Verification Batch {batch_num}: {filename}\n\n")
            f.write(f"**Model:** {model}  \n")
            f.write(f"**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}  \n")
            f.write(f"**Tokens:** {response.usage.total_tokens} "
                    f"(prompt: {response.usage.prompt_tokens}, "
                    f"completion: {response.usage.completion_tokens})  \n\n")
            f.write("---\n\n")
            f.write(content)
            f.write("\n")

        print(f"  Saved to: {output_path}")
        print(f"  Tokens used: {response.usage.total_tokens}")
        return True

    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def generate_report():
    """Scan verification results and flag issues."""
    if not OUTPUT_DIR.exists():
        print("No verification results found. Run verification queries first.")
        return

    results = sorted(OUTPUT_DIR.glob("verify_*.md"))
    if not results:
        print("No verification result files found.")
        return

    print(f"\n{'=' * 60}")
    print("VERIFICATION REPORT")
    print(f"{'=' * 60}\n")

    issues = []
    for path in results:
        content = path.read_text()
        # Look for WRONG markers
        for line in content.split("\n"):
            line_upper = line.upper()
            if "WRONG" in line_upper or "INCORRECT" in line_upper:
                issues.append((path.name, line.strip()))

    if issues:
        print(f"Found {len(issues)} potential issues:\n")
        for fname, line in issues:
            print(f"  [{fname}] {line}")
    else:
        print("No WRONG/INCORRECT flags found in verification results.")
        print("(This doesn't mean everything is correct — review results manually.)")

    print(f"\nTotal verification files: {len(results)}")


def main():
    parser = argparse.ArgumentParser(
        description="Verify coaching tree data via OpenAI API"
    )
    parser.add_argument("--batch", type=int, help="Run a specific batch number")
    parser.add_argument("--from", dest="from_b", type=int, help="Start from this batch")
    parser.add_argument("--to", dest="to_b", type=int, help="End at this batch (inclusive)")
    parser.add_argument("--list", action="store_true", help="List all batches without running")
    parser.add_argument("--model", default="gpt-4o", help="OpenAI model (default: gpt-4o)")
    parser.add_argument("--delay", type=float, default=2.0, help="Seconds between queries")
    parser.add_argument("--force", action="store_true", help="Re-run even if output exists")
    parser.add_argument("--report", action="store_true", help="Generate report from results")
    args = parser.parse_args()

    coaches = load_coaches()
    relationships = load_relationships()
    batches = build_verification_batches(coaches, relationships)

    if args.report:
        generate_report()
        return

    # List mode
    if args.list:
        print(f"\nVerification batches: {len(batches)} total")
        print(f"{'#':>3}  {'Filename':<20}  {'Coaches':<60}  {'Status'}")
        print(f"{'─' * 3}  {'─' * 20}  {'─' * 60}  {'─' * 8}")
        for i, (filename, _, coach_names) in enumerate(batches, 1):
            output_path = OUTPUT_DIR / f"{filename}.md"
            status = "DONE" if output_path.exists() else "TODO"
            names = ", ".join(coach_names)
            if len(names) > 58:
                names = names[:55] + "..."
            print(f"{i:>3}  {filename:<20}  {names:<60}  {status}")
        total = len(batches)
        done = sum(1 for fn, _, _ in batches if (OUTPUT_DIR / f"{fn}.md").exists())
        hc_count = sum(1 for _, info in coaches.items()
                       if info.get("hc_schools") and info.get("generation", 99) in (1, 2, 3))
        print(f"\n{done}/{total} batches complete ({hc_count} coaches with HC stops)")
        return

    # Validate API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Set it with: export OPENAI_API_KEY='sk-...'")
        sys.exit(1)

    client = OpenAI(api_key=api_key)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Determine which batches to run
    if args.batch:
        indices = [args.batch - 1]
    elif args.from_b or args.to_b:
        start = (args.from_b or 1) - 1
        end = args.to_b or len(batches)
        indices = list(range(start, end))
    else:
        indices = list(range(len(batches)))

    # Filter completed
    if not args.force:
        filtered = []
        for i in indices:
            if i >= len(batches):
                continue
            filename = batches[i][0]
            output_path = OUTPUT_DIR / f"{filename}.md"
            if output_path.exists():
                print(f"Skipping batch {i + 1} ({filename}) — already complete. Use --force to re-run.")
            else:
                filtered.append(i)
        indices = filtered

    if not indices:
        print("\nNo batches to run. All selected batches are complete.")
        print("Use --force to re-run, or --list to see status.")
        return

    total = len(batches)
    print(f"\nRunning {len(indices)} verification batches using model: {args.model}")
    print(f"Output directory: {OUTPUT_DIR}")

    est_cost = len(indices) * 0.10  # rough estimate
    print(f"Estimated cost: ~${est_cost:.2f}")

    for j, i in enumerate(indices):
        if j > 0:
            time.sleep(args.delay)

        filename, prompt, coach_names = batches[i]
        print(f"\n  Coaches: {', '.join(coach_names)}")
        success = run_query(client, args.model, i + 1, total, filename, prompt)

        if not success:
            print(f"  Batch {i + 1} failed. Continuing with remaining batches...")

    print(f"\n{'=' * 60}")
    print("Verification complete!")
    print(f"Results saved to: {OUTPUT_DIR}")
    print(f"Run 'python verify_coaches.py --report' to scan for issues.")


if __name__ == "__main__":
    main()
