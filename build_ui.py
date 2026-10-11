import os

os.makedirs('templates', exist_ok=True)

parts = []

parts.append('''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>INCIDENT RESPONSE SIMULATOR</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <style>
    body { background-color: #0B0F19; color: #E2E8F0; font-family: ui-sans-serif, system-ui, sans-serif; }
    .soc-card { background-color: #161B26; border: 1px solid #1E293B; }
  </style>
</head>
<body class="bg-[#0B0F19] text-[#E2E8F0] min-h-screen">
  <div id="root"></div>

  <script type="text/babel">
    const { useState, useEffect } = React;

    const OPERATION_SILENT_LOGIN = {
      id: "SCN-001",
      title: "Operation Silent Login",
      organization: "FinSecure Technologies",
      incidentType: "Credential Compromise",
      initialAlert: {
        titleTech: "Multiple failed logins followed by successful logon from unusual ASN (Event ID 4624 Type 10)",
        titlePlain: "Someone failed to log in 12 times, then logged into John Doe account from Romania.",
        source: "Auth-Proxy-01",
        severity: "HIGH",
        mitre: "T1078 (Valid Accounts), T1110 (Brute Force)"
      },
      evidenceList: [
        { id: "ev-1", name: "Authentication Logs", category: "Authentication", technical: "Event ID 4625 x12 followed by Event ID 4624 Logon Type 10 (RemoteInteractive). NTLMv2 negotiated.", plain: "Attacker tried 12 passwords before using a stolen password to gain remote desktop access." },
        { id: "ev-2", name: "User Profile & Geolocation", category: "User Activity", technical: "Normal working hours: 09:00 - 18:00 EST. Device: Unrecognized Chrome User-Agent on Linux.", plain: "John works in Atlanta, but this login happened from Eastern Europe at 4 AM local time." },
        { id: "ev-3", name: "Process Execution Tree", category: "Process", technical: "Sysmon Event ID 1: Encoded PowerShell payload attempting download from external IP 185.220.101.4:8443.", plain: "The hacker used command prompt to quietly launch a hidden script calling an external server." },
        { id: "ev-4", name: "Network & DNS Logs", category: "Network", technical: "Zeek Conn log: 4.8MB transferred over outbound SSL session with non-standard certificate.", plain: "The computer sent 4.8 Megabytes of encrypted company data out to a newly registered fake domain." }
      ],
      phases: [
        {
          step: 1,
          promptTech: "Alert triggered: Anomalous geographic login from Romania for an Atlanta-based analyst. How do you respond?",
          promptPlain: "Suspicious login from another country on John Doe account. What should our first move be?",
          choices: [
            {
              id: "c1",
              labelTech: "Investigate authentication logs & user session activity before taking active action",
              labelPlain: "Inspect login history and see what John Doe account is currently doing",
              impactScore: 10,
              business: { downtime: 0, cost: 2000, pii: 0 },
              consequenceTech: "Evidence gathered: Confirmed 12 failed attempts prior to success. Attacker actively executing reconnaissance.",
              consequencePlain: "You verified the login is definitely fake. However, the attacker began executing commands while you checked."
            },
            {
              id: "c2",
              labelTech: "Revoke active Azure AD sessions & force immediate password + MFA reset",
              labelPlain: "Immediately kick the intruder out of the account and reset all passwords",
              impactScore: 25,
              business: { downtime: 0.5, cost: 5000, pii: 0 },
              consequenceTech: "Containment optimal: Session tokens invalidated. Adversary RDP socket disconnected within 45 seconds.",
              consequencePlain: "Great move! The intruder was immediately booted off the machine before touching financial databases."
            },
            {
              id: "c3",
              labelTech: "Ignore alert as false positive (assume user is traveling on international PTO)",
              labelPlain: "Ignore the alert and assume John is on vacation in Europe",
              impactScore: -40,
              business: { downtime: 12, cost: 120000, pii: 45000 },
              consequenceTech: "Critical failure: Adversary accessed wire transfer API secrets and dumped 45,000 banking records.",
              consequencePlain: "Disaster! The attacker spent 3 hours downloading banking records and leaked customer data."
            }
          ]
        },
        {
          step: 2,
          promptTech: "Containment stage: Threat actor attempting credential dumping across local workstation subnet. Choose containment vector:",
          promptPlain: "The hacker is trying to steal passwords from other machines on the network. What containment action do we take?",
          choices: [
            {
              id: "c4",
              labelTech: "Isolate workstation via EDR network quarantine while maintaining agent telemetry",
              labelPlain: "Isolate the infected computer from the network so it cannot infect others",
              impactScore: 25,
              business: { downtime: 1.0, cost: 8000, pii: 0 },
              consequenceTech: "NIST containment standard met. Workstation quarantined. Memory dump preserved for forensics.",
              consequencePlain: "Excellent! The infected machine is trapped in quarantine and cannot touch the rest of the company."
            },
            {
              id: "c5",
              labelTech: "Pull physical power plug immediately on workstation",
              labelPlain: "Rip out the computer power cord immediately to shut it down",
              impactScore: -15,
              business: { downtime: 4.0, cost: 35000, pii: 500 },
              consequenceTech: "Evidence lost: Volatile RAM erased. C2 payload unrecoverable. Secondary backdoor remains active.",
              consequencePlain: "Warning: Pulling the plug destroyed all memory evidence. We can no longer prove what files they took."
            }
          ]
        }
      ]
    };
''')
