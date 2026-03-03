#!/usr/bin/env python3
"""BTEB Stats Updater

Fetches live stats from bteb.anbuinfosec.dev and updates README.md + chart.svg.
Runs every 30 minutes via GitHub Actions.
"""

import json
import re
import urllib.request
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

API_URL = "https://bteb.anbuinfosec.dev/api/stats/public"
DHAKA_TZ = ZoneInfo("Asia/Dhaka")


def fetch_data() -> dict:
    with urllib.request.urlopen(API_URL, timeout=15) as resp:
        return json.loads(resp.read())["data"]


def fmt_num(n: int) -> str:
    return f"{n:,}"


def fmt_date(iso: str) -> str:
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    dt_dhaka = dt.astimezone(DHAKA_TZ)
    return dt_dhaka.strftime("%-d %B %Y, %-I:%M %p BST")


def build_table(d: dict) -> str:
    connected = "Yes" if d["connected"] else "No"
    return (
        "| Metric | Value |\n"
        "|--------|--------|\n"
        f"| Database Connected | {connected} |\n"
        f"| Total Students | {fmt_num(d['studentCount'])} |\n"
        f"| Total Institutes | {fmt_num(d['instituteCount'])} |\n"
        f"| Total Passed | {fmt_num(d['passCount'])} |\n"
        f"| Total Referred | {fmt_num(d['refCount'])} |\n"
        f"| Pass Percentage | {d['passPercentage']}% |\n"
        f"| Refer Percentage | {d['refPercentage']}% |\n"
        f"| Last Result Published | {fmt_date(d['lastResultPublished'])} |"
    )


def build_api_section(d: dict) -> str:
    payload = {
        "success": True,
        "data": {
            "connected": d["connected"],
            "studentCount": d["studentCount"],
            "instituteCount": d["instituteCount"],
            "passCount": d["passCount"],
            "refCount": d["refCount"],
            "passPercentage": d["passPercentage"],
            "refPercentage": d["refPercentage"],
            "lastResultPublished": d["lastResultPublished"],
        },
    }
    json_str = json.dumps(payload, indent=2)
    return (
        "### GET /api/stats/public\n\n"
        "Returns aggregated public statistics.\n\n"
        "**Response:**\n\n"
        "```json\n"
        f"{json_str}\n"
        "```"
    )


def build_svg(d: dict) -> str:
    MAX_H = 200
    BASE_Y = 280
    max_count = d["studentCount"]

    def bar(val, max_val):
        h = max(1, round(val / max_val * MAX_H))
        return BASE_Y - h, h

    # Count bars (left panel)
    s_y, s_h = BASE_Y - MAX_H, MAX_H
    p_y, p_h = bar(d["passCount"], max_count)
    r_y, r_h = bar(d["refCount"], max_count)

    # Percentage bars (right panel)
    pp_y, pp_h = bar(d["passPercentage"], 100)
    rp_y, rp_h = bar(d["refPercentage"], 100)

    today = datetime.now(DHAKA_TZ).strftime("%-d %B %Y")

    s_label  = fmt_num(d["studentCount"])
    p_label  = fmt_num(d["passCount"])
    r_label  = fmt_num(d["refCount"])
    pp_label = str(d["passPercentage"]) + "%"
    rp_label = str(d["refPercentage"]) + "%"
    inst_label = fmt_num(d["instituteCount"])

    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="700" height="340" viewBox="0 0 700 340">',
        '  <rect width="700" height="340" fill="#0d1117" rx="12"/>',
        f'  <text x="350" y="32" text-anchor="middle" fill="#e6edf3" font-family="\'Segoe UI\',Arial,sans-serif" font-size="15" font-weight="bold">BTEB Public Stats</text>',
        f'  <text x="350" y="50" text-anchor="middle" fill="#8b949e" font-family="\'Segoe UI\',Arial,sans-serif" font-size="11">Last updated: {today}</text>',
        '  <line x1="20" y1="62" x2="680" y2="62" stroke="#21262d" stroke-width="1"/>',
        '  <text x="185" y="82" text-anchor="middle" fill="#8b949e" font-family="\'Segoe UI\',Arial,sans-serif" font-size="11">Student Counts</text>',
        '  <text x="535" y="82" text-anchor="middle" fill="#8b949e" font-family="\'Segoe UI\',Arial,sans-serif" font-size="11">Result Percentages</text>',
        '  <line x1="375" y1="70" x2="375" y2="290" stroke="#21262d" stroke-width="1"/>',
        '  <line x1="35" y1="280" x2="355" y2="280" stroke="#30363d" stroke-width="1"/>',
        '  <line x1="395" y1="280" x2="665" y2="280" stroke="#30363d" stroke-width="1"/>',
        # Students bar
        f'  <rect x="50" y="{s_y}" width="80" height="{s_h}" fill="#1f6feb" rx="4"/>',
        f'  <text x="90" y="{s_y - 6}" text-anchor="middle" fill="#79c0ff" font-family="\'Segoe UI\',Arial,sans-serif" font-size="10" font-weight="bold">{s_label}</text>',
        '  <text x="90" y="297" text-anchor="middle" fill="#8b949e" font-family="\'Segoe UI\',Arial,sans-serif" font-size="10">Students</text>',
        # Passed bar
        f'  <rect x="158" y="{p_y}" width="80" height="{p_h}" fill="#3fb950" rx="4"/>',
        f'  <text x="198" y="{p_y - 6}" text-anchor="middle" fill="#56d364" font-family="\'Segoe UI\',Arial,sans-serif" font-size="10" font-weight="bold">{p_label}</text>',
        '  <text x="198" y="297" text-anchor="middle" fill="#8b949e" font-family="\'Segoe UI\',Arial,sans-serif" font-size="10">Passed</text>',
        # Referred bar
        f'  <rect x="265" y="{r_y}" width="80" height="{r_h}" fill="#f85149" rx="4"/>',
        f'  <text x="305" y="{r_y - 6}" text-anchor="middle" fill="#ff7b72" font-family="\'Segoe UI\',Arial,sans-serif" font-size="10" font-weight="bold">{r_label}</text>',
        '  <text x="305" y="297" text-anchor="middle" fill="#8b949e" font-family="\'Segoe UI\',Arial,sans-serif" font-size="10">Referred</text>',
        # Pass % bar
        f'  <rect x="418" y="{pp_y}" width="90" height="{pp_h}" fill="#3fb950" rx="4"/>',
        f'  <text x="463" y="{pp_y - 6}" text-anchor="middle" fill="#56d364" font-family="\'Segoe UI\',Arial,sans-serif" font-size="11" font-weight="bold">{pp_label}</text>',
        '  <text x="463" y="297" text-anchor="middle" fill="#8b949e" font-family="\'Segoe UI\',Arial,sans-serif" font-size="10">Pass Rate</text>',
        # Refer % bar
        f'  <rect x="548" y="{rp_y}" width="90" height="{rp_h}" fill="#d29922" rx="4"/>',
        f'  <text x="593" y="{rp_y - 6}" text-anchor="middle" fill="#e3b341" font-family="\'Segoe UI\',Arial,sans-serif" font-size="11" font-weight="bold">{rp_label}</text>',
        '  <text x="593" y="297" text-anchor="middle" fill="#8b949e" font-family="\'Segoe UI\',Arial,sans-serif" font-size="10">Refer Rate</text>',
        # Footer
        '  <rect x="20" y="310" width="660" height="22" fill="#161b22" rx="4"/>',
        f'  <text x="350" y="325" text-anchor="middle" fill="#8b949e" font-family="\'Segoe UI\',Arial,sans-serif" font-size="10">Institutes: {inst_label} \u00b7 DB: Connected \u2713 \u00b7 Auto-updated every 30 min \u00b7 bteb.anbuinfosec.dev</text>',
        '</svg>',
    ]
    return "\n".join(lines) + "\n"


def replace_section(content: str, tag: str, new_body: str) -> str:
    pattern = rf"(<!-- {tag}:START -->).*?(<!-- {tag}:END -->)"
    replacement = rf"\1\n{new_body}\n\2"
    return re.sub(pattern, replacement, content, flags=re.DOTALL)


def main():
    print("Fetching data from API...")
    data = fetch_data()
    print(f"  studentCount   : {data['studentCount']}")
    print(f"  passCount      : {data['passCount']}")
    print(f"  refCount       : {data['refCount']}")
    print(f"  passPercentage : {data['passPercentage']}%")
    print(f"  refPercentage  : {data['refPercentage']}%")

    table       = build_table(data)
    api_section = build_api_section(data)
    svg         = build_svg(data)

    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    readme = replace_section(readme, "STATS", table)
    readme = replace_section(readme, "API",   api_section)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    with open("chart.svg", "w", encoding="utf-8") as f:
        f.write(svg)

    print("\u2705 README.md and chart.svg updated successfully.")


if __name__ == "__main__":
    main()
