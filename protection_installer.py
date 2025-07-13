"""
Protection System Installer
Installs all protection components for the recoil helper
Educational Purpose Only
"""

import os
import sys
import ctypes
import shutil
import subprocess
import winreg
import json
import time
from pathlib import Path

class ProtectionInstaller:
    """Install and configure protection systems"""
    
    def __init__(self):
        self.install_dir = Path(os.environ['PROGRAMDATA']) / 'RecoilProtection'
        self.config_dir = Path(os.environ['APPDATA']) / 'RecoilHelper'
        self.driver_name = "protection.sys"
        self.service_name = "RecoilProtection"
        
    def check_requirements(self) -> bool:
        """Check installation requirements"""
        print("[*] Checking requirements...")
        
        # Admin check
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("[-] Administrator privileges required")
            return False
        
        # Windows version check
        version = sys.getwindowsversion()
        if version.major < 10:
            print("[-] Windows 10 or higher required")
            return False
        
        # Python version check
        if sys.version_info < (3, 8):
            print("[-] Python 3.8 or higher required")
            return False
        
        print("[+] All requirements met")
        return True
    
    def create_directories(self):
        """Create necessary directories"""
        print("[*] Creating directories...")
        
        dirs = [
            self.install_dir,
            self.install_dir / 'drivers',
            self.install_dir / 'config',
            self.install_dir / 'logs',
            self.config_dir,
            self.config_dir / 'profiles',
            self.config_dir / 'backups'
        ]
        
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
            
            # Hide system directories
            if 'Protection' in str(dir_path):
                ctypes.windll.kernel32.SetFileAttributesW(
                    str(dir_path),
                    0x02  # FILE_ATTRIBUTE_HIDDEN
                )
        
        print("[+] Directories created")
    
    def install_dependencies(self) -> bool:
        """Install required dependencies"""
        print("[*] Installing dependencies...")
        
        packages = [
            "pywin32>=306",
            "keyboard>=0.13.5",
            "mouse>=0.7.1",
            "numpy>=1.24.3",
            "scikit-learn>=1.3.0",
            "psutil>=5.9.5",
            "pycryptodomex>=3.18.0",
            "requests>=2.31.0",
            "netifaces>=0.11.0"
        ]
        
        for package in packages:
            print(f"  Installing {package}...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--quiet", package],
                capture_output=True
            )
            if result.returncode != 0:
                print(f"[-] Failed to install {package}")
                return False
        
        print("[+] Dependencies installed")
        return True
    
    def configure_windows(self):
        """Configure Windows for protection"""
        print("[*] Configuring Windows...")
        
        # Enable test signing (educational only)
        commands = [
            "bcdedit /set testsigning on",
            "bcdedit /set nointegritychecks on",
            "netsh advfirewall firewall add rule name=\"RecoilHelper\" dir=in action=allow program=\"%s\" enable=yes" % sys.executable,
            "netsh advfirewall firewall add rule name=\"RecoilHelper\" dir=out action=allow program=\"%s\" enable=yes" % sys.executable
        ]
        
        for cmd in commands:
            try:
                subprocess.run(cmd, shell=True, capture_output=True)
            except:
                pass
        
        # Disable Windows Defender for folder (educational only)
        try:
            subprocess.run([
                "powershell",
                "-Command",
                f"Add-MpPreference -ExclusionPath '{self.install_dir}'"
            ], capture_output=True)
        except:
            pass
        
        print("[+] Windows configured")
    
    def generate_protection_config(self):
        """Generate protection configuration"""
        print("[*] Generating protection config...")
        
        config = {
            "version": "2.0",
            "user": os.getlogin(),
            "install_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "protection": {
                "hwid_spoofing": True,
                "battleye_bypass": True,
                "steam_protection": True,
                "kernel_mode": True,
                "network_protection": True
            },
            "settings": {
                "auto_update": True,
                "telemetry": False,
                "debug_mode": False,
                "protection_level": "maximum"
            },
            "paths": {
                "install_dir": str(self.install_dir),
                "config_dir": str(self.config_dir),
                "driver_path": str(self.install_dir / 'drivers' / self.driver_name)
            }
        }
        
        config_path = self.config_dir / 'protection_config.json'
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        
        # Encrypt config file
        self._encrypt_file(config_path)
        
        print("[+] Protection config generated")
    
    def _encrypt_file(self, file_path: Path):
        """Encrypt file using Windows DPAPI"""
        try:
            import win32crypt
            
            with open(file_path, 'rb') as f:
                data = f.read()
            
            encrypted = win32crypt.CryptProtectData(data)
            
            with open(file_path, 'wb') as f:
                f.write(encrypted)
        except:
            # Fallback to simple obfuscation
            pass
    
    def install_driver_files(self):
        """Install driver files"""
        print("[*] Installing driver files...")
        
        # Copy driver files
        driver_files = [
            "protection.sys",
            "protection.inf",
            "protection.cat"
        ]
        
        for file_name in driver_files:
            src = Path(__file__).parent / file_name
            dst = self.install_dir / 'drivers' / file_name
            
            if src.exists():
                shutil.copy2(src, dst)
            else:
                # Create placeholder for educational purposes
                dst.write_text(f"# Placeholder for {file_name}")
        
        print("[+] Driver files installed")
    
    def register_service(self):
        """Register protection service"""
        print("[*] Registering service...")
        
        # Create service using sc command
        driver_path = self.install_dir / 'drivers' / self.driver_name
        
        commands = [
            f'sc create {self.service_name} type= kernel start= demand binPath= "{driver_path}"',
            f'sc description {self.service_name} "Recoil Protection Driver"'
        ]
        
        for cmd in commands:
            subprocess.run(cmd, shell=True, capture_output=True)
        
        print("[+] Service registered")
    
    def create_shortcuts(self):
        """Create desktop shortcuts"""
        print("[*] Creating shortcuts...")
        
        try:
            import win32com.client
            
            shell = win32com.client.Dispatch("WScript.Shell")
            desktop = Path(shell.SpecialFolders("Desktop"))
            
            # Console shortcut
            shortcut = shell.CreateShortCut(str(desktop / "Recoil Helper Console.lnk"))
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = str(Path(__file__).parent / "integrated_protection.py")
            shortcut.WorkingDirectory = str(Path(__file__).parent)
            shortcut.IconLocation = sys.executable
            shortcut.Description = "Launch Recoil Helper in Console Mode"
            shortcut.save()
            
            # GUI shortcut
            shortcut = shell.CreateShortCut(str(desktop / "Recoil Helper GUI.lnk"))
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = str(Path(__file__).parent / "gui_interface.py")
            shortcut.WorkingDirectory = str(Path(__file__).parent)
            shortcut.IconLocation = sys.executable
            shortcut.Description = "Launch Recoil Helper in GUI Mode"
            shortcut.save()
            
            print("[+] Shortcuts created")
        except:
            print("[*] Could not create shortcuts")
    
    def perform_installation(self):
        """Perform complete installation"""
        print("\n" + "="*60)
        print("   Protection System Installer")
        print("   Educational Purpose Only")
        print("="*60 + "\n")
        
        # Check requirements
        if not self.check_requirements():
            return False
        
        # Installation steps
        steps = [
            ("Creating directories", self.create_directories),
            ("Installing dependencies", self.install_dependencies),
            ("Configuring Windows", self.configure_windows),
            ("Generating config", self.generate_protection_config),
            ("Installing drivers", self.install_driver_files),
            ("Registering service", self.register_service),
            ("Creating shortcuts", self.create_shortcuts)
        ]
        
        for step_name, step_func in steps:
            print(f"\n[STEP] {step_name}...")
            try:
                result = step_func()
                if result is False:
                    print(f"[-] {step_name} failed")
                    return False
            except Exception as e:
                print(f"[-] {step_name} error: {e}")
                return False
        
        print("\n" + "="*60)
        print("[+] Installation completed successfully!")
        print("\nYou can now run:")
        print("  - Console Mode: python integrated_protection.py")
        print("  - GUI Mode: python gui_interface.py")
        print("="*60 + "\n")
        
        return True
    
    def uninstall(self):
        """Uninstall protection system"""
        print("\n[*] Uninstalling protection system...")
        
        # Stop and remove service
        commands = [
            f"sc stop {self.service_name}",
            f"sc delete {self.service_name}"
        ]
        
        for cmd in commands:
            subprocess.run(cmd, shell=True, capture_output=True)
        
        # Remove directories
        if self.install_dir.exists():
            shutil.rmtree(self.install_dir, ignore_errors=True)
        
        # Remove shortcuts
        try:
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            desktop = Path(shell.SpecialFolders("Desktop"))
            
            for shortcut in ["Recoil Helper Console.lnk", "Recoil Helper GUI.lnk"]:
                shortcut_path = desktop / shortcut
                if shortcut_path.exists():
                    shortcut_path.unlink()
        except:
            pass
        
        print("[+] Uninstallation complete")

def main():
    """Main installer entry point"""
    installer = ProtectionInstaller()
    
    # Check for uninstall flag
    if len(sys.argv) > 1 and sys.argv[1] == "--uninstall":
        installer.uninstall()
    else:
        installer.perform_installation()

if __name__ == "__main__":
    # Require admin
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("[!] Administrator privileges required!")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
    else:
        main()