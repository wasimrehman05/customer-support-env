from typing import Dict, List, Any


TICKETS: Dict[str, Dict[str, Any]] = {
    # =========================================================================
    # TASK 1: FAQ Resolution (Easy) — 4 tickets
    # Agent: search KB -> find article -> send solution
    # =========================================================================
    "T1-01": {
        "task_id": "faq_resolution",
        "ticket_id": "T1-01",
        "customer_name": "Sarah Chen",
        "issue": (
            "Hi, I forgot my password and can't log in to CloudDash. "
            "I've tried a few times and now it seems locked. "
            "How do I reset it?"
        ),
        "priority": "low",
        "category": "Account",
        "correct_kb_ids": ["KB001"],
        "diagnosis_keywords": [],
        "solution_keywords": [
            "forgot password",
            "reset link",
            "check email",
            "new password",
        ],
        "clarification_qa": {},
        "should_escalate": False,
        "max_steps": 8,
        "max_achievable_reward": 0.50,
    },
    "T1-02": {
        "task_id": "faq_resolution",
        "ticket_id": "T1-02",
        "customer_name": "David Park",
        "issue": (
            "I need to download some data from my dashboards as a CSV. "
            "Is there a way to export reports from CloudDash?"
        ),
        "priority": "low",
        "category": "Features",
        "correct_kb_ids": ["KB013"],
        "diagnosis_keywords": [],
        "solution_keywords": [
            "export",
            "csv",
            "download",
            "date range",
        ],
        "clarification_qa": {},
        "should_escalate": False,
        "max_steps": 8,
        "max_achievable_reward": 0.50,
    },
    "T1-03": {
        "task_id": "faq_resolution",
        "ticket_id": "T1-03",
        "customer_name": "Aisha Mohammed",
        "issue": (
            "I want to add an extra layer of security to my account. "
            "How do I enable two-factor authentication?"
        ),
        "priority": "low",
        "category": "Account",
        "correct_kb_ids": ["KB002"],
        "diagnosis_keywords": [],
        "solution_keywords": [
            "settings",
            "security",
            "two-factor",
            "authenticator",
            "qr code",
            "backup recovery codes",
        ],
        "clarification_qa": {},
        "should_escalate": False,
        "max_steps": 8,
        "max_achievable_reward": 0.50,
    },
    "T1-04": {
        "task_id": "faq_resolution",
        "ticket_id": "T1-04",
        "customer_name": "Tom Baker",
        "issue": (
            "I was charged this month but I thought I cancelled. "
            "Can I get a refund? What's your refund policy?"
        ),
        "priority": "medium",
        "category": "Billing",
        "correct_kb_ids": ["KB006"],
        "diagnosis_keywords": [],
        "solution_keywords": [
            "refund",
            "billing history",
            "dispute charge",
            "14 days",
            "billing team",
        ],
        "clarification_qa": {},
        "should_escalate": False,
        "max_steps": 8,
        "max_achievable_reward": 0.50,
    },
    # =========================================================================
    # TASK 2: Troubleshooting (Medium) — 4 tickets
    # Agent: ask clarifying Qs -> diagnose -> search KB -> solve
    # =========================================================================
    "T2-01": {
        "task_id": "troubleshooting",
        "ticket_id": "T2-01",
        "customer_name": "James Wilson",
        "issue": (
            "My dashboard isn't loading at all. I just see a blank white "
            "screen. This is urgent — I need it for a meeting in 2 hours."
        ),
        "priority": "high",
        "category": "Technical",
        "correct_kb_ids": ["KB007"],
        "diagnosis_keywords": [
            "cache",
            "browser",
            "extension",
        ],
        "solution_keywords": [
            "clear cache",
            "hard refresh",
            "incognito",
            "try different browser",
            "disable extensions",
        ],
        "clarification_qa": {
            "browser": (
                "I'm using Chrome version 120 on Windows 11."
            ),
            "error": (
                "No error message, just a completely white screen. "
                "The URL bar shows the correct address."
            ),
            "when": (
                "It started about 2 hours ago. It was working fine this morning."
            ),
            "device": (
                "Actually, I just tried on my phone and it works fine there!"
            ),
            "extension": (
                "I do have a few extensions — an ad blocker and a dark mode extension."
            ),
        },
        "should_escalate": False,
        "max_steps": 12,
        "max_achievable_reward": 0.90,
    },
    "T2-02": {
        "task_id": "troubleshooting",
        "ticket_id": "T2-02",
        "customer_name": "Priya Patel",
        "issue": (
            "The data on my monitoring dashboard isn't updating. "
            "It's showing metrics from hours ago. We rely on this for "
            "real-time production monitoring."
        ),
        "priority": "high",
        "category": "Technical",
        "correct_kb_ids": ["KB011"],
        "diagnosis_keywords": [
            "sync",
            "data source",
            "rate limit",
            "plan",
        ],
        "solution_keywords": [
            "check data source connection",
            "sync now",
            "force manual sync",
            "check source api",
            "verify source is producing data",
        ],
        "clarification_qa": {
            "plan": (
                "We're on the Pro plan, so it should update every 5 minutes."
            ),
            "data source": (
                "We use AWS CloudWatch as our primary data source. "
                "All other tools show fresh data from AWS."
            ),
            "when": (
                "I noticed it about 3 hours ago. Last good data point "
                "is from 10:30 AM."
            ),
            "change": (
                "Nothing changed on our end. No config changes recently."
            ),
            "other dashboards": (
                "Actually, some dashboards work fine. It's specifically "
                "the AWS CloudWatch ones that are stale."
            ),
        },
        "should_escalate": False,
        "max_steps": 12,
        "max_achievable_reward": 0.90,
    },
    "T2-03": {
        "task_id": "troubleshooting",
        "ticket_id": "T2-03",
        "customer_name": "Carlos Rivera",
        "issue": (
            "My alert rules stopped firing. I had CPU alerts set up "
            "and they were working last week, but now nothing triggers "
            "even when CPU goes above 90%."
        ),
        "priority": "medium",
        "category": "Technical",
        "correct_kb_ids": ["KB009"],
        "diagnosis_keywords": [
            "alert",
            "threshold",
            "plan change",
            "metric frequency",
        ],
        "solution_keywords": [
            "check alert is active",
            "verify threshold",
            "check metric",
            "reconfigure",
            "notification channel",
        ],
        "clarification_qa": {
            "plan": (
                "We recently downgraded from Enterprise to Pro last week "
                "to save costs."
            ),
            "alert config": (
                "The alert was set to trigger when CPU > 90% checked "
                "every 1 minute."
            ),
            "change": (
                "Just the plan downgrade from Enterprise to Pro. "
                "I didn't change any alert settings."
            ),
            "notification": (
                "We use Slack notifications. The Slack integration seems "
                "to work fine for other things."
            ),
        },
        "should_escalate": False,
        "max_steps": 12,
        "max_achievable_reward": 0.90,
    },
    "T2-04": {
        "task_id": "troubleshooting",
        "ticket_id": "T2-04",
        "customer_name": "Emily Nguyen",
        "issue": (
            "Our application that integrates with the CloudDash API "
            "started getting 403 Forbidden errors today. Nothing changed "
            "on our side. This is breaking our automated monitoring pipeline."
        ),
        "priority": "high",
        "category": "Technical",
        "correct_kb_ids": ["KB010"],
        "diagnosis_keywords": [
            "api key",
            "plan",
            "403",
            "forbidden",
        ],
        "solution_keywords": [
            "check plan includes api access",
            "regenerate api key",
            "check rate limits",
            "settings",
            "api",
        ],
        "clarification_qa": {
            "plan": (
                "We were on Pro, but our billing person changed our plan "
                "yesterday. I'm not sure what we're on now."
            ),
            "api key": (
                "We're using the same API key we generated 3 months ago. "
                "It's been working fine until today."
            ),
            "endpoint": (
                "We call the /api/v1/metrics endpoint to pull dashboard data. "
                "Every single call returns 403."
            ),
            "error details": (
                "The response body says: 'API access is not available on "
                "your current plan. Please upgrade to Pro or Enterprise.'"
            ),
        },
        "should_escalate": False,
        "max_steps": 12,
        "max_achievable_reward": 0.90,
    },
    # =========================================================================
    # TASK 3: Complex / Escalation (Hard) — 3 tickets
    # Agent: decompose multi-issue, solve some, escalate others
    # =========================================================================
    "T3-01": {
        "task_id": "complex_escalation",
        "ticket_id": "T3-01",
        "customer_name": "Maria Rodriguez",
        "issue": (
            "I have multiple urgent problems after upgrading from Basic to Pro "
            "last week:\n"
            "1) I was charged TWICE — $29 for Basic AND $79 for Pro on the same day\n"
            "2) None of my 12 team members can access the dashboard anymore — "
            "they all get 'Permission Denied'\n"
            "3) Our API integration started returning 500 errors since the upgrade\n\n"
            "This is affecting our production monitoring. Please help ASAP."
        ),
        "priority": "critical",
        "category": "Multiple",
        "correct_kb_ids": ["KB005", "KB003", "KB010"],
        "sub_issues": [
            {
                "id": "billing",
                "description": "Double charged on upgrade",
                "keywords": ["billing", "charge", "refund", "double", "overcharged"],
                "needs_escalation": True,
            },
            {
                "id": "permissions",
                "description": "Team permissions reset after upgrade",
                "keywords": ["permission", "team", "access", "role", "denied"],
                "needs_escalation": False,
            },
            {
                "id": "api_errors",
                "description": "API 500 errors after plan change",
                "keywords": ["api", "error", "500", "key", "regenerate"],
                "needs_escalation": False,
            },
        ],
        "diagnosis_keywords": [
            "plan migration",
            "permissions reset",
            "api key",
            "billing dispute",
        ],
        "solution_keywords": [
            "escalate billing",
            "reassign permissions",
            "team management",
            "regenerate api key",
            "api settings",
            "refund",
        ],
        "clarification_qa": {
            "billing": (
                "I was charged $29 on March 1st and then $79 on the same day "
                "when I upgraded. I should only have been charged the prorated $79."
            ),
            "team": (
                "All 12 members now show as 'Viewer' role. They were all "
                "'Editor' or 'Admin' before the upgrade."
            ),
            "api": (
                "We're using API v2 with key-based auth. The 500 errors "
                "started immediately after the upgrade went through."
            ),
            "timeline": (
                "The upgrade happened last Tuesday. The API errors started "
                "within minutes. The team access issues were noticed the "
                "next morning."
            ),
        },
        "should_escalate": True,
        "max_steps": 15,
        "max_achievable_reward": 1.15,
    },
    "T3-02": {
        "task_id": "complex_escalation",
        "ticket_id": "T3-02",
        "customer_name": "Alex Kim",
        "issue": (
            "URGENT: We have an executive presentation in 2 hours and "
            "multiple things are broken:\n"
            "1) Dashboard is extremely slow — pages take 30+ seconds to load\n"
            "2) The revenue chart widget is showing completely wrong numbers "
            "(showing $0 for this month when it should be ~$2M)\n"
            "3) The scheduled report that should have been emailed to our "
            "VP this morning never arrived\n\n"
            "We're on Enterprise plan. This needs immediate attention."
        ),
        "priority": "critical",
        "category": "Multiple",
        "correct_kb_ids": ["KB007", "KB012", "KB013"],
        "sub_issues": [
            {
                "id": "performance",
                "description": "Dashboard extremely slow",
                "keywords": ["slow", "performance", "loading", "cache", "browser"],
                "needs_escalation": False,
            },
            {
                "id": "wrong_data",
                "description": "Revenue widget showing wrong numbers",
                "keywords": ["widget", "wrong", "data", "revenue", "aggregation", "configure"],
                "needs_escalation": False,
            },
            {
                "id": "report",
                "description": "Scheduled report not delivered",
                "keywords": ["report", "scheduled", "email", "delivery", "recipient"],
                "needs_escalation": False,
            },
        ],
        "diagnosis_keywords": [
            "cache",
            "widget configuration",
            "aggregation",
            "scheduled report",
            "email delivery",
        ],
        "solution_keywords": [
            "clear cache",
            "hard refresh",
            "check widget data source",
            "reconfigure widget",
            "check aggregation settings",
            "verify report recipients",
            "check scheduled reports",
        ],
        "clarification_qa": {
            "browser": (
                "Using Chrome on a MacBook Pro. It's slow on all browsers actually."
            ),
            "widget": (
                "The revenue chart is connected to our PostgreSQL data source. "
                "The data in PostgreSQL is correct — I checked."
            ),
            "report": (
                "The report was scheduled to go to vp@company.com at 8 AM daily. "
                "I set it up last month and it worked fine until 3 days ago."
            ),
            "changes": (
                "Our data team ran a database migration 3 days ago that changed "
                "some column names. Could that be related?"
            ),
        },
        "should_escalate": False,
        "max_steps": 15,
        "max_achievable_reward": 1.15,
    },
    "T3-03": {
        "task_id": "complex_escalation",
        "ticket_id": "T3-03",
        "customer_name": "Rachel Foster",
        "issue": (
            "We have a compliance audit tomorrow and I need help with "
            "several things:\n"
            "1) A new team member (john@company.com) received an invitation "
            "but gets 'Invalid Invitation Link' when trying to join\n"
            "2) A former employee (mike@company.com) still has Admin access "
            "and needs to be removed immediately — this is a security concern\n"
            "3) I need to export our complete audit log for the past 6 months "
            "for the compliance review — how do I do this?\n\n"
            "The audit is at 9 AM tomorrow. I need all three resolved today."
        ),
        "priority": "high",
        "category": "Multiple",
        "correct_kb_ids": ["KB003", "KB013"],
        "sub_issues": [
            {
                "id": "invitation",
                "description": "New member invitation link not working",
                "keywords": ["invitation", "invite", "link", "join", "new member"],
                "needs_escalation": False,
            },
            {
                "id": "security",
                "description": "Former employee still has admin access",
                "keywords": ["remove", "revoke", "admin", "former", "security", "access"],
                "needs_escalation": False,
            },
            {
                "id": "audit",
                "description": "Need to export audit logs for compliance",
                "keywords": ["audit", "export", "log", "compliance", "report", "6 months"],
                "needs_escalation": False,
            },
        ],
        "diagnosis_keywords": [
            "expired invitation",
            "resend invite",
            "remove member",
            "audit log export",
        ],
        "solution_keywords": [
            "resend invitation",
            "team management",
            "remove from team",
            "revoke access",
            "export",
            "audit log",
            "reports",
        ],
        "clarification_qa": {
            "invitation": (
                "The invitation was sent about 2 weeks ago. John hasn't "
                "been able to join since then."
            ),
            "former employee": (
                "Mike left the company a month ago. His corporate email "
                "has been deactivated but he might still have the password."
            ),
            "audit": (
                "We need all user activity: logins, data access, configuration "
                "changes, and API usage from October through March."
            ),
            "plan": (
                "We're on the Pro plan."
            ),
        },
        "should_escalate": False,
        "max_steps": 15,
        "max_achievable_reward": 1.15,
    },
}


TASK_TICKETS: Dict[str, List[str]] = {
    "faq_resolution": ["T1-01", "T1-02", "T1-03", "T1-04"],
    "troubleshooting": ["T2-01", "T2-02", "T2-03", "T2-04"],
    "complex_escalation": ["T3-01", "T3-02", "T3-03"],
}
