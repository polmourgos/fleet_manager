"""
Configuration settings for Fleet Management System
"""
import os
from tkinter import font

# Database configuration
DB_PATH = "fleet.db"
IMAGES_DIR = "images"
TANK_MIN_LEVEL = 500
TANK_CAPACITY = 10000  # Συνολική χωρητικότητα δεξαμενής σε λίτρα
DEFAULT_PASSWORD = "1"
SETTINGS_FILE = "user_settings.json"  # Αρχείο για αποθήκευση ρυθμίσεων χρήστη

import json

def save_user_setting(key, value):
    """Save user setting to file"""
    try:
        # Load existing settings
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
        except FileNotFoundError:
            settings = {}
        
        # Update setting
        settings[key] = value
        
        # Save back to file
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"Error saving setting {key}: {e}")
        return False

def load_user_setting(key, default_value=None):
    """Load user setting from file"""
    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        return settings.get(key, default_value)
    except FileNotFoundError:
        return default_value
    except Exception as e:
        print(f"Error loading setting {key}: {e}")
        return default_value

# Font configuration - using system fonts for better compatibility
def get_system_fonts():
    """Get available system fonts"""
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        available_fonts = list(font.families())
        root.destroy()
        
        # Preferred fonts in order
        preferred_fonts = ["Segoe UI", "Arial", "Helvetica", "DejaVu Sans"]
        
        for font_name in preferred_fonts:
            if font_name in available_fonts:
                return font_name
        
        return "TkDefaultFont"
    except:
        return "TkDefaultFont"

SYSTEM_FONT = get_system_fonts()

def get_adaptive_font_sizes(screen_width=None, screen_height=None):
    """Get font sizes adapted to screen size"""
    if screen_width is None or screen_height is None:
        # Default sizes for unknown screen
        return {
            'FONT_BIG': (SYSTEM_FONT, 18, "bold"),
            'FONT_NORMAL': (SYSTEM_FONT, 12),
            'FONT_SMALL': (SYSTEM_FONT, 10),
            'FONT_TITLE': (SYSTEM_FONT, 16, "bold"),
            'FONT_SUBTITLE': (SYSTEM_FONT, 14, "bold")
        }
    
    # Calculate font sizes based on screen resolution
    if screen_width < 1366:  # Small laptop screens
        return {
            'FONT_BIG': (SYSTEM_FONT, 14, "bold"),
            'FONT_NORMAL': (SYSTEM_FONT, 10),
            'FONT_SMALL': (SYSTEM_FONT, 8),
            'FONT_TITLE': (SYSTEM_FONT, 12, "bold"),
            'FONT_SUBTITLE': (SYSTEM_FONT, 11, "bold")
        }
    elif screen_width < 1920:  # Standard laptop/desktop screens
        return {
            'FONT_BIG': (SYSTEM_FONT, 16, "bold"),
            'FONT_NORMAL': (SYSTEM_FONT, 11),
            'FONT_SMALL': (SYSTEM_FONT, 9),
            'FONT_TITLE': (SYSTEM_FONT, 14, "bold"),
            'FONT_SUBTITLE': (SYSTEM_FONT, 12, "bold")
        }
    else:  # Large desktop monitors
        return {
            'FONT_BIG': (SYSTEM_FONT, 18, "bold"),
            'FONT_NORMAL': (SYSTEM_FONT, 12),
            'FONT_SMALL': (SYSTEM_FONT, 10),
            'FONT_TITLE': (SYSTEM_FONT, 16, "bold"),
            'FONT_SUBTITLE': (SYSTEM_FONT, 14, "bold")
        }

# Default font sizes (will be updated dynamically)
FONT_BIG = (SYSTEM_FONT, 18, "bold")
FONT_NORMAL = (SYSTEM_FONT, 12)
FONT_SMALL = (SYSTEM_FONT, 10)
FONT_TITLE = (SYSTEM_FONT, 16, "bold")
FONT_SUBTITLE = (SYSTEM_FONT, 14, "bold")

# Modern Color themes with sophisticated palettes
THEMES = {
    "light": {
        "bg": "#f8fafc",
        "fg": "#1e293b",
        "select_bg": "#3b82f6",
        "select_fg": "#ffffff",
        "button_bg": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)",
        "button_bg_solid": "#3b82f6",
        "button_fg": "#ffffff",
        "button_hover": "#2563eb",
        "button_shadow": "rgba(59, 130, 246, 0.3)",
        "entry_bg": "#ffffff",
        "entry_border": "#e2e8f0",
        "entry_focus": "#3b82f6",
        "tree_bg": "#ffffff",
        "frame_bg": "#ffffff",
        "card_bg": "#ffffff",
        "card_shadow": "rgba(0, 0, 0, 0.1)",
        "accent": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "success": "#10b981",
        "info": "#3b82f6",
        "border": "#e2e8f0",
        "border_light": "#f1f5f9",
        "text_muted": "#64748b",
        "text_secondary": "#475569",
        "header_bg": "#ffffff",
        "header_shadow": "rgba(0, 0, 0, 0.05)"
    },
    "dark": {
        "bg": "#0f172a",
        "fg": "#f1f5f9",
        "select_bg": "#3b82f6",
        "select_fg": "#ffffff",
        "button_bg": "linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%)",
        "button_bg_solid": "#1e40af",
        "button_fg": "#ffffff",
        "button_hover": "#1d4ed8",
        "button_shadow": "rgba(30, 64, 175, 0.4)",
        "entry_bg": "#1e293b",
        "entry_border": "#334155",
        "entry_focus": "#3b82f6",
        "tree_bg": "#1e293b",
        "frame_bg": "#1e293b",
        "card_bg": "#1e293b",
        "card_shadow": "rgba(0, 0, 0, 0.3)",
        "accent": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "success": "#10b981",
        "info": "#3b82f6",
        "border": "#334155",
        "border_light": "#475569",
        "text_muted": "#94a3b8",
        "text_secondary": "#cbd5e1",
        "header_bg": "#1e293b",
        "header_shadow": "rgba(0, 0, 0, 0.2)"
    },
    "blue": {
        "bg": "#f0f9ff",
        "fg": "#0c4a6e",
        "select_bg": "#0ea5e9",
        "select_fg": "#ffffff",
        "button_bg": "linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%)",
        "button_bg_solid": "#0ea5e9",
        "button_fg": "#ffffff",
        "button_hover": "#0284c7",
        "button_shadow": "rgba(14, 165, 233, 0.3)",
        "entry_bg": "#ffffff",
        "entry_border": "#bae6fd",
        "entry_focus": "#0ea5e9",
        "tree_bg": "#ffffff",
        "frame_bg": "#ffffff",
        "card_bg": "#ffffff",
        "card_shadow": "rgba(14, 165, 233, 0.1)",
        "accent": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "success": "#10b981",
        "info": "#0ea5e9",
        "border": "#bae6fd",
        "border_light": "#e0f2fe",
        "text_muted": "#475569",
        "text_secondary": "#64748b",
        "header_bg": "#ffffff",
        "header_shadow": "rgba(14, 165, 233, 0.08)"
    },
    "green": {
        "bg": "#f0fdf4",
        "fg": "#14532d",
        "select_bg": "#22c55e",
        "select_fg": "#ffffff",
        "button_bg": "linear-gradient(135deg, #22c55e 0%, #16a34a 100%)",
        "button_bg_solid": "#22c55e",
        "button_fg": "#ffffff",
        "button_hover": "#16a34a",
        "button_shadow": "rgba(34, 197, 94, 0.3)",
        "entry_bg": "#ffffff",
        "entry_border": "#bbf7d0",
        "entry_focus": "#22c55e",
        "tree_bg": "#ffffff",
        "frame_bg": "#ffffff",
        "card_bg": "#ffffff",
        "card_shadow": "rgba(34, 197, 94, 0.1)",
        "accent": "#22c55e",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "success": "#22c55e",
        "info": "#3b82f6",
        "border": "#bbf7d0",
        "border_light": "#dcfce7",
        "text_muted": "#475569",
        "text_secondary": "#64748b",
        "header_bg": "#ffffff",
        "header_shadow": "rgba(34, 197, 94, 0.08)"
    },
    "purple": {
        "bg": "#faf5ff",
        "fg": "#581c87",
        "select_bg": "#a855f7",
        "select_fg": "#ffffff",
        "button_bg": "linear-gradient(135deg, #a855f7 0%, #9333ea 100%)",
        "button_bg_solid": "#a855f7",
        "button_fg": "#ffffff",
        "button_hover": "#9333ea",
        "button_shadow": "rgba(168, 85, 247, 0.3)",
        "entry_bg": "#ffffff",
        "entry_border": "#ddd6fe",
        "entry_focus": "#a855f7",
        "tree_bg": "#ffffff",
        "frame_bg": "#ffffff",
        "card_bg": "#ffffff",
        "card_shadow": "rgba(168, 85, 247, 0.1)",
        "accent": "#a855f7",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "success": "#10b981",
        "info": "#3b82f6",
        "border": "#ddd6fe",
        "border_light": "#ede9fe",
        "text_muted": "#475569",
        "text_secondary": "#64748b",
        "header_bg": "#ffffff",
        "header_shadow": "rgba(168, 85, 247, 0.08)"
    }
}

# Modern Button styles with enhanced visual effects
BUTTON_STYLES = {
    "primary": {
        "bg": "#3b82f6",
        "fg": "#ffffff",
        "activebackground": "#2563eb",
        "activeforeground": "#ffffff",
        "relief": "flat",
        "borderwidth": 0,
        "padx": 24,
        "pady": 12,
        "font": FONT_NORMAL,
        "cursor": "hand2",
        "compound": "left"
    },
    "success": {
        "bg": "#10b981",
        "fg": "#ffffff",
        "activebackground": "#059669",
        "activeforeground": "#ffffff",
        "relief": "flat",
        "borderwidth": 0,
        "padx": 24,
        "pady": 12,
        "font": FONT_NORMAL,
        "cursor": "hand2",
        "compound": "left"
    },
    "warning": {
        "bg": "#f59e0b",
        "fg": "#ffffff",
        "activebackground": "#d97706",
        "activeforeground": "#ffffff",
        "relief": "flat",
        "borderwidth": 0,
        "padx": 24,
        "pady": 12,
        "font": FONT_NORMAL,
        "cursor": "hand2",
        "compound": "left"
    },
    "danger": {
        "bg": "#ef4444",
        "fg": "#ffffff",
        "activebackground": "#dc2626",
        "activeforeground": "#ffffff",
        "relief": "flat",
        "borderwidth": 0,
        "padx": 24,
        "pady": 12,
        "font": FONT_NORMAL,
        "cursor": "hand2",
        "compound": "left"
    },
    "secondary": {
        "bg": "#64748b",
        "fg": "#ffffff",
        "activebackground": "#475569",
        "activeforeground": "#ffffff",
        "relief": "flat",
        "borderwidth": 0,
        "padx": 24,
        "pady": 12,
        "font": FONT_NORMAL,
        "cursor": "hand2",
        "compound": "left"
    },
    "info": {
        "bg": "#0ea5e9",
        "fg": "#ffffff",
        "activebackground": "#0284c7",
        "activeforeground": "#ffffff",
        "relief": "flat",
        "borderwidth": 0,
        "padx": 24,
        "pady": 12,
        "font": FONT_NORMAL,
        "cursor": "hand2",
        "compound": "left"
    },
    "outline": {
        "bg": "#ffffff",
        "fg": "#3b82f6",
        "activebackground": "#f8fafc",
        "activeforeground": "#2563eb",
        "relief": "flat",
        "borderwidth": 2,
        "highlightbackground": "#3b82f6",
        "highlightcolor": "#3b82f6",
        "highlightthickness": 2,
        "padx": 22,
        "pady": 10,
        "font": FONT_NORMAL,
        "cursor": "hand2",
        "compound": "left"
    }
}

# Logging configuration
LOGGING_CONFIG = {
    'filename': "fleet_manager.log",
    'level': "INFO",
    'format': "%(asctime)s %(levelname)s: %(message)s"
}