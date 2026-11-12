#!/usr/bin/env python3
"""
build_publications.py
Parses static/publications.bib (BibLaTeX format) into data/publications.json for Hugo.
Supports multiple citation styles: APA, IEEE, Harvard, ACM, and Chicago.
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
    "Reports",
    "Other Publications",
]

def clean_latex(text: str) -> str:
    if not text:
        return ""
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
        (r"--", "–"),
    ]
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)
    return text.strip()

def parse_fields(raw_fields: str) -> dict:
    fields = {}
    pattern = r'(\w+)\s*=\s*[\"{](.*?)[\"}],?\n'
    for k, v in re.findall(pattern, raw_fields + '\n', re.DOTALL):
        fields[k.lower()] = clean_latex(v)
    return fields

def extract_year(fields: dict) -> int:
    date_val = fields.get("date", "").strip()
    if date_val:
        m = re.match(r"^(\d{4})", date_val)
        if m:
            return int(m.group(1))
    year_val = fields.get("year", "").strip()
    if year_val:
        m = re.match(r"^(\d{4})", year_val)
        if m:
            return int(m.group(1))
    return 0

def get_full_title(fields: dict) -> str:
    title = fields.get("title", "").strip()
    subtitle = fields.get("subtitle", "").strip()
    if subtitle and title:
        if title.endswith((".", ":", "?", "!")):
            return f"{title} {subtitle}"
        return f"{title}: {subtitle}"
    return title or subtitle

def split_author(a: str):
    a = a.strip()
    if not a:
        return ("", "", False)
    is_me = any(n in a for n in ["Pena-Rios", "Peña-Rios", "Pena Rios", "Peña Rios"])
    if "," in a:
        parts = [p.strip() for p in a.split(",", 1)]
        last = parts[0]
        first_or_inits = parts[1]
    else:
        parts = a.split()
        last = parts[-1] if len(parts) > 1 else parts[0]
        first_or_inits = " ".join(parts[:-1]) if len(parts) > 1 else ""
    tokens = first_or_inits.split()
    parts_inits = []
    for chunk in tokens:
        if "-" in chunk:
            sub = [f"{s[0]}." for s in chunk.split("-") if s and s[0].isalpha()]
            parts_inits.append("-".join(sub))
        else:
            clean = "".join(c for c in chunk if c.isalpha())
            if clean:
                parts_inits.append(f"{clean[0]}.")
    inits = " ".join(parts_inits)
    return (last, inits, is_me)

def format_author_list(raw_author_str: str, style: str) -> str:
    if not raw_author_str:
        return ""
    authors = [a.strip() for a in raw_author_str.split(" and ") if a.strip()]
    if not authors:
        return ""

    parsed = [split_author(a) for a in authors]

    def render_name(last, inits, is_me):
        if style == "ieee":
            full = f"{inits} {last}".strip() if inits else last
        else:
            full = f"{last}, {inits}".strip().rstrip(",") if inits else last
        return f"<strong>{full}</strong>" if is_me else full

    names = [render_name(l, i, me) for l, i, me in parsed]

    if len(names) == 1:
        return names[0]
    elif len(names) == 2:
        if style == "apa":
            return f"{names[0]}, & {names[1]}"
        elif style == "harvard":
            return f"{names[0]} and {names[1]}"
        else:
            return f"{names[0]} and {names[1]}"
    else:
        if style == "apa":
            return ", ".join(names[:-1]) + f", & {names[-1]}"
        elif style == "harvard":
            return ", ".join(names[:-1]) + f" and {names[-1]}"
        else:
            return ", ".join(names[:-1]) + f", and {names[-1]}"

def punct(text: str, p: str = ".") -> str:
    text = text.strip()
    if not text:
        return ""
    clean = re.sub(r"<[^>]+>", "", text).strip()
    if clean.endswith((".", "?", "!", ":", ";", ",")):
        return text
    return f"{text}{p}"

def determine_category(etype: str, fields: dict) -> str:
    title = fields.get("title", "").lower()
    note = fields.get("note", "").lower()

    if etype == "book":
        return "Books"
    elif etype in ["incollection", "inbook"]:
        return "Book Chapters"
    elif etype == "proceedings":
        return "Proceedings"
    elif etype == "patent":
        return "Patents"
    elif etype in ["phdthesis", "mastersthesis"] or etype == "thesis":
        return "Theses"
    elif etype in ["inproceedings", "conference"]:
        return "Conference Papers"
    elif etype in ["article", "periodical"]:
        if "special issue" in title or "special issue" in note:
            return "Special Issues"
        return "Journal Articles"
    elif etype in ["report", "techreport"]:
        return "Reports"
    return "Other Publications"

def build_all_citations(entry_obj: dict) -> dict:
    etype = entry_obj["entry_type"]
    fields = entry_obj["fields"]
    cat = entry_obj["category"]

    raw_author = fields.get("author", "")
    raw_editor = fields.get("editor", "")
    raw_holder = fields.get("holder", "")

    year_int = entry_obj.get("year", 0)
    year = str(year_int) if year_int else (fields.get("year") or fields.get("date", ""))

    title = get_full_title(fields).rstrip(".")
    pub = fields.get("publisher", fields.get("institution", fields.get("organization", ""))).rstrip(".")
    journal = fields.get("journaltitle", fields.get("journal", "")).rstrip(".")
    booktitle = fields.get("booktitle", fields.get("eventtitle", fields.get("maintitle", ""))).rstrip(".")
    volume = fields.get("volume", "")
    number = fields.get("number", fields.get("issue", ""))
    pages = fields.get("pages", fields.get("eid", ""))

    number_pat = fields.get("number", fields.get("patentnumber", ""))
    location = fields.get("location", fields.get("nationality", fields.get("address", ""))).rstrip(".")

    thesistype = fields.get("type", "").lower()
    if "master" in thesistype or etype == "mastersthesis":
        degree_apa = "Master's thesis"
        degree_ieee = "Master's thesis"
    elif "doctor" in thesistype or "phd" in thesistype or etype == "phdthesis":
        degree_apa = "Doctoral dissertation"
        degree_ieee = "Ph.D. dissertation"
    elif fields.get("type"):
        degree_apa = fields.get("type")
        degree_ieee = fields.get("type")
    else:
        degree_apa = "Doctoral dissertation"
        degree_ieee = "Ph.D. dissertation"
    school = fields.get("institution", fields.get("school", "")).rstrip(".")

    citations = {}
    for style in ["apa", "ieee", "harvard", "acm", "chicago"]:
        authors = format_author_list(raw_author, style)
        editors = format_author_list(raw_editor, style)
        holders = format_author_list(raw_holder, style)

        # ------------------- 1. APA (7th) -------------------
        if style == "apa":
            a_dot = punct(authors) if authors else ""
            if cat == "Proceedings":
                lead = punct(editors) if editors else a_dot
                citations["apa"] = f"{lead} (Eds.). ({year}). <em>{title}</em>. {pub}."
            elif cat == "Patents":
                lead = a_dot if a_dot else (punct(holders) if holders else "<strong>Peña-Rios, A.</strong>.")
                pat_str = f" (Patent No. {number_pat})" if number_pat else ""
                loc_str = f" {location}." if location else (f" {pub}." if pub else " Google Patents.")
                citations["apa"] = f"{lead} ({year}). <em>{title}</em>{pat_str}.{loc_str}"
            elif cat == "Special Issues":
                lead = a_dot if a_dot else (punct(editors) if editors else "")
                citations["apa"] = f"{lead} (Guest Eds.). ({year}). {title} [Special issue]. <em>{journal}</em>."
            elif cat == "Journal Articles":
                vi = f", <em>{volume}</em>({number})" if (volume and number) else (f", <em>{volume}</em>" if volume else "")
                pg = f", {pages}" if pages else ""
                citations["apa"] = f"{a_dot} ({year}). {title}. <em>{journal}</em>{vi}{pg}."
            elif cat == "Conference Papers":
                pg = f" (pp. {pages})" if pages else ""
                pb = f" {pub}." if pub else ""
                citations["apa"] = f"{a_dot} ({year}). {title}. In <em>{booktitle}</em>{pg}.{pb}"
            elif cat == "Books":
                citations["apa"] = f"{a_dot} ({year}). <em>{title}</em>. {pub}."
            elif cat == "Book Chapters":
                pg = f" (pp. {pages})" if pages else ""
                pb = f" {pub}." if pub else ""
                in_lead = f" In {editors} (Eds.)," if editors else " In"
                citations["apa"] = f"{a_dot} ({year}). {title}.{in_lead} <em>{booktitle}</em>{pg}.{pb}"
            elif cat == "Theses":
                sc = f", {school}" if school else ""
                citations["apa"] = f"{a_dot} ({year}). <em>{title}</em> [{degree_apa}{sc}]."
            elif cat == "Reports":
                pb = f" {pub}." if pub else ""
                citations["apa"] = f"{a_dot} ({year}). <em>{title}</em> [Technical report].{pb}"
            else:
                v = journal or booktitle or pub
                v_str = f" <em>{v}</em>." if v else ""
                citations["apa"] = f"{a_dot} ({year}). {title}.{v_str}"

        # ------------------- 2. IEEE -------------------
        elif style == "ieee":
            if cat == "Proceedings":
                lead = editors if editors else authors
                citations["ieee"] = f"{lead}, Eds., <em>{title}</em>. {pub}, {year}."
            elif cat == "Patents":
                lead = authors if authors else (holders if holders else "<strong>A. Peña-Rios</strong>")
                citations["ieee"] = f'{lead}, "{title}," {location} Patent {number_pat}, {year}.'
            elif cat == "Special Issues":
                lead = editors if editors else authors
                citations["ieee"] = f'{lead}, Guest Eds., "{title}," <em>{journal}</em>, {year}.'
            elif cat == "Journal Articles":
                vi = f", vol. {volume}" if volume else ""
                no = f", no. {number}" if number else ""
                pg = f", pp. {pages}" if pages else ""
                citations["ieee"] = f'{authors}, "{title}," <em>{journal}</em>{vi}{no}{pg}, {year}.'
            elif cat == "Conference Papers":
                pg = f", pp. {pages}" if pages else ""
                pb = f", {pub}" if pub else ""
                citations["ieee"] = f'{authors}, "{title}," in <em>{booktitle}</em>{pb}, {year}{pg}.'
            elif cat == "Books":
                citations["ieee"] = f"{authors}, <em>{title}</em>. {pub}, {year}."
            elif cat == "Book Chapters":
                ed = f", {editors}, Eds." if editors else ""
                pg = f", pp. {pages}" if pages else ""
                pb = f", {pub}" if pub else ""
                citations["ieee"] = f'{authors}, "{title}," in <em>{booktitle}</em>{ed}{pb}, {year}{pg}.'
            elif cat == "Theses":
                citations["ieee"] = f'{authors}, "{title}," {degree_ieee}, {school}, {year}.'
            elif cat == "Reports":
                citations["ieee"] = f'{authors}, "{title}," Tech. Rep., {pub}, {year}.'
            else:
                v = journal or booktitle or pub
                v_str = f", <em>{v}</em>" if v else ""
                citations["ieee"] = f'{authors}, "{title}"{v_str}, {year}.'

        # ------------------- 3. Harvard -------------------
        elif style == "harvard":
            if cat == "Proceedings":
                lead = editors if editors else authors
                citations["harvard"] = f"{lead} (eds.) ({year}) <em>{title}</em>. {pub}."
            elif cat == "Patents":
                lead = authors if authors else (holders if holders else "<strong>Peña-Rios, A.</strong>")
                citations["harvard"] = f"{lead} ({year}) <em>{title}</em>. {location} Patent {number_pat}."
            elif cat == "Special Issues":
                lead = editors if editors else authors
                citations["harvard"] = f"{lead} (Guest eds.) ({year}) '{title}', <em>{journal}</em> [Special issue]."
            elif cat == "Journal Articles":
                vi = f", {volume}" if volume else ""
                no = f"({number})" if number else ""
                pg = f", pp. {pages}" if pages else ""
                citations["harvard"] = f"{authors} ({year}) '{title}', <em>{journal}</em>{vi}{no}{pg}."
            elif cat == "Conference Papers":
                pg = f", pp. {pages}" if pages else ""
                pb = f". {pub}" if pub else ""
                citations["harvard"] = f"{authors} ({year}) '{title}', in <em>{booktitle}</em>{pb}{pg}."
            elif cat == "Books":
                citations["harvard"] = f"{authors} ({year}) <em>{title}</em>. {pub}."
            elif cat == "Book Chapters":
                ed = f" in {editors} (eds.)" if editors else " in"
                pg = f", pp. {pages}" if pages else ""
                pb = f". {pub}" if pub else ""
                citations["harvard"] = f"{authors} ({year}) '{title}',{ed} <em>{booktitle}</em>{pb}{pg}."
            elif cat == "Theses":
                citations["harvard"] = f"{authors} ({year}) <em>{title}</em>. {degree_apa}, {school}."
            elif cat == "Reports":
                citations["harvard"] = f"{authors} ({year}) <em>{title}</em>. Technical Report. {pub}."
            else:
                v = journal or booktitle or pub
                v_str = f", <em>{v}</em>" if v else ""
                citations["harvard"] = f"{authors} ({year}) '{title}'{v_str}."

        # ------------------- 4. ACM -------------------
        elif style == "acm":
            a_dot = punct(authors) if authors else ""
            if cat == "Proceedings":
                lead = punct(editors) if editors else a_dot
                citations["acm"] = f"{lead} (Eds.). {year}. <em>{title}</em>. {pub}."
            elif cat == "Patents":
                lead = a_dot if a_dot else (punct(holders) if holders else "<strong>Peña-Rios, A.</strong>.")
                citations["acm"] = f"{lead} {year}. {title}. {location} Patent {number_pat}."
            elif cat == "Special Issues":
                lead = punct(editors) if editors else a_dot
                citations["acm"] = f"{lead} (Eds.). {year}. {title}. <em>{journal}</em>."
            elif cat == "Journal Articles":
                vi = f" {volume}" if volume else ""
                no = f", {number}" if number else ""
                pg = f", {pages}" if pages else ""
                citations["acm"] = f"{a_dot} {year}. {title}. <em>{journal}</em>{vi}{no} ({year}){pg}."
            elif cat == "Conference Papers":
                pg = f", {pages}" if pages else ""
                pb = f", {pub}" if pub else ""
                citations["acm"] = f"{a_dot} {year}. {title}. In <em>{booktitle}</em>{pb}{pg}."
            elif cat == "Books":
                citations["acm"] = f"{a_dot} {year}. <em>{title}</em>. {pub}."
            elif cat == "Book Chapters":
                ed = f", {editors} (Eds.)" if editors else ""
                pg = f", {pages}" if pages else ""
                pb = f", {pub}" if pub else ""
                citations["acm"] = f"{a_dot} {year}. {title}. In <em>{booktitle}</em>{ed}{pb}{pg}."
            elif cat == "Theses":
                citations["acm"] = f"{a_dot} {year}. <em>{title}</em>. {degree_apa}. {school}."
            elif cat == "Reports":
                citations["acm"] = f"{a_dot} {year}. <em>{title}</em>. Technical Report. {pub}."
            else:
                v = journal or booktitle or pub
                v_str = f" <em>{v}</em>." if v else ""
                citations["acm"] = f"{a_dot} {year}. {title}.{v_str}"

        # ------------------- 5. Chicago -------------------
        elif style == "chicago":
            a_dot = punct(authors) if authors else ""
            if cat == "Proceedings":
                lead = editors if editors else authors
                citations["chicago"] = f"{lead}, eds. {year}. <em>{title}</em>. {pub}."
            elif cat == "Patents":
                lead = a_dot if a_dot else (punct(holders) if holders else "<strong>Peña-Rios, A.</strong>.")
                citations["chicago"] = f'{lead} {year}. <em>{title}</em>. {location} Patent {number_pat}.'
            elif cat == "Special Issues":
                lead = editors if editors else authors
                citations["chicago"] = f'{lead}, eds. {year}. "{title}." <em>{journal}</em>.'
            elif cat == "Journal Articles":
                vi = f" {volume}" if volume else ""
                no = f" ({number})" if number else ""
                pg = f": {pages}" if pages else ""
                citations["chicago"] = f'{a_dot} {year}. "{title}." <em>{journal}</em>{vi}{no}{pg}.'
            elif cat == "Conference Papers":
                pg = f", {pages}" if pages else ""
                pb = f". {pub}" if pub else ""
                citations["chicago"] = f'{a_dot} {year}. "{title}." In <em>{booktitle}</em>{pg}{pb}.'
            elif cat == "Books":
                citations["chicago"] = f"{a_dot} {year}. <em>{title}</em>. {pub}."
            elif cat == "Book Chapters":
                ed = f", edited by {editors}" if editors else ""
                pg = f", {pages}" if pages else ""
                pb = f". {pub}" if pub else ""
                citations["chicago"] = f'{a_dot} {year}. "{title}." In <em>{booktitle}</em>{ed}{pg}{pb}.'
            elif cat == "Theses":
                citations["chicago"] = f'{a_dot} {year}. "{title}." {degree_apa}, {school}.'
            elif cat == "Reports":
                citations["chicago"] = f'{a_dot} {year}. "{title}." Technical Report. {pub}.'
            else:
                v = journal or booktitle or pub
                v_str = f" <em>{v}</em>." if v else ""
                citations["chicago"] = f'{a_dot} {year}. "{title}."{v_str}'

    return citations

def main():
    root = Path(__file__).resolve().parent.parent
    bib_file = root / "static" / "publications.bib"
    output_file = root / "data" / "publications.json"

    if not bib_file.exists():
        print(f"Error: {bib_file} does not exist!")
        return

    print(f"Reading BibLaTeX from: {bib_file}")
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
        year_num = extract_year(fields)

        # Build clean raw BibLaTeX snippet
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
            "year": year_num,
            "title": get_full_title(fields),
            "author": fields.get("author", fields.get("holder", "")),
            "doi": fields.get("doi", ""),
            "doi_url": f"https://doi.org/{fields.get('doi')}" if fields.get("doi") else "",
            "url": fields.get("url", ""),
            "raw_bib": raw_bib,
        }
        all_citations = build_all_citations(entry_obj)
        entry_obj["citations"] = all_citations
        entry_obj["citation_html"] = all_citations.get("apa", "")
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

    print(f"Successfully parsed {len(entries)} BibLaTeX publications with multi-style citations into {output_file}")
    for y_info in years_list:
        print(f"  Year {y_info['year']}: {y_info['count']} publications across {len(y_info['categories'])} categories")

if __name__ == "__main__":
    main()
