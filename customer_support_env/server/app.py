import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from openenv.core.env_server import create_fastapi_app

from customer_support_env.models import SupportAction, SupportObservation
from customer_support_env.server.environment import CustomerSupportEnvironment

app = create_fastapi_app(
    CustomerSupportEnvironment,
    SupportAction,
    SupportObservation,
)


@app.get("/", response_class=HTMLResponse)
async def root():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>customer_support_env — OpenEnv</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{
    --bg:#0c0c0c;
    --fg:#e8e8e8;
    --muted:#888;
    --dim:#555;
    --line:#222;
    --accent:#c6ff5e;
    --code-bg:#161616;
    --warn:#ff8866;
}
*{margin:0;padding:0;box-sizing:border-box}
html{font-size:15px}
body{
    font-family:'Inter',-apple-system,sans-serif;
    background:var(--bg);
    color:var(--fg);
    line-height:1.6;
    -webkit-font-smoothing:antialiased;
}
.mono{font-family:'JetBrains Mono',monospace}

.wrap{max-width:1080px;margin:0 auto;padding:0 28px}

/* Header */
.top{padding:28px 0 16px;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between}
.top .id{font-family:'JetBrains Mono',monospace;font-size:0.82rem;color:var(--muted)}
.top .id .accent{color:var(--accent)}
.top nav a{font-family:'JetBrains Mono',monospace;font-size:0.78rem;color:var(--muted);text-decoration:none;margin-left:18px}
.top nav a:hover{color:var(--fg)}

/* Hero */
.hero{padding:64px 0 48px;border-bottom:1px solid var(--line)}
.hero .meta{font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:var(--muted);margin-bottom:14px;letter-spacing:0.5px}
.hero h1{font-size:2.4rem;font-weight:700;line-height:1.15;letter-spacing:-0.02em;margin-bottom:18px;color:#fff}
.hero p{font-size:1.05rem;color:#bbb;max-width:560px;line-height:1.65}
.hero .actions{margin-top:24px;display:flex;gap:14px;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;gap:8px;padding:10px 18px;font-family:'JetBrains Mono',monospace;font-size:0.78rem;font-weight:500;text-decoration:none;border-radius:0;border:1px solid var(--line);color:var(--fg);background:transparent;transition:all 0.12s}
.btn:hover{border-color:var(--accent);color:var(--accent)}
.btn.primary{background:var(--accent);color:#0c0c0c;border-color:var(--accent);font-weight:700}
.btn.primary:hover{background:#b8f048;color:#0c0c0c}

/* Sections */
section{padding:56px 0;border-bottom:1px solid var(--line)}
section h2{font-family:'JetBrains Mono',monospace;font-size:0.78rem;color:var(--accent);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px;font-weight:600}
section h3{font-size:1.5rem;font-weight:700;color:#fff;margin-bottom:24px;letter-spacing:-0.01em}

/* Specs table */
.specs{width:100%;border-collapse:collapse;font-family:'JetBrains Mono',monospace;font-size:0.85rem}
.specs td{padding:10px 0;border-bottom:1px solid var(--line);vertical-align:top}
.specs td:first-child{color:var(--muted);width:160px}
.specs td:last-child{color:var(--fg)}
.specs .num{color:var(--accent);font-weight:700}

/* Tasks list */
.tasks-list{margin-top:8px}
.task-row{padding:18px 0;border-bottom:1px solid var(--line);display:flex;align-items:flex-start;gap:18px}
.task-row:last-child{border-bottom:none}
.task-row .tag{font-family:'JetBrains Mono',monospace;font-size:0.7rem;font-weight:700;padding:3px 8px;border:1px solid;letter-spacing:0.5px;text-transform:uppercase;flex-shrink:0;margin-top:2px}
.tag.easy{color:#9be572;border-color:#3a5a2a}
.tag.med{color:#e5c172;border-color:#5a4a2a}
.tag.hard{color:#e57272;border-color:#5a2a2a}
.task-row .body h4{font-size:1rem;color:#fff;font-weight:600;margin-bottom:4px}
.task-row .body p{color:var(--muted);font-size:0.9rem;line-height:1.55}
.task-row .body .stats{font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:var(--dim);margin-top:6px}

/* Architecture diagram (ASCII-style) */
.diagram{font-family:'JetBrains Mono',monospace;font-size:0.78rem;line-height:1.7;color:var(--muted);background:var(--code-bg);border:1px solid var(--line);padding:20px 24px;margin-top:8px;overflow-x:auto;white-space:pre}
.diagram .arrow{color:var(--accent)}
.diagram .label{color:#fff}

/* Code block */
.code{background:var(--code-bg);border:1px solid var(--line);padding:18px 22px;font-family:'JetBrains Mono',monospace;font-size:0.78rem;line-height:1.75;overflow-x:auto;margin-top:8px;color:#d4d4d4;white-space:pre}
.code .c{color:var(--dim)}
.code .k{color:#c486f0}
.code .s{color:#c6ff5e}
.code .v{color:#82d8ff}
.code .n{color:#ff9966}
.code .f{color:#82d8ff}

/* Terminal */
.terminal{background:#080808;border:1px solid var(--line);margin-top:8px;font-family:'JetBrains Mono',monospace;font-size:0.74rem}
.terminal-bar{padding:8px 14px;border-bottom:1px solid var(--line);font-size:0.7rem;color:var(--dim);display:flex;align-items:center;gap:8px}
.terminal-bar::before{content:'$';color:var(--accent);font-weight:700}
.terminal-body{padding:18px 22px;line-height:1.85;color:#d4d4d4;overflow-x:auto;white-space:pre}
.t-tag{color:#82d8ff;font-weight:700}
.t-end{color:#c486f0;font-weight:700}
.t-pos{color:var(--accent)}
.t-score{color:#ff9966;font-weight:700}
.t-c{color:var(--dim)}

/* API endpoints */
.api-list{font-family:'JetBrains Mono',monospace;font-size:0.85rem;margin-top:8px}
.api-row{padding:12px 0;border-bottom:1px solid var(--line);display:flex;gap:14px;align-items:center}
.api-row:last-child{border-bottom:none}
.api-row .method{font-weight:700;font-size:0.7rem;padding:2px 8px;letter-spacing:0.5px}
.api-row .method.post{color:#9be572;border:1px solid #3a5a2a}
.api-row .method.get{color:#82d8ff;border:1px solid #2a4a5a}
.api-row .path{color:#fff;flex:1}
.api-row .desc{color:var(--muted);font-size:0.8rem;font-family:'Inter',sans-serif}

/* Reward table */
.rewards{width:100%;border-collapse:collapse;font-family:'JetBrains Mono',monospace;font-size:0.84rem;margin-top:8px}
.rewards td{padding:9px 0;border-bottom:1px solid var(--line)}
.rewards td:first-child{color:var(--muted)}
.rewards td:nth-child(2){text-align:right;width:80px;font-weight:700}
.rewards .pos{color:var(--accent)}
.rewards .neg{color:var(--warn)}

/* Footer */
.footer{padding:36px 0;color:var(--muted);font-family:'JetBrains Mono',monospace;font-size:0.75rem;line-height:1.8}
.footer a{color:var(--accent);text-decoration:none}
.footer a:hover{text-decoration:underline}

p{color:#bbb}
.muted{color:var(--muted)}
code{font-family:'JetBrains Mono',monospace;background:var(--code-bg);padding:1px 6px;font-size:0.85em;color:var(--accent)}

@media(max-width:640px){
    html{font-size:14px}
    .hero h1{font-size:1.8rem}
    .specs td:first-child{width:120px}
}
</style>
</head>
<body>

<div class="wrap">

<header class="top">
    <div class="id">
        <span class="accent">~</span>/customer_support_env <span class="accent">v0.1.0</span>
    </div>
    <nav>
        <a href="/docs">api</a>
        <a href="/health">health</a>
        <a href="https://huggingface.co/spaces/wasimrehman05/customer-support-env/tree/main" target="_blank">source</a>
    </nav>
</header>

<section class="hero" style="border-bottom:1px solid var(--line);padding-bottom:48px">
    <div class="meta">openenv-spec/1 · meta-pytorch hackathon 2026</div>
    <h1>An RL environment for customer support resolution.</h1>
    <p>Train and evaluate LLM agents on multi-step ticket resolution tasks. Eleven scenarios across three difficulty tiers, deterministic graders, partial reward signals, and full OpenEnv spec compliance.</p>
    <div class="actions">
        <a href="/docs" class="btn primary">→ try the api</a>
        <a href="https://huggingface.co/spaces/wasimrehman05/customer-support-env/tree/main" target="_blank" class="btn">view source</a>
    </div>
</section>

<section>
    <h2>// specs</h2>
    <table class="specs">
        <tr><td>knowledge_base</td><td><span class="num">15</span> articles · 5 categories</td></tr>
        <tr><td>tickets</td><td><span class="num">11</span> scenarios · 3 difficulty tiers</td></tr>
        <tr><td>actions</td><td><code>search_kb</code> · <code>ask_clarification</code> · <code>send_response</code> · <code>escalate</code></td></tr>
        <tr><td>observation</td><td>typed Pydantic model · ticket, search results, customer reply, system message</td></tr>
        <tr><td>reward range</td><td><span class="num">[0.0, 1.0]</span> · normalized after partial signals</td></tr>
        <tr><td>max steps</td><td><span class="num">8 / 12 / 15</span> per difficulty tier</td></tr>
        <tr><td>runtime</td><td>~15s for full inference (3 tasks) · vcpu=2 · mem=8gb</td></tr>
        <tr><td>baseline</td><td>Qwen2.5-72B-Instruct → avg score <span class="num">0.73</span></td></tr>
    </table>
</section>

<section>
    <h2>// architecture</h2>
    <div class="diagram">
                <span class="label">[ticket]</span>
                    <span class="arrow">│</span>
                    <span class="arrow">▼</span>
       ┌────── env.reset() ──────┐
       <span class="arrow">│</span>                          <span class="arrow">│</span>
       <span class="arrow">│</span>    <span class="label">CustomerSupportEnv</span>    <span class="arrow">│</span>
       <span class="arrow">│</span>                          <span class="arrow">│</span>
       <span class="arrow">│</span>   ┌──────────────┐       <span class="arrow">│</span>
   ┌─→<span class="arrow">│</span>   │  state       │       <span class="arrow">│</span>
   <span class="arrow">│</span>   <span class="arrow">│</span>   │  rewards     │       <span class="arrow">│</span>
   <span class="arrow">│</span>   <span class="arrow">│</span>   │  trajectory  │       <span class="arrow">│</span>
   <span class="arrow">│</span>   <span class="arrow">│</span>   └──────────────┘       <span class="arrow">│</span>
   <span class="arrow">│</span>   └──────────┬───────────────┘
   <span class="arrow">│</span>              <span class="arrow">│</span> env.step(action)
   <span class="arrow">│</span>              <span class="arrow">▼</span>
   <span class="arrow">│</span>      ┌───────────────┐
   <span class="arrow">│</span>      <span class="arrow">│</span>  <span class="label">LLM AGENT</span>    <span class="arrow">│</span>     observes & decides
   <span class="arrow">│</span>      └───────┬───────┘
   <span class="arrow">│</span>              <span class="arrow">│</span>
   └──────────────┘ next action
</div>
</section>

<section>
    <h2>// tasks</h2>
    <div class="tasks-list">
        <div class="task-row">
            <div class="tag easy">easy</div>
            <div class="body">
                <h4>faq_resolution</h4>
                <p>Direct knowledge base questions. Agent must search the KB, find the matching article, and return the solution. No clarification needed.</p>
                <div class="stats">4 tickets · max 8 steps · grader: kb_search + solution_keywords</div>
            </div>
        </div>
        <div class="task-row">
            <div class="tag med">medium</div>
            <div class="body">
                <h4>troubleshooting</h4>
                <p>Technical issues requiring investigation. Agent must ask clarifying questions, narrow down the cause, then craft a solution informed by both KB articles and customer responses.</p>
                <div class="stats">4 tickets · max 12 steps · grader: clarifications + diagnosis + solution</div>
            </div>
        </div>
        <div class="task-row">
            <div class="tag hard">hard</div>
            <div class="body">
                <h4>complex_escalation</h4>
                <p>Multi-issue tickets where some sub-issues are KB-solvable and others require human escalation. Agent must decompose, prioritize, and decide. Partial credit for each sub-issue addressed.</p>
                <div class="stats">3 tickets · max 15 steps · grader: sub_issues + escalation_decision + solution</div>
            </div>
        </div>
    </div>
</section>

<section>
    <h2>// example</h2>
    <p style="margin-bottom:16px;color:var(--muted);font-size:0.9rem">Async client usage with the OpenEnv core library:</p>
    <div class="code"><span class="c"># pip install openenv-core</span>
<span class="k">from</span> customer_support_env <span class="k">import</span> CustomerSupportEnv, SupportAction

<span class="k">async with</span> CustomerSupportEnv(base_url=<span class="s">"https://wasimrehman05-customer-support-env.hf.space"</span>) <span class="k">as</span> env:
    <span class="v">obs</span> = <span class="k">await</span> env.reset(task_id=<span class="s">"troubleshooting"</span>, ticket_id=<span class="s">"T2-01"</span>)
    <span class="c"># obs.ticket → "My dashboard isn't loading at all..."</span>

    <span class="v">obs</span> = <span class="k">await</span> env.step(SupportAction(
        action_type=<span class="s">"search_kb"</span>,
        content=<span class="s">"dashboard not loading blank screen"</span>,
    ))
    <span class="c"># obs.search_results → [KB007, KB008, KB011] · reward=+0.15</span>

    <span class="v">obs</span> = <span class="k">await</span> env.step(SupportAction(
        action_type=<span class="s">"ask_clarification"</span>,
        content=<span class="s">"What browser are you using?"</span>,
    ))
    <span class="c"># obs.customer_reply → "Chrome 120 on Windows 11" · reward=+0.10</span>

    <span class="v">obs</span> = <span class="k">await</span> env.step(SupportAction(
        action_type=<span class="s">"send_response"</span>,
        content=<span class="s">"Try clearing your browser cache with Ctrl+Shift+R..."</span>,
    ))
    <span class="c"># done=True · cumulative reward → score in [0, 1]</span></div>
</section>

<section>
    <h2>// baseline run</h2>
    <p style="margin-bottom:16px;color:var(--muted);font-size:0.9rem">Stdout from <code>inference.py</code> running Qwen2.5-72B-Instruct against the environment:</p>
    <div class="terminal">
        <div class="terminal-bar">python inference.py</div>
        <div class="terminal-body"><span class="t-tag">[START]</span> task=faq_resolution env=customer_support_env model=Qwen/Qwen2.5-72B-Instruct
<span class="t-tag">[STEP]</span>  step=1 action=search_kb:password reset account lock <span class="t-pos">reward=0.15</span> done=false error=null
<span class="t-tag">[STEP]</span>  step=2 action=send_response:Hi Sarah, to reset your CloudDash password... <span class="t-pos">reward=0.19</span> done=true error=null
<span class="t-end">[END]</span>    success=<span class="t-pos">true</span> steps=2 <span class="t-score">score=0.88</span> rewards=0.15,0.19

<span class="t-tag">[START]</span> task=troubleshooting env=customer_support_env model=Qwen/Qwen2.5-72B-Instruct
<span class="t-tag">[STEP]</span>  step=1 action=search_kb:dashboard not loading blank screen <span class="t-pos">reward=0.15</span> done=false error=null
<span class="t-tag">[STEP]</span>  step=2 action=send_response:Hi James, I understand your dashboard... <span class="t-pos">reward=0.30</span> done=true error=null
<span class="t-end">[END]</span>    success=<span class="t-pos">true</span> steps=2 <span class="t-score">score=0.70</span> rewards=0.15,0.30

<span class="t-tag">[START]</span> task=complex_escalation env=customer_support_env model=Qwen/Qwen2.5-72B-Instruct
<span class="t-tag">[STEP]</span>  step=1 action=search_kb:double charge after upgrade, permission denied... <span class="t-pos">reward=0.15</span> done=false error=null
<span class="t-tag">[STEP]</span>  step=2 action=ask_clarification:Could you confirm if you checked billing... <span class="t-pos">reward=0.07</span> done=false error=null
<span class="t-tag">[STEP]</span>  step=3 action=ask_clarification:Could you check if the API key was regenerated... <span class="t-pos">reward=0.07</span> done=false error=null
<span class="t-tag">[STEP]</span>  step=4 action=send_response:Thank you for the details, Maria. Let's address each issue... <span class="t-pos">reward=0.43</span> done=true error=null
<span class="t-end">[END]</span>    success=<span class="t-pos">true</span> steps=4 <span class="t-score">score=0.60</span> rewards=0.15,0.07,0.07,0.43

<span class="t-c">[DEBUG] Average score across 3 tasks: 0.725</span></div>
    </div>
</section>

<section>
    <h2>// rewards</h2>
    <table class="rewards">
        <tr><td>found correct kb article</td><td class="pos">+0.15</td></tr>
        <tr><td>useful clarification (matched Q&amp;A)</td><td class="pos">+0.075</td></tr>
        <tr><td>correct diagnosis in response</td><td class="pos">+0.20</td></tr>
        <tr><td>solution keyword coverage</td><td class="pos">+0.25</td></tr>
        <tr><td>each sub-issue addressed (complex)</td><td class="pos">+0.10</td></tr>
        <tr><td>correct escalation decision</td><td class="pos">+0.15</td></tr>
        <tr><td>irrelevant search</td><td class="neg">−0.05</td></tr>
        <tr><td>wasted clarification</td><td class="neg">−0.05</td></tr>
        <tr><td>redundant action</td><td class="neg">−0.03</td></tr>
        <tr><td>wrong escalation</td><td class="neg">−0.10</td></tr>
    </table>
</section>

<section>
    <h2>// api</h2>
    <div class="api-list">
        <div class="api-row">
            <span class="method post">POST</span>
            <span class="path">/reset</span>
            <span class="desc">start a new ticket episode</span>
        </div>
        <div class="api-row">
            <span class="method post">POST</span>
            <span class="path">/step</span>
            <span class="desc">submit an action, observe next state</span>
        </div>
        <div class="api-row">
            <span class="method get">GET</span>
            <span class="path">/state</span>
            <span class="desc">read current environment state</span>
        </div>
        <div class="api-row">
            <span class="method get">GET</span>
            <span class="path">/health</span>
            <span class="desc">service health probe</span>
        </div>
        <div class="api-row">
            <span class="method get">GET</span>
            <span class="path">/docs</span>
            <span class="desc">interactive openapi/swagger docs</span>
        </div>
    </div>
</section>

<footer class="footer">
    <p>Built for the meta-pytorch openenv hackathon 2026.</p>
    <p>By <a href="https://huggingface.co/wasimrehman05" target="_blank">@wasimrehman05</a> · source on <a href="https://huggingface.co/spaces/wasimrehman05/customer-support-env/tree/main" target="_blank">huggingface spaces</a>.</p>
</footer>

</div>

</body>
</html>"""


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
