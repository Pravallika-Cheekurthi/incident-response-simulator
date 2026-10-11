import tkinter as tk
from tkinter import messagebox
import webbrowser
import os

PROJECT_INFO_PATH = r"IR info.html"

class CybersecuritySimulator:
    def __init__(self):
        self.scenarios = {
            "Phishing Attack": {
                "description": "An employee receives a suspicious email with a link. What do they do?",
                "options": {
                    "A": "Click the link to see what it is.",
                    "B": "Report the email to IT and delete it.",
                    "C": "Forward the email to a colleague to get their opinion."
                },
                "consequences": {
                    "A": "The link deploys ransomware, encrypting critical files. The incident response team is activated.",
                    "B": "IT confirms the email is malicious and blocks the sender. No compromise occurred.",
                    "C": "The colleague also clicks the link, leading to a wider compromise."
                },
                "correct_option": "B"
            },
            "Operation Silent Login": {
                "description": "Multiple Event 4625 brute force alerts detected followed by Logon Type 10 from Romania.",
                "options": {
                    "A": "Dismiss the alert as a routine VPN failure.",
                    "B": "Revoke active session tokens and enforce EDR host isolation.",
                    "C": "Immediately pull the server power cable."
                },
                "consequences": {
                    "A": "The attacker accesses customer databases and exfiltrates unencrypted records.",
                    "B": "Unauthorized session terminated within 40 seconds; volatile RAM artifacts preserved.",
                    "C": "Connection terminated, but volatile memory evidence erased, violating RFC 3227."
                },
                "correct_option": "B"
            }
        }
        self.scenario_names = list(self.scenarios.keys())
        self.total_scenarios = len(self.scenario_names)
        self.current_scenario_index = 0
        self.score = 0

    def get_scenario(self):
        if self.current_scenario_index < self.total_scenarios:
            name = self.scenario_names[self.current_scenario_index]
            return name, self.scenarios[name]
        return None, None

    def process_choice(self, choice):
        _, scenario = self.get_scenario()
        if choice == scenario["correct_option"]:
            self.score += 1
            return "correct"
        return "incorrect"

    def get_feedback(self, choice):
        _, scenario = self.get_scenario()
        return scenario["consequences"][choice]

    def next_scenario(self):
        self.current_scenario_index += 1
        return self.current_scenario_index < self.total_scenarios


class SimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("INCIDENT RESPONSE SIMULATOR")
        self.root.geometry("900x580")
        self.root.configure(bg="#0b0f19")
        self.simulator = CybersecuritySimulator()

        top_frame = tk.Frame(root, bg="#161b26", padx=16, pady=10)
        top_frame.pack(fill="x", side="top")

        title_lbl = tk.Label(top_frame, text="INCIDENT RESPONSE SIMULATOR", font=("Arial", 15, "bold"), fg="#38bdf8", bg="#161b26")
        title_lbl.pack(side="left")

        btn_info = tk.Button(top_frame, text="Documentation", bg="#0284c7", fg="white", font=("Arial", 9, "bold"),
                             command=self.open_info, relief="flat", padx=10, pady=4)
        btn_info.pack(side="right", padx=4)

        btn_web = tk.Button(top_frame, text="Launch Web HUD", bg="#10b981", fg="white", font=("Arial", 9, "bold"),
                            command=self.open_web, relief="flat", padx=10, pady=4)
        btn_web.pack(side="right", padx=4)

        main_frame = tk.Frame(root, bg="#0b0f19", padx=14, pady=14)
        main_frame.pack(fill="both", expand=True)

        left_frame = tk.Frame(main_frame, bg="#0b0f19")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        obj_frame = tk.LabelFrame(left_frame, text=" OBJECTIVE ", font=("Arial", 10, "bold"), fg="#38bdf8", bg="#161b26", padx=10, pady=6)
        obj_frame.pack(fill="x", pady=(0, 8))
        self.obj_text = tk.Label(obj_frame, text="Detect and contain the unauthorized access", font=("Arial", 11), fg="#e2e8f0", bg="#161b26", anchor="w")
        self.obj_text.pack(fill="x")

        inc_frame = tk.LabelFrame(left_frame, text=" INCIDENT ", font=("Arial", 10, "bold"), fg="#f59e0b", bg="#161b26", padx=10, pady=6)
        inc_frame.pack(fill="x", pady=(0, 8))
        self.scenario_lbl = tk.Label(inc_frame, text="", font=("Arial", 10), fg="#f8fafc", bg="#161b26", wraplength=480, justify="left", anchor="w")
        self.scenario_lbl.pack(fill="x")

        act_frame = tk.LabelFrame(left_frame, text=" ACTIONS ", font=("Arial", 10, "bold"), fg="#10b981", bg="#161b26", padx=10, pady=6)
        act_frame.pack(fill="x", pady=(0, 8))
        self.options_frame = tk.Frame(act_frame, bg="#161b26")
        self.options_frame.pack(fill="x")

        fb_frame = tk.LabelFrame(left_frame, text=" FEEDBACK & CONSEQUENCE ", font=("Arial", 10, "bold"), fg="#94a3b8", bg="#161b26", padx=10, pady=6)
        fb_frame.pack(fill="both", expand=True)
        self.feedback_text = tk.Text(fb_frame, height=4, bg="#0f172a", fg="#e2e8f0", font=("Consolas", 10), wrap="word", relief="flat")
        self.feedback_text.pack(fill="both", expand=True)
        self.feedback_text.tag_config("correct_tag", foreground="#4ade80")
        self.feedback_text.tag_config("incorrect_tag", foreground="#f87171")
        self.feedback_text.config(state="disabled")

        ctrl_frame = tk.Frame(left_frame, bg="#0b0f19", pady=6)
        ctrl_frame.pack(fill="x")
        self.next_button = tk.Button(ctrl_frame, text="Next Scenario →", font=("Arial", 10, "bold"), bg="#3b82f6", fg="white",
                                     command=self.next_scenario, relief="flat", padx=14, pady=5, state="disabled")
        self.next_button.pack(side="right")

        right_frame = tk.LabelFrame(main_frame, text=" NETWORK ", font=("Arial", 10, "bold"), fg="#38bdf8", bg="#161b26", padx=10, pady=10)
        right_frame.pack(side="right", fill="both", expand=False)
        self.canvas = tk.Canvas(right_frame, width=280, height=360, bg="#0f172a", highlightthickness=0)
        self.canvas.pack()
        self.draw_network_topology()

        self.load_scenario()

    def draw_network_topology(self):
        self.canvas.delete("all")
        cx, cy = 140, 180
        nodes = [(60, 75, "WS-01"), (220, 75, "WS-02"), (60, 285, "SERVER"), (220, 285, "GATEWAY")]
        for nx, ny, label in nodes:
            self.canvas.create_line(cx, cy, nx, ny, fill="#334155", width=2, dash=(3, 2))
            self.canvas.create_rectangle(nx-28, ny-18, nx+28, ny+18, fill="#1e293b", outline="#38bdf8", width=2)
            self.canvas.create_text(nx, ny, text=label, fill="#e2e8f0", font=("Arial", 8, "bold"))

        self.canvas.create_oval(cx-32, cy-32, cx+32, cy+32, fill="#ef4444", outline="#b91c1c", width=3)
        self.canvas.create_text(cx, cy, text="!", fill="#ffffff", font=("Arial", 26, "bold"))

    def load_scenario(self):
        name, scenario = self.simulator.get_scenario()
        if not scenario:
            return

        self.scenario_lbl.config(text=f"Scenario: {name}\n{scenario['description']}")
        
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        for key, opt_text in scenario["options"].items():
            btn = tk.Button(self.options_frame, text=f"({key}) {opt_text}", font=("Arial", 9), bg="#1e293b", fg="#e2e8f0",
                            anchor="w", justify="left", padx=8, pady=6, relief="flat",
                            command=lambda k=key: self.process_choice(k))
            btn.pack(fill="x", pady=2)

        self.feedback_text.config(state="normal")
        self.feedback_text.delete(1.0, tk.END)
        self.feedback_text.insert(tk.END, "Select an action to mitigate the incident...")
        self.feedback_text.config(state="disabled")
        self.next_button.config(state="disabled")

    def process_choice(self, choice):
        feedback = self.simulator.get_feedback(choice)
        outcome = self.simulator.process_choice(choice)

        self.feedback_text.config(state="normal")
        self.feedback_text.delete(1.0, tk.END)
        self.feedback_text.insert(tk.END, f"Selected: '{choice}'\nOutcome: {feedback}\n\n")

        if outcome == "correct":
            self.feedback_text.insert(tk.END, "✔ Correct response aligned with best practices.", "correct_tag")
        else:
            correct_opt = self.simulator.scenarios[self.simulator.scenario_names[self.simulator.current_scenario_index]]["correct_option"]
            self.feedback_text.insert(tk.END, f"✖ Negative impact detected. Recommended: Option ({correct_opt}).", "incorrect_tag")

        self.feedback_text.config(state="disabled")

        for widget in self.options_frame.winfo_children():
            widget.config(state="disabled")

        self.next_button.config(state="normal")

    def next_scenario(self):
        if self.simulator.next_scenario():
            self.load_scenario()
        else:
            final_score = f"Final Score: {self.simulator.score} / {self.simulator.total_scenarios}"
            messagebox.showinfo("Simulation Complete", f"Completed all scenarios!\n{final_score}")
            self.root.destroy()

    def open_info(self):
        if os.path.exists(PROJECT_INFO_PATH):
            webbrowser.open(os.path.abspath(PROJECT_INFO_PATH))
        else:
            messagebox.showwarning("File Missing", "IR info.html not found.")

    def open_web(self):
        webbrowser.open("http://127.0.0.1:8000")


if __name__ == "__main__":
    root = tk.Tk()
    app = SimulatorGUI(root)
    root.mainloop()