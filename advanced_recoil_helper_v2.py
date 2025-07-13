"""
Enhanced Advanced Recoil Helper v2.0 with Full Protection Integration
User: RobocoCh
Date: 2025-07-13 16:26:38 UTC
"""

import os
import sys
import time
import threading
import ctypes
import random
import hashlib
import subprocess
import winreg
import keyboard
import mouse
import numpy as np
from dataclasses import dataclass
from typing import Dict, Tuple, Optional, List
import json
import struct
import socket
import win32api
import win32con
import win32process
import win32security
import psutil
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import requests

# Import protection modules
from advanced_protection_v2 import (
    HWIDSpoofer, BattleEyeBypass, SteamProtection,
    initialize_protection, get_protection_status, cleanup_protection
)
from driver_interface import DriverInterface, KernelCallbacks
from memory_utils import MemoryProtection, CodeInjection
from pattern_analyzer import PatternAnalyzer, AdaptiveCompensation
from anti_detection import AntiDetection
from config_generator import ConfigGenerator
from network_protection import NetworkProtection, P2PProtection

@dataclass
class WeaponProfile:
    """Enhanced weapon profile with protection awareness"""
    name: str
    base_vertical: float
    base_horizontal: float
    fire_rate: float
    pattern_complexity: float
    spray_pattern: list
    attachment_modifiers: dict
    protection_factor: float = 1.0  # Additional protection multiplier

class ProtectedMouseDriver:
    """Protected mouse driver with anti-detection"""
    
    def __init__(self):
        self.driver_handle = None
        self.protection_active = False
        self.movement_queue = []
        self.last_movement_time = 0
        self._init_protected_driver()
        
    def _init_protected_driver(self):
        """Initialize driver with protection"""
        # Check protection status
        protection_status = get_protection_status()
        if protection_status and protection_status['active']:
            self.protection_active = True
            
            # Use kernel driver if available
            if protection_status['kernel']['driver_loaded']:
                self.driver_handle = ctypes.c_void_p(random.randint(10000, 99999))
        
        return self.protection_active
    
    def move_mouse_protected(self, dx: int, dy: int):
        """Move mouse with protection and anti-pattern detection"""
        if not self.protection_active:
            # Fallback to standard movement
            self._standard_mouse_move(dx, dy)
            return
        
        # Add to movement queue for pattern obfuscation
        current_time = time.time()
        self.movement_queue.append({
            'dx': dx,
            'dy': dy,
            'time': current_time
        })
        
        # Clean old movements
        self.movement_queue = [
            m for m in self.movement_queue 
            if current_time - m['time'] < 1.0
        ]
        
        # Check for pattern detection
        if self._is_pattern_suspicious():
            # Add random noise
            dx += random.randint(-2, 2)
            dy += random.randint(-2, 2)
            
            # Add random delay
            time.sleep(random.uniform(0.0001, 0.0005))
        
        # Apply movement with protection
        if self.driver_handle:
            # Use driver-level movement
            self._driver_mouse_move(dx, dy)
        else:
            # Use protected API calls
            self._protected_api_move(dx, dy)
        
        self.last_movement_time = current_time
    
    def _is_pattern_suspicious(self) -> bool:
        """Check if movement pattern might trigger detection"""
        if len(self.movement_queue) < 10:
            return False
        
        # Check for too consistent timing
        times = [m['time'] for m in self.movement_queue[-10:]]
        time_diffs = [times[i+1] - times[i] for i in range(len(times)-1)]
        avg_diff = sum(time_diffs) / len(time_diffs)
        variance = sum((d - avg_diff)**2 for d in time_diffs) / len(time_diffs)
        
        # Too consistent = suspicious
        if variance < 0.0001:
            return True
        
        # Check for too consistent movement values
        movements = [(m['dx'], m['dy']) for m in self.movement_queue[-10:]]
        unique_movements = len(set(movements))
        
        # Too few unique movements = suspicious
        if unique_movements < 3:
            return True
        
        return False
    
    def _driver_mouse_move(self, dx: int, dy: int):
        """Move mouse using kernel driver"""
        # Send IOCTL to driver
        IOCTL_MOUSE_MOVE = 0x222000
        input_buffer = struct.pack("ii", dx, dy)
        
        # Simulate driver communication
        # In real implementation, would use DeviceIoControl
        pass
    
    def _protected_api_move(self, dx: int, dy: int):
        """Move mouse using protected API calls"""
        # Use multiple methods randomly
        method = random.choice(['sendinput', 'mouse_event', 'setcursorpos'])
        
        if method == 'sendinput':
            # SendInput method
            extra = ctypes.c_ulong(0)
            ii_ = win32api.INPUT_union()
            ii_.mi = win32api.MOUSEINPUT(dx, dy, 0, win32con.MOUSEEVENTF_MOVE, 0, ctypes.pointer(extra))
            command = win32api.INPUT(win32con.INPUT_MOUSE, ii_)
            win32api.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))
            
        elif method == 'mouse_event':
            # mouse_event method
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dx, dy, 0, 0)
            
        else:
            # SetCursorPos method (absolute positioning)
            current_x, current_y = win32api.GetCursorPos()
            win32api.SetCursorPos((current_x + dx, current_y + dy))
    
    def _standard_mouse_move(self, dx: int, dy: int):
        """Fallback standard mouse movement"""
        human_factor = np.random.normal(1.0, 0.05)
        dx = int(dx * human_factor)
        dy = int(dy * human_factor)
        
        extra = ctypes.c_ulong(0)
        ii_ = win32api.INPUT_union()
        ii_.mi = win32api.MOUSEINPUT(dx, dy, 0, win32con.MOUSEEVENTF_MOVE, 0, ctypes.pointer(extra))
        command = win32api.INPUT(win32con.INPUT_MOUSE, ii_)
        win32api.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))

class AdvancedRecoilHelperV2:
    """Enhanced recoil helper with full protection integration"""
    
    def __init__(self):
        # Protection layer
        self.protection_initialized = False
        self.protection_status = {}
        
        # Initialize protection first
        self._init_protection()
        
        # Mouse driver with protection
        self.mouse_driver = ProtectedMouseDriver()
        
        # Core functionality
        self.is_active = False
        self.is_firing = False
        self.current_weapon = "M416"
        self.current_scope = 1.0
        self.is_crouching = False
        self.is_prone = False
        
        # User settings
        self.user_settings = {
            "general_sens": 39,
            "vertical_multiplier": 1.2,
            "aim_sens": 30,
            "ads_sens": 26,
            "scope_2x": 27,
            "scope_3x": 29,
            "scope_4x": 29
        }
        
        # Advanced features
        self.smooth_factor = 0.75
        self.assist_strength = 0.65
        self.humanization_factor = 0.15
        
        # Pattern analysis
        self.pattern_analyzer = PatternAnalyzer()
        self.adaptive_comp = AdaptiveCompensation(self.pattern_analyzer)
        
        # Movement tracking
        self.movement_buffer = []
        self.prediction_samples = 10
        
        # Network protection
        self.network_protection = NetworkProtection()
        self.p2p_protection = P2PProtection()
        
        # Memory protection
        self.memory_protection = MemoryProtection()
        
        # Anti-detection
        self.anti_detection = AntiDetection()
        
        # Load weapon profiles
        self.weapon_profiles = self._load_protected_profiles()
        
        # Protection monitoring
        self.protection_monitor_thread = None
        self.start_protection_monitor()
    
    def _init_protection(self):
        """Initialize all protection systems"""
        print("[*] Initializing protection systems...")
        
        # Initialize protection
        self.protection_initialized = initialize_protection()
        if self.protection_initialized:
            self.protection_status = get_protection_status()
            print("[+] Protection systems initialized")
        else:
            print("[!] Protection initialization failed - running in limited mode")
        
        # Apply memory protection to self
        if self.protection_initialized:
            self._protect_self_memory()
    
    def _protect_self_memory(self):
        """Apply memory protection to helper process"""
        try:
            # Get current process
            current_process = psutil.Process()
            
            # Hide from process list
            if self.protection_status.get('kernel', {}).get('driver_loaded'):
                # Use kernel driver to hide
                pass
            
            # Protect memory regions
            mem_protect = MemoryProtection()
            
            # Allocate hidden memory for sensitive data
            sensitive_data_size = 0x10000  # 64KB
            hidden_memory = mem_protect.allocate_hidden_memory(sensitive_data_size)
            
            if hidden_memory:
                # Store sensitive data in hidden memory
                self.hidden_memory_base = hidden_memory
                
                # Encrypt and store weapon profiles
                encrypted_profiles = self._encrypt_profiles()
                mem_protect.encrypt_memory_region(
                    hidden_memory,
                    len(encrypted_profiles),
                    get_random_bytes(32)
                )
        except Exception as e:
            print(f"[!] Memory protection error: {e}")
    
    def _encrypt_profiles(self) -> bytes:
        """Encrypt weapon profiles"""
        profiles_json = json.dumps({
            name: {
                'vertical': p.base_vertical,
                'horizontal': p.base_horizontal,
                'rate': p.fire_rate,
                'pattern': p.spray_pattern
            }
            for name, p in self.weapon_profiles.items()
        })
        
        # Encrypt with AES
        key = get_random_bytes(32)
        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(profiles_json.encode())
        
        return cipher.nonce + tag + ciphertext
    
    def _load_protected_profiles(self) -> Dict[str, WeaponProfile]:
        """Load weapon profiles with protection awareness"""
        profiles = {}
        
        # M416 with enhanced pattern
        m416_pattern = [
            (0, 4.2), (0.5, 4.3), (0.3, 4.5), (-0.2, 4.6), (-0.4, 4.8),
            (0.2, 5.0), (0.6, 5.1), (0.4, 5.2), (-0.3, 5.3), (-0.5, 5.4),
            (0.1, 5.5), (0.7, 5.6), (0.3, 5.7), (-0.4, 5.8), (-0.6, 5.9)
        ]
        profiles["M416"] = WeaponProfile(
            "M416", 4.5, 1.2, 750, 0.3, m416_pattern,
            {"compensator": 0.8, "vertical_grip": 0.85, "half_grip": 0.9},
            protection_factor=1.0
        )
        
        # AKM with complex pattern
        akm_pattern = [
            (0, 5.8), (1.0, 6.0), (0.8, 6.2), (-0.5, 6.4), (-1.2, 6.6),
            (0.6, 6.8), (1.5, 7.0), (0.9, 7.1), (-0.8, 7.2), (-1.4, 7.3),
            (0.4, 7.4), (1.3, 7.5), (0.7, 7.6), (-0.9, 7.7), (-1.5, 7.8)
        ]
        profiles["AKM"] = WeaponProfile(
            "AKM", 6.2, 1.8, 600, 0.6, akm_pattern,
            {"compensator": 0.75, "vertical_grip": 0.8},
            protection_factor=0.95
        )
        
        # SCAR-L with stable pattern
        scar_pattern = [
            (0, 3.6), (0.3, 3.7), (0.2, 3.8), (-0.1, 3.9), (-0.3, 4.0),
            (0.1, 4.1), (0.4, 4.2), (0.2, 4.3), (-0.2, 4.4), (-0.4, 4.5),
            (0, 4.6), (0.3, 4.7), (0.1, 4.8), (-0.2, 4.9), (-0.3, 5.0)
        ]
        profiles["SCAR-L"] = WeaponProfile(
            "SCAR-L", 3.8, 1.0, 650, 0.2, scar_pattern,
            {"compensator": 0.85, "vertical_grip": 0.88, "half_grip": 0.92},
            protection_factor=1.05
        )
        
        # Beryl with high recoil
        beryl_pattern = [
            (0, 7.2), (1.8, 7.5), (1.5, 7.8), (-0.8, 8.0), (-2.0, 8.2),
            (1.0, 8.4), (2.2, 8.6), (1.6, 8.8), (-1.2, 9.0), (-2.3, 9.2),
            (0.8, 9.3), (2.0, 9.4), (1.4, 9.5), (-1.4, 9.6), (-2.4, 9.7)
        ]
        profiles["Beryl"] = WeaponProfile(
            "Beryl", 7.5, 2.2, 700, 0.8, beryl_pattern,
            {"compensator": 0.7, "vertical_grip": 0.75, "half_grip": 0.8},
            protection_factor=0.9
        )
        
        # M762 pattern
        m762_pattern = [
            (0, 6.5), (1.4, 6.8), (1.1, 7.0), (-0.6, 7.2), (-1.6, 7.4),
            (0.7, 7.6), (1.8, 7.8), (1.2, 8.0), (-1.0, 8.1), (-1.9, 8.2),
            (0.5, 8.3), (1.6, 8.4), (1.0, 8.5), (-1.1, 8.6), (-2.0, 8.7)
        ]
        profiles["M762"] = WeaponProfile(
            "M762", 6.8, 2.0, 680, 0.7, m762_pattern,
            {"compensator": 0.72, "vertical_grip": 0.77},
            protection_factor=0.92
        )
        
        # QBZ pattern
        qbz_pattern = [
            (0, 4.0), (0.4, 4.1), (0.3, 4.2), (-0.2, 4.3), (-0.4, 4.4),
            (0.2, 4.5), (0.5, 4.6), (0.3, 4.7), (-0.3, 4.8), (-0.5, 4.9),
            (0.1, 5.0), (0.4, 5.1), (0.2, 5.2), (-0.3, 5.3), (-0.4, 5.4)
        ]
        profiles["QBZ"] = WeaponProfile(
            "QBZ", 4.2, 1.1, 650, 0.3, qbz_pattern,
            {"compensator": 0.82, "vertical_grip": 0.86},
            protection_factor=1.02
        )
        
        return profiles
    
    def start_protection_monitor(self):
        """Start continuous protection monitoring"""
        def monitor_loop():
            check_interval = 15  # seconds
            detection_count = 0
            
            while self.protection_initialized:
                try:
                    # Check protection status
                    current_status = get_protection_status()
                    
                    # Check for debuggers
                    if self.anti_detection.detect_debugger():
                        detection_count += 1
                        print(f"[!] Debugger detected ({detection_count}x)")
                        
                        if detection_count > 3:
                            print("[!] Multiple detections - terminating for safety")
                            self.emergency_shutdown()
                            break
                        
                        # Apply countermeasures
                        self.anti_detection.apply_anti_debugging()
                    
                    # Check for analysis tools
                    if self.anti_detection.detect_analysis_tools():
                        print("[!] Analysis tools detected")
                        # Temporarily disable functionality
                        self.is_active = False
                        time.sleep(5)
                    
                    # Check BattleEye status
                    if self._check_battleye_running():
                        print("[!] BattleEye detected - applying enhanced protection")
                        # Re-apply bypasses
                        if hasattr(self, 'battleye_bypass'):
                            self.battleye_bypass.apply_all_bypasses()
                    
                    # Verify HWID spoofing
                    if current_status.get('hwid', {}).get('spoofed'):
                        # Refresh spoofing
                        pass
                    
                    # Network heartbeat
                    if self.network_protection.is_connected:
                        telemetry = {
                            'status': 'active',
                            'detections': detection_count,
                            'uptime': time.time()
                        }
                        self.network_protection.send_telemetry(telemetry)
                    
                except Exception as e:
                    print(f"[!] Monitor error: {e}")
                
                time.sleep(check_interval)
        
        self.protection_monitor_thread = threading.Thread(
            target=monitor_loop,
            daemon=True
        )
        self.protection_monitor_thread.start()
    
    def _check_battleye_running(self) -> bool:
        """Check if BattleEye is running"""
        be_processes = ['BEService.exe', 'BEDaisy.sys']
        
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] in be_processes:
                    return True
            except:
                pass
        
        return False
    
    def calculate_protected_compensation(self, shot_count: int) -> Tuple[float, float]:
        """Calculate compensation with protection awareness"""
        weapon = self.weapon_profiles.get(self.current_weapon)
        if not weapon:
            return 0.0, 0.0
        
        # Check protection status
        if not self.protection_initialized:
            # Reduce effectiveness without protection
            protection_penalty = 0.5
        else:
            protection_penalty = 1.0
        
        # Get base pattern
        pattern_index = min(shot_count, len(weapon.spray_pattern) - 1)
        base_h, base_v = weapon.spray_pattern[pattern_index]
        
        # Apply sensitivity and protection
        sens_scale = self.user_settings["ads_sens"] / 50.0
        vertical = base_v * sens_scale * self.user_settings["vertical_multiplier"]
        horizontal = base_h * sens_scale
        
        # Apply protection factor
        vertical *= weapon.protection_factor * protection_penalty
        horizontal *= weapon.protection_factor * protection_penalty
        
        # Scope compensation
        scope_mult = self._calculate_scope_multiplier()
        vertical *= scope_mult
        horizontal *= scope_mult
        
        # Stance modifiers
        stance_mult = self._get_stance_multiplier()
        vertical *= stance_mult[1]
        horizontal *= stance_mult[0]
        
        # Humanization with protection
        if self.protection_initialized:
            vertical, horizontal = self._protected_humanize(vertical, horizontal)
        else:
            vertical, horizontal = self._basic_humanize(vertical, horizontal)
        
        # Adaptive compensation
        if self.adaptive_comp:
            vertical, horizontal = self.adaptive_comp.get_adapted_compensation(
                self.current_weapon, (horizontal, vertical)
            )
        
        # Pattern prediction
        if len(self.movement_buffer) >= self.prediction_samples:
            predicted = self._predict_next_movement()
            vertical = vertical * 0.7 + predicted[1] * 0.3
            horizontal = horizontal * 0.7 + predicted[0] * 0.3
        
        # Apply final modifiers
        vertical *= self.assist_strength
        horizontal *= self.assist_strength
        
        # Store in buffer
        self.movement_buffer.append((horizontal, vertical))
        if len(self.movement_buffer) > self.prediction_samples * 2:
            self.movement_buffer.pop(0)
        
        # Record pattern for learning
        if self.pattern_analyzer and shot_count % 5 == 0:
            self.pattern_analyzer.record_pattern(
                self.current_weapon,
                self.movement_buffer[-10:] if len(self.movement_buffer) >= 10 else self.movement_buffer
            )
        
        return horizontal, vertical
    
    def _protected_humanize(self, x: float, y: float) -> Tuple[float, float]:
        """Advanced humanization with protection"""
        # Multi-layer randomization
        
        # Base micro movements
        micro_x = np.random.normal(0, self.humanization_factor)
        micro_y = np.random.normal(0, self.humanization_factor)
        
        # Sine wave with variable frequency
        time_factor = time.time() * (8 + random.uniform(-2, 2))
        sine_x = np.sin(time_factor) * 0.1
        sine_y = np.cos(time_factor * 1.3) * 0.1
        
        # Perlin-like noise
        noise_x = self._perlin_noise(time.time(), 0.1) * 0.2
        noise_y = self._perlin_noise(time.time() + 1000, 0.1) * 0.2
        
        # Breathing simulation
        breath_cycle = np.sin(time.time() * 0.3) * 0.05
        
        # Combine all factors
        final_x = x + micro_x + sine_x + noise_x
        final_y = y + micro_y + sine_y + noise_y + breath_cycle
        
        return (final_x, final_y)
    
    def _basic_humanize(self, x: float, y: float) -> Tuple[float, float]:
        """Basic humanization without protection"""
        micro_x = np.random.normal(0, self.humanization_factor * 0.5)
        micro_y = np.random.normal(0, self.humanization_factor * 0.5)
        
        return (x + micro_x, y + micro_y)
    
    def _perlin_noise(self, x: float, scale: float) -> float:
        """Simple Perlin noise implementation"""
        x = x * scale
        x0 = int(np.floor(x))
        x1 = x0 + 1
        
        t = x - x0
        t = t * t * (3 - 2 * t)  # Smoothstep
        
        # Random gradients
        g0 = (x0 * 12345) % 100 / 100.0 - 0.5
        g1 = (x1 * 12345) % 100 / 100.0 - 0.5
        
        return g0 * (1 - t) + g1 * t
    
    def _calculate_scope_multiplier(self) -> float:
        """Calculate scope-specific multiplier"""
        scope_mults = {
            1.0: 1.0,
            2.0: self.user_settings["scope_2x"] / self.user_settings["ads_sens"],
            3.0: self.user_settings["scope_3x"] / self.user_settings["ads_sens"],
            4.0: self.user_settings["scope_4x"] / self.user_settings["ads_sens"],
            6.0: 1.5
        }
        return scope_mults.get(self.current_scope, 1.0)
    
    def _get_stance_multiplier(self) -> Tuple[float, float]:
        """Get stance-based multipliers"""
        if self.is_prone:
            return (0.4, 0.5)
        elif self.is_crouching:
            return (0.6, 0.7)
        return (1.0, 1.0)
    
    def _predict_next_movement(self) -> Tuple[float, float]:
        """Predict next movement with ML"""
        if self.pattern_analyzer:
            predictions = self.pattern_analyzer.predict_next_shots(
                self.current_weapon,
                self.movement_buffer[-5:],
                1
            )
            if predictions:
                return predictions[0]
        
        # Fallback to simple prediction
        if len(self.movement_buffer) < self.prediction_samples:
            return (0, 0)
        
        recent = self.movement_buffer[-self.prediction_samples:]
        avg_x = sum(m[0] for m in recent) / len(recent)
        avg_y = sum(m[1] for m in recent) / len(recent)
        
        return (avg_x, avg_y)
    
    def apply_compensation_loop(self):
        """Main compensation loop with protection"""
        shot_count = 0
        last_fire_time = 0
        protection_check_time = time.time()
        performance_monitor = {'shots': 0, 'time': time.time()}
        
        while self.is_active:
            try:
                # Periodic protection check
                if time.time() - protection_check_time > 20:
                    if not self._verify_protection():
                        print("[!] Protection compromised - pausing")
                        self.is_active = False
                        break
                    protection_check_time = time.time()
                
                # Main compensation logic
                if self.is_firing and mouse.is_pressed("left"):
                    current_time = time.time()
                    
                    # Reset shot count if stopped firing
                    if current_time - last_fire_time > 0.5:
                        shot_count = 0
                        self.movement_buffer.clear()
                    
                    # Calculate protected compensation
                    dx, dy = self.calculate_protected_compensation(shot_count)
                    
                    # Apply movement with protection
                    if abs(dx) > 0.1 or abs(dy) > 0.1:
                        self.mouse_driver.move_mouse_protected(int(dx), int(dy))
                    
                    # Performance tracking
                    performance_monitor['shots'] += 1
                    if current_time - performance_monitor['time'] > 10:
                        shots_per_sec = performance_monitor['shots'] / 10
                        if shots_per_sec > 15:  # Suspicious rate
                            # Add extra delay
                            time.sleep(0.002)
                        performance_monitor = {'shots': 0, 'time': current_time}
                    
                    # Dynamic delay based on weapon
                    weapon = self.weapon_profiles.get(self.current_weapon)
                    if weapon:
                        base_delay = 60.0 / weapon.fire_rate
                        # Randomize delay with protection
                        if self.protection_initialized:
                            delay = base_delay * np.random.uniform(0.92, 1.08)
                        else:
                            delay = base_delay * np.random.uniform(0.95, 1.05)
                    else:
                        delay = 0.1
                    
                    shot_count += 1
                    last_fire_time = current_time
                    time.sleep(delay)
                    
                else:
                    # Not firing
                    shot_count = 0
                    time.sleep(0.001)
                    
            except Exception as e:
                print(f"[!] Compensation error: {e}")
                time.sleep(0.01)
    
    def _verify_protection(self) -> bool:
        """Verify protection is still active"""
        if not self.protection_initialized:
            return False
        
        status = get_protection_status()
        if not status.get('active'):
            return False
        
        # Additional checks
        if self.anti_detection.detect_debugger():
            return False
        
        return True
    
    def emergency_shutdown(self):
        """Emergency shutdown procedure"""
        print("[!] EMERGENCY SHUTDOWN INITIATED")
        
        # Stop all activity
        self.is_active = False
        self.is_firing = False
        
        # Clear sensitive data
        self.movement_buffer.clear()
        self.weapon_profiles.clear()
        
        # Cleanup protection
        cleanup_protection()
        
        # Exit
        sys.exit(1)
    
    def toggle_script(self):
        """Toggle with protection verification"""
        if not self.protection_initialized:
            print("[!] Protection not active - initializing...")
            self._init_protection()
            if not self.protection_initialized:
                print("[!] Cannot start without protection")
                return
        
        self.is_active = not self.is_active
        status = "ENABLED" if self.is_active else "DISABLED"
        print(f"\n[{time.strftime('%H:%M:%S')}] Protected Recoil Helper {status}")
        
        if self.is_active:
            # Start compensation thread
            comp_thread = threading.Thread(
                target=self.apply_compensation_loop,
                daemon=True
            )
            comp_thread.start()
            
            # Log activation
            if self.network_protection.is_connected:
                self.network_protection.send_telemetry({
                    'event': 'activation',
                    'weapon': self.current_weapon,
                    'protection': self.protection_status
                })
    
    def set_weapon(self, weapon_name: str):
        """Set weapon with protection check"""
        if weapon_name in self.weapon_profiles:
            self.current_weapon = weapon_name
            print(f"[{time.strftime('%H:%M:%S')}] Weapon: {weapon_name}")
            
            # Clear movement buffer for new weapon
            self.movement_buffer.clear()
            
            # Reset adaptive compensation
            if self.adaptive_comp:
                self.adaptive_comp.current_compensation.pop(weapon_name, None)
    
    def set_scope(self, scope: float):
        """Set scope with validation"""
        valid_scopes = [1.0, 2.0, 3.0, 4.0, 6.0]
        if scope in valid_scopes:
            self.current_scope = scope
            print(f"[{time.strftime('%H:%M:%S')}] Scope: {scope}x")
    
    def setup_protected_hotkeys(self):
        """Setup hotkeys with protection"""
        # Main toggle
        keyboard.on_press_key("insert", lambda _: self.toggle_script())
        
        # Weapon selection
        weapon_keys = {
            "f1": "M416", "f2": "AKM", "f3": "SCAR-L",
            "f4": "Beryl", "f5": "M762", "f6": "QBZ"
        }
        
        for key, weapon in weapon_keys.items():
            keyboard.on_press_key(key, lambda _, w=weapon: self.set_weapon(w))
        
        # Scope selection
        for i in range(1, 5):
            keyboard.on_press_key(str(i), lambda _, s=float(i): self.set_scope(s))
        
        # Stance detection
        keyboard.on_press_key("c", lambda _: setattr(self, 'is_crouching', True))
        keyboard.on_release_key("c", lambda _: setattr(self, 'is_crouching', False))
        keyboard.on_press_key("z", lambda _: setattr(self, 'is_prone', True))
        keyboard.on_release_key("z", lambda _: setattr(self, 'is_prone', False))
        
        # Protected mouse hooks
        self._setup_protected_mouse_hooks()
    
    def _setup_protected_mouse_hooks(self):
        """Setup mouse hooks with anti-detection"""
        # Use multiple detection methods
        detection_methods = []
        
        # Method 1: Direct mouse state
        def check_mouse_direct():
            return mouse.is_pressed("left")
        
        # Method 2: Win32 API
        def check_mouse_win32():
            return win32api.GetAsyncKeyState(win32con.VK_LBUTTON) & 0x8000
        
        # Method 3: GetKeyState
        def check_mouse_keystate():
            return win32api.GetKeyState(win32con.VK_LBUTTON) < 0
        
        detection_methods = [check_mouse_direct, check_mouse_win32, check_mouse_keystate]
        
        # Polling thread with method rotation
        def poll_mouse():
            method_index = 0
            last_state = False
            
            while True:
                try:
                    # Rotate detection methods
                    current_method = detection_methods[method_index]
                    current_state = current_method()
                    
                    if current_state != last_state:
                        self.is_firing = current_state
                        last_state = current_state
                    
                    # Rotate method
                    method_index = (method_index + 1) % len(detection_methods)
                    
                    # Variable delay
                    time.sleep(random.uniform(0.0008, 0.0012))
                    
                except Exception:
                    time.sleep(0.001)
        
        mouse_thread = threading.Thread(target=poll_mouse, daemon=True)
        mouse_thread.start()
    
    def display_protected_menu(self):
        """Display menu with protection status"""
        protection_symbol = "🛡️" if self.protection_initialized else "⚠️"
        
        print(f"\n{'='*70}")
        print(f"   {protection_symbol} Advanced PUBG Recoil Helper v2.0 - Protected Edition")
        print(f"{'='*70}")
        print(f"User: {os.getlogin()} | Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Protection Status: {'ACTIVE' if self.protection_initialized else 'LIMITED'}")
        
        if self.protection_status:
            print(f"├─ HWID Spoofing: {'✓' if self.protection_status.get('hwid', {}).get('spoofed') else '✗'}")
            print(f"├─ BattleEye Bypass: {'✓' if self.protection_status.get('battleye', {}).get('hooks_installed') else '✗'}")
            print(f"├─ Steam Protection: {'✓' if self.protection_status.get('steam', {}).get('steam_id') else '✗'}")
            print(f"└─ Kernel Driver: {'✓' if self.protection_status.get('kernel', {}).get('driver_loaded') else '✗'}")
        
        print(f"\n{'─'*70}")
        print("Controls:")
        print("  [Insert]     - Toggle ON/OFF")
        print("  [F1-F6]      - Weapon Selection")
        print("  [1-4]        - Scope Selection")
        print("  [C/Z]        - Crouch/Prone (hold)")
        print(f"\n{'─'*70}")
        print("Settings:")
        print(f"  Smooth Factor: {self.smooth_factor}")
        print(f"  Assist Strength: {self.assist_strength}")
        print(f"  Humanization: {self.humanization_factor}")
        print(f"  Current Weapon: {self.current_weapon}")
        print(f"  Current Scope: {self.current_scope}x")
        print(f"\n{'─'*70}")
        print("[!] Educational purposes only - Do not use in online games")
        print(f"{'='*70}\n")
    
    def run(self):
        """Main run method with full protection"""
        try:
            # Display menu
            self.display_protected_menu()
            
            # Setup hotkeys
            self.setup_protected_hotkeys()
            
            # Connect to protection network
            self.network_protection.establish_secure_connection()
            
            print("Press [Insert] to start...")
            print("Press [Ctrl+C] to exit\n")
            
            # Main loop
            keyboard.wait()
            
        except KeyboardInterrupt:
            print("\n\nShutting down...")
        except Exception as e:
            print(f"\n[!] Fatal error: {e}")
            self.emergency_shutdown()
        finally:
            # Cleanup
            self.is_active = False
            cleanup_protection()
            if self.network_protection.is_connected:
                self.network_protection.close_connection()
            print("Cleanup complete.")

# Create global instance
def create_protected_helper():
    """Create helper instance with protection"""
    return AdvancedRecoilHelperV2()

if __name__ == "__main__":
    # Check admin
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("[!] Administrator privileges required!")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
    else:
        helper = create_protected_helper()
        helper.run()