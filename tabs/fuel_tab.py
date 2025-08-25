"""
Fuel Tab Module for Fleet Management System
Handles all fuel-related functionality
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging

from ui_components import ModernButton, ModernFrame, SearchableCombobox
from config import THEMES, FONT_NORMAL, FONT_SUBTITLE, TANK_CAPACITY
from utils import format_fuel, format_currency, log_user_action


class FuelTab:
    """Manages the fuel tab functionality"""
    
    def __init__(self, parent_app, tab_widget, db, tooltip_manager):
        """
        Initialize fuel tab
        
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
        self.fuel_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.fuel_liters_var = tk.StringVar()
        self.fuel_mileage_var = tk.StringVar()
        self.fuel_cost_var = tk.StringVar()
        self.fuel_pump_var = tk.StringVar()
        
        # Combo boxes will be initialized in build method
        self.fuel_vehicle_combo = None
        self.fuel_driver_combo = None
        self.fuel_pump_combo = None
        
        # Tree widget for fuel records
        self.tree_fuel = None
        
        # Tank information labels
        self.tank_level_label = None
        self.tank_capacity_label = None
    
    def _build_tab(self):
        """Build the complete fuel tab"""
        # Main content frame
        main_content = tk.Frame(self.tab, bg=THEMES[self.current_theme]["bg"])
        main_content.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Configure grid weights for responsive design
        main_content.grid_columnconfigure(0, weight=1)  # Left column (form + tank)
        main_content.grid_columnconfigure(1, weight=2)  # Right column (fuel records)
        main_content.grid_rowconfigure(0, weight=1)
        
        # LEFT COLUMN - Fuel form and tank info
        self._create_fuel_form_and_tank(main_content)
        
        # RIGHT COLUMN - Fuel records list
        self._create_fuel_records_list(main_content)
        
        # Load initial data
        self.refresh_data()
    
    def _create_fuel_form_and_tank(self, parent):
        """Create the fuel form and tank information section"""
        left_frame = tk.Frame(parent, bg=THEMES[self.current_theme]["bg"])
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=0)
        
        # Fuel form
        self._create_fuel_form(left_frame)
        
        # Tank information
        self._create_tank_info(left_frame)
    
    def _create_fuel_form(self, parent):
        """Create fuel form section"""
        form_frame = ModernFrame(parent, bg=THEMES[self.current_theme]["frame_bg"])
        form_frame.pack(fill="x", pady=(0, 10))
        
        # Title
        title_label = tk.Label(form_frame, text="⛽ Καταγραφή Καυσίμων", 
                              font=FONT_SUBTITLE, fg=THEMES[self.current_theme]["accent"],
                              bg=THEMES[self.current_theme]["frame_bg"])
        title_label.pack(pady=(15, 15))

        # Create form container
        form_container = tk.Frame(form_frame, bg=THEMES[self.current_theme]["frame_bg"])
        form_container.pack(fill="x", padx=15, pady=5)
        
        # Configure grid weights
        form_container.grid_columnconfigure(1, weight=1)
        
        # Date field
        tk.Label(form_container, text="📅 Ημερομηνία:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.fuel_date_entry = tk.Entry(
            form_container, 
            textvariable=self.fuel_date_var, 
            font=FONT_NORMAL,
            relief="flat", 
            borderwidth=1, 
            highlightthickness=1,
            highlightbackground=THEMES[self.current_theme]["border"],
            highlightcolor=THEMES[self.current_theme]["accent"]
        )
        self.fuel_date_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        # Vehicle field
        tk.Label(form_container, text="🚗 Όχημα:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        self.fuel_vehicle_combo = SearchableCombobox(
            form_container, 
            font=FONT_NORMAL,
            placeholder="Επιλέξτε όχημα..."
        )
        self.fuel_vehicle_combo.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # Driver field
        tk.Label(form_container, text="👤 Οδηγός:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        
        self.fuel_driver_combo = SearchableCombobox(
            form_container, 
            font=FONT_NORMAL,
            placeholder="Επιλέξτε οδηγό..."
        )
        self.fuel_driver_combo.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        
        # Liters field
        tk.Label(form_container, text="⛽ Λίτρα:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).grid(row=3, column=0, sticky="w", padx=5, pady=5)
        
        self.fuel_liters_entry = tk.Entry(
            form_container, 
            textvariable=self.fuel_liters_var, 
            font=FONT_NORMAL,
            relief="flat", 
            borderwidth=1, 
            highlightthickness=1,
            highlightbackground=THEMES[self.current_theme]["border"],
            highlightcolor=THEMES[self.current_theme]["accent"]
        )
        self.fuel_liters_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        
        # Mileage field
        tk.Label(form_container, text="🛣️ Χλμ:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).grid(row=4, column=0, sticky="w", padx=5, pady=5)
        
        self.fuel_mileage_entry = tk.Entry(
            form_container, 
            textvariable=self.fuel_mileage_var, 
            font=FONT_NORMAL,
            relief="flat", 
            borderwidth=1, 
            highlightthickness=1,
            highlightbackground=THEMES[self.current_theme]["border"],
            highlightcolor=THEMES[self.current_theme]["accent"]
        )
        self.fuel_mileage_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=5)
        
        # Cost field
        tk.Label(form_container, text="💰 Κόστος:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).grid(row=5, column=0, sticky="w", padx=5, pady=5)
        
        self.fuel_cost_entry = tk.Entry(
            form_container, 
            textvariable=self.fuel_cost_var, 
            font=FONT_NORMAL,
            relief="flat", 
            borderwidth=1, 
            highlightthickness=1,
            highlightbackground=THEMES[self.current_theme]["border"],
            highlightcolor=THEMES[self.current_theme]["accent"]
        )
        self.fuel_cost_entry.grid(row=5, column=1, sticky="ew", padx=5, pady=5)
        
        # Pump field
        tk.Label(form_container, text="⛽ Αντλία:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).grid(row=6, column=0, sticky="w", padx=5, pady=5)
        
        self.fuel_pump_combo = SearchableCombobox(
            form_container,
            values=["Αντλία Αμαξοστασίου", "Εξωτερικό Πρατήριο"],
            font=FONT_NORMAL,
            placeholder="Επιλέξτε αντλία..."
        )
        self.fuel_pump_combo.grid(row=6, column=1, sticky="ew", padx=5, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg=THEMES[self.current_theme]["frame_bg"])
        btn_frame.pack(pady=15)
        
        ModernButton(btn_frame, text="➕ Προσθήκη", style="success", 
                    command=self.add_fuel).pack(side="left", padx=3)
        ModernButton(btn_frame, text="🧹 Εκκαθάριση", style="warning", 
                    command=self.clear_form).pack(side="left", padx=3)
    
    def _create_tank_info(self, parent):
        """Create tank information section"""
        tank_frame = ModernFrame(parent, bg=THEMES[self.current_theme]["frame_bg"])
        tank_frame.pack(fill="x", pady=(10, 0))
        
        # Title
        title_label = tk.Label(tank_frame, text="🛢️ Πληροφορίες Δεξαμενής", 
                              font=FONT_SUBTITLE, fg=THEMES[self.current_theme]["accent"],
                              bg=THEMES[self.current_theme]["frame_bg"])
        title_label.pack(pady=(15, 10))
        
        # Tank info container
        info_container = tk.Frame(tank_frame, bg=THEMES[self.current_theme]["frame_bg"])
        info_container.pack(fill="x", padx=15, pady=5)
        
        # Current level
        self.tank_level_label = tk.Label(info_container, text="Τρέχον Επίπεδο: Υπολογίζεται...", 
                                        font=FONT_NORMAL, fg=THEMES[self.current_theme]["fg"],
                                        bg=THEMES[self.current_theme]["frame_bg"])
        self.tank_level_label.pack(anchor="w", pady=2)
        
        # Total capacity
        self.tank_capacity_label = tk.Label(info_container, text=f"Συνολική Χωρητικότητα: {format_fuel(TANK_CAPACITY)}", 
                                           font=FONT_NORMAL, fg=THEMES[self.current_theme]["fg"],
                                           bg=THEMES[self.current_theme]["frame_bg"])
        self.tank_capacity_label.pack(anchor="w", pady=2)
        
        # Refill button
        refill_btn = ModernButton(tank_frame, text="⛽ Ανεφοδιασμός Δεξαμενής", 
                                 style="info", command=self.refill_tank)
        refill_btn.pack(pady=10)
    
    def _create_fuel_records_list(self, parent):
        """Create the fuel records list section"""
        records_frame = ModernFrame(parent, bg=THEMES[self.current_theme]["frame_bg"])
        records_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=0)
        
        # Title
        title_label = tk.Label(records_frame, text="📋 Ιστορικό Καυσίμων", 
                              font=FONT_SUBTITLE, fg=THEMES[self.current_theme]["accent"],
                              bg=THEMES[self.current_theme]["frame_bg"])
        title_label.pack(pady=(15, 10))
        
        # Tree container
        tree_container = tk.Frame(records_frame, bg=THEMES[self.current_theme]["frame_bg"])
        tree_container.pack(fill="both", expand=True, padx=15, pady=5)
        
        self.tree_fuel = ttk.Treeview(tree_container, 
                                     columns=("date", "vehicle", "driver", "liters", "mileage", "cost", "pump"), 
                                     show="headings", height=15)
        
        # Configure columns
        columns_config = [
            ("date", "📅 Ημερομηνία", 100),
            ("vehicle", "🚗 Όχημα", 100),
            ("driver", "👤 Οδηγός", 120),
            ("liters", "⛽ Λίτρα", 80),
            ("mileage", "🛣️ Χλμ", 80),
            ("cost", "💰 Κόστος", 80),
            ("pump", "⛽ Αντλία", 120)
        ]
        
        for col, text, width in columns_config:
            self.tree_fuel.heading(col, text=text)
            self.tree_fuel.column(col, width=width, anchor="center")
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree_fuel.yview)
        h_scrollbar = ttk.Scrollbar(tree_container, orient="horizontal", command=self.tree_fuel.xview)
        self.tree_fuel.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.tree_fuel.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
    
    # Delegated methods to main app
    def add_fuel(self):
        """Add fuel record - delegate to main app"""
        self.app._add_fuel()
    
    def clear_form(self):
        """Clear form - delegate to main app"""
        self.app._clear_fuel_form()
    
    def refill_tank(self):
        """Refill tank - delegate to main app"""
        self.app._refill_tank()
    
    def load_fuel_records(self):
        """Load fuel records - delegate to main app"""
        self.app._load_fuel_records()
    
    def update_tank_info(self):
        """Update tank information - delegate to main app"""
        self.app._update_tank_info()
    
    def refresh_data(self):
        """Refresh all data in the tab"""
        # Update vehicle options
        vehicles = self.db.get_vehicles()
        vehicle_options = [f"{v[1]} ({v[2]} - {v[3]})" for v in vehicles]
        if self.fuel_vehicle_combo:
            self.fuel_vehicle_combo.set_values(vehicle_options)
        
        # Update driver options
        drivers = self.db.get_drivers()
        driver_options = [f"{d[1]} {d[2]}" for d in drivers]
        if self.fuel_driver_combo:
            self.fuel_driver_combo.set_values(driver_options)
        
        # Load fuel records
        self.load_fuel_records()
        
        # Update tank info
        self.update_tank_info()
