"""
Purposes Tab Module for Fleet Management System
Handles all purpose-related functionality
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging

from ui_components import ModernButton, ModernFrame
from config import THEMES, FONT_NORMAL, FONT_SUBTITLE
from utils import log_user_action


class PurposesTab:
    """Manages the purposes tab functionality"""
    
    def __init__(self, parent_app, tab_widget, db, tooltip_manager):
        """
        Initialize purposes tab
        
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
        self.purposes_search_var = tk.StringVar()
        
        # Form entries (will be initialized in build method)
        self.ent_purpose_name = None
        self.ent_purpose_description = None
        self.purpose_active_var = tk.BooleanVar(value=True)
        
        # Tree widget
        self.tree_purposes = None
        self.purpose_context_menu = None
        
        # Selected purpose ID for editing
        self.selected_purpose_id = None
    
    def _build_tab(self):
        """Build purposes tab with two-column layout"""
        # Main content frame
        main_content = tk.Frame(self.tab, bg=THEMES[self.current_theme]["bg"])
        main_content.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Configure grid weights for responsive design  
        main_content.grid_columnconfigure(0, weight=1)  # Left column (form)
        main_content.grid_columnconfigure(1, weight=2)  # Right column (list)
        main_content.grid_rowconfigure(0, weight=1)
        
        # LEFT COLUMN - Purpose form
        self._create_purpose_form(main_content)
        
        # RIGHT COLUMN - Purposes list section
        self._create_purposes_list(main_content)
        
        # Load initial data
        self.refresh_data()
    
    def _create_purpose_form(self, parent):
        """Create the purpose form section"""
        form_frame = ModernFrame(parent, bg=THEMES[self.current_theme]["frame_bg"])
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=0)
        
        # Title with modern styling
        title_label = tk.Label(form_frame, text="🎯 Διαχείριση Σκοπών", 
                              font=FONT_SUBTITLE, fg=THEMES[self.current_theme]["accent"],
                              bg=THEMES[self.current_theme]["frame_bg"])
        title_label.pack(pady=(15, 15))

        # Create form container
        form_container = tk.Frame(form_frame, bg=THEMES[self.current_theme]["frame_bg"])
        form_container.pack(fill="x", padx=15, pady=5)
        
        # Configure grid weights for responsive design
        form_container.grid_columnconfigure(1, weight=1)
        
        # Purpose name field
        tk.Label(form_container, text="📝 Όνομα Σκοπού:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.ent_purpose_name = tk.Entry(
            form_container, 
            font=FONT_NORMAL,
            relief="flat", 
            borderwidth=1, 
            highlightthickness=1,
            highlightbackground=THEMES[self.current_theme]["border"],
            highlightcolor=THEMES[self.current_theme]["accent"]
        )
        self.ent_purpose_name.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        # Purpose description field
        tk.Label(form_container, text="📋 Περιγραφή:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).grid(row=1, column=0, sticky="nw", padx=5, pady=5)
        
        self.ent_purpose_description = tk.Text(
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
        self.ent_purpose_description.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # Active checkbox
        self.purpose_active_check = tk.Checkbutton(
            form_container,
            text="✅ Ενεργός Σκοπός",
            variable=self.purpose_active_var,
            font=FONT_NORMAL,
            bg=THEMES[self.current_theme]["frame_bg"],
            fg=THEMES[self.current_theme]["fg"],
            selectcolor=THEMES[self.current_theme]["accent"]
        )
        self.purpose_active_check.grid(row=2, column=1, sticky="w", padx=5, pady=10)

        # Buttons with compact modern styling
        btn_frame = tk.Frame(form_frame, bg=THEMES[self.current_theme]["frame_bg"])
        btn_frame.pack(pady=15)
        
        ModernButton(btn_frame, text="➕ Προσθήκη", style="success", 
                    command=self.add_purpose).pack(side="left", padx=3)
        ModernButton(btn_frame, text="✏️ Ενημέρωση", style="primary", 
                    command=self.update_purpose).pack(side="left", padx=3)
        ModernButton(btn_frame, text="🗑️ Διαγραφή", style="danger", 
                    command=self.delete_purpose).pack(side="left", padx=3)
        ModernButton(btn_frame, text="🔄 Επαναφορά", style="warning", 
                    command=self.restore_purpose).pack(side="left", padx=3)
        ModernButton(btn_frame, text="🧹 Εκκαθάριση", style="secondary", 
                    command=self.clear_form).pack(side="left", padx=3)
    
    def _create_purposes_list(self, parent):
        """Create the purposes list section"""
        purposes_frame = ModernFrame(parent, bg=THEMES[self.current_theme]["frame_bg"])
        purposes_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=0)
        
        # Title for purposes list
        purposes_title = tk.Label(purposes_frame, text="📋 Λίστα Σκοπών", 
                                 font=FONT_SUBTITLE, fg=THEMES[self.current_theme]["accent"],
                                 bg=THEMES[self.current_theme]["frame_bg"])
        purposes_title.pack(pady=(15, 10))

        # Search frame with modern styling
        search_frame = tk.Frame(purposes_frame, bg=THEMES[self.current_theme]["frame_bg"])
        search_frame.pack(fill="x", pady=5, padx=15)
        tk.Label(search_frame, text="🔍 Αναζήτηση:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).pack(side="left")
        
        self.purposes_search_entry = tk.Entry(search_frame, textvariable=self.purposes_search_var, 
                                             font=FONT_NORMAL, relief="flat", borderwidth=1, highlightthickness=1,
                                             highlightbackground=THEMES[self.current_theme]["border"],
                                             highlightcolor=THEMES[self.current_theme]["accent"])
        self.purposes_search_entry.pack(side="left", padx=10, fill="x", expand=True)
        self.purposes_search_var.trace("w", lambda *args: self.load_purposes())

        # Tree with modern styling
        tree_container = tk.Frame(purposes_frame, bg=THEMES[self.current_theme]["frame_bg"])
        tree_container.pack(fill="both", expand=True, padx=15, pady=5)
        
        self.tree_purposes = ttk.Treeview(tree_container, 
                                         columns=("name", "description", "active", "created"), 
                                         show="headings", height=12)
        
        # Configure columns
        columns_config = [
            ("name", "📝 Όνομα", 150),
            ("description", "📋 Περιγραφή", 250),
            ("active", "✅ Ενεργός", 80),
            ("created", "📅 Δημιουργία", 120)
        ]
        
        for col, text, width in columns_config:
            self.tree_purposes.heading(col, text=text)
            self.tree_purposes.column(col, width=width, anchor="center")
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree_purposes.yview)
        h_scrollbar = ttk.Scrollbar(tree_container, orient="horizontal", command=self.tree_purposes.xview)
        self.tree_purposes.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.tree_purposes.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Bind events
        self.tree_purposes.bind("<Double-1>", self.select_from_tree)
        self.tree_purposes.bind("<Button-3>", self.show_context_menu)  # Right click
        
        # Create context menu for purposes
        self.purpose_context_menu = tk.Menu(self.app.root, tearoff=0, 
                                           bg=THEMES[self.current_theme]["frame_bg"], 
                                           fg=THEMES[self.current_theme]["fg"],
                                           activebackground=THEMES[self.current_theme]["select_bg"],
                                           activeforeground=THEMES[self.current_theme]["select_fg"])
        self.purpose_context_menu.add_command(label="📊 Στατιστικά Χρήσης", command=self.show_purpose_usage)
        self.purpose_context_menu.add_separator()
        self.purpose_context_menu.add_command(label="✏️ Επεξεργασία", command=self.select_from_tree)
        self.purpose_context_menu.add_command(label="🗑️ Διαγραφή", command=self.delete_purpose)
        self.purpose_context_menu.add_command(label="🔄 Επαναφορά", command=self.restore_purpose)
    
    # Delegated methods to main app
    def add_purpose(self):
        """Add new purpose - delegate to main app"""
        self.app._add_purpose()
    
    def update_purpose(self):
        """Update purpose - delegate to main app"""
        self.app._update_purpose()
    
    def delete_purpose(self):
        """Delete purpose - delegate to main app"""
        self.app._delete_purpose()
    
    def restore_purpose(self):
        """Restore purpose - delegate to main app"""
        self.app._restore_purpose()
    
    def clear_form(self):
        """Clear form - delegate to main app"""
        self.app._clear_purpose_form()
    
    def select_from_tree(self, event=None):
        """Select purpose from tree - delegate to main app"""
        self.app._select_purpose_from_tree(event)
    
    def show_context_menu(self, event):
        """Show context menu - delegate to main app"""
        self.app._show_purpose_context_menu(event)
    
    def show_purpose_usage(self):
        """Show purpose usage statistics - delegate to main app"""
        self.app._show_purpose_usage()
    
    def load_purposes(self):
        """Load purposes - delegate to main app"""
        self.app._load_purposes()
    
    def refresh_data(self):
        """Refresh all data in the tab"""
        self.load_purposes()
