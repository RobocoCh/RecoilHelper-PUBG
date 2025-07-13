"""
Optional GUI Interface for Advanced Recoil Helper
Educational Purpose Only
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import queue
import json
import os
from datetime import datetime
from typing import Dict, Any

from advanced_recoil_helper import AdvancedRecoilHelper
from pattern_analyzer import PatternAnalyzer
from config_generator import ConfigGenerator

class RecoilHelperGUI:
    """GUI Interface for the recoil helper"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced Recoil Helper v2.0 - Educational")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Set dark theme
        self.root.configure(bg='#1e1e1e')
        
        # Variables
        self.is_running = False
        self.current_weapon = tk.StringVar(value="M416")
        self.current_scope = tk.DoubleVar(value=1.0)
        self.assist_strength = tk.DoubleVar(value=0.65)
        self.smooth_factor = tk.DoubleVar(value=0.75)
        
        # Queue for thread communication
        self.message_queue = queue.Queue()
        
        # Helper instance
        self.helper = None
        self.helper_thread = None
        
        # Initialize UI
        self._create_widgets()
        self._start_message_handler()
    
    def _create_widgets(self):
        """Create all GUI widgets"""
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Dark.TFrame', background='#1e1e1e')
        style.configure('Dark.TLabel', background='#1e1e1e', foreground='white')
        style.configure('Dark.TButton', background='#2d2d2d', foreground='white')
        style.configure('Status.TLabel', background='#1e1e1e', foreground='#00ff00')
        
        # Main container
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Advanced PUBG Recoil Helper",
            font=('Arial', 20, 'bold'),
            style='Dark.TLabel'
        )
        title_label.pack(pady=(0, 10))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", style='Dark.TFrame')
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = ttk.Label(
            status_frame,
            text="● INACTIVE",
            font=('Arial', 12),
            style='Status.TLabel'
        )
        self.status_label.pack(padx=10, pady=5)
        
        # Control frame
        control_frame = ttk.LabelFrame(main_frame, text="Controls", style='Dark.TFrame')
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Toggle button
        self.toggle_button = ttk.Button(
            control_frame,
            text="START",
            command=self._toggle_helper,
            style='Dark.TButton'
        )
        self.toggle_button.pack(pady=10)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", style='Dark.TFrame')
        settings_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Weapon selection
        weapon_frame = ttk.Frame(settings_frame, style='Dark.TFrame')
        weapon_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(weapon_frame, text="Weapon:", style='Dark.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        
        weapons = ["M416", "AKM", "SCAR-L", "Beryl", "M762", "QBZ"]
        weapon_menu = ttk.Combobox(
            weapon_frame,
            textvariable=self.current_weapon,
            values=weapons,
            state='readonly',
            width=15
        )
        weapon_menu.pack(side=tk.LEFT)
        weapon_menu.bind('<<ComboboxSelected>>', self._on_weapon_change)
        
        # Scope selection
        scope_frame = ttk.Frame(settings_frame, style='Dark.TFrame')
        scope_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(scope_frame, text="Scope:", style='Dark.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        
        scope_buttons_frame = ttk.Frame(scope_frame, style='Dark.TFrame')
        scope_buttons_frame.pack(side=tk.LEFT)
        
        for scope in [1, 2, 3, 4]:
            btn = ttk.Button(
                scope_buttons_frame,
                text=f"{scope}x",
                command=lambda s=scope: self._set_scope(float(s)),
                width=5,
                style='Dark.TButton'
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        # Sliders
        sliders_frame = ttk.Frame(settings_frame, style='Dark.TFrame')
        sliders_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Assist strength slider
        assist_frame = ttk.Frame(sliders_frame, style='Dark.TFrame')
        assist_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(assist_frame, text="Assist Strength:", style='Dark.TLabel').pack(anchor=tk.W)
        self.assist_label = ttk.Label(assist_frame, text="65%", style='Dark.TLabel')
        self.assist_label.pack(anchor=tk.E)
        
        assist_scale = ttk.Scale(
            assist_frame,
            from_=0.1,
            to=1.0,
            variable=self.assist_strength,
            orient=tk.HORIZONTAL,
            command=self._on_assist_change
        )
        assist_scale.pack(fill=tk.X)
        
        # Smooth factor slider
        smooth_frame = ttk.Frame(sliders_frame, style='Dark.TFrame')
        smooth_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(smooth_frame, text="Smoothing:", style='Dark.TLabel').pack(anchor=tk.W)
        self.smooth_label = ttk.Label(smooth_frame, text="75%", style='Dark.TLabel')
        self.smooth_label.pack(anchor=tk.E)
        
        smooth_scale = ttk.Scale(
            smooth_frame,
            from_=0.1,
            to=1.0,
            variable=self.smooth_factor,
            orient=tk.HORIZONTAL,
            command=self._on_smooth_change
        )
        smooth_scale.pack(fill=tk.X)
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", style='Dark.TFrame')
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Log text widget
        self.log_text = tk.Text(
            log_frame,
            height=8,
            bg='#2d2d2d',
            fg='white',
            font=('Consolas', 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar for log
        scrollbar = ttk.Scrollbar(self.log_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_text.yview)
        
        # Warning label
        warning_label = ttk.Label(
            main_frame,
            text="⚠ Educational Purpose Only - Do not use in online games",
            font=('Arial', 10, 'italic'),
            foreground='yellow',
            style='Dark.TLabel'
        )
        warning_label.pack(pady=(5, 0))
        
        # Initial log
        self._log("Advanced Recoil Helper GUI initialized")
        self._log("User: RobocoCh")
        self._log("Ready to start...")
    
    def _toggle_helper(self):
        """Toggle helper on/off"""
        if not self.is_running:
            self._start_helper()
        else:
            self._stop_helper()
    
    def _start_helper(self):
        """Start the helper in a separate thread"""
        self.is_running = True
        self.toggle_button.config(text="STOP")
        self.status_label.config(text="● ACTIVE", foreground='#00ff00')
        
        # Create helper instance with current settings
        self.helper = AdvancedRecoilHelper()
        self.helper.assist_strength = self.assist_strength.get()
        self.helper.smooth_factor = self.smooth_factor.get()
        self.helper.current_weapon = self.current_weapon.get()
        self.helper.current_scope = self.current_scope.get()
        
        # Override some methods to send messages to GUI
        original_toggle = self.helper.toggle_script
        def gui_toggle():
            original_toggle()
            self.message_queue.put(("status", "Helper toggled"))
        self.helper.toggle_script = gui_toggle
        
        # Start in thread
        self.helper_thread = threading.Thread(target=self._run_helper, daemon=True)
        self.helper_thread.start()
        
        self._log(f"Helper started - Weapon: {self.current_weapon.get()}, Scope: {self.current_scope.get()}x")
    
    def _stop_helper(self):
        """Stop the helper"""
        self.is_running = False
        self.toggle_button.config(text="START")
        self.status_label.config(text="● INACTIVE", foreground='red')
        
        if self.helper:
            self.helper.is_active = False
            self.helper = None
        
        self._log("Helper stopped")
    
    def _run_helper(self):
        """Run helper in thread"""
        try:
            # Initialize and run
            self.helper.setup_hotkeys()
            self.helper.toggle_script()  # Activate
            
            # Keep thread alive
            while self.is_running:
                threading.Event().wait(0.1)
                
        except Exception as e:
            self.message_queue.put(("error", str(e)))
    
    def _on_weapon_change(self, event=None):
        """Handle weapon change"""
        weapon = self.current_weapon.get()
        if self.helper:
            self.helper.current_weapon = weapon
        self._log(f"Weapon changed to: {weapon}")
    
    def _set_scope(self, scope: float):
        """Set scope value"""
        self.current_scope.set(scope)
        if self.helper:
            self.helper.current_scope = scope
        self._log(f"Scope set to: {scope}x")
    
    def _on_assist_change(self, value):
        """Handle assist strength change"""
        strength = float(value)
        self.assist_label.config(text=f"{int(strength * 100)}%")
        if self.helper:
            self.helper.assist_strength = strength
    
    def _on_smooth_change(self, value):
        """Handle smooth factor change"""
        smooth = float(value)
        self.smooth_label.config(text=f"{int(smooth * 100)}%")
        if self.helper:
            self.helper.smooth_factor = smooth
    
    def _log(self, message: str):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
    
    def _start_message_handler(self):
        """Start message queue handler"""
        def handle_messages():
            try:
                while True:
                    msg_type, msg_data = self.message_queue.get_nowait()
                    if msg_type == "log":
                        self._log(msg_data)
                    elif msg_type == "error":
                        self._log(f"ERROR: {msg_data}")
                        messagebox.showerror("Error", msg_data)
            except queue.Empty:
                pass
            
            self.root.after(100, handle_messages)
        
        handle_messages()
    
    def run(self):
        """Run the GUI"""
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"800x600+{x}+{y}")
        
        # Set icon (if available)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Run
        self.root.mainloop()

if __name__ == "__main__":
    # Check if running as admin
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Please run as administrator!")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
    else:
        gui = RecoilHelperGUI()
        gui.run()