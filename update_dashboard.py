import os

os.makedirs("templates", exist_ok=True)

ui_code = r'''<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>INCIDENT RESPONSE SIMULATOR // CYBER DEFENSE OPERATIONS</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
            orbitron: ['"Orbitron"', 'sans-serif']
          },
          colors: {
            cyber: {
              950: '#02050E',
              900: '#040C1D',
              850: '#08142D',
              800: '#0E2145',
              card: 'rgba(7, 18, 42, 0.75)',
              border: '#112C5B',
              neonBlue: '#00D2FF',
              neonCyan: '#00F0FF',
              neonRed: '#FF2A55',
              neonGreen: '#00F59B',
              neonAmber: '#FFB800'
            }
          }
        }
      }
    }
  </script>
  <style>
    body {
      background-color: #02050E;
      color: #E2E8F0;
      background-image: 
        radial-gradient(circle at 50% 0%, rgba(0, 210, 255, 0.08) 0%, transparent 60%),
        radial-gradient(circle at 85% 15%, rgba(255, 42, 85, 0.06) 0%, transparent 50%),
        linear-gradient(rgba(2, 5, 14, 0.95), rgba(2, 5, 14, 0.95)),
        repeating-linear-gradient(0deg, transparent, transparent 1px, rgba(0, 210, 255, 0.015) 1px, rgba(0, 210, 255, 0.015) 2px);
      background-size: 100% 100%, 100% 100%, 100% 100%, 100% 4px;
    }
    .cyber-panel {
      background: linear-gradient(135deg, rgba(8, 20, 45, 0.85) 0%, rgba(4, 12, 29, 0.85) 100%);
      border: 1px solid #13346B;
      box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.6), inset 0 0 12px 0 rgba(0, 210, 255, 0.05);
      backdrop-filter: blur(8px);
    }
    .cyber-panel:hover {
      border-color: rgba(0, 210, 255, 0.5);
      box-shadow: 0 0 25px rgba(0, 210, 255, 0.15), inset 0 0 16px rgba(0, 210, 255, 0.08);
    }
    .cyber-glow-red {
      box-shadow: 0 0 20px rgba(255, 42, 85, 0.4);
    }
    .cyber-glow-blue {
      box-shadow: 0 0 20px rgba(0, 210, 255, 0.4);
    }
    .cyber-glow-green {
      box-shadow: 0 0 20px rgba(0, 245, 155, 0.4);
    }
  </style>
</head>
<body class="min-h-screen selection:bg-cyber-neonBlue/20 selection:text-white font-sans antialiased">
  <div id="root"></div>

  <script type="text/babel">
    const { useState, useEffect } = React;

    // SVG Circular Speedometer Gauge
    function CircularGauge({ value, label, max = 100, color = "#FF2A55", status = "High" }) {
      const radius = 62;
      const stroke = 12;
      const normalizedValue = Math.min(Math.max(value, 0), max);
      const circumference = radius * Math.PI; // Half-gauge
      const strokeDashoffset = circumference - (normalizedValue / max) * circumference;

      return (
        <div className="flex flex-col items-center justify-center relative p-3">
          <div className="relative w-44 h-28 flex items-end justify-center overflow-hidden">
            <svg className="w-44 h-44 -rotate-180 transform" viewBox="0 0 160 160">
              {/* Background Arc */}
              <circle
                cx="80"
                cy="80"
                r={radius}
                fill="transparent"
                stroke="#0E244D"
                strokeWidth={stroke}
                strokeDasharray={`${circumference} ${circumference}`}
                strokeLinecap="round"
              />
              {/* Active Glowing Value Arc */}
              <circle
                cx="80"
                cy="80"
                r={radius}
                fill="transparent"
                stroke={color}
                strokeWidth={stroke}
                strokeDasharray={`${circumference} ${circumference}`}
                strokeDashoffset={strokeDashoffset}
                strokeLinecap="round"
                style={{
                  filter: `drop-shadow(0 0 8px ${color})`,
                  transition: 'stroke-dashoffset 0.8s ease'
                }}
              />
            </svg>

            {/* Inner Center Label */}
            <div className="absolute bottom-2 flex flex-col items-center">
              <span className="text-[11px] font-mono text-slate-400 uppercase tracking-widest">{status}</span>
              <span className="text-3xl font-orbitron font-extrabold text-white tracking-wider" style={{ textShadow: `0 0 15px ${color}` }}>
                {normalizedValue}%
              </span>
            </div>
          </div>
          <span className="text-xs font-mono font-bold text-slate-300 mt-2 tracking-wide uppercase">{label}</span>
        </div>
      );
    }

    // Mini Sparkline SVG
    function Sparkline({ points, strokeColor = "#FF2A55", fillColor = "rgba(255, 42, 85, 0.15)" }) {
      const max = Math.max(...points);
      const min = Math.min(...points);
      const height = 30;
      const width = 110;
      const step = width / (points.length - 1);
      
      const coords = points.map((p, i) => {
        const x = i * step;
        const y = height - ((p - min) / (max - min || 1)) * (height - 6) - 3;
        return `${x},${y}`;
      }).join(' ');

      const fillPath = `M 0,${height} L ${coords} L ${width},${height} Z`;

      return (
        <svg className="w-28 h-8 overflow-visible" viewBox={`0 0 ${width} ${height}`}>
          <polygon points={`0,${height} ${coords} ${width},${height}`} fill={fillColor} />
          <polyline fill="none" stroke={strokeColor} strokeWidth="2" points={coords} strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      );
    }

    // Interactive 3D Isometric Network Topology Canvas
    function NetworkTopology({ compromisedHost = "FIN-GATEWAY-01", isIsolated = false }) {
      return (
        <div className="relative w-full h-44 rounded-xl overflow-hidden bg-gradient-to-b from-[#030B1C] to-[#01050F] border border-[#0E2C5B] p-3 flex flex-col justify-between">
          <div className="flex justify-between items-center text-[10px] font-mono">
            <span className="text-cyber-neonCyan font-bold tracking-wider">● TOPOLOGY TELEMETRY</span>
            <span className={isIsolated ? "text-cyber-neonGreen font-bold" : "text-cyber-neonRed font-bold animate-pulse"}>
              {isIsolated ? "EDR: HOST QUARANTINED" : "THREAT VECTOR: ACTIVE C2"}
            </span>
          </div>

          {/* Isometric Perspective Grid & Attack Rays */}
          <div className="relative w-full h-28 flex items-center justify-center">
            <svg className="w-full h-full" viewBox="0 0 340 100">
              {/* Isometric grid wires */}
              <path d="M 30,70 L 170,10 L 310,70 L 170,95 Z" fill="rgba(0, 210, 255, 0.04)" stroke="#0E3060" strokeWidth="1" />
              <path d="M 65,55 L 170,25 L 275,55 L 170,82 Z" fill="none" stroke="#0E3060" strokeWidth="1" strokeDasharray="3 3" />

              {/* External Source Attacker Node (Romania ASN 14061) */}
              <circle cx="50" cy="65" r="5" fill="#FF2A55" style={{ filter: 'drop-shadow(0 0 8px #FF2A55)' }} />
              <text x="25" y="85" fill="#FF2A55" fontSize="8" fontFamily="JetBrains Mono">185.220.101.4</text>

              {/* Malicious Inbound Red Beam */}
              {!isIsolated ? (
                <path d="M 50,65 Q 110,15 170,50" fill="none" stroke="#FF2A55" strokeWidth="2.5" strokeDasharray="6 3" className="animate-pulse" />
              ) : (
                <path d="M 50,65 Q 110,15 170,50" fill="none" stroke="#334155" strokeWidth="1.5" strokeDasharray="2 4" />
              )}

              {/* Target Compromised Host Node (FIN-GATEWAY-01) */}
              <circle cx="170" cy="50" r="7" fill={isIsolated ? "#00F59B" : "#FF2A55"} style={{ filter: `drop-shadow(0 0 10px ${isIsolated ? '#00F59B' : '#FF2A55'})` }} />
              <text x="135" y="35" fill="#FFFFFF" fontSize="9" fontWeight="bold" fontFamily="JetBrains Mono">{compromisedHost}</text>

              {/* Internal Clean Segment Nodes */}
              <path d="M 170,50 Q 230,25 285,45" fill="none" stroke={isIsolated ? "rgba(0, 245, 155, 0.4)" : "rgba(255, 42, 85, 0.4)"} strokeWidth="1.5" strokeDasharray="4 4" />
              <circle cx="285" cy="45" r="4.5" fill="#00D2FF" style={{ filter: 'drop-shadow(0 0 6px #00D2FF)' }} />
              <text x="260" y="60" fill="#00D2FF" fontSize="8" fontFamily="JetBrains Mono">DB-CLUSTER-01</text>
            </svg>
          </div>

          <div className="flex justify-between items-center text-[9px] font-mono text-slate-500">
            <span>External Source (Bucharest, RO)</span>
            <span>Internal Banking Segment (10.240.0.0/16)</span>
          </div>
        </div>
      );
    }

    const INCIDENTS_DATA = [
      {
        id: "INC-2026-001",
        title: "Operation Silent Login",
        org: "FinSecure Core Banking Gateway",
        targetHost: "FIN-GATEWAY-01 (10.240.12.8)",
        classification: "Credential Compromise // Cobalt Strike C2 Lateral Pivot",
        severityScore: 76,
        systemHealth: 74,
        financialLoss: 24500,
        downtimeHours: 0.8,
        mitreCodes: ["T1078.002", "T1110.001", "T1059.001", "T1021.001"],
        stages: [
          {
            stepIdx: 1,
            title: "STAGE 01 // INITIAL RECONNAISSANCE & TOKEN PURGE",
            briefing: "Adversary logged into John Doe's session using NTLM credential hash replay from IP 185.220.101.4. Actively issuing whoami /groups and domain recon.",
            choices: [
              {
                id: "act-1",
                label: "Revoke Active Azure AD Sessions & Force Immediate Ticket Purge",
                impactSeverity: -22,
                impactHealth: +12,
                cost: 2500,
                downtime: 0.2,
                outcome: "Threat socket severed! Attacker evicted from active RDP session within 34 seconds."
              },
              {
                id: "act-2",
                label: "Passively Monitor Attacker to Map Command-and-Control Infrastructure",
                impactSeverity: +18,
                impactHealth: -15,
                cost: 32000,
                downtime: 2.5,
                outcome: "Dwell failure: Attacker identified telemetry sensor and dumped 4,200 payroll hashes."
              },
              {
                id: "act-3",
                label: "Dismiss Alert as Authorized International Employee Travel",
                impactSeverity: +24,
                impactHealth: -40,
                cost: 145000,
                downtime: 12.0,
                outcome: "CRITICAL FAILURE: Adversary gained domain administrator rights; banking records dumped."
              }
            ]
          },
          {
            stepIdx: 2,
            title: "STAGE 02 // LATERAL INFECTION & ISOLATION WORKBENCH",
            briefing: "EDR telemetry flags encoded PowerShell backdoor spawning persistent service 'UpdateHealthSvc' attempting to probe internal core databases.",
            choices: [
              {
                id: "act-4",
                label: "Execute EDR Host Network Isolation (Preserve Volatile RAM Forensics)",
                impactSeverity: -35,
                impactHealth: +22,
                cost: 4500,
                downtime: 0.5,
                outcome: "RFC 3227 containment verified! Host air-gapped from subnet. Full RAM dump preserved for root-cause audit."
              },
              {
                id: "act-5",
                label: "Hard Power Disconnect (Physically Yank Power Cord)",
                impactSeverity: -5,
                impactHealth: -25,
                cost: 48000,
                downtime: 5.0,
                outcome: "Evidence destroyed: Volatile RAM erased. Secondary persistence on storage NAS remained active."
              }
            ]
          }
        ]
      }
    ];

    function App() {
      const [view, setView] = useState("auth"); // auth | command_center | debrief
      const [operatorEmail, setOperatorEmail] = useState(localStorage.getItem("irs_email") || "");
      const [emailInput, setEmailInput] = useState("");
      const [activeStep, setActiveStep] = useState(0);
      const [threatSeverity, setThreatSeverity] = useState(76);
      const [systemHealth, setSystemHealth] = useState(74);
      const [financialBurn, setFinancialBurn] = useState(12450);
      const [downtime, setDowntime] = useState(0.8);
      const [isHostIsolated, setIsHostIsolated] = useState(false);
      const [timelineStage, setTimelineStage] = useState("Containment"); // Detection | Analysis | Containment | Resolution
      const [actionHistory, setActionHistory] = useState([]);
      const [stopwatch, setStopwatch] = useState(32 * 60); // 32 minutes elapsed
      const [terminalInput, setTerminalInput] = useState("");
      const [terminalLogs, setTerminalLogs] = useState([
        "SOC FORENSIC CLI READY // HOST: FIN-GATEWAY-01",
        "Type 'netstat -ano', 'ps aux', 'history', or 'isolate-host' to inspect clues."
      ]);

      const incident = INCIDENTS_DATA[0];

      useEffect(() => {
        let t = setInterval(() => setStopwatch(s => s + 1), 1000);
        return () => clearInterval(t);
      }, []);

      const formatTimer = (sec) => {
        const m = Math.floor(sec / 60);
        const s = sec % 60;
        return `${m}m ${s}s`;
      };

      const handleLogin = (e) => {
        e.preventDefault();
        const clean = emailInput.trim();
        if (!clean || !clean.includes("@")) return;
        setOperatorEmail(clean);
        localStorage.setItem("irs_email", clean);
        setView("command_center");
      };

      const handleDecision = async (choice) => {
        const nextThreat = Math.max(10, Math.min(99, threatSeverity + choice.impactSeverity));
        const nextHealth = Math.max(10, Math.min(99, systemHealth + choice.impactHealth));
        const nextCost = financialBurn + choice.cost;
        const nextDowntime = Number((downtime + choice.downtime).toFixed(1));

        setThreatSeverity(nextThreat);
        setSystemHealth(nextHealth);
        setFinancialBurn(nextCost);
        setDowntime(nextDowntime);

        if (choice.id === 'act-4') setIsHostIsolated(true);

        const rec = {
          ...choice,
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };
        setActionHistory(prev => [rec, ...prev]);

        if (activeStep + 1 < incident.stages.length && choice.impactSeverity <= 0) {
          setActiveStep(s => s + 1);
          setTimelineStage("Resolution");
        } else {
          setTimelineStage("Resolution");
          try {
            await fetch('/api/simulations/save', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                user_email: operatorEmail || "analyst@finsecure.com",
                scenario_id: incident.id,
                scenario_title: incident.title,
                outcome: nextThreat <= 30 ? "Threat Mitigated & Contained" : "SLA Critical Breach",
                overall_score: Math.round(100 - nextThreat * 0.7 + nextHealth * 0.3),
                detection_pct: 95,
                investigation_pct: 88,
                containment_pct: nextThreat <= 30 ? 94 : 45,
                evidence_pct: choice.id === 'act-5' ? 30 : 92,
                communication_pct: 80,
                downtime_hours: nextDowntime,
                financial_cost: nextCost,
                data_leaked_records: nextThreat > 60 ? 42000 : 0,
                mttr_seconds: stopwatch,
                decisions_summary: choice.outcome,
                weakness_identified: nextThreat > 50 ? "Containment Speed" : "Optimal Protocol",
                next_drill_recommendation: "Operation Silent Login — Host Isolation Drill"
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
        let resp = `Command '${cmd}' not recognized. Type 'help'`;
        if (cmd === 'help') {
          resp = "Available commands: netstat -ano, ps aux, history, isolate-host, clear";
        } else if (cmd.includes('netstat')) {
          resp = "TCP 0.0.0.0:443 0.0.0.0:0 LISTENING [PID 4821]\nTCP 10.240.12.8:49211 -> 185.220.101.4:443 ESTABLISHED [PID 4821 - Cobalt Strike C2 Channel]";
        } else if (cmd.includes('ps')) {
          resp = "PID 4821 | CPU 89.2% | runner.exe -worker [Active Backdoor]\nPID 684  | CPU  0.1% | lsass.exe [Local Security Authority]";
        } else if (cmd === 'history') {
          resp = "101 net user /domain\n102 Get-AuthHash -DumpTarget\n103 schtasks /create /tn UpdateHealthSvc";
        } else if (cmd === 'isolate-host') {
          setIsHostIsolated(true);
          resp = "[EDR AGENT] FIN-GATEWAY-01 network quarantined. All LAN/WAN sockets severed. RAM memory dump preserved.";
        } else if (cmd === 'clear') {
          setTerminalLogs([]);
          setTerminalInput("");
          return;
        }
        setTerminalLogs(prev => [...prev, `$ ${terminalInput}`, resp]);
        setTerminalInput("");
      };

      return (
        <div className="min-h-screen flex flex-col p-4 md:p-6 max-w-[1600px] mx-auto space-y-4">
          
          {/* Top Cyber Command Bar */}
          <header className="cyber-panel rounded-2xl px-6 py-4 flex flex-wrap items-center justify-between gap-4 border border-[#13346B]">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyber-neonBlue to-blue-600 flex items-center justify-center font-orbitron font-extrabold text-black text-xl shadow-lg shadow-cyber-neonBlue/30">
                ⚡
              </div>
              <div>
                <h1 className="font-orbitron font-extrabold text-lg md:text-xl tracking-wider text-white flex items-center gap-2">
                  INCIDENT RESPONSE SIMULATOR
                  <span className="text-[10px] px-2 py-0.5 rounded font-mono bg-cyber-neonBlue/20 text-cyber-neonBlue border border-cyber-neonBlue/40">
                    LIVE DEFENSE CENTER
                  </span>
                </h1>
                <span className="text-xs font-mono text-slate-400">“Every decision changes the incident.”</span>
              </div>
            </div>

            {/* Operator Auth State */}
            <div className="flex items-center gap-4 font-mono text-xs">
              {operatorEmail ? (
                <div className="flex items-center gap-3 bg-[#061226] px-4 py-2 rounded-xl border border-[#143A75]">
                  <span className="w-2.5 h-2.5 rounded-full bg-cyber-neonGreen animate-pulse"></span>
                  <span className="text-slate-300">OPERATOR: <b className="text-white">{operatorEmail}</b></span>
                  <button onClick={() => { localStorage.removeItem("irs_email"); setOperatorEmail(""); setView("auth"); }} className="text-slate-500 hover:text-cyber-neonRed ml-2">
                    Sign Out
                  </button>
                </div>
              ) : (
                <span className="px-3 py-1.5 rounded bg-cyber-neonAmber/10 border border-cyber-neonAmber/40 text-cyber-neonAmber">
                  OPERATOR UNVERIFIED
                </span>
              )}
            </div>
          </header>

          {/* VIEW 1: OPERATOR AUTHENTICATION GATE */}
          {view === "auth" && (
            <main className="flex-1 flex flex-col items-center justify-center py-16">
              <div className="cyber-panel p-8 rounded-3xl max-w-md w-full border border-cyber-neonBlue/40 text-left space-y-6 shadow-2xl relative overflow-hidden">
                <div className="absolute top-0 right-0 w-32 h-32 bg-cyber-neonBlue/10 rounded-full blur-2xl pointer-events-none"></div>
                <div>
                  <span className="text-[10px] font-mono text-cyber-neonCyan uppercase tracking-widest block mb-1">SECURITY ACCESS GATE</span>
                  <h2 className="text-2xl font-orbitron font-bold text-white">Operator Station Login</h2>
                  <p className="text-xs text-slate-400 mt-1">Sign in with your corporate security email to enter the operations center.</p>
                </div>

                <form onSubmit={handleLogin} className="space-y-4">
                  <div>
                    <label className="text-[11px] font-mono text-slate-300 block mb-1">Corporate Security Email</label>
                    <input
                      type="email"
                      required
                      placeholder="e.g. analyst@finsecure.com"
                      value={emailInput}
                      onChange={(e) => setEmailInput(e.target.value)}
                      className="w-full px-4 py-3 rounded-xl bg-[#040C1D] border border-[#13346B] text-white text-xs font-mono focus:outline-none focus:border-cyber-neonBlue placeholder-slate-600"
                    />
                  </div>

                  <button
                    type="submit"
                    className="w-full py-3.5 rounded-xl bg-gradient-to-r from-cyber-neonBlue to-blue-600 hover:from-cyber-neonCyan hover:to-blue-500 text-black font-orbitron font-bold text-xs tracking-wider transition shadow-lg shadow-cyber-neonBlue/30 uppercase"
                  >
                    Enter Command Center ▶
                  </button>
                </form>
              </div>
            </main>
          )}

          {/* VIEW 2: THE FULL HIGH-TECH OPERATIONS COMMAND CENTER */}
          {view === "command_center" && (
            <main className="space-y-4 flex-1">
              
              {/* TOP ROW: TIMELINE & CIRCULAR GAUGES */}
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
                
                {/* 1. Incident Response Timeline (5 cols) */}
                <div className="lg:col-span-5 cyber-panel rounded-2xl p-5 flex flex-col justify-between">
                  <div className="flex justify-between items-center mb-3">
                    <h3 className="font-orbitron font-bold text-sm text-white tracking-wide">Incident Response Timeline</h3>
                    <span className="text-xs font-mono text-cyber-neonBlue">LIVE INC-2026-001</span>
                  </div>

                  {/* Progressive Timeline Milestones */}
                  <div className="relative py-3">
                    <div className="h-1 w-full bg-[#0E244D] rounded-full absolute top-5 z-0"></div>
                    <div
                      className="h-1 bg-gradient-to-r from-cyber-neonBlue to-cyber-neonRed rounded-full absolute top-5 z-0 transition-all duration-700"
                      style={{
                        width: timelineStage === "Detection" ? "25%" : timelineStage === "Analysis" ? "50%" : timelineStage === "Containment" ? "75%" : "100%"
                      }}
                    ></div>

                    <div className="grid grid-cols-4 relative z-10 text-center font-mono">
                      {[
                        { name: "Detection", time: "12:45 PM", active: true },
                        { name: "Analysis", time: "01:10 PM", active: true },
                        { name: "Containment", time: "01:35 PM", active: timelineStage !== "Detection" && timelineStage !== "Analysis" },
                        { name: "Resolution", time: "02:05 PM", active: timelineStage === "Resolution" }
                      ].map((m, i) => (
                        <div key={i} className="flex flex-col items-center">
                          <div className={`w-3.5 h-3.5 rounded-full border-2 transition-all ${m.active ? "bg-cyber-neonCyan border-white shadow-[0_0_10px_#00F0FF]" : "bg-[#040C1D] border-[#13346B]"}`}></div>
                          <span className={`text-[11px] font-bold mt-2 ${m.active ? "text-white" : "text-slate-500"}`}>{m.name}</span>
                          <span className="text-[10px] text-slate-400">{m.time}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Horizontal Bar Breakdown */}
                  <div className="space-y-2 pt-2 border-t border-[#13346B]/60 text-xs font-mono">
                    <div className="flex justify-between items-center">
                      <span className="text-slate-400">Active Incident Elapsed</span>
                      <span className="font-bold text-cyber-neonBlue">{formatTimer(stopwatch)}</span>
                    </div>
                    <div className="w-full bg-[#0E244D] h-1.5 rounded-full overflow-hidden">
                      <div className="bg-cyber-neonBlue h-full rounded-full" style={{ width: '65%' }}></div>
                    </div>

                    <div className="flex justify-between items-center">
                      <span className="text-slate-400">Containment in Progress</span>
                      <span className="font-bold text-cyber-neonRed">{isHostIsolated ? "Completed (Host Air-Gapped)" : "25m In Dwell"}</span>
                    </div>
                    <div className="w-full bg-[#0E244D] h-1.5 rounded-full overflow-hidden">
                      <div className={`h-full rounded-full ${isHostIsolated ? "bg-cyber-neonGreen" : "bg-cyber-neonRed"}`} style={{ width: isHostIsolated ? '100%' : '52%' }}></div>
                    </div>
                  </div>
                </div>

                {/* 2. Threat Severity Radial Gauge (3.5 cols) */}
                <div className="lg:col-span-3 cyber-panel rounded-2xl p-4 flex flex-col items-center justify-between relative overflow-hidden">
                  <div className="w-full flex justify-between items-center mb-1">
                    <span className="font-orbitron font-bold text-xs text-white">Threat Severity</span>
                    <span className="text-[10px] font-mono text-cyber-neonRed font-bold animate-pulse">● CRITICAL</span>
                  </div>
                  <CircularGauge
                    value={threatSeverity}
                    label="Active Threat Index"
                    color={threatSeverity >= 70 ? "#FF2A55" : threatSeverity >= 40 ? "#FFB800" : "#00F59B"}
                    status={threatSeverity >= 70 ? "High" : threatSeverity >= 40 ? "Elevated" : "Controlled"}
                  />
                  <div className="text-[10px] font-mono text-slate-400 text-center">
                    Financial Impact: <b className="text-cyber-neonRed">${financialBurn.toLocaleString()}</b>
                  </div>
                </div>

                {/* 3. System Health Radial Gauge (3.5 cols) */}
                <div className="lg:col-span-4 cyber-panel rounded-2xl p-4 flex flex-col items-center justify-between relative overflow-hidden">
                  <div className="w-full flex justify-between items-center mb-1">
                    <span className="font-orbitron font-bold text-xs text-white">System Health</span>
                    <span className="text-[10px] font-mono text-cyber-neonGreen font-bold">● ACTIVE AGENTS</span>
                  </div>
                  <CircularGauge
                    value={systemHealth}
                    label="Core Banking Availability"
                    color={systemHealth >= 80 ? "#00F59B" : systemHealth >= 60 ? "#FFB800" : "#FF2A55"}
                    status={systemHealth >= 80 ? "Normal" : systemHealth >= 60 ? "Degraded" : "Critical"}
                  />
                  <div className="text-[10px] font-mono text-slate-400 text-center">
                    Service Downtime: <b className="text-cyber-neonBlue">{downtime} hrs</b>
                  </div>
                </div>

              </div>

              {/* MIDDLE ROW: 3D ISOMETRIC NETWORK & TELEMETRY SPARKLINE CARDS */}
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
                
                {/* Left: 3D Isometric Network Topology (5 cols) */}
                <div className="lg:col-span-5 cyber-panel rounded-2xl p-5 flex flex-col justify-between">
                  <div className="flex justify-between items-center mb-2">
                    <h3 className="font-orbitron font-bold text-sm text-white">Network Traffic & Attack Geometry</h3>
                    <span className="text-xs font-mono text-slate-400">FIN-GATEWAY-01</span>
                  </div>
                  <NetworkTopology isIsolated={isHostIsolated} />
                </div>

                {/* Right: Alert Statistics Cards with Sparklines (7 cols) */}
                <div className="lg:col-span-7 cyber-panel rounded-2xl p-5 flex flex-col justify-between">
                  <div className="flex justify-between items-center mb-3">
                    <h3 className="font-orbitron font-bold text-sm text-white">Alert Statistics & Ingestion Telemetry</h3>
                    <span className="text-xs font-mono text-cyber-neonBlue">SIEM FEED: LIVE</span>
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    {/* Stat Card 1 */}
                    <div className="p-3 rounded-xl bg-[#040C1D] border border-[#112C5B] flex flex-col justify-between">
                      <span className="text-[10px] font-mono text-slate-400 uppercase">Total Alerts</span>
                      <div className="text-2xl font-orbitron font-bold text-white mt-1">324</div>
                      <div className="mt-2"><Sparkline points={[12, 18, 15, 25, 22, 34, 40]} strokeColor="#00D2FF" fillColor="rgba(0, 210, 255, 0.15)" /></div>
                    </div>

                    {/* Stat Card 2 */}
                    <div className="p-3 rounded-xl bg-[#040C1D] border border-cyber-neonRed/30 flex flex-col justify-between">
                      <span className="text-[10px] font-mono text-cyber-neonRed uppercase font-bold">Critical Alerts</span>
                      <div className="text-2xl font-orbitron font-bold text-cyber-neonRed mt-1">56</div>
                      <div className="mt-2"><Sparkline points={[8, 14, 12, 28, 35, 48, 56]} strokeColor="#FF2A55" fillColor="rgba(255, 42, 85, 0.2)" /></div>
                    </div>

                    {/* Stat Card 3 */}
                    <div className="p-3 rounded-xl bg-[#040C1D] border border-[#112C5B] flex flex-col justify-between">
                      <span className="text-[10px] font-mono text-slate-400 uppercase">Intrusion Attempts</span>
                      <div className="text-2xl font-orbitron font-bold text-cyber-neonAmber mt-1">88</div>
                      <div className="mt-2"><Sparkline points={[20, 25, 40, 55, 60, 72, 88]} strokeColor="#FFB800" fillColor="rgba(255, 184, 0, 0.15)" /></div>
                    </div>

                    {/* Stat Card 4 */}
                    <div className="p-3 rounded-xl bg-[#040C1D] border border-[#112C5B] flex flex-col justify-between">
                      <span className="text-[10px] font-mono text-slate-400 uppercase">Malware Detections</span>
                      <div className="text-2xl font-orbitron font-bold text-cyber-neonGreen mt-1">27</div>
                      <div className="mt-2"><Sparkline points={[5, 9, 14, 12, 19, 24, 27]} strokeColor="#00F59B" fillColor="rgba(0, 245, 155, 0.15)" /></div>
                    </div>
                  </div>
                </div>

              </div>

              {/* BOTTOM ROW: TOP THREATS TABLE + INTERACTIVE WAR ROOM WORKBENCH */}
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
                
                {/* 1. Live Top Threats Ledger (5 cols) */}
                <div className="lg:col-span-5 cyber-panel rounded-2xl p-5 flex flex-col justify-between">
                  <div className="flex justify-between items-center mb-3">
                    <h3 className="font-orbitron font-bold text-sm text-white">Top Active Threats</h3>
                    <span className="text-xs font-mono text-slate-400">4 Monitored Vectors</span>
                  </div>

                  <div className="overflow-x-auto">
                    <table className="w-full text-left font-mono text-xs">
                      <thead className="text-slate-400 border-b border-[#13346B] text-[10px]">
                        <tr>
                          <th className="pb-2">Attack Type</th>
                          <th className="pb-2">Source IP</th>
                          <th className="pb-2">Severity</th>
                          <th className="pb-2">Status</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-[#13346B]/50 text-slate-300 text-[11px]">
                        <tr>
                          <td className="py-2.5 font-bold text-white flex items-center gap-1.5">
                            <span className="w-1.5 h-1.5 rounded-full bg-cyber-neonRed animate-pulse"></span>
                            Ransomware Lateral
                          </td>
                          <td className="py-2.5 text-slate-400">Bucharest, RO</td>
                          <td className="py-2.5 text-cyber-neonRed font-bold">High</td>
                          <td className="py-2.5 text-cyber-neonGreen font-semibold">{isHostIsolated ? "Contained" : "Active"}</td>
                        </tr>
                        <tr>
                          <td className="py-2.5 font-semibold text-white flex items-center gap-1.5">
                            <span className="w-1.5 h-1.5 rounded-full bg-cyber-neonAmber"></span>
                            Credential Stuffing
                          </td>
                          <td className="py-2.5 text-slate-400">Tor Exit Node</td>
                          <td className="py-2.5 text-cyber-neonAmber font-bold">Medium</td>
                          <td className="py-2.5 text-cyber-neonBlue">In Progress</td>
                        </tr>
                        <tr>
                          <td className="py-2.5 font-semibold text-white flex items-center gap-1.5">
                            <span className="w-1.5 h-1.5 rounded-full bg-cyber-neonRed"></span>
                            Brute Force NTLM
                          </td>
                          <td className="py-2.5 text-slate-400">185.220.101.4</td>
                          <td className="py-2.5 text-cyber-neonRed font-bold">High</td>
                          <td className="py-2.5 text-cyber-neonGreen">Mitigated</td>
                        </tr>
                        <tr>
                          <td className="py-2.5 font-semibold text-white flex items-center gap-1.5">
                            <span className="w-1.5 h-1.5 rounded-full bg-cyber-neonBlue"></span>
                            Data Exfiltration
                          </td>
                          <td className="py-2.5 text-slate-400">Port 443 C2</td>
                          <td className="py-2.5 text-cyber-neonAmber font-bold">Medium</td>
                          <td className="py-2.5 text-cyber-neonGreen">{isHostIsolated ? "Severed" : "Active"}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>

                  {/* Interactive CLI Terminal Drawer */}
                  <div className="mt-4 pt-3 border-t border-[#13346B] font-mono text-xs">
                    <span className="text-[10px] text-cyber-neonCyan font-bold block mb-1">LIVE FORENSIC CLI INVESTIGATION SANDBOX</span>
                    <div className="bg-[#040C1D] p-2.5 rounded-xl border border-[#112C5B] max-h-24 overflow-y-auto text-[10px] text-slate-300 space-y-1 mb-2">
                      {terminalLogs.map((l, i) => <div key={i}>{l}</div>)}
                    </div>
                    <form onSubmit={handleCli} className="flex gap-2">
                      <span className="text-cyber-neonCyan font-bold">$</span>
                      <input
                        type="text"
                        placeholder="type netstat -ano, ps aux, isolate-host..."
                        value={terminalInput}
                        onChange={(e) => setTerminalInput(e.target.value)}
                        className="flex-1 bg-transparent text-white focus:outline-none text-xs font-mono"
                      />
                      <button type="submit" className="px-2.5 py-1 bg-[#0E244D] text-cyber-neonCyan rounded text-[11px] font-bold">
                        EXEC
                      </button>
                    </form>
                  </div>
                </div>

                {/* 2. Interactive Containment Decision Workbench (7 cols) */}
                <div className="lg:col-span-7 cyber-panel rounded-2xl p-6 flex flex-col justify-between border-2 border-cyber-neonBlue/30">
                  <div className="space-y-4">
                    <div className="flex justify-between items-center font-mono text-xs pb-3 border-b border-[#13346B]">
                      <span className="text-cyber-neonCyan font-bold uppercase tracking-wider">
                        {incident.stages[activeStep].title}
                      </span>
                      <span className="text-slate-400">PHASE {activeStep + 1} OF {incident.stages.length}</span>
                    </div>

                    <div className="p-4 rounded-xl bg-[#040C1D] border border-cyber-neonBlue/30 font-mono text-xs text-slate-200 leading-relaxed">
                      {incident.stages[activeStep].briefing}
                    </div>

                    {/* Decision Action Buttons */}
                    <div className="space-y-3 pt-1">
                      {incident.stages[activeStep].choices.map(c => (
                        <button
                          key={c.id}
                          onClick={() => handleDecision(c)}
                          className="w-full text-left p-4 rounded-xl bg-gradient-to-r from-[#040C1D] to-[#081735] hover:from-[#081B3E] hover:to-[#0D295C] border border-[#112C5B] hover:border-cyber-neonCyan/70 transition-all flex flex-col gap-1.5 group font-mono shadow-md"
                        >
                          <div className="flex justify-between items-center">
                            <span className="font-bold text-xs text-white group-hover:text-cyber-neonCyan transition">
                              {c.label}
                            </span>
                            <span className="text-slate-500 group-hover:text-white transition">▶</span>
                          </div>
                          <div className="flex gap-4 text-[10px] text-slate-400">
                            <span>Cost Delta: +${c.cost}</span>
                            <span>SLA Impact: +{c.downtime}h</span>
                            <span className="text-cyber-neonGreen">{c.outcome}</span>
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="pt-4 border-t border-[#13346B] text-[11px] font-mono text-slate-500 text-center">
                    “Every decision recalculates the operational blast radius and threat index.”
                  </div>
                </div>

              </div>

            </main>
          )}

          {/* VIEW 3: NIST COMPLIANT EXECUTIVE DEBRIEF */}
          {view === "debrief" && (
            <main className="flex-1 max-w-4xl mx-auto w-full p-8 space-y-6 my-auto">
              <div className="cyber-panel p-8 rounded-2xl border border-cyber-neonGreen/40 space-y-6">
                <div className="flex justify-between items-center border-b border-[#13346B] pb-6">
                  <div>
                    <span className="text-xs font-mono text-cyber-neonGreen uppercase tracking-widest block mb-1">NIST SP 800-61R2 INCIDENT REPORT</span>
                    <h2 className="text-2xl font-orbitron font-bold text-white">Incident Response Operational Brief</h2>
                  </div>
                  <div className={`px-4 py-1.5 rounded text-xs font-mono font-bold ${threatSeverity <= 40 ? "bg-cyber-neonGreen/10 text-cyber-neonGreen border border-cyber-neonGreen/40" : "bg-cyber-neonRed/10 text-cyber-neonRed border border-cyber-neonRed/40"}`}>
                    {threatSeverity <= 40 ? "SUCCESSFUL CONTAINMENT" : "CRITICAL SLA BREACH"}
                  </div>
                </div>

                <div className="grid grid-cols-4 gap-4 text-center font-mono">
                  <div className="p-4 rounded-xl bg-[#040C1D] border border-[#112C5B]">
                    <span className="text-[10px] text-slate-400 uppercase block mb-1">Threat Index</span>
                    <span className="text-2xl font-orbitron font-bold text-cyber-neonRed">{threatSeverity}%</span>
                  </div>
                  <div className="p-4 rounded-xl bg-[#040C1D] border border-[#112C5B]">
                    <span className="text-[10px] text-slate-400 uppercase block mb-1">System Health</span>
                    <span className="text-2xl font-orbitron font-bold text-cyber-neonGreen">{systemHealth}%</span>
                  </div>
                  <div className="p-4 rounded-xl bg-[#040C1D] border border-[#112C5B]">
                    <span className="text-[10px] text-slate-400 uppercase block mb-1">Financial Loss</span>
                    <span className="text-xl font-bold text-white">${financialBurn.toLocaleString()}</span>
                  </div>
                  <div className="p-4 rounded-xl bg-[#040C1D] border border-[#112C5B]">
                    <span className="text-[10px] text-slate-400 uppercase block mb-1">Service Outage</span>
                    <span className="text-xl font-bold text-cyber-neonBlue">{downtime}h</span>
                  </div>
                </div>

                <div className="space-y-2 pt-2 font-mono text-xs">
                  <h4 className="font-bold text-white uppercase text-[11px] text-slate-400">Playbook Execution Ledger:</h4>
                  {actionHistory.map((act, i) => (
                    <div key={i} className="p-3 rounded bg-[#040C1D] border border-[#112C5B]">
                      <span className="text-slate-500">[{act.time}]</span> <b className="text-cyber-neonCyan">{act.label}</b>
                      <p className="text-slate-300 mt-1">{act.outcome}</p>
                    </div>
                  ))}
                </div>

                <div className="flex justify-end gap-3 pt-6 border-t border-[#13346B] font-mono text-xs">
                  <button onClick={() => window.print()} className="px-4 py-2 bg-[#0E244D] hover:bg-[#13346B] text-white rounded-xl">
                    PRINT DEBRIEF (PDF)
                  </button>
                  <button onClick={() => { setActiveStep(0); setThreatSeverity(76); setSystemHealth(74); setFinancialBurn(12450); setDowntime(0.8); setIsHostIsolated(false); setView("command_center"); }} className="px-5 py-2 bg-cyber-neonBlue hover:bg-cyber-neonCyan text-black font-bold rounded-xl transition">
                    REPLAY SCENARIO ▶
                  </button>
                </div>
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

print("SUCCESS: High-tech cyber defense command center compiled cleanly!")
