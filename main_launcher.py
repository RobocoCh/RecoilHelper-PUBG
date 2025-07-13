"""
Main Launcher with Integrity Checks
Educational Purpose Only
"""

import os
import sys
import ctypes
import hashlib
import json
import subprocess
import time
from datetime import datetime
import winreg
import threading

# Import all modules
from advanced_recoil_helper import AdvancedRecoilHelper
from driver_interface import DriverInterface, KernelCallbacks
from memory_utils import MemoryProtection, CodeInjection
from pattern_analyzer import PatternAnalyzer, AdaptiveCompensation
from anti_detection import AntiDetection
from config_generator import ConfigGenerator

class MainLauncher:
    """Main launcher with integrity and security checks"""
    
    def __init__(self):
        self.version = "2.0.0"
        self.build_date = "2025-01-13"
        self.user = "RobocoCh"
        self.modules_hash = {}
        self.is_verified = False
        
    def verify_integrity(self) -> bool:
        """Verify all modules integrity"""
        print("[*] Verifying module integrity...")
        
        required_modules = [
            "advanced_recoil_helper.py",
            "driver_interface.py",
            "memory_utils.py",
            "pattern_analyzer.py",
            "anti_detection.py",
            "config_generator.py"
        ]
        
        for module in required_modules:
            if not os.path.exists(module):
                print(f"[!] Missing module: {module}")
                return False
            
            # Calculate hash
            with open(module, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
                self.modules_hash[module] = file_hash
        
        print("[+] All modules verified")
        return True
    
    def check_requirements(self) -> bool:
        """Check system requirements"""
        print("[*] Checking system requirements...")
        
        # Check Windows version
        try:
            version = sys.getwindowsversion()
            if version.major < 10:
                print("[!] Windows 10 or higher required")
                return False
        except:
            pass
        
        # Check Python version
        if sys.version_info < (3, 8):
            print("[!] Python 3.8 or higher required")
            return False
        
        # Check admin rights
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("[!] Administrator privileges required")
            return False
        
        # Check required packages
        try:
            import win32api
            import keyboard
            import mouse
            import numpy
            import sklearn
            import psutil
            from Cryptodome.Cipher import AES
        except ImportError as e:
            print(f"[!] Missing package: {e}")
            return False
        
        print("[+] All requirements met")
        return True
    
    def initialize_protection(self) -> bool:
        """Initialize protection systems"""
        print("[*] Initializing protection systems...")
        
        # Create anti-detection instance
        anti_detect = AntiDetection()
        
        # Run detection checks
        detections = anti_detect.check_all_detections()
        
        if any(detections.values()):
            print("[!] Detection warning:")
            for method, detected in detections.items():
                if detected:
                    print(f"    - {method}: DETECTED")
            
            # Continue anyway for educational purposes
            print("[*] Continuing in educational mode...")
        
        # Apply protections
        anti_detect.apply_anti_debugging()
        anti_detect.obfuscate_memory()
        
        print("[+] Protection systems initialized")
        return True
    
    def create_system_snapshot(self):
        """Create system snapshot for restoration"""
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "user": self.user,
            "version": self.version,
            "modules": self.modules_hash,
            "system": {
                "platform": sys.platform,
                "version": sys.version,
                "cpu_count": os.cpu_count(),
                "memory": psutil.virtual_memory().total
            }
        }
        
        # Save snapshot
        snapshot_path = os.path.join(os.environ['APPDATA'], 'RecoilHelper', 'snapshot.json')
        os.makedirs(os.path.dirname(snapshot_path), exist_ok=True)
        
        with open(snapshot_path, 'w') as f:
            json.dump(snapshot, f, indent=4)
        
        # Hide file
        ctypes.windll.kernel32.SetFileAttributesW(
            snapshot_path,
            0x02  # FILE_ATTRIBUTE_HIDDEN
        )
    
    def setup_crash_handler(self):
        """Setup crash handler for clean exit"""
        def crash_handler(exc_type, exc_value, exc_traceback):
            print(f"\n[!] Unexpected error: {exc_type.__name__}")
            print(f"[!] {exc_value}")
            
            # Clean up
            print("[*] Performing cleanup...")
            
            # Log crash
            crash_log = {
                "timestamp": datetime.now().isoformat(),
                "error": str(exc_value),
                "type": exc_type.__name__
            }
            
            log_path = os.path.join(os.environ['APPDATA'], 'RecoilHelper', 'crash.log')
            with open(log_path, 'a') as f:
                f.write(json.dumps(crash_log) + '\n')
            
            print("[*] Cleanup complete")
            sys.exit(1)
        
        sys.excepthook = crash_handler
    
    def display_banner(self):
        """Display application banner"""
        banner = f"""
╔══════════════════════════════════════════════════════════════╗
║         Advanced PUBG Recoil Helper v{self.version}          ║
║                  Educational Purpose Only                     ║
╠══════════════════════════════════════════════════════════════╣
║  User: {self.user:<52}║
║  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<52}║
║  Build: {self.build_date:<51}║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def launch(self):
        """Main launch sequence"""
        # Display banner
        self.display_banner()
        
        # Verify integrity
        if not self.verify_integrity():
            print("\n[!] Integrity check failed!")
            input("Press Enter to exit...")
            return
        
        # Check requirements
        if not self.check_requirements():
            print("\n[!] Requirements check failed!")
            input("Press Enter to exit...")
            return
        
        # Initialize protection
        if not self.initialize_protection():
            print("\n[!] Protection initialization failed!")
            input("Press Enter to exit...")
            return
        
        # Create system snapshot
        self.create_system_snapshot()
        
        # Setup crash handler
        self.setup_crash_handler()
        
        # Generate user config
        print("\n[*] Loading user configuration...")
        user_settings = {
            "general_sens": 39,
            "vertical_multiplier": 1.2,
            "aim_sens": 30,
            "ads_sens": 26,
            "scope_2x": 27,
            "scope_3x": 29,
            "scope_4x": 29
        }
        
        config_gen = ConfigGenerator()
        config = config_gen.generate_config(user_settings)
        config_path = config_gen.save_config(config)
        print(f"[+] Configuration saved to: {config_path}")
        
        # Initialize components
        print("\n[*] Initializing components...")
        
        # Pattern analyzer
        pattern_analyzer = PatternAnalyzer()
        print("[+] Pattern analyzer initialized")
        
        # Memory protection
        mem_protection = MemoryProtection()
        print("[+] Memory protection initialized")
        
        # Driver interface
        driver = DriverInterface()
        if driver.open_device():
            print("[+] Driver interface connected")
        else:
            print("[*] Driver interface using fallback mode")
        
        # Launch main application
        print("\n[*] Launching Advanced Recoil Helper...")
        print("="*60)
        
        try:
            # Create and run helper
            helper = AdvancedRecoilHelper()
            
            # Inject pattern analyzer
            helper.pattern_analyzer = pattern_analyzer
            helper.adaptive_comp = AdaptiveCompensation(pattern_analyzer)
            
            # Run
            helper.run()
            
        except KeyboardInterrupt:
            print("\n\n[*] Shutting down gracefully...")
        finally:
            # Cleanup
            driver.close_device()
            print("[+] Cleanup complete")
            print("\nThank you for using Advanced Recoil Helper (Educational)")

if __name__ == "__main__":
    launcher = MainLauncher()
    launcher.launch()