from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
from datetime import datetime
import os, json

DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    badge_id = Column(String, default="TRAINEE-01")
    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    detection_score = Column(Float, default=70.0)
    investigation_score = Column(Float, default=65.0)
    containment_score = Column(Float, default=50.0)
    evidence_score = Column(Float, default=60.0)
    decision_score = Column(Float, default=65.0)
    communication_score = Column(Float, default=60.0)
    weakest_skill = Column(String, default="Incident Containment")
    recommended_scenario = Column(String, default="Operation Silent Login")
    created_at = Column(DateTime, default=datetime.utcnow)
    sessions = relationship("SimulationSession", back_populates="user")
    results = relationship("SimulationResult", back_populates="user")

class SimulationSession(Base):
    __tablename__ = "simulation_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    scenario_id = Column(String, default="SCN-001")
    current_phase = Column(Integer, default=0)
    threat_severity = Column(Integer, default=76)
    system_health = Column(Integer, default=74)
    simulated_cost = Column(Integer, default=125000)
    simulated_downtime = Column(Float, default=0.2)
    is_contained = Column(Boolean, default=False)
    is_failed = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    discovered_evidence = Column(Text, default="[]")
    decision_history = Column(Text, default="[]")
    terminal_history = Column(Text, default="[]")
    hints_used = Column(Integer, default=0)
    elapsed_seconds = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="sessions")

class SimulationResult(Base):
    __tablename__ = "simulation_results"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user_email = Column(String)
    scenario_id = Column(String)
    scenario_title = Column(String)
    outcome = Column(String)
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
    decisions_audit = Column(Text)
    weakness_identified = Column(String)
    next_recommended_drill = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="results")

Base.metadata.create_all(bind=engine)

# Backward-compatible auto-migration for existing SQLite files
with engine.connect() as conn:
    for col, col_type in [
        ("decision_score", "FLOAT DEFAULT 65.0"),
        ("communication_score", "FLOAT DEFAULT 60.0"),
        ("weakest_skill", "VARCHAR DEFAULT 'Incident Containment'"),
        ("recommended_scenario", "VARCHAR DEFAULT 'Operation Silent Login'")
    ]:
        try:
            conn.execute(text(f"ALTER TABLE users ADD COLUMN {col} {col_type}"))
            conn.commit()
        except Exception:
            pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="Incident Response Simulator")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

SCENARIOS = {
    "SCN-001": {
        "id": "SCN-001",
        "title": "Operation Silent Login",
        "organization": "FinSecure Technologies Ltd.",
        "difficulty": "Intermediate",
        "incident_type": "Simulated Credential Compromise & Lateral Movement",
        "baseline_timeline": [
            {"time": "09:12 UTC", "desc": "12 failed authentication attempts against user 'jdoe@finsecure.com'."},
            {"time": "09:15 UTC", "desc": "Successful RDP logon from foreign ASN 14061 (185.220.101.4)."},
            {"time": "09:17 UTC", "desc": "Encoded PowerShell execution spawned under PID 4821."},
            {"time": "09:20 UTC", "desc": "Internal reconnaissance commands executed: whoami /groups, net user /domain."},
            {"time": "09:24 UTC", "desc": "LSASS memory handle requested; persistent service 'UpdateHealthSvc' created."},
            {"time": "09:28 UTC", "desc": "Outbound 4.8MB encrypted socket burst over TLS v1.3 to 185.220.101.4:443."}
        ],
        "evidence_store": {
            "ev_auth": {"id": "ev_auth", "name": "Windows Authentication Logs (Event 4624/4625)", "category": "Authentication", "tech": "Event ID 4625 x12 followed by Event ID 4624 Logon Type 10 at 09:15:20 UTC.", "plain": "12 incorrect password attempts before foreign interactive RDP login established.", "ioc": "185.220.101.4 (Bucharest, Romania)"},
            "ev_proc": {"id": "ev_proc", "name": "Sysmon Endpoint Process Tree", "category": "Endpoint EDR", "tech": "powershell.exe (PID 4821) -NoP -NonI -W Hidden -Enc SUVY(New-Object Net.WebClient)...", "plain": "Hidden PowerShell process establishing remote command-and-control connection.", "ioc": "SHA256: d8f4c2e68a3064e6ec4c311c1d6832dbfae431e15b5df8083818e19e917dcb6f"},
            "ev_net": {"id": "ev_net", "name": "Network Socket & Zeek Conn Telemetry", "category": "Network Traffic", "tech": "Outbound TCP socket 10.240.12.8:49211 -> 185.220.101.4:443 (4.8MB sent).", "plain": "Continuous encrypted channel transmitting staging files out to Romania.", "ioc": "Domain: c2-stage-finsecure.xyz"},
            "ev_user": {"id": "ev_user", "name": "Active Directory User Workstation Baseline", "category": "Identity Context", "tech": "Account: John Doe. Location: Atlanta, GA. Foreign login initiated at 04:15 EST.", "plain": "John is based in the US, but the account connected from Eastern Europe during sleep hours.", "ioc": "Impossible Travel Flag: Atlanta -> Bucharest in 18 mins"}
        },
        "phases": [
            {
                "phase_index": 0,
                "label": "Phase 1: Alert Triage & Initial Authentication Spike (09:12 - 09:15 UTC)",
                "context_tech": "SIEM correlates Event 4625 brute-force cluster followed by successful Logon Type 10 from 185.220.101.4. Select defensive action:",
                "context_plain": "Someone failed 12 passwords and logged into John Doe's computer from another country. What should we do?",
                "options": [
                    {
                        "id": "opt_triage_logs",
                        "label_tech": "Investigate Authentication Logs & User Geolocation Baseline",
                        "label_plain": "Inspect login history and check John Doe's usual work location",
                        "is_investigation_only": True,
                        "unlocked_evidence": ["ev_auth", "ev_user"],
                        "score_impact": {"detection": 20, "investigation": 25, "containment": 5, "evidence": 20, "decision": 15, "comm": 10},
                        "threat_delta": -5, "health_delta": 0, "cost_delta": 15000, "downtime_delta": 0.0,
                        "outcome_tech": "Evidence correlated: Foreign NTLM replay confirmed. Attacker actively holding interactive session.",
                        "outcome_plain": "Intruder verified: You confirmed John is in the US and this connection is malicious."
                    },
                    {
                        "id": "opt_immediate_revoke",
                        "label_tech": "Revoke Azure AD Sessions, Reset Password & Purge Kerberos TGT",
                        "label_plain": "Immediately kick the user account out and force a password reset",
                        "is_investigation_only": False,
                        "unlocked_evidence": ["ev_auth"],
                        "score_impact": {"detection": 15, "investigation": 10, "containment": 30, "evidence": 15, "decision": 25, "comm": 15},
                        "threat_delta": -25, "health_delta": 10, "cost_delta": 30000, "downtime_delta": 0.2,
                        "outcome_tech": "Optimal Containment: Session tokens revoked. Adversary RDP socket disconnected within 40 seconds.",
                        "outcome_plain": "Rapid containment: Attacker disconnected before lateral elevation was completed."
                    },
                    {
                        "id": "opt_ignore_alert",
                        "label_tech": "Suppress Alert as False Positive (Assume International Travel)",
                        "label_plain": "Ignore the alarm assuming John is on vacation in Europe",
                        "is_investigation_only": False,
                        "unlocked_evidence": [],
                        "score_impact": {"detection": 5, "investigation": 0, "containment": -35, "evidence": 0, "decision": -35, "comm": 0},
                        "threat_delta": 30, "health_delta": -35, "cost_delta": 450000, "downtime_delta": 6.0,
                        "outcome_tech": "Catastrophic Hesitation: Threat actor spawned encoded PowerShell and began dumping memory hashes.",
                        "outcome_plain": "Breach progressed: While you ignored the alarm, the intruder launched malicious scripts on the machine."
                    }
                ]
            },
            {
                "phase_index": 1,
                "label": "Phase 2: Process Execution & Persistence Staging (09:17 - 09:20 UTC)",
                "context_tech": "EDR flags Sysmon Event 1: Encoded PowerShell spawned by w3wp.exe establishing C2 beacon. Select containment action:",
                "context_plain": "The intruder is running hidden scripts attempting to spread to other company servers. How do we contain it?",
                "options": [
                    {
                        "id": "opt_edr_isolate",
                        "label_tech": "Enforce EDR Network Isolation (Preserve RFC 3227 Volatile RAM)",
                        "label_plain": "Isolate the computer from the network but keep power ON to preserve memory",
                        "is_investigation_only": False,
                        "unlocked_evidence": ["ev_proc", "ev_net"],
                        "score_impact": {"detection": 20, "investigation": 20, "containment": 35, "evidence": 25, "decision": 25, "comm": 15},
                        "threat_delta": -35, "health_delta": 25, "cost_delta": 45000, "downtime_delta": 0.5,
                        "outcome_tech": "NIST SP 800-61r2 Standard Met: Workstation quarantined. C2 severed. Memory dump preserved for forensics.",
                        "outcome_plain": "Masterful containment: The infected host is isolated from others and RAM evidence is saved."
                    },
                    {
                        "id": "opt_hard_shutdown",
                        "label_tech": "Execute Hard Power Cut (Pull Physical Power Cord / Hard Reset)",
                        "label_plain": "Yank the power cord from the wall to instantly shut the machine down",
                        "is_investigation_only": False,
                        "unlocked_evidence": [],
                        "score_impact": {"detection": 15, "investigation": 5, "containment": 15, "evidence": -25, "decision": -15, "comm": 5},
                        "threat_delta": -15, "health_delta": -20, "cost_delta": 350000, "downtime_delta": 4.5,
                        "outcome_tech": "Forensic Destruction: Volatile RAM erased. Injected payload lost. Secondary persistence unverified.",
                        "outcome_plain": "Mistake: Pulling the plug killed the attack, but completely wiped RAM memory evidence."
                    },
                    {
                        "id": "opt_passive_sniff",
                        "label_tech": "Passively Monitor Attacker to Trace Remote C2 IP Infrastructure",
                        "label_plain": "Wait and watch what the hacker does to learn their methods",
                        "is_investigation_only": False,
                        "unlocked_evidence": ["ev_net"],
                        "score_impact": {"detection": 10, "investigation": 10, "containment": -35, "evidence": 5, "decision": -25, "comm": 0},
                        "threat_delta": 35, "health_delta": -40, "cost_delta": 850000, "downtime_delta": 10.0,
                        "outcome_tech": "Data Loss Event: Attacker exfiltrated 4.8MB of confidential wire transfer records over port 443.",
                        "outcome_plain": "Critical error: The attacker stole 42,000 banking customer records while you waited."
                    }
                ]
            }
        ]
    }
}

class AuthReq(BaseModel):
    email: str
    badge_id: Optional[str] = "TRAINEE-01"

class StartReq(BaseModel):
    email: str
    scenario_id: str

class DecisionReq(BaseModel):
    session_id: int
    option_id: str

class CliReq(BaseModel):
    session_id: int
    command: str

class HintReq(BaseModel):
    session_id: int
    tier: int

@app.get("/", response_class=HTMLResponse)
def index():
    path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/api/auth/login")
def login(req: AuthReq, db: Session = Depends(get_db)):
    em = req.email.strip().lower()
    user = db.query(User).filter(User.email == em).first()
    if not user:
        user = User(email=em, badge_id=req.badge_id)
        db.add(user)
        db.commit()
        db.refresh(user)
    
    results = db.query(SimulationResult).filter(SimulationResult.user_id == user.id).all()
    comp = len(results)
    avg = round(sum(r.overall_score for r in results) / comp, 1) if comp > 0 else 0.0
    best = max([r.overall_score for r in results], default=0)
    act = db.query(SimulationSession).filter(SimulationSession.user_id == user.id, SimulationSession.is_completed == False).first()

    return {
        "email": user.email, "badge_id": user.badge_id, "level": user.level, "xp": user.xp,
        "skills": {
            "threat_detection": user.detection_score, "investigation": user.investigation_score,
            "containment": user.containment_score, "evidence_handling": user.evidence_score,
            "decision_making": user.decision_score, "communication": user.communication_score
        },
        "weakest_skill": user.weakest_skill, "recommended_scenario": user.recommended_scenario,
        "stats": {"completed_simulations": comp, "average_score": avg, "best_score": best, "has_active_session": act is not None, "active_session_id": act.id if act else None}
    }

@app.get("/api/scenarios")
def scenarios():
    return [{"id": s["id"], "title": s["title"], "organization": s["organization"], "difficulty": s["difficulty"], "incident_type": s["incident_type"], "phase_count": len(s["phases"]), "timeline": s["baseline_timeline"]} for s in SCENARIOS.values()]

@app.post("/api/simulations/start")
def start_sim(req: StartReq, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email.strip().lower()).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.query(SimulationSession).filter(SimulationSession.user_id == user.id, SimulationSession.is_completed == False).delete()
    sess = SimulationSession(
        user_id=user.id, scenario_id=req.scenario_id,
        terminal_history=json.dumps(["SIMULATED FORENSIC CLI READY // Connected to FIN-GATEWAY-01", "Type 'help', 'netstat -ano', 'ps aux', 'history', or 'isolate-host'"])
    )
    db.add(sess)
    db.commit()
    db.refresh(sess)
    return get_state(sess)

@app.get("/api/simulations/session/{sid}")
def get_session(sid: int, db: Session = Depends(get_db)):
    sess = db.query(SimulationSession).filter(SimulationSession.id == sid).first()
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")
    return get_state(sess)

def get_state(sess: SimulationSession):
    scn = SCENARIOS[sess.scenario_id]
    discovered = json.loads(sess.discovered_evidence)
    evs = [scn["evidence_store"][k] for k in discovered if k in scn["evidence_store"]]
    active_phase = scn["phases"][sess.current_phase] if sess.current_phase < len(scn["phases"]) and not sess.is_completed else None
    return {
        "session_id": sess.id, "scenario_id": sess.scenario_id, "scenario_title": scn["title"], "organization": scn["organization"],
        "difficulty": scn["difficulty"], "current_phase": sess.current_phase, "total_phases": len(scn["phases"]),
        "threat_severity": sess.threat_severity, "system_health": sess.system_health, "simulated_cost": sess.simulated_cost,
        "simulated_downtime": sess.simulated_downtime, "is_contained": sess.is_contained, "is_completed": sess.is_completed,
        "hints_used": sess.hints_used, "active_phase_data": active_phase, "discovered_evidence": evs,
        "decision_history": json.loads(sess.decision_history), "terminal_history": json.loads(sess.terminal_history), "baseline_timeline": scn["baseline_timeline"]
    }

@app.post("/api/simulations/decide")
def decide(req: DecisionReq, db: Session = Depends(get_db)):
    sess = db.query(SimulationSession).filter(SimulationSession.id == req.session_id).first()
    if not sess or sess.is_completed:
        raise HTTPException(status_code=400, detail="Invalid session or simulation already completed")

    scn = SCENARIOS[sess.scenario_id]
    phase = scn["phases"][sess.current_phase]
    opt = next((o for o in phase["options"] if o["id"] == req.option_id), None)
    if not opt:
        raise HTTPException(status_code=400, detail="Invalid decision option for this stage")

    # Guard against repeating the same decision
    d_list = json.loads(sess.decision_history)
    if any(d.get("option_id") == opt["id"] for d in d_list):
        raise HTTPException(status_code=400, detail="Action already executed in this drill")

    sess.threat_severity = max(5, min(99, sess.threat_severity + opt["threat_delta"]))
    sess.system_health = max(5, min(99, sess.system_health + opt["health_delta"]))
    sess.simulated_cost += opt["cost_delta"]
    sess.simulated_downtime = round(sess.simulated_downtime + opt["downtime_delta"], 2)

    ev_list = json.loads(sess.discovered_evidence)
    for e in opt["unlocked_evidence"]:
        if e not in ev_list: ev_list.append(e)
    sess.discovered_evidence = json.dumps(ev_list)

    d_list.append({
        "option_id": opt["id"],
        "label_tech": opt["label_tech"], "label_plain": opt["label_plain"],
        "outcome_tech": opt["outcome_tech"], "outcome_plain": opt["outcome_plain"],
        "impact": opt["score_impact"], "cost": opt["cost_delta"], "downtime": opt["downtime_delta"],
        "timestamp": datetime.utcnow().strftime("%H:%M:%S UTC")
    })
    sess.decision_history = json.dumps(d_list)

    if opt["id"] in ["opt_immediate_revoke", "opt_edr_isolate"]:
        sess.is_contained = True

    # Advance phase only if containment/terminal decision was executed
    if not opt.get("is_investigation_only", False):
        if sess.current_phase + 1 < len(scn["phases"]) and opt["id"] != "opt_ignore_alert":
            sess.current_phase += 1
        else:
            sess.is_completed = True
            finalize(sess, db)

    db.commit()
    db.refresh(sess)
    return get_state(sess)

def finalize(sess: SimulationSession, db: Session):
    user = sess.user
    decisions = json.loads(sess.decision_history)
    det, inv, con, evi, dec, com = 70, 60, 50, 50, 60, 60
    for d in decisions:
        imp = d.get("impact", {})
        det = max(0, min(100, det + imp.get("detection", 0)))
        inv = max(0, min(100, inv + imp.get("investigation", 0)))
        con = max(0, min(100, con + imp.get("containment", 0)))
        evi = max(0, min(100, evi + imp.get("evidence", 0)))
        dec = max(0, min(100, dec + imp.get("decision", 0)))
        com = max(0, min(100, com + imp.get("comm", 0)))

    score = round((0.20*det) + (0.20*inv) + (0.25*con) + (0.15*evi) + (0.10*dec) + (0.10*com) - min(20, sess.hints_used * 5))
    score = max(5, min(100, score))
    outcome = "Excellent Containment" if score >= 80 else "Partial Containment" if score >= 60 else "Critical SLA Breach"
    weakness = "Incident Containment" if con < 65 else "Evidence Handling" if evi < 65 else "Threat Detection"

    res = SimulationResult(
        user_id=user.id, user_email=user.email, scenario_id=sess.scenario_id, scenario_title=SCENARIOS[sess.scenario_id]["title"],
        outcome=outcome, overall_score=score, detection_score=det, investigation_score=inv, containment_score=con,
        evidence_score=evi, decision_score=dec, communication_score=com, downtime_hours=sess.simulated_downtime,
        financial_cost=sess.simulated_cost, records_leaked=42000 if score < 50 else 0, mttr_seconds=sess.elapsed_seconds,
        hints_used=sess.hints_used, decisions_audit=sess.decision_history, weakness_identified=weakness, next_recommended_drill="Operation Silent Login — Host Isolation Drill"
    )
    db.add(res)
    user.xp += score * 15
    if user.xp >= user.level * 1000: user.level += 1
    user.containment_score = round(user.containment_score * 0.7 + con * 0.3, 1)
    user.investigation_score = round(user.investigation_score * 0.7 + inv * 0.3, 1)
    user.detection_score = round(user.detection_score * 0.7 + det * 0.3, 1)
    user.weakest_skill = weakness

@app.post("/api/simulations/cli")
def cli(req: CliReq, db: Session = Depends(get_db)):
    sess = db.query(SimulationSession).filter(SimulationSession.id == req.session_id).first()
    cmd = req.command.strip().lower()
    evs = json.loads(sess.discovered_evidence)
    out = f"Command '{req.command}' not recognized. Type 'help'."
    if cmd == "help": out = "Commands: netstat -ano, ps aux, history, isolate-host, clear"
    elif "netstat" in cmd:
        out = "Proto Local Foreign State PID\nTCP 0.0.0.0:443 0.0.0.0:0 LISTENING 4821\nTCP 10.240.12.8:49211 185.220.101.4:443 ESTABLISHED 4821 [C2 Channel]"
        if "ev_net" not in evs: evs.append("ev_net")
    elif "ps" in cmd:
        out = "PID COMMAND CPU% STATUS\n4821 powershell.exe -Enc 89.4% SUSPICIOUS C2 STAGER\n684 lsass.exe 0.1% SYSTEM"
        if "ev_proc" not in evs: evs.append("ev_proc")
    elif cmd == "history": out = "101 whoami /groups\n102 net user /domain\n103 schtasks /create /tn UpdateHealthSvc"
    elif cmd == "isolate-host":
        sess.is_contained = True
        sess.threat_severity = max(10, sess.threat_severity - 30)
        sess.system_health = min(95, sess.system_health + 20)
        out = "[EDR AGENT] FIN-GATEWAY-01 network quarantined. Telemetry preserved."
    elif cmd == "clear":
        sess.terminal_history = json.dumps(["CLI cleared."])
        db.commit()
        return {"output": "CLI cleared.", "terminal_history": ["CLI cleared."]}

    sess.discovered_evidence = json.dumps(evs)
    h = json.loads(sess.terminal_history)
    h.extend([f"$ {req.command}", out])
    sess.terminal_history = json.dumps(h)
    db.commit()
    return {"output": out, "terminal_history": h}

@app.post("/api/ai/hint")
def hint(req: HintReq, db: Session = Depends(get_db)):
    sess = db.query(SimulationSession).filter(SimulationSession.id == req.session_id).first()
    sess.hints_used += 1
    db.commit()
    hints = {
        0: {1: "Direction: Check authentication logs before touching the network.", 2: "Clue: Examine Event ID 4625 and compare John's normal Atlanta location.", 3: "Playbook: Revoke session tokens immediately via Microsoft Graph."},
        1: {1: "Direction: The attacker is attempting lateral movement. Contain host movement without destroying evidence.", 2: "Clue: Do not pull the physical plug; that wipes volatile RAM (RFC 3227).", 3: "Playbook: Apply EDR host isolation to sever C2 while keeping RAM telemetry intact."}
    }
    return {"tier": req.tier, "hint": hints.get(sess.current_phase, {}).get(req.tier, "Focus on RFC 3227 order of volatility.")}

@app.get("/api/reports")
def reports(db: Session = Depends(get_db)):
    records = db.query(SimulationResult).order_by(SimulationResult.created_at.desc()).all()
    return [{
        "id": r.id, "user_email": r.user_email, "scenario_title": r.scenario_title, "outcome": r.outcome,
        "overall_score": r.overall_score, "detection_score": r.detection_score, "investigation_score": r.investigation_score,
        "containment_score": r.containment_score, "evidence_score": r.evidence_score, "decision_score": r.decision_score,
        "communication_score": r.communication_score, "downtime_hours": r.downtime_hours, "financial_cost": r.financial_cost,
        "records_leaked": r.records_leaked, "weakness": r.weakness_identified, "next_drill": r.next_recommended_drill, "date": r.created_at.strftime("%Y-%m-%d %H:%M UTC")
    } for r in records]

@app.get("/api/leaderboard")
def leaderboard(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.xp.desc()).limit(10).all()
    return [{"rank": idx + 1, "email": u.email, "level": u.level, "xp": u.xp, "containment_score": u.containment_score, "weakest_skill": u.weakest_skill} for idx, u in enumerate(users)]
