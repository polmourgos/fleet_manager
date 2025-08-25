"""
Simple Vehicles Tab Module for testing modular architecture
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging

from ui_components import ModernButton, ModernFrame
from config import THEMES, FONT_NORMAL, FONT_SUBTITLE
from utils import normalize_plate, log_user_action


class SimpleVehiclesTab:
    """Simple vehicles tab for testing modular structure"""
    
    def __init__(self, parent_app, tab_widget, db, tooltip_manager):
        """Initialize simple vehicles tab"""
        self.app = parent_app
        self.tab = tab_widget
        self.db = db
        self.tooltip_manager = tooltip_manager
        self.current_theme = parent_app.current_theme
        
        # Build the tab
        self._build_tab()
        
        logging.info("Simple Vehicles Tab initialized successfully")
    
    def _build_tab(self):
        """Build simple vehicles tab"""
        # Main frame
        main_frame = ModernFrame(self.tab, theme=self.current_theme)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🚗 Vehicles Module Test",
            font=FONT_SUBTITLE,
            fg=THEMES[self.current_theme]["accent"],
            bg=THEMES[self.current_theme]["frame_bg"]
        )
        title_label.pack(pady=20)
        
        # Status
        status_label = tk.Label(
            main_frame,
            text="✅ Vehicles Tab Module Loaded Successfully!",
            font=FONT_NORMAL,
            fg=THEMES[self.current_theme]["fg"],
            bg=THEMES[self.current_theme]["frame_bg"]
        )
        status_label.pack(pady=10)
        
        # Test info
        info_label = tk.Label(
            main_frame,
            text="This is a test of the modular architecture.\nThe vehicles tab is now a separate module!",
            font=FONT_NORMAL,
            fg=THEMES[self.current_theme]["fg"],
            bg=THEMES[self.current_theme]["frame_bg"],
            justify="center"
        )
        info_label.pack(pady=20)
        
        # Test button
        test_btn = ModernButton(
            main_frame,
            text="🔍 Test Vehicles Data",
            style="primary",
            command=self._test_vehicles_data
        )
        test_btn.pack(pady=10)
        
        # Vehicle count
        self._show_vehicle_count(main_frame)
    
    def _test_vehicles_data(self):
        """Test vehicle data access"""
        try:
            vehicles = self.db.get_vehicles()
            messagebox.showinfo(
                "Vehicles Test",
                f"✅ Vehicles Module Working!\n\nTotal Vehicles: {len(vehicles)}\n\nModule: vehicles_tab.py\nDatabase: Connected\nUI: Responsive"
            )
            log_user_action("Tested vehicles data from module")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error accessing vehicles: {e}")
    
    def _show_vehicle_count(self, parent):
        """Show current vehicle count"""
        try:
            vehicles = self.db.get_vehicles()
            count_frame = tk.Frame(parent, bg=THEMES[self.current_theme]["frame_bg"])
            count_frame.pack(pady=20)
            
            tk.Label(
                count_frame,
                text="📊 Current Statistics:",
                font=FONT_NORMAL,
                fg=THEMES[self.current_theme]["accent"],
                bg=THEMES[self.current_theme]["frame_bg"]
            ).pack()
            
            tk.Label(
                count_frame,
                text=f"Total Vehicles: {len(vehicles)}",
                font=FONT_NORMAL,
                fg=THEMES[self.current_theme]["fg"],
                bg=THEMES[self.current_theme]["frame_bg"]
            ).pack(pady=5)
            
        except Exception as e:
            logging.error(f"Error showing vehicle count: {e}")
    
    def refresh_data(self):
        """Refresh data in the tab"""
        logging.info("Vehicles tab data refreshed")
        # This would reload vehicle data in a full implementation
