import os

os.makedirs("templates", exist_ok=True)

html_content = r'''<!DOCTYPE html>
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

    const INCIDENTS = [
      {
        id: "INC-2026-001",
        name: "Operation Silent Login",
        target: "FinSecure Core Banking Gateway (10.240.12.8)",
        classification: "APT Credential Compromise & Lateral Reconnaissance",
        severity: "CRITICAL",
        hourlyLoss: "$24,500 / hr",
        description: "12 brute-force authentication failures on Azure AD proxy, followed by NTLMv2 replay and interactive RDP login from Bucharest, Romania (185.220.101.4). Threat actor probing domain trusts.",
        mitre: ["T1078.002 Valid Accounts", "T1110 Brute Force", "T1059.001 PowerShell", "T1021.001 RDP"],
        telemetry: [
          { time: "09:12:04 UTC", source: "Auth-Proxy-01", event: "Security 4625", note: "12 failed NTLM auth attempts for user jdoe@finsecure.com" },
          { time: "09:15:20 UTC", source: "DC-FIN-01", event: "Security 4624", note: "Logon Type 10 (RemoteInteractive) from ASN 14061 (185.220.101.4)" },
          { time: "09:17:42 UTC", source: "FIN-GATEWAY-01", event: "Sysmon 1", note: "powershell.exe -NoP -NonI -W Hidden -Enc SUVY(New-Object...) spawned under PID 4821" },
          { time: "09:20:05 UTC", source: "Network Flow", event: "TCP Socket", note: "Outbound socket established to 185.220.101.4:443 [Cobalt Strike C2]" }
        ],
        stages: [
          {
            stageTitle: "STAGE 01: INITIAL ACCESS & DWELL LATENCY TRIAGE",
            context: "Adversary actively connected via RDP session on FIN-GATEWAY-01 under analyst John Doe's identity. Running whoami /groups and net user /domain.",
            choices: [
              {
                id: "c1",
                title: "Invalidate Azure AD Refresh Tokens & Force Kerberos Ticket Purge",
                description: "Execute immediate Microsoft Graph token invalidation and purge active tickets to drop the adversary socket immediately.",
                impact: 30,
                cost: 3000,
                downtime: 0.2,
                outcome: "Containment successful: Adversary RDP connection dropped in 32 seconds before database exfiltration."
              },
              {
                id: "c2",
                title: "Passively Monitor Attacker to Map Command-and-Control Infrastructure",
                description: "Allow the adversary to remain active for 30 minutes to harvest external IP indicators for threat intelligence.",
                impact: -15,
                cost: 38000,
                downtime: 2.5,
                outcome: "Adversary detected the telemetry trap and extracted 4,200 financial records before pivoting."
              },
              {
                id: "c3",
                title: "Dismiss Alert as Authorized International Employee Travel",
                description: "Close alert without verifying with employee or checking travel itineraries.",
                impact: -50,
                cost: 160000,
                downtime: 14.0,
                outcome: "CRITICAL BREACH: Adversary gained domain administrator rights and deployed multi-subnet ransomware."
              }
            ]
          },
          {
            stageTitle: "STAGE 02: LATERAL INFECTION & PERSISTENCE CONTAINMENT",
            context: "EDR detects an unauthorized scheduled task 'UpdateHealthSvc' created by PID 4821 attempting to spread to neighboring server subnets.",
            choices: [
              {
                id: "c4",
                title: "Deploy EDR Network Isolation (Preserve Volatile Memory for Forensics)",
                description: "Quarantine FIN-GATEWAY-01 from LAN/WAN using host firewall while keeping telemetry daemon online for RAM dump.",
                impact: 25,
                cost: 5000,
                downtime: 0.5,
                outcome: "RFC 3227 standard met. Threat isolated. Complete RAM dump captured for root-cause audit."
              },
              {
                id: "c5",
                title: "Depower Server Immediately (Hard Physical Power Disconnect)",
                description: "Pull physical power cord from the rack to shut down operating system execution instantly.",
                impact: -20,
                cost: 52000,
                downtime: 5.0,
                outcome: "Evidence destroyed: Volatile RAM wiped. Injected payload lost. Secondary persistence on NAS remained active."
              }
            ]
          }
        ]
      }
    ];

    function App() {
      const [view, setView] = useState("landing"); // landing | incidents | console | debrief | audits
      const [operator, setOperator] = useState(localStorage.getItem("irs_operator") || "");
      const [emailInput, setEmailInput] = useState("");
      const [badgeInput, setBadgeInput] = useState("");
      const [inputError, setInputError] = useState("");
      const [incident, setIncident] = useState(INCIDENTS[0]);
      const [currentStage, setCurrentStage] = useState(0);
      const [postureScore, setPostureScore] = useState(72);
      const [burnCost, setBurnCost] = useState(2500);
      const [downtimeHours, setDowntimeHours] = useState(0.0);
      const [auditLogs, setAuditLogs] = useState([]);
      const [timer, setTimer] = useState(0);
      const [isTimerRunning, setIsTimerRunning] = useState(false);
      const [terminalInput, setTerminalInput] = useState("");
      const [terminalLines, setTerminalLines] = useState([
        "INCIDENT RESPONSE SIMULATOR // SOC Forensic Terminal [v3.4.1]",
        "Target Host: FIN-GATEWAY-01.corp.internal (Online)",
        "Type 'help', 'netstat', 'ps', or 'history' to inspect artifacts."
      ]);
      const [persistedRuns, setPersistedRuns] = useState([]);

      useEffect(() => {
        let interval = null;
        if (isTimerRunning) {
          interval = setInterval(() => setTimer(t => t + 1), 1000);
        }
        return () => clearInterval(interval);
      }, [isTimerRunning]);

      useEffect(() => {
        fetch('/api/reports')
          .then(r => r.json())
          .then(data => setPersistedRuns(data))
          .catch(() => {});
      }, [view]);

      const formatClock = (sec) => {
        const m = Math.floor(sec / 60).toString().padStart(2, '0');
        const s = (sec % 60).toString().padStart(2, '0');
        return `${m}:${s}`;
      };

      const handleLogin = (e) => {
        e.preventDefault();
        const trimmedEmail = emailInput.trim();
        if (!trimmedEmail) {
          setInputError("Corporate email address is required.");
          return;
        }
        if (!trimmedEmail.includes("@")) {
          setInputError("Please enter a valid email address (e.g., analyst@finsecure.com).");
          return;
        }
        setOperator(trimmedEmail);
        localStorage.setItem("irs_operator", trimmedEmail);
        setInputError("");
        setView("incidents"); // Move directly to Page 2 (Incidents Queue)
      };

      const handleSignOut = () => {
        localStorage.removeItem("irs_operator");
        setOperator("");
        setEmailInput("");
        setBadgeInput("");
        setView("landing");
      };

      const launchIncident = (selected) => {
        setIncident(selected);
        setCurrentStage(0);
        setPostureScore(72);
        setBurnCost(2500);
        setDowntimeHours(0.0);
        setAuditLogs([]);
        setTimer(0);
        setIsTimerRunning(true);
        setView("console");
      };

      const executeDecision = async (choice) => {
        const nextScore = Math.max(5, Math.min(100, postureScore + choice.impact));
        const nextBurn = burnCost + choice.cost;
        const nextDowntime = Number((downtimeHours + choice.downtime).toFixed(1));

        setPostureScore(nextScore);
        setBurnCost(nextBurn);
        setDowntimeHours(nextDowntime);

        const now = new Date().toISOString().substring(11, 19) + " UTC";
        setAuditLogs(prev => [{ ...choice, timestamp: now }, ...prev]);

        if (currentStage + 1 < incident.stages.length && choice.impact > -30) {
          setCurrentStage(s => s + 1);
        } else {
          setIsTimerRunning(false);
          try {
            await fetch('/api/simulations/save', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                user_id: 1,
                scenario_id: incident.id,
                scenario_title: incident.name,
                outcome: nextScore >= 80 ? "Incident Contained Successfully" : "Severe Breach // SLA Penalty",
                score: nextScore,
                detection_pct: 95,
                investigation_pct: 88,
                containment_pct: nextScore >= 80 ? 94 : 45,
                evidence_pct: 92,
                communication_pct: 78,
                decision_pct: nextScore,
                downtime_hours: nextDowntime,
                financial_cost: nextBurn,
                records_exposed: choice.impact < 0 ? 42000 : 0,
                hints_used: 0,
                response_time_seconds: timer,
                weakness_identified: nextScore < 80 ? "Containment Hesitation" : "Optimal Protocol",
                recommended_training: "Host Isolation & Token Revocation Drill"
              })
            });
          } catch(e) {}
          setView("debrief");
        }
      };

      const handleCli = (e) => {
        e.preventDefault();
        const cmd = terminalInput.trim().toLowerCase();
        if (!cmd) return;
        let output = `Command not recognized: '${cmd}'. Type 'help' for options.`;
        if (cmd === 'help') {
          output = "Commands: netstat (sockets), ps (processes), history (recon commands), isolate-host, clear";
        } else if (cmd.includes('netstat')) {
          output = "TCP 0.0.0.0:443 0.0.0.0:0 LISTENING [PID 4821]\nTCP 10.240.12.8:49211 -> 185.220.101.4:443 ESTABLISHED [PID 4821 - C2 Channel]";
        } else if (cmd.includes('ps')) {
          output = "PID 4821 | CPU 89.2% | runner.exe -worker [Active Backdoor]\nPID 684  | CPU  0.1% | lsass.exe [Local Security Authority]";
        } else if (cmd === 'history') {
          output = "101 net user /domain\n102 Get-AuthHash -DumpTarget\n103 schtasks /create /tn UpdateHealthSvc";
        } else if (cmd === 'isolate-host') {
          output = "[SUCCESS] EDR Agent quarantined FIN-GATEWAY-01. Network severed. Telemetry online.";
        } else if (cmd === 'clear') {
          setTerminalLines([]);
          setTerminalInput("");
          return;
        }
        setTerminalLines(prev => [...prev, `$ ${terminalInput}`, output]);
        setTerminalInput("");
      };

      return (
        <div className="min-h-screen flex flex-col bg-soc-950 text-slate-200">
          
          {/* Top Enterprise Brand Navigation */}
          <nav className="h-20 border-b border-soc-border bg-soc-900/90 backdrop-blur px-8 flex items-center justify-between sticky top-0 z-50">
            <div className="flex items-center gap-10">
              <button onClick={() => setView(operator ? "incidents" : "landing")} className="flex items-center gap-3.5 text-left">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-soc-emerald to-emerald-400 flex items-center justify-center font-bold text-black text-xl shadow-lg shadow-soc-emerald/20">
                  ⚡
                </div>
                <div>
                  <h1 className="font-extrabold text-base tracking-wider text-white leading-none">INCIDENT RESPONSE SIMULATOR</h1>
                  <span className="text-[10px] font-mono text-soc-emerald tracking-widest uppercase">ENTERPRISE SOC SUITE</span>
                </div>
              </button>

              {operator && (
                <div className="hidden md:flex items-center gap-6 text-xs font-mono text-slate-400">
                  <button onClick={() => setView("incidents")} className={`hover:text-white transition ${view === "incidents" ? "text-soc-emerald font-bold" : ""}`}>
                    ACTIVE INCIDENTS
                  </button>
                  <button onClick={() => setView("audits")} className={`hover:text-white transition ${view === "audits" ? "text-soc-emerald font-bold" : ""}`}>
                    AUDIT LOGS ({persistedRuns.length})
                  </button>
                </div>
              )}
            </div>

            <div className="flex items-center gap-4">
              {operator ? (
                <div className="flex items-center gap-3 bg-soc-850 px-4 py-2 rounded-full border border-soc-border text-xs font-mono">
                  <span className="w-2 h-2 rounded-full bg-soc-emerald animate-pulse"></span>
                  <span className="text-slate-400">ANALYST: <b className="text-white">{operator}</b></span>
                  <button onClick={handleSignOut} className="text-slate-500 hover:text-rose-400 ml-2">Sign Out</button>
                </div>
              ) : (
                <span className="px-3 py-1 rounded bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-mono">
                  AUTH REQUIRED
                </span>
              )}
            </div>
          </nav>

          {/* PAGE 1: DEDICATED HERO LANDING & CORPORATE AUTHENTICATION */}
          {view === "landing" && (
            <main className="flex-1 hero-glow flex flex-col justify-center items-center p-8 max-w-4xl mx-auto w-full text-center space-y-8 my-auto">
              <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-soc-850 border border-soc-emerald/30 text-soc-emerald text-xs font-mono tracking-widest uppercase">
                <span>●</span> ENTERPRISE CYBER RANGE
              </div>

              <h2 className="text-4xl md:text-6xl font-extrabold text-white tracking-tight uppercase leading-tight">
                “Every decision changes the incident.”
              </h2>

              <p className="text-sm md:text-base text-slate-400 leading-relaxed font-light max-w-2xl mx-auto">
                Real-time incident response platform. Authenticate to access live enterprise SIEM feeds, execute containment playbooks, and analyze financial and operational blast radius.
              </p>

              {/* Clean Corporate Login Card */}
              <div className="w-full max-w-md mx-auto p-6 rounded-2xl bg-soc-900 border border-soc-border text-left shadow-2xl space-y-4">
                <div className="border-b border-soc-border pb-3">
                  <h3 className="font-bold text-sm text-white font-mono uppercase">SOC Analyst Portal Access</h3>
                  <span className="text-xs text-slate-400">Sign in with your corporate credentials to begin.</span>
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
                    <label className="text-[11px] font-mono text-slate-400 block mb-1">Security Badge ID / Password</label>
                    <input
                      type="password"
                      placeholder="••••••••••••"
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

          {/* PAGE 2: AUTHENTICATED INCIDENT FEED (ONLY SHOWN AFTER LOGIN) */}
          {view === "incidents" && (
            <main className="flex-1 p-8 max-w-7xl mx-auto w-full space-y-8">
              <div className="flex justify-between items-end border-b border-soc-border pb-4">
                <div>
                  <span className="text-[10px] font-mono text-soc-emerald tracking-widest uppercase block mb-1">AUTHORIZED SOC QUEUE</span>
                  <h3 className="text-2xl font-bold text-white font-mono">Active Critical Incidents</h3>
                </div>
                <div className="text-right text-xs font-mono text-slate-500">
                  Operator: <span className="text-soc-emerald font-bold">{operator}</span>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {INCIDENTS.map(inc => (
                  <div key={inc.id} className="p-7 rounded-2xl bg-soc-900 border border-soc-border soc-glow transition flex flex-col justify-between space-y-6">
                    <div className="space-y-4">
                      <div className="flex justify-between items-center text-xs font-mono">
                        <span className="px-3 py-1 rounded bg-rose-500/10 text-rose-400 border border-rose-500/30 font-bold">
                          {inc.severity} SEVERITY
                        </span>
                        <span className="text-soc-blue font-semibold">{inc.id}</span>
                      </div>

                      <div>
                        <h4 className="text-xl font-bold text-white">{inc.name}</h4>
                        <span className="text-xs font-mono text-soc-emerald mt-1 block">{inc.classification}</span>
                      </div>

                      <p className="text-xs text-slate-400 leading-relaxed font-sans">{inc.description}</p>

                      <div className="p-3.5 rounded-xl bg-soc-950 border border-soc-border font-mono text-xs space-y-1">
                        <div className="text-slate-400">Target Asset: <span className="text-amber-400">{inc.target}</span></div>
                        <div className="text-slate-400">Financial Burn: <span className="text-rose-400 font-bold">{inc.hourlyLoss}</span></div>
                      </div>

                      <div className="flex flex-wrap gap-1.5 pt-1">
                        {inc.mitre.map(m => (
                          <span key={m} className="px-2 py-0.5 rounded bg-soc-850 text-slate-400 text-[10px] font-mono border border-soc-border">
                            {m}
                          </span>
                        ))}
                      </div>
                    </div>

                    <div className="pt-4 border-t border-soc-border flex justify-end">
                      <button
                        onClick={() => launchIncident(inc)}
                        className="px-6 py-2.5 rounded-xl bg-soc-emerald hover:bg-emerald-400 text-black font-mono font-bold text-xs transition shadow-lg shadow-soc-emerald/20 flex items-center gap-2"
                      >
                        LAUNCH INCIDENT WAR ROOM ▶
                      </button>
                    </div>
                  </div>
                ))}

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
                    <p className="text-xs text-slate-500 leading-relaxed">Compromised access key actively streaming tables to external IP address.</p>
                    <div className="p-3.5 rounded-xl bg-soc-950/60 border border-soc-border/40 font-mono text-xs text-slate-600">
                      Asset: arn:aws:iam::1492049102:role/ProductionDataSync
                    </div>
                  </div>
                  <div className="pt-4 border-t border-soc-border/40 text-xs font-mono text-slate-600 text-right">
                    🔒 Tier 2 Authorization Required
                  </div>
                </div>
              </div>
            </main>
          )}

          {/* PAGE 3: LIVE SIMULATION WAR ROOM */}
          {view === "console" && (
            <main className="flex-1 p-6 max-w-7xl mx-auto w-full flex flex-col gap-6">
              <div className="p-4 rounded-xl bg-soc-900 border border-soc-border flex items-center justify-between font-mono text-xs">
                <div className="flex items-center gap-3">
                  <span className="w-2.5 h-2.5 rounded-full bg-rose-500 animate-ping"></span>
                  <span className="text-white font-bold">{incident.id} // {incident.name}</span>
                  <span className="text-slate-600">|</span>
                  <span className="text-slate-400">{incident.target}</span>
                </div>
                <div className="flex items-center gap-6">
                  <div>ACTIVE MTTR: <b className="text-soc-emerald">{formatClock(timer)}</b></div>
                  <button onClick={() => setView("incidents")} className="text-slate-500 hover:text-white">✕ Exit War Room</button>
                </div>
              </div>

              <div className="grid grid-cols-4 gap-4">
                <div className="p-4 rounded-xl bg-soc-900 border border-soc-border font-mono">
                  <span className="text-[10px] text-slate-500 uppercase block mb-1">Financial Loss</span>
                  <span className="text-xl font-bold text-rose-400">${burnCost.toLocaleString()}</span>
                </div>
                <div className="p-4 rounded-xl bg-soc-900 border border-soc-border font-mono">
                  <span className="text-[10px] text-slate-500 uppercase block mb-1">Service Downtime</span>
                  <span className="text-xl font-bold text-soc-blue">{downtimeHours} hrs</span>
                </div>
                <div className="p-4 rounded-xl bg-soc-900 border border-soc-border font-mono">
                  <span className="text-[10px] text-slate-500 uppercase block mb-1">Containment Score</span>
                  <span className={`text-xl font-bold ${postureScore >= 75 ? "text-soc-emerald" : "text-amber-400"}`}>{postureScore}%</span>
                </div>
                <div className="p-4 rounded-xl bg-soc-900 border border-soc-border font-mono">
                  <span className="text-[10px] text-slate-500 uppercase block mb-1">Assigned Investigator</span>
                  <span className="text-sm font-bold text-slate-200 truncate block mt-1">{operator}</span>
                </div>
              </div>

              <div className="grid grid-cols-12 gap-6 flex-1 min-h-[500px]">
                <div className="col-span-12 lg:col-span-7 flex flex-col gap-6">
                  <div className="p-5 rounded-xl bg-soc-900 border border-soc-border font-mono text-xs space-y-3">
                    <div className="flex justify-between items-center pb-2 border-b border-soc-border">
                      <span className="text-slate-400 font-bold uppercase">Telemetry & SIEM Ingestion Stream</span>
                      <span className="text-soc-emerald text-[10px]">INGESTION: ACTIVE</span>
                    </div>
                    <div className="space-y-2">
                      {incident.telemetry.map((t, idx) => (
                        <div key={idx} className="p-2.5 rounded bg-soc-950 border border-soc-border/60 flex gap-3 text-[11px]">
                          <span className="text-slate-500 shrink-0">{t.time}</span>
                          <span className="text-soc-blue font-semibold shrink-0">{t.event}</span>
                          <span className="text-slate-300">{t.note}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="flex-1 p-5 rounded-xl bg-soc-900 border border-soc-border flex flex-col justify-between font-mono text-xs">
                    <div>
                      <div className="flex justify-between items-center pb-2 border-b border-soc-border mb-3">
                        <span className="text-slate-400 font-bold">FORENSIC CLI INVESTIGATION SANDBOX</span>
                        <span className="text-[10px] text-slate-500">HOST: FIN-GATEWAY-01</span>
                      </div>
                      <div className="space-y-1 max-h-44 overflow-y-auto text-slate-300 text-[11px]">
                        {terminalLines.map((line, i) => (
                          <div key={i} className="whitespace-pre-wrap">{line}</div>
                        ))}
                      </div>
                    </div>

                    <form onSubmit={handleCli} className="mt-4 pt-3 border-t border-soc-border flex gap-2">
                      <span className="text-soc-emerald font-bold">$</span>
                      <input
                        type="text"
                        placeholder="type netstat, ps, history, isolate-host..."
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

                <div className="col-span-12 lg:col-span-5 p-6 rounded-xl bg-soc-900 border border-soc-border flex flex-col justify-between">
                  <div className="space-y-4">
                    <div className="flex justify-between items-center font-mono text-xs">
                      <span className="text-soc-emerald font-bold uppercase">{incident.stages[currentStage].stageTitle}</span>
                      <span className="text-slate-500">PHASE {currentStage + 1} OF {incident.stages.length}</span>
                    </div>

                    <p className="text-xs text-slate-300 leading-relaxed font-mono p-3 bg-soc-950 rounded border border-soc-border">
                      {incident.stages[currentStage].context}
                    </p>

                    <div className="space-y-3 pt-2">
                      {incident.stages[currentStage].choices.map(c => (
                        <button
                          key={c.id}
                          onClick={() => executeDecision(c)}
                          className="w-full text-left p-4 rounded-xl bg-soc-950 hover:bg-soc-850 border border-soc-border hover:border-soc-emerald/50 transition flex flex-col gap-1.5 group font-mono"
                        >
                          <div className="flex justify-between items-center">
                            <span className="font-bold text-xs text-white group-hover:text-soc-emerald transition">
                              {c.title}
                            </span>
                            <span className="text-slate-500 group-hover:text-white transition">→</span>
                          </div>
                          <p className="text-[11px] text-slate-400 leading-normal">{c.description}</p>
                          <div className="flex gap-4 pt-1 text-[10px] text-slate-500">
                            <span>Cost: +${c.cost}</span>
                            <span>Downtime: +{c.downtime}h</span>
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="pt-4 border-t border-soc-border font-mono text-[11px] text-slate-500 text-center">
                    RFC 3227 Volatility Guard: Active
                  </div>
                </div>
              </div>
            </main>
          )}

          {/* PAGE 4: NIST EXECUTIVE DEBRIEF */}
          {view === "debrief" && (
            <main className="flex-1 max-w-4xl mx-auto w-full p-8 space-y-6 my-auto">
              <div className="p-8 rounded-xl bg-soc-900 border border-soc-border space-y-6">
                <div className="flex justify-between items-center border-b border-soc-border pb-6">
                  <div>
                    <span className="text-xs font-mono text-soc-emerald uppercase tracking-widest block mb-1">NIST SP 800-61R2 COMPLIANT DEBRIEF</span>
                    <h2 className="text-2xl font-mono font-bold text-white">Incident Response Operational Brief</h2>
                  </div>
                  <div className={`px-4 py-1.5 rounded text-xs font-mono font-bold ${postureScore >= 80 ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/30" : "bg-rose-500/10 text-rose-400 border border-rose-500/30"}`}>
                    {postureScore >= 80 ? "INCIDENT CONTAINED" : "CRITICAL SLA BREACH"}
                  </div>
                </div>

                <div className="grid grid-cols-4 gap-4 text-center font-mono">
                  <div className="p-4 rounded bg-soc-950 border border-soc-border">
                    <span className="text-[10px] text-slate-500 uppercase block mb-1">Final Score</span>
                    <span className="text-xl font-bold text-white">{postureScore}%</span>
                  </div>
                  <div className="p-4 rounded bg-soc-950 border border-soc-border">
                    <span className="text-[10px] text-slate-500 uppercase block mb-1">Total MTTR</span>
                    <span className="text-xl font-bold text-soc-emerald">{formatClock(timer)}</span>
                  </div>
                  <div className="p-4 rounded bg-soc-950 border border-soc-border">
                    <span className="text-[10px] text-slate-500 uppercase block mb-1">Financial Loss</span>
                    <span className="text-xl font-bold text-rose-400">${burnCost.toLocaleString()}</span>
                  </div>
                  <div className="p-4 rounded bg-soc-950 border border-soc-border">
                    <span className="text-[10px] text-slate-500 uppercase block mb-1">Service Outage</span>
                    <span className="text-xl font-bold text-soc-blue">{downtimeHours}h</span>
                  </div>
                </div>

                <div className="space-y-2 pt-2 font-mono text-xs">
                  <h4 className="font-bold text-white uppercase text-[11px] text-slate-400">Playbook Execution Ledger:</h4>
                  {auditLogs.map((log, i) => (
                    <div key={i} className="p-3 rounded bg-soc-950 border border-soc-border">
                      <span className="text-slate-500">[{log.timestamp}]</span> <b className="text-soc-emerald">{log.title}</b>
                      <p className="text-slate-400 mt-1">{log.outcome}</p>
                    </div>
                  ))}
                </div>

                <div className="flex justify-end gap-3 pt-6 border-t border-soc-border font-mono text-xs">
                  <button onClick={() => window.print()} className="px-4 py-2 bg-soc-800 hover:bg-soc-border text-white rounded">
                    PRINT EXECUTIVE BRIEF (PDF)
                  </button>
                  <button onClick={() => setView("incidents")} className="px-5 py-2 bg-soc-emerald hover:bg-emerald-400 text-black font-bold rounded">
                    RETURN TO INCIDENT FEEDS →
                  </button>
                </div>
              </div>
            </main>
          )}

          {/* PAGE 5: AUDIT TRAIL */}
          {view === "audits" && (
            <main className="flex-1 max-w-6xl mx-auto w-full p-8 space-y-6">
              <div className="flex justify-between items-center border-b border-soc-border pb-4 font-mono">
                <div>
                  <span className="text-[10px] font-mono text-soc-emerald uppercase tracking-widest block mb-1">PERMANENT LOG PERSISTENCE</span>
                  <h2 className="text-2xl font-bold text-white">SQLite Incident Audit Trail</h2>
                </div>
                <button onClick={() => setView("incidents")} className="text-xs text-slate-400 hover:text-white">← Back to Feeds</button>
              </div>

              <div className="rounded-xl bg-soc-900 border border-soc-border overflow-hidden font-mono text-xs">
                <table className="w-full text-left">
                  <thead className="bg-soc-950 text-slate-500 border-b border-soc-border">
                    <tr><th className="p-3.5">ID</th><th className="p-3.5">Incident Title</th><th className="p-3.5">Outcome</th><th className="p-3.5">Score</th><th className="p-3.5">Downtime</th><th className="p-3.5">Cost</th><th className="p-3.5">Timestamp</th></tr>
                  </thead>
                  <tbody className="divide-y divide-soc-border text-slate-300">
                    {persistedRuns.length === 0 ? (
                      <tr><td colSpan="7" className="p-6 text-center text-slate-500">No completed incident records yet.</td></tr>
                    ) : (
                      persistedRuns.map(r => (
                        <tr key={r.id} className="hover:bg-soc-850">
                          <td className="p-3.5 text-slate-500">#{r.id}</td>
                          <td className="p-3.5 font-bold text-white">{r.scenario_title}</td>
                          <td className="p-3.5 text-emerald-400">{r.outcome}</td>
                          <td className="p-3.5 font-bold text-soc-blue">{r.score}%</td>
                          <td className="p-3.5">{r.downtime_hours}h</td>
                          <td className="p-3.5 text-rose-400">${r.financial_cost.toLocaleString()}</td>
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
    f.write(html_content)

print("SUCCESS: Full enterprise flow compiled cleanly!")
