import os

ui_code = r'''<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>INCIDENT RESPONSE SIMULATOR</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace']
          },
          colors: {
            soc: {
              950: '#03080C',
              900: '#071018',
              850: '#0C1924',
              800: '#142535',
              border: '#1B3247',
              emerald: '#00E599',
              red: '#FF3355',
              amber: '#FFB800',
              blue: '#00A3FF'
            }
          }
        }
      }
    }
  </script>
  <style>
    body { background-color: #03080C; color: #E2E8F0; font-family: 'Plus Jakarta Sans', sans-serif; }
    .hero-glow {
      background: radial-gradient(circle at 50% 20%, rgba(0, 229, 153, 0.12) 0%, rgba(3, 8, 12, 0) 70%);
    }
    .soc-glow:hover {
      box-shadow: 0 0 25px rgba(0, 229, 153, 0.12);
      border-color: #00E599;
    }
  </style>
</head>
<body class="bg-soc-950 min-h-screen selection:bg-soc-emerald/20 selection:text-white">
  <div id="root"></div>

  <script type="text/babel">
    const { useState, useEffect } = React;

    const SCENARIOS = [
      {
        id: "INC-2026-001",
        title: "Operation Silent Login",
        organization: "FinSecure Core Technologies",
        type: "Credential Compromise // Adversary Lateral Progression",
        difficulty: "Intermediate",
        estimatedTime: "8 mins",
        mitreCodes: ["T1078.002", "T1110.001", "T1059.001", "T1021.001"],
        initialAlert: {
          titleTech: "Sysmon 4624 (Logon Type 10) from foreign ASN 14061 post 12 brute-force failures on Azure AD proxy",
          titlePlain: "Someone failed 12 passwords, then logged into John Doe's account from Romania at 4 AM.",
          targetHost: "FIN-GATEWAY-01.corp.internal (10.240.12.8)",
          compromisedUser: "jdoe@finsecure.com (John Doe - Senior Financial Analyst)",
          foreignIP: "185.220.101.4 (Bucharest, Romania [AS14061 DigitalOcean])"
        },
        evidence: [
          { name: "Authentication Logs", category: "Auth Proxy", tech: "Security Event 4625 x12 followed by 4624 Type 10 (RemoteInteractive). NTLMv2 negotiated.", plain: "12 wrong passwords tried in 3 minutes before guessing/using a stolen password for remote desktop access." },
          { name: "User Identity Telemetry", category: "Active Directory", tech: "Normal working hours: 09:00 - 18:00 EST from Atlanta, GA. Abnormal session launched from Linux Chrome UA at 04:12 EST.", plain: "John Doe is asleep in Atlanta, but his computer account was accessed from Europe outside work hours." },
          { name: "Process Execution Tree", category: "Endpoint EDR", tech: "PID 4821: powershell.exe -NoP -NonI -W Hidden -Enc SUVY(New-Object...) spawned under w3wp.exe worker.", plain: "A hidden PowerShell script was quietly launched in the background to contact an outside attacker server." },
          { name: "Network Beaconing Sockets", category: "Network Firewall", tech: "Outbound persistent TCP 443 socket established: 10.240.12.8:49211 -> 185.220.101.4:443 [TLS v1.3 self-signed].", plain: "The server is continuously sending secret encrypted messages out to the attacker's server in Romania." }
        ],
        steps: [
          {
            stepNumber: 1,
            phaseLabel: "PHASE 01: INITIAL COMPROMISE TRIAGE & TOKEN HANDLING",
            promptTech: "Alert triage: Threat actor actively connected via RDP session on FIN-GATEWAY-01. Reconnaissance commands (whoami /groups, net user /domain) detected.",
            promptPlain: "The intruder is currently inside John Doe's computer checking what permissions they have. What is your first action?",
            choices: [
              {
                id: "act-1",
                labelTech: "Revoke Active Azure AD Sessions & Force Immediate Password / MFA Reset",
                labelPlain: "Instantly kick the intruder out of the account and reset all passwords",
                impact: 30,
                cost: 3000,
                downtime: 0.2,
                techFeedback: "NIST Playbook Optimal: Session tokens invalidated via Microsoft Graph. Adversary RDP socket disconnected within 32 seconds.",
                plainFeedback: "Great move! The intruder was immediately booted off the computer before touching any core databases."
              },
              {
                id: "act-2",
                labelTech: "Passively Monitor Attacker to Map External Command-and-Control Infrastructure",
                labelPlain: "Wait and silently watch what the hacker does to see where they connect",
                impact: -15,
                cost: 38000,
                downtime: 2.5,
                techFeedback: "Adversary Progression: Threat actor recognized telemetry traps and dumped 4,200 payroll password hashes before severing the socket.",
                plainFeedback: "Delayed response! While you watched, the hacker stole 4,200 employee password hashes."
              },
              {
                id: "act-3",
                labelTech: "Suppress Alert as False Positive (Assume User is Traveling on International PTO)",
                labelPlain: "Ignore the alarm and assume John Doe is on vacation in Europe",
                impact: -50,
                cost: 160000,
                downtime: 14.0,
                techFeedback: "Critical Failure: Attacker extracted wire transfer API secrets; 42,000 banking transaction records dumped to darknet.",
                plainFeedback: "Disaster! The attacker spent 4 hours downloading client bank records and leaked them."
              }
            ]
          },
          {
            stepNumber: 2,
            phaseLabel: "PHASE 02: LATERAL PERSISTENCE & SYSTEM ISOLATION",
            promptTech: "Containment decision: Threat actor configured a persistence scheduled task 'UpdateHealthSvc' and is attempting to access local subnet servers.",
            promptPlain: "The hacker created a hidden timer task to infect other computers on our network. How do we contain the machine?",
            choices: [
              {
                id: "act-4",
                labelTech: "Execute EDR Network Isolation (RFC 3227 Volatile RAM Forensics Preserved)",
                labelPlain: "Isolate the computer from the network so it cannot infect others, but keep power on",
                impact: 25,
                cost: 5000,
                downtime: 0.5,
                techFeedback: "Containment Standard Met: Machine quarantined from corporate LAN. Memory dump captured for forensic IOC extraction.",
                plainFeedback: "Excellent decision! The infected computer is isolated from other machines, and we preserved evidence in memory."
              },
              {
                id: "act-5",
                labelTech: "Depower Machine Immediately (Hard Physical Power Disconnect)",
                labelPlain: "Rip out the physical power cord immediately to shut it down cold",
                impact: -20,
                cost: 52000,
                downtime: 5.0,
                techFeedback: "Forensic Evidence Loss: Pulling the plug cleared volatile RAM. Injected DLLs lost. Secondary backdoor on storage NAS remained active.",
                plainFeedback: "Warning: Pulling the plug wiped all RAM memory evidence. We can no longer prove what files were accessed."
              }
            ]
          }
        ]
      }
    ];

    function App() {
      const [view, setView] = useState("auth"); // auth | dashboard | console | debrief | reports
      const [technicalMode, setTechnicalMode] = useState(true);
      const [operator, setOperator] = useState(null);
      const [emailInput, setEmailInput] = useState("");
      const [badgeInput, setBadgeInput] = useState("");
      const [inputError, setInputError] = useState("");
      const [activeScenario, setActiveScenario] = useState(SCENARIOS[0]);
      const [currentStepIdx, setCurrentStepIdx] = useState(0);
      const [containmentScore, setContainmentScore] = useState(72);
      const [financialCost, setFinancialCost] = useState(2500);
      const [downtimeHours, setDowntimeHours] = useState(0.0);
      const [decisionHistory, setDecisionHistory] = useState([]);
      const [stopwatch, setStopwatch] = useState(0);
      const [isTimerRunning, setIsTimerRunning] = useState(false);
      const [selectedEvidenceTab, setSelectedEvidenceTab] = useState(0);
      const [terminalInput, setTerminalInput] = useState("");
      const [terminalLogs, setTerminalLogs] = useState([
        "SOC FORENSIC CLI // Host: FIN-GATEWAY-01 (10.240.12.8)",
        "Type 'help', 'netstat -ano', 'ps aux', 'history', or 'isolate-host'"
      ]);
      const [pastReports, setPastReports] = useState([]);

      useEffect(() => {
        let t = null;
        if (isTimerRunning) {
          t = setInterval(() => setStopwatch(s => s + 1), 1000);
        }
        return () => clearInterval(t);
      }, [isTimerRunning]);

      useEffect(() => {
        fetch('/api/reports')
          .then(r => r.json())
          .then(data => setPastReports(data))
          .catch(() => {});
      }, [view]);

      const formatClock = (sec) => {
        const m = Math.floor(sec / 60).toString().padStart(2, '0');
        const s = (sec % 60).toString().padStart(2, '0');
        return `${m}:${s}`;
      };

      const handleLogin = async (e) => {
        e.preventDefault();
        const cleanEmail = emailInput.trim();
        if (!cleanEmail || !cleanEmail.includes("@")) {
          setInputError("A valid corporate email is required (e.g., analyst@finsecure.com).");
          return;
        }
        try {
          const res = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: cleanEmail, badge_id: badgeInput || "SEC-OP-01" })
          });
          const data = await res.json();
          setOperator(data);
          setInputError("");
          setView("dashboard");
        } catch(err) {
          setInputError("Backend connection error. Ensure FastAPI server is running.");
        }
      };

      const handleSignOut = () => {
        setOperator(null);
        setEmailInput("");
        setBadgeInput("");
        setView("auth");
      };

      const startSimulation = (scn) => {
        setActiveScenario(scn);
        setCurrentStepIdx(0);
        setContainmentScore(72);
        setFinancialCost(2500);
        setDowntimeHours(0.0);
        setDecisionHistory([]);
        setStopwatch(0);
        setIsTimerRunning(true);
        setView("console");
      };

      const handleDecision = async (choice) => {
        const nextScore = Math.max(5, Math.min(100, containmentScore + choice.impact));
        const nextCost = financialCost + choice.cost;
        const nextDowntime = Number((downtimeHours + choice.downtime).toFixed(1));

        setContainmentScore(nextScore);
        setFinancialCost(nextCost);
        setDowntimeHours(nextDowntime);

        const record = {
          ...choice,
          time: formatClock(stopwatch)
        };
        setDecisionHistory(prev => [record, ...prev]);

        if (currentStepIdx + 1 < activeScenario.steps.length && choice.impact > -30) {
          setCurrentStepIdx(s => s + 1);
        } else {
          setIsTimerRunning(false);
          const outcomeText = nextScore >= 80 ? "Incident Contained Successfully" : nextScore >= 50 ? "Partially Contained With Dwell Latency" : "Critical Security Breach // SLA Penalty";
          const weaknessText = nextScore < 80 ? "Containment Speed & Revocation Latency" : "Optimal Protocol Execution";
          const nextDrill = nextScore < 80 ? "Operation Silent Login — Rapid Isolation Drill" : "Ransomware Lateral Movement Air-Gap Containment";

          try {
            await fetch('/api/simulations/save', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                user_email: operator.email,
                scenario_id: activeScenario.id,
                scenario_title: activeScenario.title,
                outcome: outcomeText,
                overall_score: nextScore,
                detection_pct: 94,
                investigation_pct: 88,
                containment_pct: nextScore >= 80 ? 95 : 48,
                evidence_pct: 90,
                communication_pct: 78,
                downtime_hours: nextDowntime,
                financial_cost: nextCost,
                data_leaked_records: choice.impact < 0 ? 42000 : 0,
                mttr_seconds: stopwatch,
                decisions_summary: `${choice.labelTech} — ${choice.techFeedback}`,
                weakness_identified: weaknessText,
                next_drill_recommendation: nextDrill
              })
            });
            // Update operator stats locally
            setOperator(prev => ({
              ...prev,
              weakest_skill: weaknessText,
              recommended_scenario: nextDrill
            }));
          } catch(e) {}
          setView("debrief");
        }
      };

      const handleCliSubmit = (e) => {
        e.preventDefault();
        const cmd = terminalInput.trim().toLowerCase();
        if (!cmd) return;
        let resp = `Command not recognized: '${cmd}'. Type 'help' for options.`;
        if (cmd === 'help') {
          resp = "Available: netstat -ano, ps aux, history, isolate-host, clear";
        } else if (cmd.includes('netstat')) {
          resp = "TCP 0.0.0.0:443 0.0.0.0:0 LISTENING [PID 4821]\nTCP 10.240.12.8:49211 -> 185.220.101.4:443 ESTABLISHED [PID 4821 - Active C2 Channel]";
        } else if (cmd.includes('ps')) {
          resp = "PID 4821 | CPU 89.2% | runner.exe -worker (Backdoor Beacon)\nPID 684  | CPU  0.1% | lsass.exe (Local Security Authority)";
        } else if (cmd === 'history') {
          resp = "101 net user /domain\n102 Get-AuthHash -DumpTarget\n103 schtasks /create /tn UpdateHealthSvc";
        } else if (cmd === 'isolate-host') {
          resp = "[STATUS: QUARANTINED] EDR Agent dropped LAN/WAN routing. Memory telemetry preserved.";
        } else if (cmd === 'clear') {
          setTerminalLogs([]);
          setTerminalInput("");
          return;
        }
        setTerminalLogs(prev => [...prev, `$ ${terminalInput}`, resp]);
        setTerminalInput("");
      };

      return (
        <div className="min-h-screen flex flex-col bg-soc-950 text-slate-200">
          
          {/* Top Enterprise Header */}
          <nav className="h-20 border-b border-soc-border bg-soc-900/90 backdrop-blur px-8 flex items-center justify-between sticky top-0 z-50">
            <div className="flex items-center gap-10">
              <button onClick={() => setView(operator ? "dashboard" : "auth")} className="flex items-center gap-3.5 text-left">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-soc-emerald to-emerald-400 flex items-center justify-center font-bold text-black text-xl shadow-lg shadow-soc-emerald/20">
                  ⚡
                </div>
                <div>
                  <h1 className="font-extrabold text-base tracking-wider text-white leading-none">INCIDENT RESPONSE SIMULATOR</h1>
                  <span className="text-[10px] font-mono text-soc-emerald tracking-widest uppercase">ENTERPRISE DEFENSIVE RANGE</span>
                </div>
              </button>

              {operator && (
                <div className="hidden md:flex items-center gap-6 text-xs font-mono text-slate-400">
                  <button onClick={() => setView("dashboard")} className={`hover:text-white transition ${view === "dashboard" ? "text-soc-emerald font-bold" : ""}`}>
                    DASHBOARD & SCENARIOS
                  </button>
                  <button onClick={() => setView("reports")} className={`hover:text-white transition ${view === "reports" ? "text-soc-emerald font-bold" : ""}`}>
                    AUDIT HISTORY ({pastReports.length})
                  </button>
                </div>
              )}
            </div>

            <div className="flex items-center gap-4">
              {operator && (
                <div className="flex items-center bg-soc-950 border border-soc-border p-1 rounded-xl text-xs font-mono">
                  <button
                    onClick={() => setTechnicalMode(true)}
                    className={`px-3 py-1 rounded-lg transition ${technicalMode ? "bg-soc-800 text-white font-bold" : "text-slate-400"}`}
                  >
                    SOC Technical
                  </button>
                  <button
                    onClick={() => setTechnicalMode(false)}
                    className={`px-3 py-1 rounded-lg transition ${!technicalMode ? "bg-soc-emerald text-black font-bold" : "text-slate-400"}`}
                  >
                    Plain English
                  </button>
                </div>
              )}

              {operator ? (
                <div className="flex items-center gap-3 bg-soc-850 px-4 py-2 rounded-full border border-soc-border text-xs font-mono">
                  <span className="w-2 h-2 rounded-full bg-soc-emerald animate-pulse"></span>
                  <span className="text-slate-400">ANALYST: <b className="text-white">{operator.email}</b></span>
                  <button onClick={handleSignOut} className="text-slate-500 hover:text-rose-400 ml-2">Sign Out</button>
                </div>
              ) : (
                <span className="px-3 py-1 rounded bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-mono">
                  AUTH REQUIRED
                </span>
              )}
            </div>
          </nav>

          {/* VIEW 1: AUTHENTICATION PORTAL (HERO) */}
          {view === "auth" && (
            <main className="flex-1 hero-glow flex flex-col justify-center items-center p-8 max-w-4xl mx-auto w-full text-center space-y-8 my-auto">
              <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-soc-850 border border-soc-emerald/30 text-soc-emerald text-xs font-mono tracking-widest uppercase">
                <span>●</span> DEFENSIVE CYBER INCIDENT PLATFORM
              </div>

              <h2 className="text-4xl md:text-6xl font-extrabold text-white tracking-tight uppercase leading-tight">
                “Every decision changes the incident.”
              </h2>

              <p className="text-sm md:text-base text-slate-400 leading-relaxed font-light max-w-2xl mx-auto">
                Authenticate to access live enterprise SIEM feeds, investigate forensic artifacts, and make critical containment decisions with explainable feedback and adaptive training.
              </p>

              <div className="w-full max-w-md mx-auto p-6 rounded-2xl bg-soc-900 border border-soc-border text-left shadow-2xl space-y-4">
                <div className="border-b border-soc-border pb-3">
                  <h3 className="font-bold text-sm text-white font-mono uppercase">SOC Analyst Portal Access</h3>
                  <span className="text-xs text-slate-400">Sign in with your corporate email address to load your profile.</span>
                </div>

                <form onSubmit={handleLogin} className="space-y-4">
                  <div>
                    <label className="text-[11px] font-mono text-slate-400 block mb-1">Corporate Email Address</label>
                    <input
                      type="email"
                      placeholder="e.g. analyst@finsecure.com"
                      value={emailInput}
                      onChange={(e) => { setEmailInput(e.target.value); setInputError(""); }}
                      className="w-full px-4 py-2.5 rounded-xl bg-soc-950 border border-soc-border text-white text-xs font-mono focus:outline-none focus:border-soc-emerald placeholder-slate-600"
                    />
                  </div>

                  <div>
                    <label className="text-[11px] font-mono text-slate-400 block mb-1">Security Badge ID</label>
                    <input
                      type="text"
                      placeholder="e.g. OP-SEC-774"
                      value={badgeInput}
                      onChange={(e) => setBadgeInput(e.target.value)}
                      className="w-full px-4 py-2.5 rounded-xl bg-soc-950 border border-soc-border text-white text-xs font-mono focus:outline-none focus:border-soc-emerald placeholder-slate-600"
                    />
                  </div>

                  {inputError && <p className="text-xs text-rose-400 font-mono">{inputError}</p>}

                  <button
                    type="submit"
                    className="w-full py-3 bg-soc-emerald hover:bg-emerald-400 text-black font-mono font-bold text-xs rounded-xl transition shadow-lg shadow-soc-emerald/20 uppercase tracking-wider"
                  >
                    Authenticate & Access Feeds →
                  </button>
                </form>
              </div>
            </main>
          )}

          {/* VIEW 2: AUTHENTICATED DASHBOARD, SKILL VECTOR & SCENARIO CATALOG */}
          {view === "dashboard" && operator && (
            <main className="flex-1 p-8 max-w-7xl mx-auto w-full space-y-8">
              
              {/* Top Overview & Adaptive Recommendations */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="p-6 rounded-2xl bg-soc-900 border border-soc-border space-y-4 md:col-span-2">
                  <div className="flex justify-between items-center border-b border-soc-border pb-3">
                    <span className="text-xs font-mono uppercase text-soc-emerald font-bold">Personal Defensive Skill Profile</span>
                    <span className="text-xs font-mono text-slate-400">Level {operator.level} // {operator.xp} XP</span>
                  </div>
                  <div className="space-y-3 font-mono text-xs">
                    {[
                      { name: "Threat Detection", val: operator.skills.detection, col: "bg-emerald-500" },
                      { name: "Investigation Rigor", val: operator.skills.investigation, col: "bg-blue-500" },
                      { name: "Containment Speed", val: operator.skills.containment, col: "bg-rose-500" },
                      { name: "Evidence Handling", val: operator.skills.evidence, col: "bg-indigo-500" },
                      { name: "Incident Communication", val: operator.skills.communication, col: "bg-amber-500" }
                    ].map(s => (
                      <div key={s.name}>
                        <div className="flex justify-between text-[11px] mb-1">
                          <span className="text-slate-300">{s.name}</span>
                          <span className="font-bold text-white">{s.val}%</span>
                        </div>
                        <div className="w-full bg-soc-950 h-2 rounded-full overflow-hidden">
                          <div className={`${s.col} h-full rounded-full`} style={{ width: `${s.val}%` }}></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Adaptive Recommendation Card */}
                <div className="p-6 rounded-2xl bg-soc-900 border border-soc-border flex flex-col justify-between border-l-4 border-l-rose-500">
                  <div className="space-y-3">
                    <span className="text-[10px] font-mono text-rose-400 uppercase font-bold block">Adaptive Diagnostics</span>
                    <h4 className="text-base font-bold text-white font-mono">Weakest Skill: {operator.weakest_skill}</h4>
                    <p className="text-xs text-slate-400 leading-relaxed font-sans">
                      Performance metrics indicate you accurately detect anomalies but delay token revocation and host isolation, extending adversary dwell time.
                    </p>
                  </div>

                  <div className="pt-4 border-t border-soc-border space-y-2">
                    <span className="text-[10px] font-mono text-soc-emerald uppercase block">Prescribed Next Drill:</span>
                    <button
                      onClick={() => startSimulation(SCENARIOS[0])}
                      className="w-full py-2.5 bg-soc-emerald hover:bg-emerald-400 text-black font-mono font-bold text-xs rounded-xl transition shadow-lg shadow-soc-emerald/20"
                    >
                      Launch Recommended Drill ▶
                    </button>
                  </div>
                </div>
              </div>

              {/* Active Incident Catalog */}
              <div className="space-y-4">
                <div className="flex justify-between items-end border-b border-soc-border pb-3">
                  <div>
                    <span className="text-[10px] font-mono text-soc-emerald tracking-widest uppercase block mb-1">SIEM & EDR INGESTION FEED</span>
                    <h3 className="text-2xl font-bold text-white font-mono">Active Critical Incidents</h3>
                  </div>
                  <span className="text-xs font-mono text-slate-500">Source: Azure AD, Okta, CrowdStrike</span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {SCENARIOS.map(scn => (
                    <div key={scn.id} className="p-7 rounded-2xl bg-soc-900 border border-soc-border soc-glow transition flex flex-col justify-between space-y-6">
                      <div className="space-y-4">
                        <div className="flex justify-between items-center text-xs font-mono">
                          <span className="px-3 py-1 rounded bg-rose-500/10 text-rose-400 border border-rose-500/30 font-bold">
                            CRITICAL SEVERITY
                          </span>
                          <span className="text-soc-blue font-semibold">{scn.id}</span>
                        </div>

                        <div>
                          <h4 className="text-xl font-bold text-white">{scn.title}</h4>
                          <span className="text-xs font-mono text-soc-emerald mt-1 block">{scn.type}</span>
                        </div>

                        <p className="text-xs text-slate-400 leading-relaxed font-sans">{scn.initialAlert.titleTech}</p>

                        <div className="p-3.5 rounded-xl bg-soc-950 border border-soc-border font-mono text-xs space-y-1">
                          <div className="text-slate-400">Target Asset: <span className="text-amber-400">{scn.initialAlert.targetHost}</span></div>
                          <div className="text-slate-400">Threat Geolocation: <span className="text-rose-400">{scn.initialAlert.foreignIP}</span></div>
                        </div>

                        <div className="flex flex-wrap gap-1.5 pt-1">
                          {scn.mitreCodes.map(m => (
                            <span key={m} className="px-2 py-0.5 rounded bg-soc-850 text-slate-400 text-[10px] font-mono border border-soc-border">
                              {m}
                            </span>
                          ))}
                        </div>
                      </div>

                      <div className="pt-4 border-t border-soc-border flex justify-end">
                        <button
                          onClick={() => startSimulation(scn)}
                          className="px-6 py-2.5 rounded-xl bg-soc-emerald hover:bg-emerald-400 text-black font-mono font-bold text-xs transition shadow-lg shadow-soc-emerald/20 flex items-center gap-2"
                        >
                          LAUNCH INCIDENT WAR ROOM ▶
                        </button>
                      </div>
                    </div>
                  ))}

                  {/* Queued Secondary Drill */}
                  <div className="p-7 rounded-2xl bg-soc-900/50 border border-soc-border/50 opacity-60 flex flex-col justify-between space-y-6">
                    <div className="space-y-4">
                      <div className="flex justify-between items-center text-xs font-mono">
                        <span className="px-3 py-1 rounded bg-amber-500/10 text-amber-400 border border-amber-500/30 font-bold">
                          HIGH SEVERITY
                        </span>
                        <span className="text-slate-500">INC-2026-002</span>
                      </div>
                      <div>
                        <h4 className="text-xl font-bold text-white">AWS S3 Token Leakage & Exfiltration</h4>
                        <span className="text-xs font-mono text-slate-400 mt-1 block">Cloud IAM Credential Compromise</span>
                      </div>
                      <p className="text-xs text-slate-500 leading-relaxed">Compromised temporary STS token streaming customer records from encrypted bucket.</p>
                      <div className="p-3.5 rounded-xl bg-soc-950/60 border border-soc-border/40 font-mono text-xs text-slate-600">
                        Asset: arn:aws:iam::1492049102:role/ProductionDataSync
                      </div>
                    </div>
                    <div className="pt-4 border-t border-soc-border/40 text-xs font-mono text-slate-600 text-right">
                      🔒 Unlocks at Operator Level 3
                    </div>
                  </div>
                </div>
              </div>
            </main>
          )}

          {/* VIEW 3: LIVE SIMULATION WAR ROOM (INVESTIGATION & DECISION CONSOLE) */}
          {view === "console" && (
            <main className="flex-1 p-6 max-w-7xl mx-auto w-full flex flex-col gap-6">
              
              {/* Status Header */}
              <div className="p-4 rounded-xl bg-soc-900 border border-soc-border flex items-center justify-between font-mono text-xs">
                <div className="flex items-center gap-3">
                  <span className="w-2.5 h-2.5 rounded-full bg-rose-500 animate-ping"></span>
                  <span className="text-white font-bold">{activeScenario.id} // {activeScenario.title}</span>
                  <span className="text-slate-600">|</span>
                  <span className="text-slate-400">{activeScenario.initialAlert.targetHost}</span>
                </div>
                <div className="flex items-center gap-6">
                  <div>ACTIVE MTTR: <b className="text-soc-emerald">{formatClock(stopwatch)}</b></div>
                  <button onClick={() => setView("dashboard")} className="text-slate-500 hover:text-white">✕ Exit War Room</button>
                </div>
              </div>

              {/* Blast Radius Metrics */}
              <div className="grid grid-cols-4 gap-4">
                <div className="p-4 rounded-xl bg-soc-900 border border-soc-border font-mono">
                  <span className="text-[10px] text-slate-500 uppercase block mb-1">Financial Loss</span>
                  <span className="text-xl font-bold text-rose-400">${financialCost.toLocaleString()}</span>
                </div>
                <div className="p-4 rounded-xl bg-soc-900 border border-soc-border font-mono">
                  <span className="text-[10px] text-slate-500 uppercase block mb-1">Service Downtime</span>
                  <span className="text-xl font-bold text-soc-blue">{downtimeHours} hrs</span>
                </div>
                <div className="p-4 rounded-xl bg-soc-900 border border-soc-border font-mono">
                  <span className="text-[10px] text-slate-500 uppercase block mb-1">Containment Score</span>
                  <span className={`text-xl font-bold ${containmentScore >= 75 ? "text-soc-emerald" : "text-amber-400"}`}>{containmentScore}%</span>
                </div>
                <div className="p-4 rounded-xl bg-soc-900 border border-soc-border font-mono">
                  <span className="text-[10px] text-slate-500 uppercase block mb-1">Assigned Investigator</span>
                  <span className="text-sm font-bold text-slate-200 truncate block mt-1">{operator.email}</span>
                </div>
              </div>

              {/* Split Console: Evidence & CLI on Left / Decision Tree on Right */}
              <div className="grid grid-cols-12 gap-6 flex-1 min-h-[520px]">
                
                {/* Left 7 Columns: Forensic Evidence Tabs + Working Terminal */}
                <div className="col-span-12 lg:col-span-7 flex flex-col gap-6">
                  
                  {/* Evidence Drawer */}
                  <div className="p-5 rounded-xl bg-soc-900 border border-soc-border font-mono text-xs flex flex-col gap-3">
                    <div className="flex justify-between items-center pb-2 border-b border-soc-border">
                      <div className="flex gap-2">
                        {activeScenario.evidence.map((ev, i) => (
                          <button
                            key={i}
                            onClick={() => setSelectedEvidenceTab(i)}
                            className={`px-2.5 py-1 rounded text-[11px] transition ${selectedEvidenceTab === i ? "bg-soc-800 text-soc-emerald font-bold border border-soc-emerald/30" : "text-slate-400 hover:text-white"}`}
                          >
                            {ev.name}
                          </button>
                        ))}
                      </div>
                      <span className="text-soc-emerald text-[10px]">EVIDENCE: VERIFIED</span>
                    </div>

                    <div className="p-3 bg-soc-950 rounded border border-soc-border text-xs leading-relaxed">
                      <span className="text-slate-500 block mb-1 text-[10px] uppercase font-bold">Category: {activeScenario.evidence[selectedEvidenceTab].category}</span>
                      <p className="text-slate-300">
                        {technicalMode ? activeScenario.evidence[selectedEvidenceTab].tech : activeScenario.evidence[selectedEvidenceTab].plain}
                      </p>
                    </div>
                  </div>

                  {/* Interactive CLI Terminal */}
                  <div className="flex-1 p-5 rounded-xl bg-soc-900 border border-soc-border flex flex-col justify-between font-mono text-xs">
                    <div>
                      <div className="flex justify-between items-center pb-2 border-b border-soc-border mb-3">
                        <span className="text-slate-400 font-bold">LIVE FORENSIC CLI SANDBOX</span>
                        <span className="text-[10px] text-slate-500">HOST: FIN-GATEWAY-01</span>
                      </div>
                      <div className="space-y-1 max-h-40 overflow-y-auto text-slate-300 text-[11px]">
                        {terminalLogs.map((l, i) => (
                          <div key={i} className="whitespace-pre-wrap">{l}</div>
                        ))}
                      </div>
                    </div>

                    <form onSubmit={handleCliSubmit} className="mt-4 pt-3 border-t border-soc-border flex gap-2">
                      <span className="text-soc-emerald font-bold">$</span>
                      <input
                        type="text"
                        placeholder="type netstat -ano, ps aux, history, isolate-host..."
                        value={terminalInput}
                        onChange={(e) => setTerminalInput(e.target.value)}
                        className="flex-1 bg-transparent text-white focus:outline-none text-xs font-mono"
                      />
                      <button type="submit" className="px-3 py-1 bg-soc-800 text-slate-300 rounded text-xs hover:bg-soc-border">
                        RUN
                      </button>
                    </form>
                  </div>
                </div>

                {/* Right 5 Columns: Decision Playbook */}
                <div className="col-span-12 lg:col-span-5 p-6 rounded-xl bg-soc-900 border border-soc-border flex flex-col justify-between">
                  <div className="space-y-4">
                    <div className="flex justify-between items-center font-mono text-xs">
                      <span className="text-soc-emerald font-bold uppercase">{activeScenario.steps[currentStepIdx].phaseLabel}</span>
                      <span className="text-slate-500">PHASE {currentStepIdx + 1} OF {activeScenario.steps.length}</span>
                    </div>

                    <p className="text-xs text-slate-300 leading-relaxed font-mono p-3 bg-soc-950 rounded border border-soc-border">
                      {technicalMode ? activeScenario.steps[currentStepIdx].promptTech : activeScenario.steps[currentStepIdx].promptPlain}
                    </p>

                    <div className="space-y-3 pt-2">
                      {activeScenario.steps[currentStepIdx].choices.map(c => (
                        <button
                          key={c.id}
                          onClick={() => handleDecision(c)}
                          className="w-full text-left p-4 rounded-xl bg-soc-950 hover:bg-soc-850 border border-soc-border hover:border-soc-emerald/50 transition flex flex-col gap-1.5 group font-mono"
                        >
                          <div className="flex justify-between items-center">
                            <span className="font-bold text-xs text-white group-hover:text-soc-emerald transition">
                              {technicalMode ? c.labelTech : c.labelPlain}
                            </span>
                            <span className="text-slate-500 group-hover:text-white transition">→</span>
                          </div>
                          <p className="text-[11px] text-slate-400 leading-normal">
                            {technicalMode ? c.techFeedback : c.plainFeedback}
                          </p>
                          <div className="flex gap-4 pt-1 text-[10px] text-slate-500">
                            <span>Cost: +${c.cost}</span>
                            <span>Downtime: +{c.downtime}h</span>
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="pt-4 border-t border-soc-border font-mono text-[11px] text-slate-500 text-center">
                    “Every decision changes the incident.”
                  </div>
                </div>

              </div>
            </main>
          )}

          {/* VIEW 4: NIST-COMPLIANT EXECUTIVE DEBRIEF & ADAPTIVE FEEDBACK */}
          {view === "debrief" && (
            <main className="flex-1 max-w-4xl mx-auto w-full p-8 space-y-6 my-auto">
              <div className="p-8 rounded-xl bg-soc-900 border border-soc-border space-y-6">
                <div className="flex justify-between items-center border-b border-soc-border pb-6">
                  <div>
                    <span className="text-xs font-mono text-soc-emerald uppercase tracking-widest block mb-1">NIST SP 800-61R2 COMPLIANT AUDIT</span>
                    <h2 className="text-2xl font-mono font-bold text-white">Incident Response Operational Brief</h2>
                  </div>
                  <div className={`px-4 py-1.5 rounded text-xs font-mono font-bold ${containmentScore >= 80 ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/30" : "bg-rose-500/10 text-rose-400 border border-rose-500/30"}`}>
                    {containmentScore >= 80 ? "INCIDENT CONTAINED" : "SLA CRITICAL BREACH"}
                  </div>
                </div>

                <div className="grid grid-cols-4 gap-4 text-center font-mono">
                  <div className="p-4 rounded bg-soc-950 border border-soc-border">
                    <span className="text-[10px] text-slate-500 uppercase block mb-1">Final Score</span>
                    <span className="text-xl font-bold text-white">{containmentScore}%</span>
                  </div>
                  <div className="p-4 rounded bg-soc-950 border border-soc-border">
                    <span className="text-[10px] text-slate-500 uppercase block mb-1">Total MTTR</span>
                    <span className="text-xl font-bold text-soc-emerald">{formatClock(stopwatch)}</span>
                  </div>
                  <div className="p-4 rounded bg-soc-950 border border-soc-border">
                    <span className="text-[10px] text-slate-500 uppercase block mb-1">Financial Loss</span>
                    <span className="text-xl font-bold text-rose-400">${financialCost.toLocaleString()}</span>
                  </div>
                  <div className="p-4 rounded bg-soc-950 border border-soc-border">
                    <span className="text-[10px] text-slate-500 uppercase block mb-1">Service Outage</span>
                    <span className="text-xl font-bold text-soc-blue">{downtimeHours}h</span>
                  </div>
                </div>

                {/* Explainable Decision Feedback */}
                <div className="space-y-2 pt-2 font-mono text-xs">
                  <h4 className="font-bold text-white uppercase text-[11px] text-slate-400">Decision Consequence Audit:</h4>
                  {decisionHistory.map((d, i) => (
                    <div key={i} className="p-3 rounded bg-soc-950 border border-soc-border space-y-1">
                      <div className="flex justify-between">
                        <b className="text-soc-emerald">{technicalMode ? d.labelTech : d.labelPlain}</b>
                        <span className="text-slate-500">{d.time}</span>
                      </div>
                      <p className="text-slate-400">{technicalMode ? d.techFeedback : d.plainFeedback}</p>
                    </div>
                  ))}
                </div>

                {/* Adaptive Learning Recommendation */}
                <div className="p-4 rounded-xl bg-soc-950 border border-soc-emerald/30 font-mono text-xs space-y-2">
                  <span className="text-soc-emerald font-bold uppercase text-[10px] block">Adaptive Recommendation Engine</span>
                  <p className="text-slate-300">
                    Weakness Flagged: <b className="text-rose-400">{operator.weakest_skill}</b>.
                  </p>
                  <p className="text-slate-400">
                    Prescribed Training: <span className="text-white">{operator.recommended_scenario}</span>.
                  </p>
                </div>

                <div className="flex justify-end gap-3 pt-6 border-t border-soc-border font-mono text-xs">
                  <button onClick={() => window.print()} className="px-4 py-2 bg-soc-800 hover:bg-soc-border text-white rounded">
                    PRINT EXECUTIVE BRIEF (PDF)
                  </button>
                  <button onClick={() => setView("dashboard")} className="px-5 py-2 bg-soc-emerald hover:bg-emerald-400 text-black font-bold rounded">
                    RETURN TO DASHBOARD →
                  </button>
                </div>
              </div>
            </main>
          )}

          {/* VIEW 5: PERSISTENT AUDIT HISTORY (SQLITE) */}
          {view === "reports" && (
            <main className="flex-1 max-w-6xl mx-auto w-full p-8 space-y-6">
              <div className="flex justify-between items-center border-b border-soc-border pb-4 font-mono">
                <div>
                  <span className="text-[10px] font-mono text-soc-emerald uppercase tracking-widest block mb-1">PERMANENT LOG PERSISTENCE</span>
                  <h2 className="text-2xl font-bold text-white">SQLite Incident Audit Trail</h2>
                </div>
                <button onClick={() => setView("dashboard")} className="text-xs text-slate-400 hover:text-white">← Back to Dashboard</button>
              </div>

              <div className="rounded-xl bg-soc-900 border border-soc-border overflow-hidden font-mono text-xs">
                <table className="w-full text-left">
                  <thead className="bg-soc-950 text-slate-500 border-b border-soc-border">
                    <tr><th className="p-3.5">ID</th><th className="p-3.5">Operator</th><th className="p-3.5">Incident Title</th><th className="p-3.5">Outcome</th><th className="p-3.5">Score</th><th className="p-3.5">Cost</th><th className="p-3.5">Weakness</th><th className="p-3.5">Timestamp</th></tr>
                  </thead>
                  <tbody className="divide-y divide-soc-border text-slate-300">
                    {pastReports.length === 0 ? (
                      <tr><td colSpan="8" className="p-6 text-center text-slate-500">No completed incident records yet.</td></tr>
                    ) : (
                      pastReports.map(r => (
                        <tr key={r.id} className="hover:bg-soc-850">
                          <td className="p-3.5 text-slate-500">#{r.id}</td>
                          <td className="p-3.5 text-slate-400">{r.user_email}</td>
                          <td className="p-3.5 font-bold text-white">{r.scenario_title}</td>
                          <td className="p-3.5 text-emerald-400">{r.outcome}</td>
                          <td className="p-3.5 font-bold text-soc-blue">{r.overall_score}%</td>
                          <td className="p-3.5 text-rose-400">${r.financial_cost.toLocaleString()}</td>
                          <td className="p-3.5 text-amber-400">{r.weakness}</td>
                          <td className="p-3.5 text-slate-500">{r.date}</td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </main>
          )}

        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById("root")).render(<App />);
  </script>
</body>
</html>'''

with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(ui_code)

print("SUCCESS: Complete 9-stage incident workflow compiled cleanly!")
