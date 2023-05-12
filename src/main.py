import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Style

class LogAnalyzer:
    def __init__(self):
        self.keywords = ["logged in", "issued server command", "lost connection", "left the game"]
        self.log_file_path = ""
        self.spam_logs_count = 0
        self.dark_mode = False
        
        self.root = tk.Tk()
        self.root.title("Log Analyzer")
        self.root.geometry("400x300")
        
        # Configure the style for light and dark mode
        self.style = Style()
        self.style.theme_use("clam")
        self.style.configure("Light.TLabel", background="white")
        self.style.configure("Dark.TLabel", background="#303030", foreground="white")
        
        # Create the mode switch icon button
        self.mode_icon = tk.PhotoImage(file="images/mode_icon_light.png")
        self.mode_button = tk.Button(self.root, image=self.mode_icon, command=self.toggle_mode)
        self.mode_button.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Create the open log file button
        self.open_button = tk.Button(self.root, text="Open Log File", command=self.open_log_file)
        self.open_button.pack(pady=20)
        
        # Create the analyze logs button
        self.analyze_button = tk.Button(self.root, text="Analyze Logs", command=self.analyze_logs)
        self.analyze_button.pack(pady=10)
        
        # Create the spam logs label
        self.spam_logs_label = tk.Label(self.root, text="Spam Logs: 0")
        self.spam_logs_label.pack(pady=10)
        
        # Create the remove spam logs button
        self.remove_spam_button = tk.Button(self.root, text="Remove Spam Logs", command=self.remove_spam_logs)
        self.remove_spam_button.pack(pady=10)
        
        # Create the result label
        self.result_label = tk.Label(self.root, text="", wraplength=380, justify=tk.LEFT)
        self.result_label.pack(pady=10)
        
        self.root.mainloop()
        
    def open_log_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.log")])
        if file_path:
            self.log_file_path = file_path
            self.spam_logs_count = 0
            self.spam_logs_label.configure(text="Spam Logs: 0")
            self.result_label.configure(text="")
    
    def analyze_logs(self):
        if not self.log_file_path:
            messagebox.showerror("Error", "Please open a log file first.")
            return
        
        try:
            with open(self.log_file_path, "r") as log_file:
                lines = log_file.readlines()
                result = ""
                spam_logs = []
                for line in lines:
                    if any(keyword in line for keyword in self.keywords):
                        result += line
                        spam_logs.append(line)
                
                self.spam_logs_count = len(spam_logs)
                self.spam_logs_label.configure(text=f"Spam Logs: {self.spam_logs_count}")
                self.result_label.configure(text=result)
        except IOError:
            messagebox.showerror("Error", "Failed to open the log file.")
            
    def remove_spam_logs(self):
        if self.spam_logs_count == 0:
            messagebox.showinfo("No Spam Logs", "There are no spam logs to remove.")
        else:
            with open(self.log_file_path, "r+") as log_file:
                lines = log_file.readlines()
                log_file.seek(0)
                for line in lines:
                    if not any(keyword in line for keyword in self.keywords):
                        log_file.write(line)
                log_file.truncate()
            
            messagebox.showinfo("Spam Logs Removed", f"{self.spam_logs_count} spam logs have been removed.")
            self.spam_logs_count = 0
            self.spam_logs_label.configure(text="Spam Logs: 0")
            self.result_label.configure(text="")
            
    def toggle_mode(self):
        if self.dark_mode:
            self.style.theme_use("clam")
            self.mode_icon = tk.PhotoImage(file="images/mode_icon_light.png")
            self.mode_button.configure(image=self.mode_icon)
            self.dark_mode = False
        else:
            self.style.theme_use("clam")
            self.style.configure("TLabel", background="#303030", foreground="white")
            self.mode_icon = tk.PhotoImage(file="images/mode_icon_dark.png")
            self.mode_button.configure(image=self.mode_icon)
            self.dark_mode = True
            
LogAnalyzer()