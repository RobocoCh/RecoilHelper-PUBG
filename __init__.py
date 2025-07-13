"""
Advanced Recoil Helper Package v2.0
With Full Protection Integration

"""

__version__ = "2.0.0"
__author__ = "HikiNaoru"
__user__ = "RobocoCh"
__date__ = "2025-07-13 16:26:38 UTC"

# Import all core modules
from .advanced_recoil_helper_v2 import (
    AdvancedRecoilHelperV2,
    ProtectedMouseDriver,
    WeaponProfile,
    create_protected_helper
)

# Import protection modules
from .advanced_protection_v2 import (
    HWIDSpoofer,
    BattleEyeBypass,
    SteamProtection,
    KernelProtection,
    AdvancedProtectionSystem,
    initialize_protection,
    get_protection_status,
    cleanup_protection
)

# Import utility modules
from .driver_interface import DriverInterface, KernelCallbacks
from .memory_utils import MemoryProtection, CodeInjection
from .pattern_analyzer import PatternAnalyzer, AdaptiveCompensation
from .anti_detection import AntiDetection
from .config_generator import ConfigGenerator
from .network_protection import NetworkProtection, P2PProtection

# Import integration modules
from .integrated_protection import IntegratedProtectionSystem
from .protection_installer import ProtectionInstaller
from .driver_generator import DriverGenerator, generate_protection_driver

# Import GUI if available
try:
    from .gui_interface import RecoilHelperGUI
except ImportError:
    RecoilHelperGUI = None

__all__ = [
    # Core
    'AdvancedRecoilHelperV2',
    'ProtectedMouseDriver',
    'WeaponProfile',
    'create_protected_helper',
    
    # Protection
    'HWIDSpoofer',
    'BattleEyeBypass',
    'SteamProtection',
    'KernelProtection',
    'AdvancedProtectionSystem',
    'initialize_protection',
    'get_protection_status',
    'cleanup_protection',
    
    # Utilities
    'DriverInterface',
    'KernelCallbacks',
    'MemoryProtection',
    'CodeInjection',
    'PatternAnalyzer',
    'AdaptiveCompensation',
    'AntiDetection',
    'ConfigGenerator',
    'NetworkProtection',
    'P2PProtection',
    
    # Integration
    'IntegratedProtectionSystem',
    'ProtectionInstaller',
    'DriverGenerator',
    'generate_protection_driver',
    
    # GUI
    'RecoilHelperGUI'
]

def check_system():
    """Check if system is ready for protected operation"""
    import ctypes
    import sys
    
    # Check admin
    if not ctypes.windll.shell32.IsUserAnAdmin():
        return False, "Administrator privileges required"
    
    # Check Python version
    if sys.version_info < (3, 8):
        return False, "Python 3.8 or higher required"
    
    # Check Windows version
    if sys.platform != 'win32':
        return False, "Windows only"
    
    return True, "System ready"

def init_protected_mode():
    """Initialize protected mode operation"""
    ready, message = check_system()
    if not ready:
        print(f"[!] {message}")
        return None
    
    # Initialize protection
    if not initialize_protection():
        print("[!] Failed to initialize protection")
        return None
    
    # Create protected helper
    helper = create_protected_helper()
    return helper