
from collections import Counter
from pathlib import Path
from datetime import datetime

from src.entity_resolution.entity_store import get_all_entities
from src.entity_resolution.resolver import find_duplicate_candidates


def run_analysis():
    entities = get_all_entities()

    total = len(entities)
    type_counts = Counter(
        (entity.get("entity_type") or "UNKNOWN").upper()
        for entity in entities
    )
    source_counts = Counter(
        entity.get("source_url") or "Unknown"
        for entity in entities
    )

    duplicate_candidates = find_duplicate_candidates(
        entities, threshold=0.88
    )

    unique_names = len({
        (entity.get("name") or "").strip().lower()
        for entity in entities
    })

    report = []
    report.append("# AI Intelligence Analysis Report")
    report.append("")
    report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("")
    report.append("## Executive Summary")
    report.append("")
    report.append(
        f"The knowledge base currently contains **{total} entity records**, "
        f"representing approximately **{unique_names} unique normalized names**."
    )
    report.append("")
    report.append("## Entity Statistics")
    report.append("")
    report.append(f"- Total records: {total}")
    report.append(f"- Unique normalized names: {unique_names}")
    report.append(f"- Duplicate candidate pairs: {len(duplicate_candidates)}")
    report.append("")
    report.append("### Entity Type Distribution")
    report.append("")
    for entity_type, count in type_counts.most_common():
        report.append(f"- **{entity_type}:** {count}")

    report.append("")
    report.append("### Source Coverage")
    report.append("")
    for source, count in source_counts.most_common():
        report.append(f"- {source}: {count} entities")

    report.append("")
    report.append("### Duplicate Candidates")
    report.append("")
    if duplicate_candidates:
        for candidate in duplicate_candidates:
            report.append(
                f"- **{candidate['entity_1']}** ↔ "
                f"**{candidate['entity_2']}** "
                f"(similarity: {candidate['similarity']}) "
                f"[{candidate['type']}] — review required"
            )
    else:
        report.append("No duplicate candidates detected.")

    report.append("")
    report.append("## Top Entity Records")
    report.append("")
    for entity in entities[:15]:
        name = entity.get("name", "Unnamed")
        entity_type = entity.get("entity_type", "UNKNOWN")
        description = entity.get("description") or "No description available"
        report.append(f"- **{name}** ({entity_type}): {description}")

    report.append("")
    report.append("## Limitations")
    report.append("")
    report.append("- Entity quality depends on the source content and LLM extraction.")
    report.append("- Duplicate candidates require human review before merging.")
    report.append("- Current analysis is based on stored entities, not live web monitoring.")
    report.append("- Entity statistics may include multiple records from different sources.")

    report.append("")
    report.append("## Future Work")
    report.append("")
    report.append("- Automated duplicate consolidation with review controls.")
    report.append("- Multi-source intelligence correlation.")
    report.append("- Temporal trend and entity relationship analysis.")
    report.append("- Dashboard visualization and API access.")

    output_dir = Path("reports")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "intelligence_analysis.md"

    output_file.write_text("\n".join(report), encoding="utf-8")

    print("=" * 60)
    print("INTELLIGENCE ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"Total entities: {total}")
    print(f"Unique normalized names: {unique_names}")
    print(f"Duplicate candidate pairs: {len(duplicate_candidates)}")
    print(f"Entity types: {dict(type_counts)}")
    print(f"Report saved to: {output_file}")
    print("=" * 60)


if __name__ == "__main__":
    run_analysis()
