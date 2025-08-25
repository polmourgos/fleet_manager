"""
Drivers Tab Module for Fleet Management System
Handles all driver-related functionality
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging

from ui_components import ModernButton, ModernFrame
from config import THEMES, FONT_NORMAL, FONT_SUBTITLE
from utils import normalize_name, log_user_action


class DriversTab:
    """Manages the drivers tab functionality"""
    
    def __init__(self, parent_app, tab_widget, db, tooltip_manager):
        """
        Initialize drivers tab
        
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
        self.drivers_search_var = tk.StringVar()
        
        # Form entries (will be initialized in build method)
        self.ent_name = None
        self.ent_surname = None
        self.ent_notes = None
        
        # Tree widget
        self.tree_drivers = None
        self.driver_context_menu = None
    
    def _build_tab(self):
        """Build improved drivers tab with two-column layout"""
        # Main content frame
        main_content = tk.Frame(self.tab, bg=THEMES[self.current_theme]["bg"])
        main_content.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Configure grid weights for responsive design  
        main_content.grid_columnconfigure(0, weight=1)  # Left column (form)
        main_content.grid_columnconfigure(1, weight=2)  # Right column (list)
        main_content.grid_rowconfigure(0, weight=1)
        
        # LEFT COLUMN - Driver form
        self._create_driver_form(main_content)
        
        # RIGHT COLUMN - Drivers list section
        self._create_drivers_list(main_content)
        
        # Load initial data
        self.refresh_data()
    
    def _create_driver_form(self, parent):
        """Create the driver form section"""
        form_frame = ModernFrame(parent, bg=THEMES[self.current_theme]["frame_bg"])
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=0)
        
        # Title with modern styling
        title_label = tk.Label(form_frame, text="👤 Προσθήκη/Επεξεργασία Οδηγού", 
                              font=FONT_SUBTITLE, fg=THEMES[self.current_theme]["accent"],
                              bg=THEMES[self.current_theme]["frame_bg"])
        title_label.pack(pady=(15, 15))

        # Create form container
        form_container = tk.Frame(form_frame, bg=THEMES[self.current_theme]["frame_bg"])
        form_container.pack(fill="x", padx=15, pady=5)
        
        # Configure grid weights for responsive design
        form_container.grid_columnconfigure(1, weight=1)
        
        # Name field
        tk.Label(form_container, text="📝 Όνομα:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.ent_name = tk.Entry(
            form_container, 
            font=FONT_NORMAL,
            relief="flat", 
            borderwidth=1, 
            highlightthickness=1,
            highlightbackground=THEMES[self.current_theme]["border"],
            highlightcolor=THEMES[self.current_theme]["accent"]
        )
        self.ent_name.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        # Surname field
        tk.Label(form_container, text="📝 Επώνυμο:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        self.ent_surname = tk.Entry(
            form_container, 
            font=FONT_NORMAL,
            relief="flat", 
            borderwidth=1, 
            highlightthickness=1,
            highlightbackground=THEMES[self.current_theme]["border"],
            highlightcolor=THEMES[self.current_theme]["accent"]
        )
        self.ent_surname.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # Notes field
        tk.Label(form_container, text="📋 Σημειώσεις:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).grid(row=2, column=0, sticky="nw", padx=5, pady=5)
        
        self.ent_notes = tk.Text(
            form_container, 
            font=FONT_NORMAL,
            relief="flat", 
            borderwidth=1, 
            highlightthickness=1,
            highlightbackground=THEMES[self.current_theme]["border"],
            highlightcolor=THEMES[self.current_theme]["accent"],
            height=4,
            wrap=tk.WORD
        )
        self.ent_notes.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        # Buttons with compact modern styling
        btn_frame = tk.Frame(form_frame, bg=THEMES[self.current_theme]["frame_bg"])
        btn_frame.pack(pady=15)
        
        ModernButton(btn_frame, text="➕ Προσθήκη", style="success", 
                    command=self.add_driver).pack(side="left", padx=3)
        ModernButton(btn_frame, text="✏️ Ενημέρωση", style="primary", 
                    command=self.update_driver).pack(side="left", padx=3)
        ModernButton(btn_frame, text="🗑️ Διαγραφή", style="danger", 
                    command=self.delete_driver).pack(side="left", padx=3)
        ModernButton(btn_frame, text="🧹 Εκκαθάριση", style="warning", 
                    command=self.clear_form).pack(side="left", padx=3)
    
    def _create_drivers_list(self, parent):
        """Create the drivers list section"""
        drivers_frame = ModernFrame(parent, bg=THEMES[self.current_theme]["frame_bg"])
        drivers_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=0)
        
        # Title for drivers list
        drivers_title = tk.Label(drivers_frame, text="📋 Λίστα Οδηγών", 
                                font=FONT_SUBTITLE, fg=THEMES[self.current_theme]["accent"],
                                bg=THEMES[self.current_theme]["frame_bg"])
        drivers_title.pack(pady=(15, 10))

        # Search frame with modern styling
        search_frame_d = tk.Frame(drivers_frame, bg=THEMES[self.current_theme]["frame_bg"])
        search_frame_d.pack(fill="x", pady=5, padx=15)
        tk.Label(search_frame_d, text="🔍 Αναζήτηση:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).pack(side="left")
        
        self.drivers_search_entry = tk.Entry(search_frame_d, textvariable=self.drivers_search_var, 
                                            font=FONT_NORMAL, relief="flat", borderwidth=1, highlightthickness=1,
                                            highlightbackground=THEMES[self.current_theme]["border"],
                                            highlightcolor=THEMES[self.current_theme]["accent"])
        self.drivers_search_entry.pack(side="left", padx=10, fill="x", expand=True)
        self.drivers_search_var.trace("w", lambda *args: self.load_drivers())

        # Tree with modern styling
        tree_container = tk.Frame(drivers_frame, bg=THEMES[self.current_theme]["frame_bg"])
        tree_container.pack(fill="both", expand=True, padx=15, pady=5)
        
        self.tree_drivers = ttk.Treeview(tree_container, 
                                        columns=("name", "surname", "notes"), 
                                        show="headings", height=12)
        
        # Configure columns
        columns_config = [
            ("name", "📝 Όνομα", 150),
            ("surname", "📝 Επώνυμο", 150),
            ("notes", "📋 Σημειώσεις", 250)
        ]
        
        for col, text, width in columns_config:
            self.tree_drivers.heading(col, text=text)
            self.tree_drivers.column(col, width=width, anchor="center")
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree_drivers.yview)
        h_scrollbar = ttk.Scrollbar(tree_container, orient="horizontal", command=self.tree_drivers.xview)
        self.tree_drivers.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.tree_drivers.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Bind events
        self.tree_drivers.bind("<Double-1>", self.select_from_tree)
        self.tree_drivers.bind("<Button-3>", self.show_context_menu)  # Right click
        
        # Create context menu for drivers
        self.driver_context_menu = tk.Menu(self.app.root, tearoff=0, 
                                          bg=THEMES[self.current_theme]["frame_bg"], 
                                          fg=THEMES[self.current_theme]["fg"],
                                          activebackground=THEMES[self.current_theme]["select_bg"],
                                          activeforeground=THEMES[self.current_theme]["select_fg"])
        self.driver_context_menu.add_command(label="📋 Ιστορικό Κινήσεων", command=self.show_driver_history)
        self.driver_context_menu.add_command(label="⛽ Ιστορικό Καυσίμων", command=self.show_driver_fuel_history)
        self.driver_context_menu.add_separator()
        self.driver_context_menu.add_command(label="📊 Στατιστικά Οδηγού", command=self.show_driver_statistics)
        self.driver_context_menu.add_separator()
        self.driver_context_menu.add_command(label="✏️ Επεξεργασία", command=self.select_from_tree)
    
    # Delegated methods to main app
    def add_driver(self):
        """Add new driver - delegate to main app"""
        self.app._add_driver()
    
    def update_driver(self):
        """Update driver - delegate to main app"""
        self.app._update_driver()
    
    def delete_driver(self):
        """Delete driver - delegate to main app"""
        self.app._delete_driver()
    
    def clear_form(self):
        """Clear form - delegate to main app"""
        self.app._clear_driver_form()
    
    def select_from_tree(self, event=None):
        """Select driver from tree - delegate to main app"""
        self.app._select_driver_from_tree(event)
    
    def show_context_menu(self, event):
        """Show context menu - delegate to main app"""
        self.app._show_driver_context_menu(event)
    
    def show_driver_history(self):
        """Show driver history - delegate to main app"""
        self.app._show_driver_history()
    
    def show_driver_fuel_history(self):
        """Show driver fuel history - delegate to main app"""
        self.app._show_driver_fuel_history()
    
    def show_driver_statistics(self):
        """Show driver statistics - delegate to main app"""
        self.app._show_driver_statistics()
    
    def load_drivers(self):
        """Load drivers - delegate to main app"""
        self.app._load_drivers()
    
    def refresh_data(self):
        """Refresh all data in the tab"""
        self.load_drivers()
