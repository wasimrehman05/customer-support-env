from typing import Dict, List, Any


KB_ARTICLES: Dict[str, Dict[str, Any]] = {
    "KB001": {
        "id": "KB001",
        "title": "How to Reset Your Password",
        "category": "Account",
        "keywords": [
            "password", "reset", "forgot", "login", "credentials",
            "change password", "locked out", "can't log in", "sign in",
        ],
        "content": (
            "To reset your CloudDash password:\n"
            "1. Go to the CloudDash login page at app.clouddash.io\n"
            "2. Click 'Forgot Password?' below the login form\n"
            "3. Enter the email address associated with your account\n"
            "4. Check your email for a password reset link (check spam folder if needed)\n"
            "5. Click the reset link and create a new password\n"
            "6. Your new password must be at least 12 characters with one uppercase, "
            "one number, and one special character\n\n"
            "If you don't receive the email within 5 minutes, contact support. "
            "Password reset links expire after 24 hours. If your account is locked "
            "due to too many failed attempts, wait 30 minutes before trying again."
        ),
        "solution_steps": [
            "go to login page",
            "click forgot password",
            "enter email",
            "check email for reset link",
            "create new password",
        ],
    },
    "KB002": {
        "id": "KB002",
        "title": "Setting Up Two-Factor Authentication (2FA)",
        "category": "Account",
        "keywords": [
            "2fa", "two-factor", "authentication", "mfa", "multi-factor",
            "security", "authenticator", "otp", "verification code",
        ],
        "content": (
            "To enable Two-Factor Authentication on your CloudDash account:\n"
            "1. Log in and navigate to Settings > Security\n"
            "2. Click 'Enable Two-Factor Authentication'\n"
            "3. Choose your preferred method: Authenticator App (recommended) or SMS\n"
            "4. For Authenticator App: scan the QR code with Google Authenticator, "
            "Authy, or any TOTP-compatible app\n"
            "5. Enter the 6-digit verification code to confirm setup\n"
            "6. Save your backup recovery codes in a secure location\n\n"
            "Important: If you lose access to your 2FA device, you can use a backup "
            "recovery code to log in. Each code can only be used once. Contact support "
            "if you've lost both your 2FA device and recovery codes."
        ),
        "solution_steps": [
            "settings",
            "security",
            "enable two-factor",
            "authenticator app",
            "scan qr code",
            "enter verification code",
            "save backup recovery codes",
        ],
    },
    "KB003": {
        "id": "KB003",
        "title": "Managing Team Member Permissions and Roles",
        "category": "Account",
        "keywords": [
            "team", "permissions", "roles", "access", "admin", "editor",
            "viewer", "invite", "member", "add user", "remove user",
            "role assignment", "permission denied",
        ],
        "content": (
            "CloudDash has three permission levels:\n"
            "- Admin: Full access including billing, team management, and all dashboards\n"
            "- Editor: Can create/edit dashboards, configure data sources, manage alerts\n"
            "- Viewer: Read-only access to dashboards and reports\n\n"
            "To manage team permissions:\n"
            "1. Go to Settings > Team Management\n"
            "2. To invite: Click 'Invite Member', enter email, select role, click Send\n"
            "3. To change role: Click the member's name > Change Role > select new role\n"
            "4. To remove: Click the member's name > Remove from Team > Confirm\n\n"
            "Role changes take effect immediately. When a plan is upgraded or downgraded, "
            "all custom role assignments are preserved. If members report 'Permission Denied' "
            "after a plan change, verify their roles haven't been affected in Team Management."
        ),
        "solution_steps": [
            "settings",
            "team management",
            "invite member",
            "change role",
            "select role",
            "admin editor viewer",
        ],
    },
    "KB004": {
        "id": "KB004",
        "title": "Understanding Your Billing Statement",
        "category": "Billing",
        "keywords": [
            "billing", "invoice", "statement", "charges", "payment",
            "receipt", "subscription", "cost", "pricing",
        ],
        "content": (
            "Your CloudDash billing statement includes:\n"
            "- Plan charges: Monthly or annual subscription fee\n"
            "- Add-on charges: Additional data sources, premium integrations\n"
            "- Overage charges: API calls or storage exceeding plan limits\n"
            "- Credits: Promotional credits or refunds applied\n\n"
            "To view your billing history:\n"
            "1. Go to Settings > Billing\n"
            "2. Click 'Billing History' to see past invoices\n"
            "3. Click any invoice to download a PDF receipt\n\n"
            "Billing cycles start on the date you first subscribed. Payments are "
            "processed automatically via your saved payment method. If a payment fails, "
            "you'll have a 7-day grace period before service interruption."
        ),
        "solution_steps": [
            "settings",
            "billing",
            "billing history",
            "download invoice",
            "payment method",
        ],
    },
    "KB005": {
        "id": "KB005",
        "title": "Upgrading or Downgrading Your Plan",
        "category": "Billing",
        "keywords": [
            "upgrade", "downgrade", "plan", "change plan", "switch plan",
            "basic", "pro", "enterprise", "pricing", "tier",
        ],
        "content": (
            "CloudDash Plans:\n"
            "- Basic ($29/mo): 5 dashboards, 3 data sources, 5 team members\n"
            "- Pro ($79/mo): 25 dashboards, 10 data sources, 25 team members, API access\n"
            "- Enterprise ($199/mo): Unlimited everything, SSO, dedicated support\n\n"
            "To change your plan:\n"
            "1. Go to Settings > Billing > Current Plan\n"
            "2. Click 'Change Plan'\n"
            "3. Select the desired plan and click 'Confirm'\n\n"
            "Upgrades take effect immediately with prorated billing for the current cycle. "
            "Downgrades take effect at the end of the current billing cycle. "
            "When downgrading, features exceeding the new plan's limits will be "
            "deactivated (dashboards archived, data sources disconnected). "
            "Team permissions and API keys are preserved during plan changes, "
            "but API access is disabled on Basic plan."
        ),
        "solution_steps": [
            "settings",
            "billing",
            "change plan",
            "select plan",
            "prorated billing",
            "end of billing cycle",
        ],
    },
    "KB006": {
        "id": "KB006",
        "title": "Requesting a Refund",
        "category": "Billing",
        "keywords": [
            "refund", "money back", "cancel", "cancellation", "charged",
            "overcharged", "double charged", "wrong charge", "dispute",
        ],
        "content": (
            "CloudDash Refund Policy:\n"
            "- Full refund available within 14 days of initial subscription\n"
            "- Prorated refund for annual plans cancelled within 30 days\n"
            "- No refund for monthly plans past the current billing cycle\n"
            "- Double charges or billing errors: full refund processed within 5-7 business days\n\n"
            "To request a refund:\n"
            "1. Go to Settings > Billing > Billing History\n"
            "2. Find the charge in question and click 'Dispute Charge'\n"
            "3. Select a reason and provide details\n"
            "4. Our billing team will review within 2 business days\n\n"
            "For double charges or obvious billing errors, contact support directly "
            "for expedited processing. Please include your account email and the "
            "transaction ID from your billing statement."
        ),
        "solution_steps": [
            "settings",
            "billing",
            "billing history",
            "dispute charge",
            "select reason",
            "contact support for billing errors",
        ],
    },
    "KB007": {
        "id": "KB007",
        "title": "Dashboard Not Loading - Troubleshooting Steps",
        "category": "Technical",
        "keywords": [
            "dashboard", "not loading", "blank screen", "white screen",
            "loading", "stuck", "won't load", "empty", "broken",
            "cache", "browser", "clear cache",
        ],
        "content": (
            "If your CloudDash dashboard isn't loading, try these steps:\n\n"
            "Step 1: Clear Browser Cache\n"
            "- Press Ctrl+Shift+R (Cmd+Shift+R on Mac) for a hard refresh\n"
            "- Or clear browser cache: Settings > Privacy > Clear Browsing Data\n\n"
            "Step 2: Try Incognito/Private Mode\n"
            "- Open a new incognito window and navigate to app.clouddash.io\n"
            "- If it works in incognito, a browser extension is likely interfering\n\n"
            "Step 3: Try a Different Browser\n"
            "- CloudDash supports Chrome 90+, Firefox 88+, Safari 14+, Edge 90+\n\n"
            "Step 4: Check Data Source Connections\n"
            "- Go to Settings > Data Sources and verify all sources show 'Connected'\n"
            "- Reconnect any sources showing 'Disconnected' or 'Error'\n\n"
            "Step 5: Check CloudDash Status Page\n"
            "- Visit status.clouddash.io for any ongoing incidents\n\n"
            "If none of these work, contact support with: browser name/version, "
            "error messages (if any), and when the issue started."
        ),
        "solution_steps": [
            "clear browser cache",
            "hard refresh",
            "ctrl+shift+r",
            "try incognito",
            "try different browser",
            "check data source connections",
            "check status page",
        ],
    },
    "KB008": {
        "id": "KB008",
        "title": "Configuring Data Source Connections",
        "category": "Technical",
        "keywords": [
            "data source", "connection", "connect", "configure", "database",
            "api", "integration", "aws", "gcp", "azure", "postgresql",
            "mysql", "mongodb", "prometheus", "grafana",
        ],
        "content": (
            "CloudDash supports these data sources:\n"
            "- Databases: PostgreSQL, MySQL, MongoDB, Redis\n"
            "- Cloud: AWS CloudWatch, GCP Monitoring, Azure Monitor\n"
            "- Metrics: Prometheus, Datadog, New Relic\n"
            "- Custom: REST API endpoints, Webhooks\n\n"
            "To add a new data source:\n"
            "1. Go to Settings > Data Sources > Add New\n"
            "2. Select the source type\n"
            "3. Enter connection credentials (host, port, auth)\n"
            "4. Click 'Test Connection' to verify\n"
            "5. Click 'Save' once the test passes\n\n"
            "Common connection issues:\n"
            "- Firewall blocking: Add CloudDash IP range 203.0.113.0/24 to allowlist\n"
            "- Auth failures: Verify credentials and ensure the user has read permissions\n"
            "- Timeout: Check if the data source is accessible from the public internet"
        ),
        "solution_steps": [
            "settings",
            "data sources",
            "add new",
            "select source type",
            "enter credentials",
            "test connection",
            "save",
        ],
    },
    "KB009": {
        "id": "KB009",
        "title": "Setting Up Alert Rules and Notifications",
        "category": "Technical",
        "keywords": [
            "alert", "notification", "alarm", "threshold", "trigger",
            "email alert", "slack alert", "pagerduty", "monitoring",
            "alert not firing", "alert rules",
        ],
        "content": (
            "To set up alerts in CloudDash:\n"
            "1. Navigate to Alerts > Create New Alert\n"
            "2. Select the metric to monitor (e.g., CPU usage, error rate)\n"
            "3. Set the condition: above/below threshold, percentage change\n"
            "4. Set the threshold value (e.g., CPU > 90%)\n"
            "5. Configure notification channels: Email, Slack, PagerDuty, Webhook\n"
            "6. Set alert frequency: check every 1/5/15 minutes\n"
            "7. Click 'Save Alert'\n\n"
            "Troubleshooting alerts not firing:\n"
            "- Verify the metric is receiving data (check Data Sources)\n"
            "- Check alert is enabled (Alerts > click alert > toggle 'Active')\n"
            "- Verify threshold hasn't been accidentally changed\n"
            "- Confirm notification channel is configured correctly\n"
            "- Check if alert was silenced or in a maintenance window\n\n"
            "Note: Alert thresholds may need reconfiguration after a plan change "
            "if the metric frequency changed (Basic: 15min, Pro: 5min, Enterprise: 1min)."
        ),
        "solution_steps": [
            "alerts",
            "create new alert",
            "select metric",
            "set threshold",
            "configure notification",
            "check alert is active",
            "verify threshold",
        ],
    },
    "KB010": {
        "id": "KB010",
        "title": "API Authentication and Rate Limits",
        "category": "Technical",
        "keywords": [
            "api", "authentication", "rate limit", "api key", "token",
            "403", "429", "unauthorized", "forbidden", "rate exceeded",
            "api error", "500 error", "api access",
        ],
        "content": (
            "CloudDash API Authentication:\n"
            "- API access requires Pro plan or higher\n"
            "- Generate API keys at Settings > API > Generate New Key\n"
            "- Include the key in the X-CloudDash-API-Key header\n"
            "- Keys can be scoped to read-only or read-write\n\n"
            "Rate Limits:\n"
            "- Pro plan: 1,000 requests/hour\n"
            "- Enterprise plan: 10,000 requests/hour\n"
            "- Rate limit headers: X-RateLimit-Remaining, X-RateLimit-Reset\n\n"
            "Common API errors:\n"
            "- 401 Unauthorized: Invalid or missing API key\n"
            "- 403 Forbidden: API access not included in your plan, or key doesn't "
            "have required scope\n"
            "- 429 Too Many Requests: Rate limit exceeded, retry after the time "
            "specified in Retry-After header\n"
            "- 500 Internal Server Error: Check status.clouddash.io; if no incident, "
            "verify your request payload format\n\n"
            "After a plan upgrade/downgrade, existing API keys remain valid but "
            "their rate limits change immediately. If you downgrade to Basic, "
            "API access is disabled and all keys return 403. Re-upgrading to Pro "
            "reactivates existing keys automatically."
        ),
        "solution_steps": [
            "settings",
            "api",
            "generate new key",
            "x-clouddash-api-key header",
            "check plan includes api access",
            "check rate limits",
            "regenerate api key",
        ],
    },
    "KB011": {
        "id": "KB011",
        "title": "Resolving Data Sync Delays",
        "category": "Technical",
        "keywords": [
            "sync", "delay", "stale data", "not updating", "real-time",
            "data lag", "outdated", "refresh", "data sync", "latency",
        ],
        "content": (
            "Data sync intervals depend on your plan:\n"
            "- Basic: Every 15 minutes\n"
            "- Pro: Every 5 minutes\n"
            "- Enterprise: Every 1 minute (near real-time)\n\n"
            "If data appears stale beyond your plan's sync interval:\n"
            "1. Check data source connection: Settings > Data Sources > verify 'Connected'\n"
            "2. Force a manual sync: click 'Sync Now' on the data source page\n"
            "3. Check the source API rate limits: CloudDash may be throttled by the source\n"
            "4. Verify the source is actively producing data (check source's own dashboard)\n"
            "5. Check for CloudDash incidents at status.clouddash.io\n\n"
            "For real-time requirements, consider:\n"
            "- Upgrading to Enterprise for 1-minute sync intervals\n"
            "- Using the webhook data source for push-based updates\n"
            "- Configuring CloudDash streaming mode (Enterprise only)"
        ),
        "solution_steps": [
            "check data source connection",
            "force manual sync",
            "sync now",
            "check source api rate limits",
            "verify source is producing data",
            "check status page",
            "consider upgrade for faster sync",
        ],
    },
    "KB012": {
        "id": "KB012",
        "title": "Custom Dashboard Widgets Guide",
        "category": "Features",
        "keywords": [
            "widget", "custom", "dashboard", "chart", "graph", "table",
            "visualization", "create widget", "drag and drop",
        ],
        "content": (
            "CloudDash offers these widget types:\n"
            "- Line Chart: time-series data trends\n"
            "- Bar Chart: categorical comparisons\n"
            "- Gauge: single metric with thresholds\n"
            "- Table: raw data display\n"
            "- Stat: single number with change indicator\n"
            "- Heatmap: correlation or activity patterns\n\n"
            "To add a widget:\n"
            "1. Open a dashboard and click 'Add Widget'\n"
            "2. Select the widget type\n"
            "3. Choose the data source and metric\n"
            "4. Configure display options (title, colors, thresholds)\n"
            "5. Drag to resize and position on the dashboard\n"
            "6. Click 'Save Dashboard'\n\n"
            "Widget queries support aggregation functions: avg, sum, min, max, count, "
            "percentile. Use the query editor for complex queries with GROUP BY and WHERE clauses."
        ),
        "solution_steps": [
            "open dashboard",
            "add widget",
            "select widget type",
            "choose data source",
            "configure display",
            "save dashboard",
        ],
    },
    "KB013": {
        "id": "KB013",
        "title": "Exporting Reports and Data",
        "category": "Features",
        "keywords": [
            "export", "report", "download", "csv", "pdf", "data export",
            "scheduled report", "email report",
        ],
        "content": (
            "CloudDash supports multiple export options:\n\n"
            "Manual Export:\n"
            "1. Open the dashboard you want to export\n"
            "2. Click the 'Export' button in the top-right corner\n"
            "3. Choose format: PDF (visual), CSV (raw data), or PNG (image)\n"
            "4. Select date range for the data\n"
            "5. Click 'Download'\n\n"
            "Scheduled Reports (Pro and Enterprise):\n"
            "1. Go to Reports > Scheduled Reports > Create New\n"
            "2. Select dashboards to include\n"
            "3. Choose frequency: Daily, Weekly, or Monthly\n"
            "4. Add recipient email addresses\n"
            "5. Click 'Schedule'\n\n"
            "API Export (Pro and Enterprise):\n"
            "Use the /api/v1/export endpoint with your API key to "
            "programmatically export data in JSON or CSV format."
        ),
        "solution_steps": [
            "open dashboard",
            "click export",
            "choose format",
            "select date range",
            "download",
            "scheduled reports",
        ],
    },
    "KB014": {
        "id": "KB014",
        "title": "CloudDash Uptime SLA and Status Page",
        "category": "Policies",
        "keywords": [
            "sla", "uptime", "status", "downtime", "outage", "incident",
            "availability", "service level", "status page",
        ],
        "content": (
            "CloudDash Service Level Agreement:\n"
            "- Basic plan: 99.5% uptime SLA\n"
            "- Pro plan: 99.9% uptime SLA\n"
            "- Enterprise plan: 99.99% uptime SLA with dedicated support\n\n"
            "Uptime is measured monthly, excluding scheduled maintenance windows "
            "(announced 48 hours in advance). If SLA is breached, eligible customers "
            "receive service credits:\n"
            "- 99.0-99.5%: 10% credit\n"
            "- 95.0-99.0%: 25% credit\n"
            "- Below 95.0%: 50% credit\n\n"
            "Check real-time status at status.clouddash.io. Subscribe to incident "
            "notifications via email or RSS. For Enterprise customers, dedicated "
            "status updates are available through your account manager."
        ),
        "solution_steps": [
            "check status.clouddash.io",
            "subscribe to incident notifications",
            "contact account manager for enterprise",
            "request sla credit",
        ],
    },
    "KB015": {
        "id": "KB015",
        "title": "Escalation Policy and Priority Levels",
        "category": "Policies",
        "keywords": [
            "escalation", "priority", "urgent", "critical", "escalate",
            "manager", "supervisor", "sla response time", "p1", "p2",
        ],
        "content": (
            "CloudDash Support Priority Levels:\n"
            "- P1 Critical: Service completely unavailable, affecting production\n"
            "  Response: 15 min (Enterprise), 1 hour (Pro), 4 hours (Basic)\n"
            "- P2 High: Major feature degraded, workaround available\n"
            "  Response: 1 hour (Enterprise), 4 hours (Pro), 8 hours (Basic)\n"
            "- P3 Medium: Minor issue, minimal business impact\n"
            "  Response: 4 hours (Enterprise), 8 hours (Pro), 24 hours (Basic)\n"
            "- P4 Low: General questions, feature requests\n"
            "  Response: 24 hours (all plans)\n\n"
            "When to escalate a ticket:\n"
            "- Billing disputes involving incorrect charges > $50\n"
            "- Security incidents (unauthorized access, data breach)\n"
            "- Issues affecting multiple customers\n"
            "- Unresolved P1/P2 issues beyond SLA response time\n"
            "- Customer explicitly requests escalation to management"
        ),
        "solution_steps": [
            "assess priority level",
            "check sla response time",
            "escalate for billing disputes",
            "escalate for security incidents",
            "contact account manager",
        ],
    },
}


def search_knowledge_base(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """Search KB articles using keyword matching. Returns top_k results."""
    if not query or not query.strip():
        return []

    query_tokens = set(query.lower().split())

    scores: List[tuple] = []
    for article_id, article in KB_ARTICLES.items():
        score = 0.0

        # Match against keywords (highest weight)
        for kw in article["keywords"]:
            kw_tokens = set(kw.lower().split())
            if kw_tokens.issubset(query_tokens):
                score += 3.0  # exact keyword phrase match
            elif kw_tokens & query_tokens:
                score += 1.5  # partial keyword match

        # Match against title words
        title_tokens = set(article["title"].lower().split())
        score += len(query_tokens & title_tokens) * 2.0

        # Match against content words (lower weight)
        content_tokens = set(article["content"].lower().split())
        score += len(query_tokens & content_tokens) * 0.3

        if score > 0:
            scores.append((article_id, score))

    scores.sort(key=lambda x: -x[1])

    results = []
    for article_id, score in scores[:top_k]:
        a = KB_ARTICLES[article_id]
        results.append(
            {
                "id": a["id"],
                "title": a["title"],
                "category": a["category"],
                "relevance_score": round(score, 2),
                "content_snippet": a["content"][:400],
                "solution_steps": a["solution_steps"],
            }
        )
    return results
