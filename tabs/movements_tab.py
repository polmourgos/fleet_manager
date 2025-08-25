"""
Movements Tab Module for Fleet Management System
Handles all movement-related functionality
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import os
import logging

from ui_components import ModernButton, ModernFrame, SearchableCombobox
from config import THEMES, FONT_NORMAL, FONT_TITLE
from utils import normalize_plate, validate_date, log_user_action


class MovementsTab:
    """Manages the movements tab functionality"""
    
    def __init__(self, parent_app, tab_widget, db, tooltip_manager):
        """
        Initialize movements tab
        
        Args:
            parent_app: Reference to main application
            tab_widget: The tab widget to attach to
            db: Database manager instance
            tooltip_manager: Tooltip manager instance
        """
        self.app = parent_app
        self.tab = tab_widget
        self.db = db
        self.tooltip_manager = tooltip_manager
        self.current_theme = parent_app.current_theme
        
        # Initialize variables
        self._init_variables()
        
        # Build the tab
        self._build_tab()
    
    def _init_variables(self):
        """Initialize all tkinter variables"""
        self.mov_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.mov_start_km_var = tk.StringVar()
        
        # Combo boxes will be initialized in build method
        self.mov_driver_combo = None
        self.mov_vehicle_combo = None
        self.mov_purpose_combobox = None
        self.mov_route_entry = None
        
        # Tree widgets for active and completed movements
        self.active_movements_tree = None
        self.completed_movements_tree = None
    
    def _build_tab(self):
        """Build the complete movements tab"""
        # Create main scrollable container
        canvas = tk.Canvas(self.tab, bg=THEMES[self.current_theme]["bg"])
        scrollbar = ttk.Scrollbar(self.tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Build sections
        self._create_movement_form(scrollable_frame)
        self._create_active_movements_section(scrollable_frame)
        self._create_completed_movements_section(scrollable_frame)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def _create_movement_form(self, parent):
        """Create new movement form with improved validation"""
        form_frame = ModernFrame(parent, theme=self.current_theme)
        form_frame.pack(fill="x", padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            form_frame, 
            text="📝 Έκδοση Νέας Κίνησης Οχήματος", 
            font=FONT_TITLE, 
            fg=THEMES[self.current_theme]["accent"],
            bg=THEMES[self.current_theme]["frame_bg"]
        )
        title_label.pack(pady=(15, 20))
        
        # Form container with grid layout
        form_container = tk.Frame(form_frame, bg=THEMES[self.current_theme]["frame_bg"])
        form_container.pack(fill="x", padx=20, pady=10)
        
        # Configure grid weights for responsive design
        for i in range(3):
            form_container.grid_columnconfigure(i, weight=1)
        
        # Date field
        tk.Label(form_container, text="📅 Ημερομηνία:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).grid(row=0, column=0, sticky="w", padx=5, pady=8)
        
        self.mov_date_entry = tk.Entry(
            form_container, 
            textvariable=self.mov_date_var, 
            font=FONT_NORMAL,
            relief="flat", 
            borderwidth=1, 
            highlightthickness=1,
            highlightbackground=THEMES[self.current_theme]["border"],
            highlightcolor=THEMES[self.current_theme]["accent"]
        )
        self.mov_date_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=8)
        
        # Add tooltip
        self.tooltip_manager.add_tooltip(self.mov_date_entry, "Μορφή: YYYY-MM-DD")
        
        # Driver field with improved search
        tk.Label(form_container, text="👤 Οδηγός:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).grid(row=1, column=0, sticky="w", padx=5, pady=8)
        
        self.mov_driver_combo = SearchableCombobox(
            form_container, 
            font=FONT_NORMAL, 
            placeholder="Αναζήτηση οδηγού..."
        )
        self.mov_driver_combo.grid(row=1, column=1, sticky="ew", padx=5, pady=8)
        
        # Vehicle field with improved search
        tk.Label(form_container, text="🚗 Όχημα:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).grid(row=2, column=0, sticky="w", padx=5, pady=8)
        
        self.mov_vehicle_combo = SearchableCombobox(
            form_container, 
            font=FONT_NORMAL,
            placeholder="Αναζήτηση οχήματος..."
        )
        self.mov_vehicle_combo.grid(row=2, column=1, sticky="ew", padx=5, pady=8)
        
        # Start km field with validation
        tk.Label(form_container, text="🛣️ Χλμ Αναχώρησης:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).grid(row=3, column=0, sticky="w", padx=5, pady=8)
        
        self.mov_start_km_entry = tk.Entry(
            form_container, 
            textvariable=self.mov_start_km_var, 
            font=FONT_NORMAL,
            relief="flat", 
            borderwidth=1, 
            highlightthickness=1,
            highlightbackground=THEMES[self.current_theme]["border"],
            highlightcolor=THEMES[self.current_theme]["accent"]
        )
        self.mov_start_km_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=8)
        
        # Route field
        tk.Label(form_container, text="🗺️ Διαδρομή:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).grid(row=4, column=0, sticky="w", padx=5, pady=8)
        
        self.mov_route_entry = tk.Entry(
            form_container, 
            font=FONT_NORMAL,
            relief="flat", 
            borderwidth=1, 
            highlightthickness=1,
            highlightbackground=THEMES[self.current_theme]["border"],
            highlightcolor=THEMES[self.current_theme]["accent"]
        )
        self.mov_route_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=8)

        # Purpose field
        tk.Label(form_container, text="🎯 Σκοπός:", font=FONT_NORMAL,
                 bg=THEMES[self.current_theme]["frame_bg"],
                 fg=THEMES[self.current_theme]["fg"]).grid(row=5, column=0, sticky="w", padx=5, pady=8)
        
        # Get purposes from database
        self.purpose_options = self.db.get_purpose_names(active_only=True)
        self.mov_purpose_combobox = SearchableCombobox(
            form_container,
            values=self.purpose_options,
            font=FONT_NORMAL,
            width=30,
            placeholder="Επιλέξτε σκοπό..."
        )
        self.mov_purpose_combobox.grid(row=5, column=1, sticky="ew", padx=5, pady=8)
        
        # Submit button
        button_frame = tk.Frame(form_frame, bg=THEMES[self.current_theme]["frame_bg"])
        button_frame.pack(pady=20)
        
        # Movement submission button
        submit_btn = ModernButton(
            button_frame, 
            text="✅ Έκδοση Κίνησης", 
            style="success",
            command=self.add_movement
        )
        submit_btn.pack(side="left", padx=5)
        
        # Browse movements button
        browse_btn = ModernButton(
            button_frame, 
            text="📁 Περιήγηση Κινήσεων", 
            style="info",
            command=self.browse_movement_documents
        )
        browse_btn.pack(side="left", padx=5)
        
        # Add tooltips
        self.tooltip_manager.add_tooltip(submit_btn, "Δημιουργεί νέα κίνηση και εκτυπώσιμο έγγραφο")
        self.tooltip_manager.add_tooltip(browse_btn, "Περιήγηση στις αποθηκευμένες κινήσεις ανά έτος/μήνα")
        
        # Bind vehicle selection to auto-fill
        self.mov_vehicle_combo.var.trace("w", self.auto_fill_last_km)
    
    def _create_active_movements_section(self, parent):
        """Create section for active movements"""
        # Implementation will come from the main file
        # This is a placeholder for the refactoring
        pass
    
    def _create_completed_movements_section(self, parent):
        """Create section for completed movements"""
        # Implementation will come from the main file
        # This is a placeholder for the refactoring
        pass
    
    def add_movement(self):
        """Add new movement - delegate to main app"""
        self.app._add_movement()
    
    def browse_movement_documents(self):
        """Browse movement documents - delegate to main app"""
        self.app._browse_movement_documents()
    
    def auto_fill_last_km(self, *args):
        """Auto-fill last km when vehicle is selected - delegate to main app"""
        self.app._auto_fill_last_km(*args)
    
    def refresh_data(self):
        """Refresh all data in the tab"""
        # Update driver options
        drivers = self.db.get_drivers()
        driver_options = [f"{d[1]} {d[2]}" for d in drivers]
        self.mov_driver_combo.set_values(driver_options)
        
        # Update vehicle options
        vehicles = self.db.get_vehicles()
        vehicle_options = [f"{v[1]} ({v[2]} - {v[3]})" for v in vehicles]
        self.mov_vehicle_combo.set_values(vehicle_options)
        
        # Update purpose options
        self.purpose_options = self.db.get_purpose_names(active_only=True)
        self.mov_purpose_combobox.set_values(self.purpose_options)
        
        # Refresh movement lists if they exist
        if hasattr(self, 'active_movements_tree') and self.active_movements_tree:
            self.load_active_movements()
        if hasattr(self, 'completed_movements_tree') and self.completed_movements_tree:
            self.load_completed_movements()
    
    def load_active_movements(self):
        """Load active movements - to be implemented"""
        pass
    
    def load_completed_movements(self):
        """Load completed movements - to be implemented"""
        pass
