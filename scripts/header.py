#!/usr/bin/env python3
"""Render assets/header-{dark,light}.svg: a terminal that types `kubectl describe engineer andres`."""
from pathlib import Path
from xml.sax.saxutils import escape

COMMAND = "kubectl describe engineer andres"
FIELDS = [
    ("Name:", "Andrés García"),
    ("Role:", "Senior SRE / Platform Engineer"),
    ("Experience:", "9+ years · multi-cloud · multi-region · regulated"),
    ("Stack:", "AWS · GCP · Kubernetes · Terraform · ArgoCD · Go"),
    ("Location:", "Guadalajara, MX (UTC-6) · remote"),
]
STATUS = ("Status:", "Available — open to remote roles")

THEMES = {
    "dark": dict(bg="#0d1117", bar="#161b22", border="#30363d", text="#e6edf3", key="#8b949e",
                 prompt="#d2a8ff", cmd="#79c0ff", ok="#3fb950"),
    "light": dict(bg="#ffffff", bar="#f6f8fa", border="#d0d7de", text="#1f2328", key="#656d76",
                  prompt="#8250df", cmd="#0969da", ok="#1a7f37"),
}

W, FONT, CHAR, LINE, TOP = 900, 17, 10.3, 31, 86
TYPE_START, PER_CHAR = 0.6, 0.06


def render(t):
    type_end = TYPE_START + PER_CHAR * len(COMMAND)
    cmd_x = 62
    steps = ";".join(str(round(i * CHAR, 1)) for i in range(len(COMMAND) + 1))
    rows = FIELDS + [STATUS]
    height = TOP + LINE * (len(rows) + 1) + 18

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" '
        f'role="img" aria-label="Andrés García, Senior SRE / Platform Engineer, available for remote roles">',
        f'<style>text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;font-size:{FONT}px}}</style>',
        f'<rect x="1" y="1" width="{W - 2}" height="{height - 2}" rx="12" fill="{t["bg"]}" stroke="{t["border"]}"/>',
        f'<path d="M1 44V13a12 12 0 0 1 12-12h{W - 26}a12 12 0 0 1 12 12v31z" fill="{t["bar"]}"/>',
        f'<line x1="1" y1="44" x2="{W - 1}" y2="44" stroke="{t["border"]}"/>',
        '<circle cx="26" cy="23" r="6" fill="#ff5f57"/><circle cx="46" cy="23" r="6" fill="#febc2e"/>'
        '<circle cx="66" cy="23" r="6" fill="#28c840"/>',
        f'<text x="{W / 2}" y="28" text-anchor="middle" fill="{t["key"]}" style="font-size:14px">andres@platform: ~</text>',
        f'<clipPath id="typed"><rect x="{cmd_x}" y="{TOP - 20}" width="0" height="28">'
        f'<animate attributeName="width" values="{steps}" begin="{TYPE_START}s" dur="{type_end - TYPE_START}s" '
        f'calcMode="discrete" fill="freeze"/></rect></clipPath>',
        f'<text x="40" y="{TOP}" fill="{t["prompt"]}">$</text>',
        f'<text x="{cmd_x}" y="{TOP}" fill="{t["cmd"]}" clip-path="url(#typed)">{escape(COMMAND)}</text>',
    ]

    for i, (key, value) in enumerate(rows):
        y = TOP + LINE * (i + 1) + 6
        begin = type_end + 0.35 + i * 0.18
        is_status = (key, value) == STATUS
        value_x = 200
        line = [f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{begin:.2f}s" dur="0.25s" fill="freeze"/>',
                f'<text x="40" y="{y}" fill="{t["key"]}">{escape(key)}</text>']
        if is_status:
            line.append(f'<circle cx="{value_x + 6}" cy="{y - 6}" r="6" fill="{t["ok"]}">'
                        f'<animate attributeName="opacity" values="1;0.35;1" dur="2s" begin="{begin:.2f}s" repeatCount="indefinite"/></circle>')
            line.append(f'<text x="{value_x + 22}" y="{y}" fill="{t["ok"]}" font-weight="bold">{escape(value)}</text>')
        else:
            line.append(f'<text x="{value_x}" y="{y}" fill="{t["text"]}">{escape(value)}</text>')
        line.append("</g>")
        out.append("".join(line))

    cursor_y = TOP + LINE * (len(rows) + 1) + 6
    show = type_end + 0.35 + len(rows) * 0.18
    out.append(f'<text x="40" y="{cursor_y}" fill="{t["prompt"]}" opacity="0">$<animate attributeName="opacity" '
               f'from="0" to="1" begin="{show:.2f}s" dur="0.01s" fill="freeze"/></text>')
    out.append(f'<rect x="{cmd_x}" y="{cursor_y - 15}" width="10" height="19" fill="{t["text"]}" opacity="0">'
               f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.01;0.5;0.51" dur="1.1s" '
               f'begin="{show:.2f}s" repeatCount="indefinite"/></rect>')
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    assets = Path(__file__).resolve().parent.parent / "assets"
    assets.mkdir(exist_ok=True)
    for name, theme in THEMES.items():
        (assets / f"header-{name}.svg").write_text(render(theme), encoding="utf-8")
