"""
Advanced anti-detection mechanisms
Educational purposes only
"""

import ctypes
import os
import sys
import time
import hashlib
import random
import win32api
import win32con
import win32process
import win32security
import psutil
from typing import List, Dict

class AntiDetection:
    """Advanced anti-detection techniques"""
    
    def __init__(self):
        self.kernel32 = ctypes.windll.kernel32
        self.ntdll = ctypes.windll.ntdll
        self.suspicious_processes = [
            "processhacker", "x64dbg", "ollydbg", "ida", "wireshark",
            "fiddler", "cheatengine", "procmon", "procexp", "apimonitor",
            "sysinternal", "windbg", "dumpcap", "hookshark", "httpdebugger"
        ]
        self.detection_methods = []
        
    def check_all_detections(self) -> Dict[str, bool]:
        """Run all detection checks"""
        results = {
            "debugger": self.detect_debugger(),
            "vm": self.detect_virtual_machine(),
            "sandbox": self.detect_sandbox(),
            "analysis_tools": self.detect_analysis_tools(),
            "hooks": self.detect_hooks(),
            "timing": self.detect_timing_attacks()
        }
        return results
    
    def detect_debugger(self) -> bool:
        """Multiple debugger detection methods"""
        # Method 1: IsDebuggerPresent
        if self.kernel32.IsDebuggerPresent():
            return True
        
        # Method 2: CheckRemoteDebuggerPresent
        process_handle = self.kernel32.GetCurrentProcess()
        is_debugged = ctypes.c_bool(False)
        self.kernel32.CheckRemoteDebuggerPresent(process_handle, ctypes.byref(is_debugged))
        if is_debugged.value:
            return True
        
        # Method 3: NtQueryInformationProcess
        process_debug_port = ctypes.c_ulong(0)
        status = self.ntdll.NtQueryInformationProcess(
            process_handle, 7, ctypes.byref(process_debug_port),
            ctypes.sizeof(process_debug_port), None
        )
        if process_debug_port.value != 0:
            return True
        
        # Method 4: Debug flags
        process_debug_flags = ctypes.c_ulong(0)
        status = self.ntdll.NtQueryInformationProcess(
            process_handle, 31, ctypes.byref(process_debug_flags),
            ctypes.sizeof(process_debug_flags), None
        )
        if process_debug_flags.value == 0:
            return True
        
        # Method 5: PEB.BeingDebugged
        peb = ctypes.c_void_p()
        status = self.ntdll.NtQueryInformationProcess(
            process_handle, 0, ctypes.byref(peb),
            ctypes.sizeof(peb), None
        )
        if peb:
            being_debugged = ctypes.c_byte()
            self.kernel32.ReadProcessMemory(
                process_handle,
                ctypes.c_void_p(peb.value + 2),
                ctypes.byref(being_debugged),
                1,
                None
            )
            if being_debugged.value != 0:
                return True
        
        return False
    
    def detect_virtual_machine(self) -> bool:
        """Detect virtual machine environment"""
        # Check CPU ID
        try:
            cpu_info = subprocess.check_output("wmic cpu get name", shell=True).decode()
            vm_signatures = ["vmware", "virtualbox", "qemu", "kvm", "xen", "parallels"]
            for sig in vm_signatures:
                if sig in cpu_info.lower():
                    return True
        except:
            pass
        
        # Check registry keys
        vm_keys = [
            r"SOFTWARE\VMware, Inc.\VMware Tools",
            r"SOFTWARE\Oracle\VirtualBox Guest Additions",
            r"SYSTEM\CurrentControlSet\Services\VBoxGuest"
        ]
        
        for key_path in vm_keys:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)
                winreg.CloseKey(key)
                return True
            except:
                pass
        
        # Check files
        vm_files = [
            r"C:\Windows\System32\drivers\VBoxMouse.sys",
            r"C:\Windows\System32\drivers\VBoxGuest.sys",
            r"C:\Windows\System32\drivers\vmci.sys",
            r"C:\Windows\System32\drivers\vmmouse.sys"
        ]
        
        for file_path in vm_files:
            if os.path.exists(file_path):
                return True
        
        return False
    
    def detect_sandbox(self) -> bool:
        """Detect sandbox environment"""
        # Check username
        sandbox_users = ["sandbox", "virus", "malware", "test", "sample"]
        current_user = os.environ.get("USERNAME", "").lower()
        for user in sandbox_users:
            if user in current_user:
                return True
        
        # Check process count
        if len(list(psutil.process_iter())) < 50:
            return True
        
        # Check CPU cores
        if psutil.cpu_count() < 2:
            return True
        
        # Check RAM
        if psutil.virtual_memory().total < 4 * 1024 * 1024 * 1024:  # Less than 4GB
            return True
        
        # Check recent files
        recent_path = os.path.expanduser("~\\Recent")
        if os.path.exists(recent_path):
            recent_files = os.listdir(recent_path)
            if len(recent_files) < 5:
                return True
        
        return False
    
    def detect_analysis_tools(self) -> bool:
        """Detect analysis tools"""
        for proc in psutil.process_iter(['name']):
            try:
                proc_name = proc.info['name'].lower()
                for suspicious in self.suspicious_processes:
                    if suspicious in proc_name:
                        return True
            except:
                pass
        
        # Check loaded modules
        modules = []
        try:
            for proc in psutil.process_iter(['pid']):
                if proc.info['pid'] == os.getpid():
                    modules = [m.path.lower() for m in proc.memory_maps()]
                    break
        except:
            pass
        
        suspicious_dlls = ["hook", "inject", "detour", "api", "monitor", "trace"]
        for module in modules:
            for dll in suspicious_dlls:
                if dll in module:
                    return True
        
        return False
    
    def detect_hooks(self) -> bool:
        """Detect API hooks"""
        # Check common hooked functions
        functions_to_check = [
            ("kernel32.dll", "CreateProcessW"),
            ("kernel32.dll", "OpenProcess"),
            ("ntdll.dll", "NtQuerySystemInformation"),
            ("user32.dll", "SetWindowsHookExW")
        ]
        
        for dll_name, func_name in functions_to_check:
            try:
                dll = ctypes.WinDLL(dll_name)
                func = getattr(dll, func_name)
                func_addr = ctypes.cast(func, ctypes.c_void_p).value
                
                # Read first bytes
                first_bytes = ctypes.create_string_buffer(5)
                self.kernel32.ReadProcessMemory(
                    self.kernel32.GetCurrentProcess(),
                    ctypes.c_void_p(func_addr),
                    first_bytes,
                    5,
                    None
                )
                
                # Check for common hook patterns
                if first_bytes.raw[0] == 0xE9:  # JMP
                    return True
                if first_bytes.raw[0:2] == b"\xFF\x25":  # JMP [addr]
                    return True
                
            except:
                pass
        
        return False
    
    def detect_timing_attacks(self) -> bool:
        """Detect timing-based analysis"""
        # Measure execution time inconsistencies
        start = time.perf_counter()
        
        # Perform dummy operations
        result = 0
        for i in range(1000000):
            result += i * 2
            result %= 1000007
        
        elapsed = time.perf_counter() - start
        
        # Check if execution is too slow (being analyzed)
        if elapsed > 0.5:  # Should be much faster
            return True
        
        # RDTSC timing check
        if hasattr(self, '_rdtsc_check'):
            t1 = self._rdtsc_check()
            time.sleep(0.001)
            t2 = self._rdtsc_check()
            
            # Check for abnormal timing
            if t2 - t1 > 10000000:  # Arbitrary threshold
                return True
        
        return False
    
    def apply_anti_debugging(self):
        """Apply anti-debugging techniques"""
        # Disable debug privileges
        try:
            token = win32security.OpenProcessToken(
                win32api.GetCurrentProcess(),
                win32con.TOKEN_ADJUST_PRIVILEGES | win32con.TOKEN_QUERY
            )
            
            debug_privilege = win32security.LookupPrivilegeValue(
                None,
                win32security.SE_DEBUG_NAME
            )
            
            win32security.AdjustTokenPrivileges(
                token,
                False,
                [(debug_privilege, 0)]
            )
        except:
            pass
        
        # Set thread hide from debugger
        try:
            thread_handle = self.kernel32.GetCurrentThread()
            self.ntdll.NtSetInformationThread(
                thread_handle,
                17,  # ThreadHideFromDebugger
                None,
                0
            )
        except:
            pass
    
    def obfuscate_memory(self):
        """Obfuscate memory patterns"""
        # Allocate decoy regions
        for _ in range(5):
            size = random.randint(1024, 4096)
            self.kernel32.VirtualAlloc(
                None,
                size,
                win32con.MEM_COMMIT | win32con.MEM_RESERVE,
                win32con.PAGE_READWRITE
            )
        
        # Create fake patterns
        patterns = [
            b"\x90" * 100,  # NOP sled
            b"\xCC" * 50,   # INT3 breakpoints
            b"\x00" * 200,  # Zeros
            os.urandom(256) # Random data
        ]
        
        for pattern in patterns:
            addr = self.kernel32.VirtualAlloc(
                None,
                len(pattern),
                win32con.MEM_COMMIT,
                win32con.PAGE_EXECUTE_READWRITE
            )
            if addr:
                ctypes.memmove(addr, pattern, len(pattern))