"""
HTML Report Generator -- turns pipeline_results.jsonl into a readable report.

Shows the full agent journey for each query:
  Query → Router → Decomposer plan → Step-by-step execution/verification → Output

Usage:
    python -m tests.generate_report
    # Opens tests/results/pipeline_report.html
"""

import json
import sys
import os
import html as html_lib
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
RESULTS_FILE = PROJECT_ROOT / "tests" / "results" / "pipeline_results.jsonl"
OUTPUT_FILE = PROJECT_ROOT / "tests" / "results" / "pipeline_report.html"


def load_results() -> list[dict]:
    entries = []
    with open(RESULTS_FILE) as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries


def esc(text: str) -> str:
    return html_lib.escape(str(text))


def build_step_timeline(entry: dict) -> str:
    """Build the visual step execution timeline from debug messages."""
    messages = entry.get("debug_messages", [])
    snap = entry.get("state_snapshot", {})
    steps = snap.get("steps", [])
    step_results = snap.get("step_results", {})

    if not steps and not messages:
        return '<p class="muted">No execution steps (direct response)</p>'

    # Build the plan view
    plan_html = '<div class="plan-box"><h4>Execution Plan</h4><table class="plan-table"><tr><th>#</th><th>Type</th><th>Description</th><th>Tool / Prompt</th><th>Depends On</th></tr>'
    for i, step in enumerate(steps):
        sid = esc(step.get("step_id", ""))
        stype = step.get("step_type", "")
        desc = esc(step.get("description", ""))
        tool = esc(step.get("tool_name") or "")
        prompt = esc((step.get("analysis_prompt") or "")[:80])
        deps = ", ".join(step.get("depends_on", [])) or "—"
        type_cls = "tag-data" if stype == "DATA" else "tag-analysis"
        detail = tool if stype == "DATA" else (prompt + "..." if len(step.get("analysis_prompt", "") or "") > 80 else prompt)
        plan_html += f'<tr><td><code>{sid}</code></td><td><span class="{type_cls}">{stype}</span></td><td>{desc}</td><td><code>{detail}</code></td><td>{deps}</td></tr>'
    plan_html += '</table></div>'

    # Build the execution timeline from debug messages
    timeline_html = '<div class="timeline">'
    for msg in messages:
        if msg.startswith("[QueryRouter]"):
            timeline_html += f'<div class="tl-item tl-router"><span class="tl-badge">Router</span> {esc(msg[14:])}</div>'
        elif msg.startswith("[Decomposer]"):
            text = msg[13:]
            # Truncate long reasoning
            if len(text) > 200:
                text = text[:200] + "..."
            timeline_html += f'<div class="tl-item tl-decomposer"><span class="tl-badge">Decomposer</span> {esc(text)}</div>'
        elif msg.startswith("[StepExecutor]"):
            text = msg[15:]
            is_error = "ERROR" in text
            cls = "tl-executor tl-error" if is_error else "tl-executor"
            timeline_html += f'<div class="tl-item {cls}"><span class="tl-badge">Executor</span> {esc(text)}</div>'
        elif msg.startswith("[Verifier]"):
            text = msg[11:]
            if "verdict=ok" in text:
                cls = "tl-verifier tl-ok"
            elif "verdict=needs_more_data" in text:
                cls = "tl-verifier tl-retry"
            elif "verdict=replan" in text:
                cls = "tl-verifier tl-replan"
            else:
                cls = "tl-verifier"
            timeline_html += f'<div class="tl-item {cls}"><span class="tl-badge">Verifier</span> {esc(text)}</div>'
        elif msg.startswith("[OutputFormatter]"):
            timeline_html += f'<div class="tl-item tl-formatter"><span class="tl-badge">Output</span> {esc(msg[18:])}</div>'
        elif msg.startswith("[DirectResponse]"):
            timeline_html += f'<div class="tl-item tl-direct"><span class="tl-badge">Direct</span> {esc(msg[17:])}</div>'
    timeline_html += '</div>'

    return plan_html + timeline_html


def build_step_results(entry: dict) -> str:
    """Build detailed step results section."""
    snap = entry.get("state_snapshot", {})
    step_results = snap.get("step_results", {})
    if not step_results:
        return ""

    html = '<div class="results-box"><h4>Step Results</h4>'
    for sid, sr in step_results.items():
        stype = sr.get("step_type", "")
        success = sr.get("success", False)
        error = sr.get("error")
        data_keys = sr.get("data_keys")
        data_size = sr.get("data_size", 0)
        # Support both old (analysis_preview) and new (analysis_full) field names
        analysis = sr.get("analysis_full") or sr.get("analysis_preview")

        status_cls = "status-pass" if success else "status-fail"
        status_text = "Success" if success else "Failed"

        html += f'<div class="step-result"><div class="step-header">'
        html += f'<code>{sid}</code> <span class="tag-{stype.lower()}">{stype}</span> '
        html += f'<span class="{status_cls}">{status_text}</span>'
        if data_size:
            html += f' <span class="muted">({data_size:,} bytes)</span>'
        html += '</div>'

        if error:
            html += f'<div class="error-msg">{esc(error)}</div>'
        if data_keys:
            html += f'<div class="data-keys">Keys: <code>{", ".join(data_keys[:12])}</code>{"..." if len(data_keys) > 12 else ""}</div>'
        if analysis:
            collapsed_id = f"analysis-{sid}"
            # Show first 200 chars, with expand button for full text
            short = esc(analysis[:200])
            full = esc(analysis)
            if len(analysis) > 200:
                html += f'<div class="analysis-preview" id="{collapsed_id}-short">{short}... <button class="expand-btn" onclick="document.getElementById(\'{collapsed_id}-short\').style.display=\'none\';document.getElementById(\'{collapsed_id}-full\').style.display=\'block\';">Show Full Analysis</button></div>'
                html += f'<div class="analysis-preview analysis-full" id="{collapsed_id}-full" style="display:none;">{full} <button class="expand-btn" onclick="document.getElementById(\'{collapsed_id}-full\').style.display=\'none\';document.getElementById(\'{collapsed_id}-short\').style.display=\'block\';">Collapse</button></div>'
            else:
                html += f'<div class="analysis-preview">{full}</div>'
        html += '</div>'
    html += '</div>'
    return html


def _build_component_iframe(ticker: str, component_code: str) -> str:
    """Build a self-contained iframe that renders the React/TS component."""
    # We need to:
    # 1. Strip TypeScript types so Babel JSX-only transform works
    # 2. Replace imports with CDN globals
    # 3. Provide mock data so the component renders

    import re

    code = component_code

    # Strip TypeScript: interface blocks
    code = re.sub(r'interface\s+\w+\s*\{[^}]*\}', '', code, flags=re.DOTALL)
    # Strip type annotations: `: Type` from params and variables
    code = re.sub(r':\s*(React\.FC<\w+>|React\.FC)', '', code)
    code = re.sub(r'<Props>', '', code)
    # Strip import lines (we'll provide globals)
    code = re.sub(r"import\s+.*?from\s+['\"].*?['\"];?\n?", '', code)
    # Strip export default
    code = re.sub(r'export\s+default\s+\w+;?', '', code)
    # Find component name
    name_match = re.search(r'const\s+(\w+)', code)
    comp_name = name_match.group(1) if name_match else 'FinancialAnalysisDisplay'

    # Escape for embedding in HTML
    escaped_code = code.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

    iframe_html = f'''<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<script src="https://cdn.jsdelivr.net/npm/react@18/umd/react.production.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/recharts@2/umd/Recharts.min.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<script src="https://cdn.tailwindcss.com"></script>
<style>body{{margin:0;padding:8px;font-family:-apple-system,BlinkMacSystemFont,sans-serif;background:#fff;}}</style>
</head><body>
<div id="root"></div>
<script type="text/babel">
const {{ LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, AreaChart, Area,
         XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, CartesianGrid }} = Recharts;
const TrendingUp = (p) => <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" {{...p}}><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>;
const TrendingDown = (p) => <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" {{...p}}><polyline points="22 17 13.5 8.5 8.5 13.5 2 7"/><polyline points="16 17 22 17 22 11"/></svg>;
const DollarSign = (p) => <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" {{...p}}><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>;
const BarChart3 = (p) => <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" {{...p}}><path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/></svg>;
const AlertCircle = (p) => <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" {{...p}}><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>;
const ArrowUpRight = TrendingUp;
const ArrowDownRight = TrendingDown;

{escaped_code}

// Render with mock empty data that won't crash
try {{
  const mockData = {{}};
  ReactDOM.createRoot(document.getElementById('root')).render(
    React.createElement({comp_name}, {{ data: mockData }})
  );
}} catch(e) {{
  document.getElementById('root').innerHTML = '<div style="padding:16px;color:#666;font-size:13px;">Component render error: ' + e.message + '</div>';
}}
</script>
</body></html>'''

    return iframe_html


def build_output_section(entry: dict) -> str:
    """Build the final output section."""
    snap = entry.get("state_snapshot", {})
    so = snap.get("structured_output", {})
    tc = snap.get("typescript_component", {})
    raw_analysis = snap.get("raw_analysis", "")
    ticker = entry.get("ticker", "unknown")

    html = '<div class="output-box"><h4>Final Output</h4>'

    if so.get("summary_preview"):
        html += f'<div class="output-summary"><strong>Summary:</strong> {esc(so["summary_preview"])}</div>'

    # Show the final synthesis analysis prominently (if available)
    final_synthesis = None
    sr = snap.get("step_results", {})
    if "final_synthesis" in sr:
        fs = sr["final_synthesis"]
        final_synthesis = fs.get("analysis_full") or fs.get("analysis_preview")
    if final_synthesis:
        html += f'<div class="final-synthesis"><h5>Final Analysis (what the user sees)</h5><div class="synthesis-text">{esc(final_synthesis)}</div></div>'

    # Show key insights
    insights = so.get("key_insights", [])
    if isinstance(insights, list) and insights:
        html += '<div class="insights-list"><strong>Key Insights:</strong><ul>'
        for ins in insights:
            html += f'<li>{esc(str(ins))}</li>'
        html += '</ul></div>'

    # Show recommendations
    recs = so.get("recommendations", [])
    if isinstance(recs, list) and recs:
        html += '<div class="recs-list"><strong>Recommendations:</strong><ul>'
        for rec in recs:
            html += f'<li>{esc(str(rec))}</li>'
        html += '</ul></div>'

    html += '<div class="output-stats">'
    cb = so.get("content_blocks", 0)
    cb_count = cb if isinstance(cb, int) else len(cb) if isinstance(cb, list) else 0
    html += f'<span class="output-stat">Content Blocks: <strong>{cb_count}</strong></span>'
    ki = insights if isinstance(insights, list) else []
    html += f'<span class="output-stat">Key Insights: <strong>{len(ki)}</strong></span>'
    rc = recs if isinstance(recs, list) else []
    html += f'<span class="output-stat">Recommendations: <strong>{len(rc)}</strong></span>'
    if tc.get("has_component"):
        html += f'<span class="output-stat">TypeScript: <strong>{tc.get("code_length", 0):,} chars</strong></span>'
    if raw_analysis:
        html += f'<span class="output-stat">Raw Analysis: <strong>{len(raw_analysis):,} chars</strong></span>'
    html += '</div>'

    # Render the TypeScript component live
    component_code = tc.get("component_code", "")
    if component_code and len(component_code) > 50:
        iframe_id = f"component-iframe-{ticker}"
        iframe_html = _build_component_iframe(ticker, component_code)
        # Encode the iframe HTML as a data URI
        import base64
        encoded = base64.b64encode(iframe_html.encode('utf-8')).decode('ascii')
        data_uri = f"data:text/html;base64,{encoded}"

        html += f'''
        <div class="component-section">
          <div class="component-header">
            <h5>Rendered React Component</h5>
            <button class="expand-btn" onclick="var el=document.getElementById('code-{ticker}'); el.style.display=el.style.display==='none'?'block':'none';">View Source Code</button>
          </div>
          <iframe id="{iframe_id}" src="{data_uri}" class="component-iframe" sandbox="allow-scripts"></iframe>
          <div id="code-{ticker}" style="display:none;" class="source-code"><pre>{esc(component_code)}</pre></div>
        </div>'''

    # Show raw analysis (collapsed by default)
    if raw_analysis and len(raw_analysis) > 100:
        html += f'<div style="margin-top:10px;"><button class="expand-btn" onclick="var el=document.getElementById(\'raw-{ticker}\'); el.style.display=el.style.display===\'none\'?\'block\':\'none\';">Show Full Raw Analysis ({len(raw_analysis):,} chars)</button></div>'
        html += f'<div class="raw-analysis" id="raw-{ticker}" style="display:none;"><pre>{esc(raw_analysis)}</pre></div>'

    html += '</div>'
    return html


def build_entry_html(entry: dict, index: int) -> str:
    """Build the HTML for a single query result."""
    ticker = entry.get("ticker", "?")
    company = entry.get("company", "?")
    query = entry.get("query", "?")
    category = entry.get("category", "?")
    success = entry.get("success", False)
    timing = entry.get("timing_seconds", 0)
    node_calls = entry.get("node_calls", 0)
    steps_ok = entry.get("steps_succeeded", 0)
    steps_fail = entry.get("steps_failed", 0)
    steps_total = entry.get("steps_planned", 0)
    tickers = entry.get("detected_tickers", [])
    snap = entry.get("state_snapshot", {})
    reasoning = snap.get("decomposition_reasoning", "")

    status_cls = "card-pass" if success else "card-fail"
    status_text = "PASS" if success else "FAIL"
    status_badge = "status-pass" if success else "status-fail"

    html = f'''
    <div class="card {status_cls}" id="query-{index}">
      <div class="card-header" onclick="this.parentElement.classList.toggle('collapsed')">
        <div class="card-title">
          <span class="{status_badge}">{status_text}</span>
          <strong>{esc(ticker)}</strong> — {esc(company)}
          <span class="tag-category">{esc(category)}</span>
        </div>
        <div class="card-meta">
          <span>{timing:.1f}s</span>
          <span>{node_calls} nodes</span>
          <span>{steps_ok}/{steps_total} steps</span>
          <span class="expand-icon">▼</span>
        </div>
      </div>
      <div class="card-body">
        <div class="query-box">
          <div class="query-label">User Query</div>
          <div class="query-text">{esc(query)}</div>
        </div>
    '''

    if tickers:
        html += f'<div class="meta-row"><strong>Detected Tickers:</strong> {", ".join(tickers[:10])}{"..." if len(tickers) > 10 else ""}</div>'
    if reasoning:
        r = reasoning[:300] + "..." if len(reasoning) > 300 else reasoning
        html += f'<div class="reasoning-box"><strong>Decomposition Reasoning:</strong> {esc(r)}</div>'

    html += build_step_timeline(entry)
    html += build_step_results(entry)
    html += build_output_section(entry)

    if entry.get("error"):
        html += f'<div class="error-box"><strong>Error:</strong> {esc(entry["error"])}</div>'

    html += '</div></div>'
    return html


def generate_html(entries: list[dict]) -> str:
    total = len(entries)
    passed = sum(1 for e in entries if e.get("success"))
    failed = total - passed
    avg_time = sum(e.get("timing_seconds", 0) for e in entries) / total if total else 0
    total_time = sum(e.get("timing_seconds", 0) for e in entries)

    categories = {}
    for e in entries:
        c = e.get("category", "unknown")
        categories[c] = categories.get(c, 0) + 1

    cards_html = "\n".join(build_entry_html(e, i) for i, e in enumerate(entries))
    cat_pills = " ".join(f'<span class="cat-pill">{c}: {n}</span>' for c, n in sorted(categories.items()))
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sankhya Finance v2 — Pipeline Test Report</title>
<style>
  :root {{
    --bg: #0d1117; --card-bg: #161b22; --border: #30363d; --text: #e6edf3;
    --muted: #8b949e; --green: #3fb950; --red: #f85149; --blue: #58a6ff;
    --yellow: #d29922; --purple: #bc8cff; --orange: #f0883e;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; padding: 24px; }}
  .container {{ max-width: 1100px; margin: 0 auto; }}
  h1 {{ font-size: 28px; margin-bottom: 4px; }}
  .subtitle {{ color: var(--muted); margin-bottom: 24px; }}

  /* Summary */
  .summary {{ display: flex; gap: 16px; margin-bottom: 24px; flex-wrap: wrap; }}
  .stat-card {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 16px 20px; flex: 1; min-width: 140px; }}
  .stat-card .stat-value {{ font-size: 28px; font-weight: 700; }}
  .stat-card .stat-label {{ color: var(--muted); font-size: 13px; }}
  .stat-green .stat-value {{ color: var(--green); }}
  .stat-red .stat-value {{ color: var(--red); }}
  .stat-blue .stat-value {{ color: var(--blue); }}

  .cat-pills {{ margin-bottom: 20px; }}
  .cat-pill {{ display: inline-block; background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; padding: 3px 10px; font-size: 12px; margin: 2px; color: var(--muted); }}

  /* Cards */
  .card {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 10px; margin-bottom: 16px; overflow: hidden; }}
  .card-pass {{ border-left: 3px solid var(--green); }}
  .card-fail {{ border-left: 3px solid var(--red); }}
  .card-header {{ display: flex; justify-content: space-between; align-items: center; padding: 14px 20px; cursor: pointer; user-select: none; }}  
  .card-header:hover {{ background: rgba(255,255,255,0.03); }}
  .card-title {{ display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }}
  .card-meta {{ display: flex; gap: 14px; color: var(--muted); font-size: 13px; align-items: center; }}
  .expand-icon {{ transition: transform 0.2s; }}
  .collapsed .card-body {{ display: none; }}
  .collapsed .expand-icon {{ transform: rotate(-90deg); }}
  .card-body {{ padding: 0 20px 20px; }}

  /* Tags & Badges */
  .status-pass {{ background: rgba(63,185,80,0.15); color: var(--green); padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; }}
  .status-fail {{ background: rgba(248,81,73,0.15); color: var(--red); padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; }}
  .tag-data {{ background: rgba(88,166,255,0.15); color: var(--blue); padding: 2px 6px; border-radius: 3px; font-size: 11px; font-weight: 600; }}
  .tag-analysis {{ background: rgba(188,140,255,0.15); color: var(--purple); padding: 2px 6px; border-radius: 3px; font-size: 11px; font-weight: 600; }}
  .tag-category {{ background: rgba(210,153,34,0.15); color: var(--yellow); padding: 2px 6px; border-radius: 3px; font-size: 11px; }}

  /* Query Box */
  .query-box {{ background: rgba(88,166,255,0.06); border: 1px solid rgba(88,166,255,0.2); border-radius: 8px; padding: 14px; margin-bottom: 16px; }}
  .query-label {{ font-size: 11px; color: var(--blue); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }}
  .query-text {{ font-size: 16px; font-weight: 500; }}

  .meta-row {{ color: var(--muted); font-size: 13px; margin-bottom: 8px; }}
  .reasoning-box {{ background: rgba(210,153,34,0.06); border: 1px solid rgba(210,153,34,0.15); border-radius: 6px; padding: 10px; margin-bottom: 16px; font-size: 13px; color: var(--muted); }}
  .muted {{ color: var(--muted); font-size: 12px; }}

  /* Plan Table */
  .plan-box {{ margin-bottom: 16px; }}
  .plan-box h4 {{ font-size: 14px; color: var(--muted); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }}
  .plan-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  .plan-table th {{ text-align: left; padding: 6px 10px; color: var(--muted); border-bottom: 1px solid var(--border); font-weight: 600; font-size: 11px; text-transform: uppercase; }}
  .plan-table td {{ padding: 6px 10px; border-bottom: 1px solid rgba(48,54,61,0.5); vertical-align: top; }}
  .plan-table code {{ font-size: 12px; color: var(--blue); }}

  /* Timeline */
  .timeline {{ margin-bottom: 16px; }}
  .tl-item {{ padding: 6px 12px; margin: 2px 0; border-radius: 4px; font-size: 13px; border-left: 3px solid var(--border); background: rgba(255,255,255,0.02); }}
  .tl-badge {{ display: inline-block; width: 80px; font-weight: 600; font-size: 11px; text-transform: uppercase; }}
  .tl-router {{ border-left-color: var(--blue); }}
  .tl-router .tl-badge {{ color: var(--blue); }}
  .tl-decomposer {{ border-left-color: var(--yellow); }}
  .tl-decomposer .tl-badge {{ color: var(--yellow); }}
  .tl-executor {{ border-left-color: var(--purple); }}
  .tl-executor .tl-badge {{ color: var(--purple); }}
  .tl-verifier {{ border-left-color: var(--muted); }}
  .tl-verifier .tl-badge {{ color: var(--muted); }}
  .tl-ok {{ border-left-color: var(--green); }}
  .tl-ok .tl-badge {{ color: var(--green); }}
  .tl-retry {{ border-left-color: var(--orange); background: rgba(240,136,62,0.05); }}
  .tl-retry .tl-badge {{ color: var(--orange); }}
  .tl-replan {{ border-left-color: var(--red); background: rgba(248,81,73,0.05); }}
  .tl-replan .tl-badge {{ color: var(--red); }}
  .tl-error {{ background: rgba(248,81,73,0.05); border-left-color: var(--red); }}
  .tl-formatter {{ border-left-color: var(--green); }}
  .tl-formatter .tl-badge {{ color: var(--green); }}
  .tl-direct {{ border-left-color: var(--blue); }}
  .tl-direct .tl-badge {{ color: var(--blue); }}

  /* Step Results */
  .results-box {{ margin-bottom: 16px; }}
  .results-box h4 {{ font-size: 14px; color: var(--muted); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }}
  .step-result {{ background: rgba(255,255,255,0.02); border: 1px solid rgba(48,54,61,0.5); border-radius: 6px; padding: 10px 12px; margin-bottom: 6px; }}
  .step-header {{ margin-bottom: 6px; }}
  .step-header code {{ color: var(--blue); font-size: 13px; }}
  .error-msg {{ color: var(--red); font-size: 12px; background: rgba(248,81,73,0.08); padding: 6px 8px; border-radius: 4px; margin-top: 4px; }}
  .data-keys {{ font-size: 12px; color: var(--muted); margin-top: 4px; }}
  .data-keys code {{ color: var(--muted); }}
  .analysis-preview {{ font-size: 12px; color: var(--text); margin-top: 6px; background: rgba(188,140,255,0.05); padding: 8px; border-radius: 4px; white-space: pre-wrap; max-height: 120px; overflow-y: auto; }}

  /* Output */
  .output-box {{ background: rgba(63,185,80,0.05); border: 1px solid rgba(63,185,80,0.2); border-radius: 8px; padding: 14px; margin-bottom: 12px; }}
  .output-box h4 {{ font-size: 14px; color: var(--green); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }}
  .output-summary {{ font-size: 14px; margin-bottom: 10px; }}
  .output-stats {{ display: flex; gap: 16px; flex-wrap: wrap; }}
  .output-stat {{ font-size: 13px; color: var(--muted); }}
  .output-stat strong {{ color: var(--text); }}

  .error-box {{ background: rgba(248,81,73,0.08); border: 1px solid rgba(248,81,73,0.2); border-radius: 6px; padding: 10px; color: var(--red); font-size: 13px; }}
  .expand-btn {{ background: rgba(88,166,255,0.15); color: var(--blue); border: 1px solid rgba(88,166,255,0.3); border-radius: 4px; padding: 2px 8px; font-size: 11px; cursor: pointer; margin-left: 4px; }}
  .expand-btn:hover {{ background: rgba(88,166,255,0.25); }}
  .analysis-full {{ max-height: 600px; overflow-y: auto; }}
  .raw-analysis {{ margin-top: 8px; }}
  .raw-analysis pre {{ background: rgba(0,0,0,0.3); border: 1px solid var(--border); border-radius: 6px; padding: 12px; font-size: 12px; line-height: 1.5; white-space: pre-wrap; word-wrap: break-word; max-height: 600px; overflow-y: auto; color: var(--text); }}
  .final-synthesis {{ background: rgba(63,185,80,0.08); border: 1px solid rgba(63,185,80,0.25); border-radius: 8px; padding: 14px; margin: 12px 0; }}
  .final-synthesis h5 {{ font-size: 13px; color: var(--green); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }}
  .synthesis-text {{ font-size: 13px; line-height: 1.7; white-space: pre-wrap; max-height: 500px; overflow-y: auto; }}
  .insights-list {{ margin: 8px 0; font-size: 13px; }}
  .insights-list ul {{ margin: 4px 0 0 20px; }}
  .insights-list li {{ margin: 2px 0; }}
  .recs-list {{ margin: 8px 0; font-size: 13px; color: var(--yellow); }}
  .recs-list ul {{ margin: 4px 0 0 20px; }}
  .recs-list li {{ margin: 2px 0; }}
  .component-section {{ margin-top: 12px; }}
  .component-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }}
  .component-header h5 {{ font-size: 13px; color: var(--blue); text-transform: uppercase; letter-spacing: 0.5px; margin: 0; }}
  .component-iframe {{ width: 100%; height: 350px; border: 1px solid var(--border); border-radius: 8px; background: #fff; }}
  .source-code {{ margin-top: 8px; }}
  .source-code pre {{ background: rgba(0,0,0,0.4); border: 1px solid var(--border); border-radius: 6px; padding: 12px; font-size: 11px; line-height: 1.4; white-space: pre-wrap; word-wrap: break-word; max-height: 400px; overflow-y: auto; color: #a5d6ff; }}
</style>
</head>
<body>
<div class="container">
  <h1>Sankhya Finance v2 — Pipeline Test Report</h1>
  <p class="subtitle">Generated {now} · {total} queries tested</p>

  <div class="summary">
    <div class="stat-card stat-green"><div class="stat-value">{passed}</div><div class="stat-label">Passed</div></div>
    <div class="stat-card stat-red"><div class="stat-value">{failed}</div><div class="stat-label">Failed</div></div>
    <div class="stat-card stat-blue"><div class="stat-value">{avg_time:.1f}s</div><div class="stat-label">Avg Time</div></div>
    <div class="stat-card"><div class="stat-value">{total_time:.0f}s</div><div class="stat-label">Total Time</div></div>
    <div class="stat-card"><div class="stat-value">{total}</div><div class="stat-label">Queries</div></div>
  </div>

  <div class="cat-pills">Query categories: {cat_pills}</div>

  {cards_html}
</div>
</body>
</html>'''


def main():
    if not RESULTS_FILE.exists():
        print(f"  No results file found at {RESULTS_FILE}")
        print("  Run tests first: python -m tests.test_full_pipeline --count 5")
        sys.exit(1)

    entries = load_results()
    print(f"  Loaded {len(entries)} test results")

    html = generate_html(entries)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        f.write(html)

    print(f"  Report generated: {OUTPUT_FILE}")
    print(f"  Open in browser: file://{OUTPUT_FILE}")

    # Try to open in browser
    try:
        import webbrowser
        webbrowser.open(f"file://{OUTPUT_FILE}")
    except Exception:
        pass


if __name__ == "__main__":
    main()
