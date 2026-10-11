# Incident Response Simulator
> *"Every Decision Changes the Incident"*

An interactive, consequence-driven cybersecurity defensive simulator built for Tier-1 SOC analysts and collegiate incident response training.

---

## Key Capabilities
- **Operator Access Gateway:** Role-based analyst email and session authentication gate.
- **Live Operations Deck:** Dual circular speedometers (76% Threat Severity, 92% System Health), 3D isometric attack topology canvas, and live alert telemetry meters.
- **Scenario State Machine:** Real-world incident modeling (*Operation Silent Login* & *Phishing Attack*) incorporating Event ID 4625 brute force alerts, RDP logon triage, and in-memory execution containment.
- **RFC 3227 Volatile Memory Preservation:** Demonstrates the trade-offs between abrupt power disruption and software-defined host isolation.
- **Executive Scorecard:** Dark-mode debrief featuring an 86% efficiency summary ring, a 5-axis pentagon competency radar chart, and financial SLA downtime impact metrics.
- **Desktop Companion Launcher:** Standalone Python GUI built with `tkinter` and `IR info.html` integration.

---

## Technology Stack
- **Backend:** Python, FastAPI, Uvicorn ASGI, SQLAlchemy 2.0, SQLite
- **Frontend:** React 18 (Babel standalone), Tailwind CSS, Native Scalable Vector Graphics (SVG)
- **Desktop GUI:** Python Tkinter

---

## Quick Start

### 1. Web Operations Deck
```bash
pip install -r requirements.txt
uvicorn app:app --port 8000 --reload