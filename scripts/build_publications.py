#!/usr/bin/env python3
"""
build_publications.py
Parses static/publications.bib into data/publications.json for Hugo.
"""

import json
import os
import re
from pathlib import Path

CATEGORY_ORDER = [
    "Books",
    "Book Chapters",
    "Proceedings",
    "Patents",
    "Journal Articles",
    "Conference Papers",
    "Special Issues",
    "Theses",
]

def clean_latex(text: str) -> str:
    if not text:
        return ""
    # Common LaTeX replacements
    replacements = [
        (r'\\\"{a}', 'ä'), (r'\\\"{o}', 'ö'), (r'\\\"{u}', 'ü'),
        (r'\\\"{A}', 'Ä'), (r'\\\"{O}', 'Ö'), (r'\\\"{U}', 'Ü'),
        (r"\\'{a}", 'á'), (r"\\'{e}", 'é'), (r"\\'{i}", 'í'),
        (r"\\'{o}", 'ó'), (r"\\'{u}", 'ú'), (r"\\'{A}", 'Á'),
        (r"\\'{E}", 'É'), (r"\\'{I}", 'Í'), (r"\\'{O}", 'Ó'),
        (r"\\'{U}", 'Ú'), (r"\\~{n}", 'ñ'), (r"\\~{N}", 'Ñ'),
        (r"\\~{a}", 'ã'), (r"\\~{o}", 'õ'),
        (r"\\&", '&'), (r"\\%", '%'), (r"\\$", '$'),
        (r"\\_", '_'), (r"\\#", '#'),
        (r"\{", ""), (r"\}", ""),
    ]
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)
    return text.strip()

def parse_fields(raw_fields: str) -> dict:
    fields = {}
    # Matches key = {value} or key = "value"
    pattern = r'(\w+)\s*=\s*[\"{](.*?)[\"}],?\n'
    for k, v in re.findall(pattern, raw_fields + '\n', re.DOTALL):
        fields[k.lower()] = clean_latex(v)
    return fields

def format_authors(author_str: str) -> str:
    if not author_str:
        return ""
    authors = [a.strip() for a in author_str.split(" and ") if a.strip()]
    if not authors:
        return ""
    
    formatted = []
    for a in authors:
        is_me = any(n in a for n in ["Pena-Rios", "Peña-Rios", "Pena Rios", "Peña Rios"])
        if is_me:
            formatted.append(f"<strong>{a}</strong>")
        else:
            formatted.append(a)
            
    if len(formatted) == 1:
        return formatted[0]
    elif len(formatted) == 2:
        return f"{formatted[0]}, & {formatted[1]}"
    else:
        return ", ".join(formatted[:-1]) + f", & {formatted[-1]}"

def determine_category(etype: str, fields: dict) -> str:
    title = fields.get("title", "").lower()
    note = fields.get("note", "").lower()
    if etype == "book":
        return "Books"
    elif etype == "incollection":
        return "Book Chapters"
    elif etype == "proceedings":
        return "Proceedings"
    elif etype == "patent":
        return "Patents"
    elif etype in ["phdthesis", "mastersthesis"]:
        return "Theses"
    elif etype == "inproceedings":
        return "Conference Papers"
    elif etype == "article":
        if "special issue" in title or "special issue" in note:
            return "Special Issues"
        return "Journal Articles"
    return "Other Publications"

def build_citation(entry: dict) -> str:
    etype = entry["entry_type"]
    fields = entry["fields"]
    cat = entry["category"]
    authors = format_authors(fields.get("author", ""))
    editors = format_authors(fields.get("editor", ""))
    year = fields.get("year", "")
    title = fields.get("title", "")
    pub = fields.get("publisher", "")
    journal = fields.get("journal", "")
    booktitle = fields.get("booktitle", "")
    volume = fields.get("volume", "")
    number = fields.get("number", fields.get("issue", ""))
    pages = fields.get("pages", "")
    doi = fields.get("doi", "")
    url = fields.get("url", "")
    number_pat = fields.get("number", fields.get("patentnumber", ""))

    if cat == "Proceedings":
        lead = editors if editors else authors
        return f"{lead} (Eds.). ({year}). <em>{title}</em>. {pub}."

    elif cat == "Patents":
        pat_num = f" (Patent No. {number_pat})" if number_pat else ""
        pub_str = f" {pub}." if pub else " Google Patents."
        return f"{authors}. ({year}). <em>{title}</em>{pat_num}.{pub_str}"

    elif cat == "Special Issues":
        lead = authors if authors else editors
        return f"{lead} (Guest Eds.). ({year}). {title} [Special issue]. <em>{journal}</em>."

    elif cat == "Journal Articles":
        vol_issue = ""
        if volume and number:
            vol_issue = f", <em>{volume}</em>({number})"
        elif volume:
            vol_issue = f", <em>{volume}</em>"
        pages_str = f", {pages}" if pages else ""
        return f"{authors}. ({year}). {title}. <em>{journal}</em>{vol_issue}{pages_str}."

    elif cat == "Conference Papers":
        pages_str = f" (pp. {pages})" if pages else ""
        pub_str = f" {pub}." if pub else ""
        return f"{authors}. ({year}). {title}. In <em>{booktitle}</em>{pages_str}.{pub_str}"

    elif cat == "Books":
        return f"{authors}. ({year}). <em>{title}</em>. {pub}."

    elif cat == "Book Chapters":
        pages_str = f" (pp. {pages})" if pages else ""
        pub_str = f" {pub}." if pub else ""
        in_lead = f" In {editors} (Eds.)," if editors else " In"
        return f"{authors}. ({year}). {title}.{in_lead} <em>{booktitle}</em>{pages_str}.{pub_str}"

    elif cat == "Theses":
        degree = "Doctoral dissertation" if etype == "phdthesis" else "Master's thesis"
        school = fields.get("school", "")
        school_str = f", {school}" if school else ""
        return f"{authors}. ({year}). <em>{title}</em> [{degree}{school_str}]."

    # Default fallback
    return f"{authors}. ({year}). {title}. <em>{journal or booktitle or pub}</em>."

def main():
    root = Path(__file__).resolve().parent.parent
    bib_file = root / "static" / "publications.bib"
    output_file = root / "data" / "publications.json"

    if not bib_file.exists():
        print(f"Error: {bib_file} does not exist!")
        return

    print(f"Reading BibTeX from: {bib_file}")
    with open(bib_file, "r", encoding="utf-8") as f:
        text = f.read()

    pattern = r'@(\w+)\s*\{\s*([^,]+),\s*(.*?)\n\}'
    matches = re.findall(pattern, text, re.DOTALL)

    entries = []
    for entry_type, key, raw_fields in matches:
        key = key.strip()
        etype = entry_type.lower()
        fields = parse_fields(raw_fields)
        cat = determine_category(etype, fields)
        
        # Build clean raw BibTeX snippet
        raw_bib_lines = [f"@{etype}{{{key},"]
        for fk, fv in fields.items():
            raw_bib_lines.append(f"  {fk} = {{{fv}}},")
        raw_bib_lines.append("}")
        raw_bib = "\n".join(raw_bib_lines)

        entry_obj = {
            "key": key,
            "entry_type": etype,
            "category": cat,
            "fields": fields,
            "year": int(fields.get("year", 0)),
            "title": fields.get("title", ""),
            "author": fields.get("author", ""),
            "doi": fields.get("doi", ""),
            "doi_url": f"https://doi.org/{fields.get('doi')}" if fields.get("doi") else "",
            "url": fields.get("url", ""),
            "raw_bib": raw_bib,
        }
        entry_obj["citation_html"] = build_citation(entry_obj)
        entries.append(entry_obj)

    # Sort entries by year descending
    entries.sort(key=lambda x: x["year"], reverse=True)

    # Group by Year
    years_dict = {}
    for entry in entries:
        y = entry["year"]
        if y not in years_dict:
            years_dict[y] = {}
        cat = entry["category"]
        if cat not in years_dict[y]:
            years_dict[y][cat] = []
        years_dict[y][cat].append(entry)

    years_list = []
    for y in sorted(years_dict.keys(), reverse=True):
        cats_list = []
        for cat in CATEGORY_ORDER:
            if cat in years_dict[y]:
                cats_list.append({
                    "name": cat,
                    "count": len(years_dict[y][cat]),
                    "entries": years_dict[y][cat]
                })
        # Add any other categories not in CATEGORY_ORDER
        for cat, items in years_dict[y].items():
            if cat not in CATEGORY_ORDER:
                cats_list.append({
                    "name": cat,
                    "count": len(items),
                    "entries": items
                })
        years_list.append({
            "year": y,
            "count": sum(c["count"] for c in cats_list),
            "categories": cats_list
        })

    data = {
        "summary": {
            "total_publications": len(entries),
            "years_count": len(years_list),
            "latest_year": years_list[0]["year"] if years_list else 0,
            "earliest_year": years_list[-1]["year"] if years_list else 0,
        },
        "years": years_list,
        "all": entries,
    }

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Successfully parsed {len(entries)} publications into {output_file}")
    for y_info in years_list:
        print(f"  Year {y_info['year']}: {y_info['count']} publications across {len(y_info['categories'])} categories")

if __name__ == "__main__":
    main()
