"""
Vehicles Tab Module for Fleet Management System
Handles all vehicle-related functionality
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import logging
import os

from ui_components import ModernButton, ModernFrame, SearchableCombobox
from config import THEMES, FONT_NORMAL, FONT_SUBTITLE, FONT_SMALL
from utils import normalize_plate, log_user_action


class VehiclesTab:
    """Manages the vehicles tab functionality"""
    
    def __init__(self, parent_app, tab_widget, db, tooltip_manager):
        """
        Initialize vehicles tab
        
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
        self.photo_path_var = tk.StringVar()
        self.vehicles_search_var = tk.StringVar()
        
        # Form entries (will be initialized in build method)
        self.ent_plate = None
        self.ent_brand = None
        self.ent_vtype = None
        self.ent_vpurpose = None
        self.photo_label = None
        
        # Tree widget
        self.tree_vehicles = None
        self.vehicle_context_menu = None
        
        # Vehicle purpose options
        self.vehicle_purpose_options = []
    
    def _build_tab(self):
        """Build improved vehicles tab with two-column layout"""
        # Main content frame
        main_content = tk.Frame(self.tab, bg=THEMES[self.current_theme]["bg"])
        main_content.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Configure grid weights for responsive design  
        main_content.grid_columnconfigure(0, weight=1)  # Left column (form)
        main_content.grid_columnconfigure(1, weight=2)  # Right column (list)
        main_content.grid_rowconfigure(0, weight=1)
        
        # LEFT COLUMN - Vehicle form
        self._create_vehicle_form(main_content)
        
        # RIGHT COLUMN - Vehicles list section
        self._create_vehicles_list(main_content)
        
        # Load initial data
        self.refresh_data()
    
    def _create_vehicle_form(self, parent):
        """Create the vehicle form section"""
        form_frame = ModernFrame(parent, bg=THEMES[self.current_theme]["frame_bg"])
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=0)
        
        # Title with modern styling
        title_label = tk.Label(form_frame, text="🚙 Προσθήκη/Επεξεργασία Οχήματος", 
                              font=FONT_SUBTITLE, fg=THEMES[self.current_theme]["accent"],
                              bg=THEMES[self.current_theme]["frame_bg"])
        title_label.pack(pady=(15, 15))

        # Create form container
        form_container = tk.Frame(form_frame, bg=THEMES[self.current_theme]["frame_bg"])
        form_container.pack(fill="x", padx=15, pady=5)
        
        # Configure grid weights for responsive design
        form_container.grid_columnconfigure(1, weight=1)
        
        # Plate field
        tk.Label(form_container, text="🔢 Πινακίδα:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.ent_plate = tk.Entry(
            form_container, 
            font=FONT_NORMAL,
            relief="flat", 
            borderwidth=1, 
            highlightthickness=1,
            highlightbackground=THEMES[self.current_theme]["border"],
            highlightcolor=THEMES[self.current_theme]["accent"]
        )
        self.ent_plate.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        # Brand field
        tk.Label(form_container, text="🏭 Μάρκα:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        self.ent_brand = tk.Entry(
            form_container, 
            font=FONT_NORMAL,
            relief="flat", 
            borderwidth=1, 
            highlightthickness=1,
            highlightbackground=THEMES[self.current_theme]["border"],
            highlightcolor=THEMES[self.current_theme]["accent"]
        )
        self.ent_brand.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # Type field
        tk.Label(form_container, text="🚗 Τύπος:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        
        self.ent_vtype = tk.Entry(
            form_container, 
            font=FONT_NORMAL,
            relief="flat", 
            borderwidth=1, 
            highlightthickness=1,
            highlightbackground=THEMES[self.current_theme]["border"],
            highlightcolor=THEMES[self.current_theme]["accent"]
        )
        self.ent_vtype.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        # Purpose field
        tk.Label(form_container, text="🎯 Σκοπός:", font=FONT_NORMAL,
                 bg=THEMES[self.current_theme]["frame_bg"],
                 fg=THEMES[self.current_theme]["fg"]).grid(row=3, column=0, sticky="w", padx=5, pady=5)
        
        # Get purposes from database
        self.vehicle_purpose_options = self.db.get_purpose_names(active_only=True)
        self.ent_vpurpose = SearchableCombobox(
            form_container,
            values=self.vehicle_purpose_options,
            font=FONT_NORMAL,
            width=25,
            placeholder="Επιλέξτε σκοπό..."
        )
        self.ent_vpurpose.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        
        # Photo field
        tk.Label(form_container, text="🖼️ Φωτογραφία:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).grid(row=4, column=0, sticky="w", padx=5, pady=5)

        # Photo handling with modern styling
        photo_container = tk.Frame(form_container, bg=THEMES[self.current_theme]["frame_bg"])
        photo_container.grid(row=4, column=1, sticky="ew", padx=5, pady=5)
        
        self.photo_label = tk.Label(photo_container, text="Δεν έχει επιλεγεί φωτογραφία", 
                                   fg=THEMES[self.current_theme]["text_muted"],
                                   bg=THEMES[self.current_theme]["frame_bg"], font=FONT_SMALL)
        self.photo_label.pack(side="left")
        
        photo_btn_frame = tk.Frame(photo_container, bg=THEMES[self.current_theme]["frame_bg"])
        photo_btn_frame.pack(side="right")
        
        ModernButton(photo_btn_frame, text="📁", style="secondary", 
                    command=self.select_photo).pack(side="left", padx=1)
        ModernButton(photo_btn_frame, text="👁️", style="info", 
                    command=self.view_photo).pack(side="left", padx=1)

        # Buttons with compact modern styling
        btn_frame = tk.Frame(form_frame, bg=THEMES[self.current_theme]["frame_bg"])
        btn_frame.pack(pady=15)
        
        ModernButton(btn_frame, text="➕ Προσθήκη", style="success", 
                    command=self.add_vehicle).pack(side="left", padx=3)
        ModernButton(btn_frame, text="✏️ Ενημέρωση", style="primary", 
                    command=self.update_vehicle).pack(side="left", padx=3)
        ModernButton(btn_frame, text="🗑️ Διαγραφή", style="danger", 
                    command=self.delete_vehicle).pack(side="left", padx=3)
        ModernButton(btn_frame, text="🧹 Εκκαθάριση", style="warning", 
                    command=self.clear_form).pack(side="left", padx=3)
    
    def _create_vehicles_list(self, parent):
        """Create the vehicles list section"""
        vehicles_frame = ModernFrame(parent, bg=THEMES[self.current_theme]["frame_bg"])
        vehicles_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=0)
        
        # Title for vehicles list
        vehicles_title = tk.Label(vehicles_frame, text="📋 Λίστα Οχημάτων", 
                                 font=FONT_SUBTITLE, fg=THEMES[self.current_theme]["accent"],
                                 bg=THEMES[self.current_theme]["frame_bg"])
        vehicles_title.pack(pady=(15, 10))

        # Search frame with modern styling
        search_frame_v = tk.Frame(vehicles_frame, bg=THEMES[self.current_theme]["frame_bg"])
        search_frame_v.pack(fill="x", pady=5, padx=15)
        tk.Label(search_frame_v, text="🔍 Αναζήτηση:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).pack(side="left")
        
        self.vehicles_search_entry = tk.Entry(search_frame_v, textvariable=self.vehicles_search_var, 
                                             font=FONT_NORMAL, relief="flat", borderwidth=1, highlightthickness=1,
                                             highlightbackground=THEMES[self.current_theme]["border"],
                                             highlightcolor=THEMES[self.current_theme]["accent"])
        self.vehicles_search_entry.pack(side="left", padx=10, fill="x", expand=True)
        self.vehicles_search_var.trace("w", lambda *args: self.load_vehicles())

        # Tree with modern styling
        tree_container = tk.Frame(vehicles_frame, bg=THEMES[self.current_theme]["frame_bg"])
        tree_container.pack(fill="both", expand=True, padx=15, pady=5)
        
        self.tree_vehicles = ttk.Treeview(tree_container, 
                                        columns=("plate", "brand", "vtype", "purpose"), 
                                        show="headings", height=12)
        
        # Configure columns
        columns_config = [
            ("plate", "🔢 Πινακίδα", 120),
            ("brand", "🏭 Μάρκα", 150),
            ("vtype", "🚗 Τύπος", 120),
            ("purpose", "🎯 Σκοπός", 200)
        ]
        
        for col, text, width in columns_config:
            self.tree_vehicles.heading(col, text=text)
            self.tree_vehicles.column(col, width=width, anchor="center")
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree_vehicles.yview)
        h_scrollbar = ttk.Scrollbar(tree_container, orient="horizontal", command=self.tree_vehicles.xview)
        self.tree_vehicles.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.tree_vehicles.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Bind events
        self.tree_vehicles.bind("<Double-1>", self.select_from_tree)
        self.tree_vehicles.bind("<Button-3>", self.show_context_menu)  # Right click
        
        # Create context menu for vehicles with modern styling
        self.vehicle_context_menu = tk.Menu(self.app.root, tearoff=0, 
                                           bg=THEMES[self.current_theme]["frame_bg"], 
                                           fg=THEMES[self.current_theme]["fg"],
                                           activebackground=THEMES[self.current_theme]["select_bg"],
                                           activeforeground=THEMES[self.current_theme]["select_fg"])
        self.vehicle_context_menu.add_command(label="📋 Ιστορικό Κινήσεων", command=self.show_vehicle_history)
        self.vehicle_context_menu.add_command(label="⛽ Ιστορικό Καυσίμων", command=self.show_vehicle_fuel_history)
        self.vehicle_context_menu.add_separator()
        self.vehicle_context_menu.add_command(label="📊 Στατιστικά Οχήματος", command=self.show_vehicle_statistics)
        self.vehicle_context_menu.add_separator()
        self.vehicle_context_menu.add_command(label="✏️ Επεξεργασία", command=self.select_from_tree)
        self.vehicle_context_menu.add_command(label="🖼️ Προβολή Φωτογραφίας", command=self.view_photo_from_tree)
    
    # Delegated methods to main app
    def add_vehicle(self):
        """Add new vehicle - delegate to main app"""
        self.app._add_vehicle()
    
    def update_vehicle(self):
        """Update vehicle - delegate to main app"""
        self.app._update_vehicle()
    
    def delete_vehicle(self):
        """Delete vehicle - delegate to main app"""
        self.app._delete_vehicle()
    
    def clear_form(self):
        """Clear form - delegate to main app"""
        self.app._clear_vehicle_form()
    
    def select_from_tree(self, event=None):
        """Select vehicle from tree - delegate to main app"""
        self.app._select_vehicle_from_tree(event)
    
    def select_photo(self):
        """Select photo - delegate to main app"""
        self.app._select_photo()
    
    def view_photo(self):
        """View photo - delegate to main app"""
        self.app._view_photo()
    
    def view_photo_from_tree(self):
        """View photo from tree - delegate to main app"""
        self.app._view_vehicle_photo_from_tree()
    
    def show_context_menu(self, event):
        """Show context menu - delegate to main app"""
        self.app._show_vehicle_context_menu(event)
    
    def show_vehicle_history(self):
        """Show vehicle history - delegate to main app"""
        self.app._show_vehicle_history()
    
    def show_vehicle_fuel_history(self):
        """Show vehicle fuel history - delegate to main app"""
        self.app._show_vehicle_fuel_history()
    
    def show_vehicle_statistics(self):
        """Show vehicle statistics - delegate to main app"""
        self.app._show_vehicle_statistics()
    
    def load_vehicles(self):
        """Load vehicles - delegate to main app"""
        self.app._load_vehicles()
    
    def refresh_data(self):
        """Refresh all data in the tab"""
        # Update purpose options
        self.vehicle_purpose_options = self.db.get_purpose_names(active_only=True)
        if self.ent_vpurpose:
            self.ent_vpurpose.set_values(self.vehicle_purpose_options)
        
        # Load vehicles
        self.load_vehicles()
