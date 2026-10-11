import os

os.makedirs("templates", exist_ok=True)

html = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>CYBERSTRIKE // Incident Response Orchestration Platform</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Inter"', 'system-ui', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace']
          },
          colors: {
            enterprise: {
              950: '#070B11',
              900: '#0D131D',
              850: '#121A26',
              800: '#182232',
              border: '#223044',
              accent: '#00E599',
              danger: '#FF3B57',
              warning: '#F59E0B',
              blue: '#2563EB'
            }
          }
        }
      }
    }
  </script>
  <style>
    body { background-color: #070B11; color: #D1D5DB; }
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: #070B11; }
    ::-webkit-scrollbar-thumb { background: #223044; border-radius: 2px; }
    ::-webkit-scrollbar-thumb:hover { background: #374151; }
    .scan-line {
      background: linear-gradient(to bottom, rgba(255,255,255,0), rgba(255,255,255,0) 50%, rgba(0, 229, 153, 0.05) 50%, rgba(0, 229, 153, 0.05));
      background-size: 100% 4px;
    }
  </style>
</head>
<body class="bg-enterprise-950 font-sans text-slate-300 antialiased min-h-screen">
  <div id="root"></div>

  <script type="text/babel">
    const { useState, useEffect } = React;

    const ENTERPRISE_INCIDENTS = [
      {
        id: "INC-2026-8812",
        title: "Pass-The-Hash Active Directory Escalation",
        organization: "Global Fintech Services Corp",
        classification: "APT29 Coordinated Lateral Movement",
        severity: "CRITICAL",
        targetHost: "SRV-DC01.FINSEC.INT (10.200.4.15)",
        compromisedIdentity: "svc_backup_admin (NTLM Hash Exposed)",
        financialImpactPerHour: "$18,500",
        summary: "12 brute-force failures on Azure AD tenant proxy followed by NTLMv2 replay and remote RDP session from Bucharest (185.220.101.4). Threat actor attempting LSASS memory extraction.",
        mitreCodes: ["T1078.002", "T1550.002", "T1059.001", "T1021.001"],
        telemetryLogs: [
          { time: "09:12:04 UTC", event: "Security 4625", data: "12 consecutive logon failures on svc_backup_admin via NTLM auth proxy." },
          { time: "09:15:19 UTC", event: "Security 4624", data: "Successful logon (Logon Type 10) from foreign IP 185.220.101.4 (Bucharest, RO)." },
          { time: "09:17:42 UTC", event: "Sysmon PID 4821", data: "powershell.exe executed with args: -NoP -NonI -W Hidden -Enc SUVY(New-Object...)." },
          { time: "09:20:11 UTC", event: "EDR Sentinel", data: "Unauthorized access handle requested against LSASS.exe by runner.exe." }
        ],
        phases: [
          {
            phaseNumber: 1,
            phaseLabel: "INCIDENT STAGE 01: INITIAL ACCESS & CREDENTIAL PERSISTENCE",
            incidentContext: "Threat actor holds active remote session on FIN-DC01. Reconnaissance commands (whoami /priv, net group 'Domain Admins') detected in EDR telemetry.",
            playbookActions: [
              {
                id: "act-1",
                label: "Revoke Active Kerberos TGT & Invalidate Azure AD Refresh Tokens",
                technicalBrief: "Issue tenant-wide Microsoft Graph session purge. Force immediate Kerberos krbtgt password rotation and sever active TCP 443 sockets.",
                impactScore: 30,
                costDelta: 3500,
                downtimeDelta: 0.2,
                technicalConsequence: "Intruder session severed within 35s. Attacker dropped before accessing secondary backup repositories."
              },
              {
                id: "act-2",
                label: "Halt Incident to Perform Silent Network Packet Capture (Passive Sniffing)",
                technicalBrief: "Leave adversary active on domain controller for 45 minutes to trace secondary command-and-control IP infrastructure.",
                impactScore: -15,
                costDelta: 42000,
                downtimeDelta: 3.5,
                technicalConsequence: "ADVERSARY PROGRESSION: Attacker dumped NTDS.dit database during delay; 14,000 corporate credentials leaked."
              },
              {
                id: "act-3",
                label: "Suppress Alert as Authorized Vulnerability Assessment",
                technicalBrief: "Classify alert as internal penetration test without verifying scheduled authorization tickets.",
                impactScore: -50,
                costDelta: 175000,
                downtimeDelta: 16.0,
                technicalConsequence: "CRITICAL BREACH: Ransomware payload staged across all financial database clusters."
              }
            ]
          },
          {
            phaseNumber: 2,
            phaseLabel: "INCIDENT STAGE 02: LATERAL SPREAD & SECONDARY PERSISTENCE CONTAINMENT",
            incidentContext: "Attacker attempting to push scheduled task 'UpdateHealthSvc' across subnet workstations. Forensic decision required on target host FIN-DC01.",
            playbookActions: [
              {
                id: "act-4",
                label: "Execute EDR Host Network Isolation (RFC 3227 Volatile RAM Preserved)",
                technicalBrief: "Sever host LAN/WAN traffic while keeping kernel agent alive. Capture RAM memory dump for IOC extraction.",
                impactScore: 25,
                costDelta: 5000,
                downtimeDelta: 0.5,
                technicalConsequence: "Contained. Host isolated from local subnet. Threat actor unable to pivot to core banking servers."
              },
              {
                id: "act-5",
                label: "Hard Power Cut (Physically Depower Domain Controller)",
                technicalBrief: "Force hardware shutdown via smart PDU. Hard power drop to halt CPU cycles.",
                impactScore: -20,
                costDelta: 65000,
                downtimeDelta: 6.0,
                technicalConsequence: "FORENSIC LOSS: Volatile memory wiped. Injected DLLs lost. Secondary backdoor on storage NAS remained active."
              }
            ]
          }
        ]
      },
      {
        id: "INC-2026-8819",
        title: "AWS CloudTrail S3 Mass Data Exfiltration Burst",
        organization: "FinSecure Cloud Architecture",
        classification: "Cloud IAM Key Compromise // Token Leak",
        severity: "HIGH",
        targetHost: "arn:aws:iam::1492049102:role/ProductionDataSync",
        compromisedIdentity: "AKIAIOSFODNN7EXAMPLE (Leaked in Public Git Commit)",
        financialImpactPerHour: "$12,000",
        summary: "Anomalous GetObject burst on confidential customer vault S3 bucket from unrecognized TOR exit node. 84,000 PII records accessed within 6 minutes.",
        mitreCodes: ["T1552.001", "T1530", "T1567.002"],
        telemetryLogs: [
          { time: "11:02:10 UTC", event: "CloudTrail", data: "AssumeRole called from IP 198.51.100.22 using compromised access key." },
          { time: "11:04:15 UTC", event: "S3 Server Access", data: "GetObject rate exceeded: 420 requests/sec on prod-customer-records-bucket." },
          { time: "11:06:00 UTC", event: "GuardDuty Alert", data: "UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration triggered." }
        ],
        phases: [
          {
            phaseNumber: 1,
            phaseLabel: "INCIDENT STAGE 01: CLOUD IAM TOKEN REVOCATION",
            incidentContext: "Compromised IAM key active in multi-threaded Python script streaming encrypted archives out of AWS us-east-1.",
            playbookActions: [
              {
                id: "act-c1",
                label: "Attach DenyAll IAM Policy & Invalidate Role Credentials via AWS CLI",
                technicalBrief: "Deploy inline SCP denying all S3 actions to compromised ARN and revoke active temporary STS credentials immediately.",
                impactScore: 30,
                costDelta: 4000,
                downtimeDelta: 0.1,
                technicalConsequence: "Data exfiltration halted at 12% bucket volume. Compromised key rendered completely inert."
              },
              {
                id: "act-c2",
                label: "Delete S3 Bucket to Stop Data Thefts",
                technicalBrief: "Execute aws s3 rb s3://prod-customer-records --force to prevent further reads.",
                impactScore: -40,
                costDelta: 95000,
                downtimeDelta: 24.0,
                technicalConsequence: "DISASTER: Entire production database destroyed. Backup restoration takes 24 hours with massive data loss."
              }
            ]
          }
        ]
      }
    ];

    function App() {
      const [view, setView] = useState("portal"); // portal | war_room | debrief | audit_history
      const [operatorName, setOperatorName] = useState(localStorage.getItem("active_operator") || "");
      const [nameInput, setNameInput] = useState("");
      const [inputError, setInputError] = useState("");
      const [activeIncident, setActiveIncident] = useState(ENTERPRISE_INCIDENTS[0]);
      const [currentPhaseIdx, setCurrentPhaseIdx] = useState(0);
      const [containmentScore, setContainmentScore] = useState(72);
      const [financialBurn, setFinancialBurn] = useState(2500);
      const [downtime, setDowntime] = useState(0.0);
      const [executedInterventions, setExecutedInterventions] = useState([]);
      const [elapsedSeconds, setElapsedSeconds] = useState(0);
      const [isTimerRunning, setIsTimerRunning] = useState(false);
      const [terminalInput, setTerminalInput] = useState("");
      const [terminalLogs, setTerminalLogs] = useState([
        "CYBERSTRIKE EDR Forensic Terminal v4.2.1 initialized.",
        "Connected to FIN-DC01.corp.internal (Agent: ACTIVE).",
        "Type 'help', 'netstat', 'ps', or 'isolate-host' to inspect."
      ]);
      const [pastAudits, setPastAudits] = useState([]);

      useEffect(() => {
        let t = null;
        if (isTimerRunning) {
          t = setInterval(() => setElapsedSeconds(s => s + 1), 1000);
        }
        return () => clearInterval(t);
      }, [isTimerRunning]);

      useEffect(() => {
        fetch('/api/reports')
          .then(r => r.json())
          .then(d => setPastAudits(d))
          .catch(() => {});
      }, [view]);

      const formatClock = (sec) => {
        const m = Math.floor(sec / 60).toString().padStart(2, '0');
        const s = (sec % 60).toString().padStart(2, '0');
        return `${m}:${s}`;
      };

      const handleOperatorAuthentication = (e) => {
        e.preventDefault();
        const clean = nameInput.trim();
        if (!clean) {
          setInputError("Operator call-sign or SOC badge ID is required.");
          return;
        }
        setOperatorName(clean);
        localStorage.setItem("active_operator", clean);
        setInputError("");
        setView("portal");
      };

      const handleSignOut = () => {
        localStorage.removeItem("active_operator");
        setOperatorName("");
        setNameInput("");
        setView("portal");
      };

      const launchWarRoom = (incident) => {
        if (!operatorName) {
          setInputError("Please authenticate with your Operator Call-Sign first.");
          return;
        }
        setActiveIncident(incident);
        setCurrentPhaseIdx(0);
        setContainmentScore(72);
        setFinancialBurn(2500);
        setDowntime(0.0);
        setExecutedInterventions([]);
        setElapsedSeconds(0);
        setIsTimerRunning(true);
        setView("war_room");
      };

      const executePlaybookOption = async (action) => {
        const nextScore = Math.max(5, Math.min(100, containmentScore + action.impactScore));
        const nextBurn = financialBurn + action.costDelta;
        const nextDowntime = Number((downtime + action.downtimeDelta).toFixed(1));

        setContainmentScore(nextScore);
        setFinancialBurn(nextBurn);
        setDowntime(nextDowntime);
        
        const timestamp = new Date().toISOString().substring(11, 19) + " UTC";
        setExecutedInterventions(prev => [{ ...action, executedAt: timestamp }, ...prev]);

        if (currentPhaseIdx + 1 < activeIncident.phases.length && action.impactScore > -30) {
          setCurrentPhaseIdx(i => i + 1);
        } else {
          setIsTimerRunning(false);
          try {
            await fetch('/api/simulations/save', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                user_id: 1,
                scenario_id: activeIncident.id,
                scenario_title: activeIncident.title,
                outcome: nextScore >= 80 ? "Incident Contained Successfully" : "Severe SLA / Business Breach",
                score: nextScore,
                detection_pct: 95,
                investigation_pct: 88,
                containment_pct: nextScore >= 80 ? 94 : 48,
                evidence_pct: 90,
                communication_pct: 78,
                decision_pct: nextScore,
                downtime_hours: nextDowntime,
                financial_cost: nextBurn,
                records_exposed: action.impactScore < 0 ? 38000 : 0,
                hints_used: 0,
                response_time_seconds: elapsedSeconds,
                weakness_identified: nextScore < 80 ? "Decision Hesitation / SLA Breach" : "Optimal Protocol Execution",
                recommended_training: "Host Isolation & Token Revocation Drill"
              })
            });
          } catch(e) {}
          setView("debrief");
        }
      };

      const handleTerminalCommand = (e) => {
        e.preventDefault();
        const cmd = terminalInput.trim().toLowerCase();
        if (!cmd) return;
        let response = `Command not recognized: '${cmd}'. Type 'help' for available diagnostic commands.`;
        if (cmd === 'help') {
          response = "AVAILABLE: netstat (active sockets), ps (process table), history (recent commands), isolate-host, clear";
        } else if (cmd === 'netstat' || cmd === 'netstat -ano') {
          response = "TCP 0.0.0.0:443 0.0.0.0:0 LISTENING [PID 4821]\nTCP 10.200.4.15:49182 -> 185.220.101.4:443 ESTABLISHED [PID 4821 - C2 Channel]";
        } else if (cmd === 'ps' || cmd === 'ps aux') {
          response = "PID 4821 | CPU 89.2% | runner.exe -worker (Beaconing to external ASN 14061)\nPID 684  | CPU  0.1% | lsass.exe (Local Security Authority)";
        } else if (cmd === 'history') {
          response = "101 net user /domain\n102 Get-AuthHash -DumpTarget\n103 schtasks /create /tn UpdateHealthSvc";
        } else if (cmd === 'isolate-host') {
          response = "[SUCCESS] EDR Agent applied host network quarantine. LAN/WAN sockets dropped. Agent telemetry preserved.";
        } else if (cmd === 'clear') {
          setTerminalLogs([]);
          setTerminalInput("");
          return;
        }
        setTerminalLogs(prev => [...prev, `$ ${terminalInput}`, response]);
        setTerminalInput("");
      };

      return (
        <div className="min-h-screen flex flex-col bg-enterprise-950 text-slate-200 scan-line">
          
          {/* Top Enterprise Header */}
          <header className="h-16 bg-enterprise-900 border-b border-enterprise-border px-8 flex items-center justify-between sticky top-0 z-50">
            <div className="flex items-center gap-8">
              <button onClick={() => setView("portal")} className="flex items-center gap-3 text-left">
                <div className="w-8 h-8 rounded bg-enterprise-accent text-black font-mono font-bold flex items-center justify-center text-sm">
                  CS
                </div>
                <div>
                  <span className="font-mono font-bold text-sm tracking-wider text-white block leading-none">CYBERSTRIKE</span>
                  <span className="text-[9px] font-mono text-enterprise-accent tracking-widest uppercase">IR ORCHESTRATION PLATFORM</span>
                </div>
              </button>

              <nav className="hidden md:flex items-center gap-6 text-xs font-mono text-slate-400">
                <button onClick={() => setView("portal")} className={`hover:text-white transition ${view === "portal" ? "text-enterprise-accent font-semibold" : ""}`}>
                  INCIDENT FEEDS
                </button>
                <button onClick={() => setView("audit_history")} className={`hover:text-white transition ${view === "audit_history" ? "text-enterprise-accent font-semibold" : ""}`}>
                  AUDIT LOGS ({pastAudits.length})
                </button>
              </nav>
            </div>

            {/* Operator Badge & Session Controls */}
            <div className="flex items-center gap-4 text-xs font-mono">
              {operatorName ? (
                <div className="flex items-center gap-3 bg-enterprise-850 px-3 py-1.5 rounded border border-enterprise-border">
                  <span className="w-2 h-2 rounded-full bg-enterprise-accent animate-pulse"></span>
                  <span className="text-slate-400">OPERATOR: <b className="text-white">{operatorName}</b></span>
                  <button onClick={handleSignOut} className="text-slate-500 hover:text-rose-400 ml-2">Sign Out</button>
                </div>
              ) : (
                <span className="text-amber-400 bg-amber-500/10 border border-amber-500/20 px-2.5 py-1 rounded">
                  AUTH PENDING
                </span>
              )}
            </div>
          </header>

          {/* VIEW 1: ACTIVE INCIDENT FEEDS (PORTAL) */}
          {view === "portal" && (
            <main className="flex-1 max-w-7xl mx-auto w-full p-8 space-y-8">
              
              {/* Operator Verification Card */}
              {!operatorName && (
                <div className="p-6 rounded-xl bg-enterprise-900 border border-enterprise-border max-w-xl mx-auto space-y-4">
                  <div>
                    <h3 className="font-mono font-bold text-white text-base">Operator Session Verification</h3>
                    <p className="text-xs text-slate-400 mt-1">Enter your assigned SOC analyst call-sign or badge ID to access live incident war rooms.</p>
                  </div>
                  <form onSubmit={handleOperatorAuthentication} className="space-y-3">
                    <input
                      type="text"
                      placeholder="e.g. Lead_Analyst_01 or SOC-ID-442"
                      value={nameInput}
                      onChange={(e) => { setNameInput(e.target.value); setInputError(""); }}
                      className="w-full px-4 py-2.5 bg-enterprise-950 border border-enterprise-border rounded text-sm text-white font-mono focus:outline-none focus:border-enterprise-accent"
                    />
                    {inputError && <p className="text-xs text-rose-400 font-mono">{inputError}</p>}
                    <button type="submit" className="w-full py-2.5 bg-enterprise-accent text-black font-mono font-bold text-xs rounded hover:bg-emerald-400 transition">
                      VERIFY AND PROCEED →
                    </button>
                  </form>
                </div>
              )}

              {/* Enterprise Triage Queue */}
              <div className="space-y-4">
                <div className="flex justify-between items-end border-b border-enterprise-border pb-4">
                  <div>
                    <span className="text-[10px] font-mono text-enterprise-accent uppercase tracking-widest block mb-1">LIVE TELEMETRY INGESTION</span>
                    <h2 className="text-2xl font-mono font-bold text-white">Active Critical Incidents</h2>
                  </div>
                  <span className="text-xs font-mono text-slate-500">Live Feeds: Okta SSO, CrowdStrike Falcon, AWS GuardDuty</span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {ENTERPRISE_INCIDENTS.map((inc) => (
                    <div key={inc.id} className="p-6 rounded-xl bg-enterprise-900 border border-enterprise-border flex flex-col justify-between space-y-5">
                      <div className="space-y-3">
                        <div className="flex justify-between items-center text-xs font-mono">
                          <span className="px-2.5 py-0.5 rounded bg-rose-500/10 text-rose-400 border border-rose-500/30 font-bold">
                            {inc.severity} SEVERITY
                          </span>
                          <span className="text-blue-400 font-semibold">{inc.id}</span>
                        </div>

                        <h3 className="text-lg font-mono font-bold text-white">{inc.title}</h3>
                        <p className="text-xs text-slate-400 leading-relaxed">{inc.summary}</p>

                        <div className="p-3 bg-enterprise-950 rounded border border-enterprise-border font-mono text-[11px] space-y-1">
                          <div><span className="text-slate-500">Entity:</span> <span className="text-slate-300">{inc.organization}</span></div>
                          <div><span className="text-slate-500">Target Asset:</span> <span className="text-amber-400">{inc.targetHost}</span></div>
                          <div><span className="text-slate-500">Hourly Financial Burn:</span> <span className="text-rose-400">{inc.financialImpactPerHour}</span></div>
                        </div>

                        <div className="flex flex-wrap gap-1.5 pt-1">
                          {inc.mitreCodes.map(m => (
                            <span key={m} className="px-2 py-0.5 rounded bg-enterprise-850 text-slate-400 text-[10px] font-mono border border-enterprise-border">
                              {m}
                            </span>
                          ))}
                        </div>
                      </div>

                      <div className="pt-4 border-t border-enterprise-border flex justify-between items-center">
                        <span className="text-[11px] font-mono text-slate-500">Classification: {inc.classification}</span>
                        <button
                          onClick={() => launchWarRoom(inc)}
                          className="px-4 py-2 bg-enterprise-accent hover:bg-emerald-400 text-black font-mono font-bold text-xs rounded transition flex items-center gap-2"
                        >
                          OPEN WAR ROOM ▶
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </main>
          )}

          {/* VIEW 2: LIVE INCIDENT WAR ROOM */}
          {view === "war_room" && (
            <main className="flex-1 max-w-7xl mx-auto w-full p-6 flex flex-col gap-6">
              
              {/* Header Status Bar */}
              <div className="p-4 rounded-xl bg-enterprise-900 border border-enterprise-border flex items-center justify-between font-mono text-xs">
                <div className="flex items-center gap-4">
                  <span className="w-2.5 h-2.5 rounded-full bg-rose-500 animate-ping"></span>
                  <span className="text-white font-bold">{activeIncident.id} // {activeIncident.title}</span>
                  <span className="text-slate-500">|</span>
                  <span className="text-slate-400">{activeIncident.targetHost}</span>
                </div>
                <div className="flex items-center gap-6">
                  <div>ACTIVE MTTR: <b className="text-enterprise-accent">{formatClock(elapsedSeconds)}</b></div>
                  <button onClick={() => setView("portal")} className="text-slate-500 hover:text-white">✕ Exit War Room</button>
                </div>
              </div>

              {/* Blast Radius Cockpit */}
              <div className="grid grid-cols-4 gap-4">
                <div className="p-4 rounded-xl bg-enterprise-900 border border-enterprise-border font-mono">
                  <span className="text-[10px] text-slate-500 uppercase block mb-1">Financial Burn Rate</span>
                  <span className="text-xl font-bold text-rose-400">${financialBurn.toLocaleString()}</span>
                </div>
                <div className="p-4 rounded-xl bg-enterprise-900 border border-enterprise-border font-mono">
                  <span className="text-[10px] text-slate-500 uppercase block mb-1">Service SLA Impact</span>
                  <span className="text-xl font-bold text-blue-400">{downtime} hrs</span>
                </div>
                <div className="p-4 rounded-xl bg-enterprise-900 border border-enterprise-border font-mono">
                  <span className="text-[10px] text-slate-500 uppercase block mb-1">Containment Metric</span>
                  <span className={`text-xl font-bold ${containmentScore >= 75 ? "text-enterprise-accent" : "text-amber-400"}`}>{containmentScore}%</span>
                </div>
                <div className="p-4 rounded-xl bg-enterprise-900 border border-enterprise-border font-mono">
                  <span className="text-[10px] text-slate-500 uppercase block mb-1">Assigned Investigator</span>
                  <span className="text-sm font-bold text-slate-200 truncate block mt-1">{operatorName}</span>
                </div>
              </div>

              {/* Main Split Console */}
              <div className="grid grid-cols-12 gap-6 flex-1 min-h-[500px]">
                
                {/* Left Side: Telemetry Stream & Forensic CLI (7 cols) */}
                <div className="col-span-12 lg:col-span-7 flex flex-col gap-6">
                  {/* Raw Ingestion Logs */}
                  <div className="p-5 rounded-xl bg-enterprise-900 border border-enterprise-border space-y-3 font-mono text-xs">
                    <div className="flex justify-between items-center pb-2 border-b border-enterprise-border">
                      <span className="text-slate-400 font-bold uppercase">SIEM & EDR Event Feed</span>
                      <span className="text-emerald-400 text-[10px]">INGESTION: REAL-TIME</span>
                    </div>
                    <div className="space-y-2">
                      {activeIncident.telemetryLogs.map((log, idx) => (
                        <div key={idx} className="p-2.5 rounded bg-enterprise-950 border border-enterprise-border/60 flex gap-3 text-[11px]">
                          <span className="text-slate-500 shrink-0">{log.time}</span>
                          <span className="text-blue-400 font-semibold shrink-0">{log.event}</span>
                          <span className="text-slate-300">{log.data}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Interactive Forensics Terminal Sandbox */}
                  <div className="flex-1 p-5 rounded-xl bg-enterprise-900 border border-enterprise-border flex flex-col justify-between font-mono text-xs">
                    <div>
                      <div className="flex justify-between items-center pb-2 border-b border-enterprise-border mb-3">
                        <span className="text-slate-400 font-bold">LIVE FORENSIC INVESTIGATION CLI</span>
                        <span className="text-[10px] text-slate-500">FIN-DC01 // SHELL ACTIVE</span>
                      </div>
                      <div className="space-y-1 max-h-48 overflow-y-auto text-slate-300 text-[11px]">
                        {terminalLogs.map((l, i) => (
                          <div key={i} className="whitespace-pre-wrap">{l}</div>
                        ))}
                      </div>
                    </div>

                    <form onSubmit={handleTerminalCommand} className="mt-4 pt-3 border-t border-enterprise-border flex gap-2">
                      <span className="text-enterprise-accent font-bold">$</span>
                      <input
                        type="text"
                        placeholder="type netstat, ps, history, isolate-host..."
                        value={terminalInput}
                        onChange={(e) => setTerminalInput(e.target.value)}
                        className="flex-1 bg-transparent text-white focus:outline-none text-xs font-mono"
                      />
                      <button type="submit" className="px-3 py-1 bg-enterprise-800 text-slate-300 rounded text-xs hover:bg-enterprise-border">
                        RUN
                      </button>
                    </form>
                  </div>
                </div>

                {/* Right Side: Containment Playbook Actions (5 cols) */}
                <div className="col-span-12 lg:col-span-5 p-6 rounded-xl bg-enterprise-900 border border-enterprise-border flex flex-col justify-between">
                  <div className="space-y-4">
                    <div className="flex justify-between items-center font-mono text-xs">
                      <span className="text-enterprise-accent font-bold">{activeIncident.phases[currentPhaseIdx].phaseLabel}</span>
                    </div>

                    <p className="text-xs text-slate-300 leading-relaxed font-mono p-3 bg-enterprise-950 rounded border border-enterprise-border">
                      {activeIncident.phases[currentPhaseIdx].incidentContext}
                    </p>

                    <div className="space-y-3 pt-2">
                      {activeIncident.phases[currentPhaseIdx].playbookActions.map((action) => (
                        <button
                          key={action.id}
                          onClick={() => executePlaybookOption(action)}
                          className="w-full text-left p-4 rounded-xl bg-enterprise-950 hover:bg-enterprise-850 border border-enterprise-border hover:border-enterprise-accent/50 transition flex flex-col gap-1.5 group font-mono"
                        >
                          <div className="flex justify-between items-center">
                            <span className="font-bold text-xs text-white group-hover:text-enterprise-accent transition">
                              {action.label}
                            </span>
                            <span className="text-slate-500 group-hover:text-white transition">→</span>
                          </div>
                          <p className="text-[11px] text-slate-400 leading-normal">{action.technicalBrief}</p>
                          <div className="flex gap-4 pt-1 text-[10px] text-slate-500">
                            <span>Cost: +${action.costDelta}</span>
                            <span>SLA: +{action.downtimeDelta}h</span>
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="pt-4 border-t border-enterprise-border font-mono text-[11px] text-slate-500 text-center">
                    RFC 3227 Volatility Guard: Active
                  </div>
                </div>

              </div>
            </main>
          )}

          {/* VIEW 3: EXECUTIVE INCIDENT DEBRIEF */}
          {view === "debrief" && (
            <main className="flex-1 max-w-4xl mx-auto w-full p-8 space-y-6 my-auto">
              <div className="p-8 rounded-xl bg-enterprise-900 border border-enterprise-border space-y-6">
                <div className="flex justify-between items-center border-b border-enterprise-border pb-6">
                  <div>
                    <span className="text-xs font-mono text-enterprise-accent uppercase tracking-widest block mb-1">NIST SP 800-61R2 COMPLIANT DEBRIEF</span>
                    <h2 className="text-2xl font-mono font-bold text-white">Incident Response Operational Brief</h2>
                  </div>
                  <div className={`px-4 py-1.5 rounded text-xs font-mono font-bold ${containmentScore >= 80 ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/30" : "bg-rose-500/10 text-rose-400 border border-rose-500/30"}`}>
                    {containmentScore >= 80 ? "INCIDENT CONTAINED" : "SLA CRITICAL FAILURE"}
                  </div>
                </div>

                <div className="grid grid-cols-4 gap-4 text-center font-mono">
                  <div className="p-4 rounded bg-enterprise-950 border border-enterprise-border">
                    <span className="text-[10px] text-slate-500 uppercase block mb-1">Final Score</span>
                    <span className="text-xl font-bold text-white">{containmentScore}%</span>
                  </div>
                  <div className="p-4 rounded bg-enterprise-950 border border-enterprise-border">
                    <span className="text-[10px] text-slate-500 uppercase block mb-1">Total MTTR</span>
                    <span className="text-xl font-bold text-enterprise-accent">{formatClock(elapsedSeconds)}</span>
                  </div>
                  <div className="p-4 rounded bg-enterprise-950 border border-enterprise-border">
                    <span className="text-[10px] text-slate-500 uppercase block mb-1">Financial Loss</span>
                    <span className="text-xl font-bold text-rose-400">${financialBurn.toLocaleString()}</span>
                  </div>
                  <div className="p-4 rounded bg-enterprise-950 border border-enterprise-border">
                    <span className="text-[10px] text-slate-500 uppercase block mb-1">Service Outage</span>
                    <span className="text-xl font-bold text-blue-400">{downtime}h</span>
                  </div>
                </div>

                <div className="space-y-2 pt-2 font-mono text-xs">
                  <h4 className="font-bold text-white uppercase text-[11px] text-slate-400">Playbook Execution Ledger:</h4>
                  {executedInterventions.map((ex, i) => (
                    <div key={i} className="p-3 rounded bg-enterprise-950 border border-enterprise-border">
                      <span className="text-slate-500">[{ex.executedAt}]</span> <b className="text-enterprise-accent">{ex.label}</b>
                      <p className="text-slate-400 mt-1">{ex.technicalConsequence}</p>
                    </div>
                  ))}
                </div>

                <div className="flex justify-end gap-3 pt-6 border-t border-enterprise-border font-mono text-xs">
                  <button onClick={() => window.print()} className="px-4 py-2 bg-enterprise-800 hover:bg-enterprise-border text-white rounded">
                    PRINT EXECUTIVE BRIEF (PDF)
                  </button>
                  <button onClick={() => setView("portal")} className="px-5 py-2 bg-enterprise-accent hover:bg-emerald-400 text-black font-bold rounded">
                    RETURN TO INCIDENT FEEDS →
                  </button>
                </div>
              </div>
            </main>
          )}

          {/* VIEW 4: AUDIT HISTORY */}
          {view === "audit_history" && (
            <main className="flex-1 max-w-6xl mx-auto w-full p-8 space-y-6">
              <div className="flex justify-between items-center border-b border-enterprise-border pb-4 font-mono">
                <div>
                  <span className="text-[10px] text-enterprise-accent uppercase tracking-widest block mb-1">PERMANENT LOG PERSISTENCE</span>
                  <h2 className="text-2xl font-bold text-white">SQLite Incident Audit Trail</h2>
                </div>
                <button onClick={() => setView("portal")} className="text-xs text-slate-400 hover:text-white">← Back to Feeds</button>
              </div>

              <div className="rounded-xl bg-enterprise-900 border border-enterprise-border overflow-hidden font-mono text-xs">
                <table className="w-full text-left">
                  <thead className="bg-enterprise-950 text-slate-500 border-b border-enterprise-border">
                    <tr><th className="p-3.5">ID</th><th className="p-3.5">Incident Title</th><th className="p-3.5">Outcome</th><th className="p-3.5">Score</th><th className="p-3.5">Downtime</th><th className="p-3.5">Cost</th><th className="p-3.5">Timestamp</th></tr>
                  </thead>
                  <tbody className="divide-y divide-enterprise-border text-slate-300">
                    {pastAudits.length === 0 ? (
                      <tr><td colSpan="7" className="p-6 text-center text-slate-500">No completed incident logs recorded yet.</td></tr>
                    ) : (
                      pastAudits.map(a => (
                        <tr key={a.id} className="hover:bg-enterprise-850">
                          <td className="p-3.5 text-slate-500">#{a.id}</td>
                          <td className="p-3.5 font-bold text-white">{a.scenario_title}</td>
                          <td className="p-3.5 text-emerald-400">{a.outcome}</td>
                          <td className="p-3.5 font-bold text-blue-400">{a.score}%</td>
                          <td className="p-3.5">{a.downtime_hours}h</td>
                          <td className="p-3.5 text-rose-400">${a.financial_cost.toLocaleString()}</td>
                          <td className="p-3.5 text-slate-500">{a.date}</td>
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
</html>"""

with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("ENTERPRISE INCIDENT ORCHESTRATION PLATFORM COMPILED CLEANLY!")
