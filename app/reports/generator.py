from __future__ import annotations

import json
from pathlib import Path

from app.schemas import ShortlistResponse

try:
    from weasyprint import HTML
except Exception:  # pragma: no cover - optional dependency
    HTML = None

from jinja2 import Template


REPORT_TEMPLATE = Template(
    """
    <html>
      <head>
        <meta charset=\"utf-8\" />
        <style>
          body { font-family: Arial, sans-serif; margin: 32px; color: #1f2937; }
          h1, h2 { color: #111827; }
          .candidate { border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px; margin-bottom: 16px; }
          .score { font-size: 18px; font-weight: bold; }
          .muted { color: #6b7280; }
          .flag { display: inline-block; padding: 4px 8px; margin-right: 6px; border-radius: 999px; background: #f3f4f6; }
        </style>
      </head>
      <body>
        <h1>HR Shortlisting Report</h1>
        <p class=\"muted\">Role: {{ job.role_title or 'Unknown' }} | Generated: {{ generated_at }}</p>
        <h2>Summary</h2>
        <pre>{{ summary_json }}</pre>
        <h2>Rankings</h2>
        {% for candidate in rankings %}
          <div class=\"candidate\">
            <div class=\"score\">{{ loop.index }}. {{ candidate.candidate_name }} - {{ candidate.total_score }}</div>
            <p>Recommendation: {{ candidate.recommendation }} | Confidence: {{ candidate.confidence }}</p>
            <p class=\"muted\">{{ candidate.rationale | join(' | ') }}</p>
            {% for flag in candidate.flags %}<span class=\"flag\">{{ flag }}</span>{% endfor %}
          </div>
        {% endfor %}
      </body>
    </html>
    """
)


def render_html(report: ShortlistResponse) -> str:
    return REPORT_TEMPLATE.render(
        job=report.job,
        rankings=report.rankings,
        summary_json=json.dumps(report.summary, indent=2),
        generated_at=report.generated_at.isoformat(),
    )


def render_pdf(report: ShortlistResponse, output_path: str | Path) -> Path:
    if HTML is None:
        raise RuntimeError("WeasyPrint is not installed")
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=render_html(report)).write_pdf(str(output))
    return output
