"""
Reports Tab Module for Fleet Management System
Handles all reporting functionality
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import logging

from ui_components import ModernButton, ModernFrame, SearchableCombobox
from config import THEMES, FONT_NORMAL, FONT_SUBTITLE
from utils import format_currency, format_distance, format_fuel, export_to_csv, log_user_action


class ReportsTab:
    """Manages the reports tab functionality"""
    
    def __init__(self, parent_app, tab_widget, db, tooltip_manager):
        """
        Initialize reports tab
        
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
        # Date range for reports
        today = datetime.now()
        last_month = today - timedelta(days=30)
        
        self.report_start_date_var = tk.StringVar(value=last_month.strftime("%Y-%m-%d"))
        self.report_end_date_var = tk.StringVar(value=today.strftime("%Y-%m-%d"))
        
        # Report type selection
        self.report_type_var = tk.StringVar(value="movements")
        
        # Filter options
        self.filter_vehicle_combo = None
        self.filter_driver_combo = None
        self.filter_purpose_combo = None
        
        # Results tree
        self.tree_reports = None
        
        # Statistics labels
        self.stats_labels = {}
    
    def _build_tab(self):
        """Build the complete reports tab"""
        # Main content frame
        main_content = tk.Frame(self.tab, bg=THEMES[self.current_theme]["bg"])
        main_content.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Configure grid weights for responsive design
        main_content.grid_columnconfigure(0, weight=1)  # Left column (filters)
        main_content.grid_columnconfigure(1, weight=3)  # Right column (results)
        main_content.grid_rowconfigure(0, weight=1)
        
        # LEFT COLUMN - Report filters and controls
        self._create_report_controls(main_content)
        
        # RIGHT COLUMN - Report results and statistics
        self._create_report_results(main_content)
        
        # Load initial data
        self.refresh_data()
    
    def _create_report_controls(self, parent):
        """Create the report controls section"""
        controls_frame = ModernFrame(parent, bg=THEMES[self.current_theme]["frame_bg"])
        controls_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=0)
        
        # Title
        title_label = tk.Label(controls_frame, text="📊 Αναφορές & Στατιστικά", 
                              font=FONT_SUBTITLE, fg=THEMES[self.current_theme]["accent"],
                              bg=THEMES[self.current_theme]["frame_bg"])
        title_label.pack(pady=(15, 15))

        # Report type selection
        type_frame = tk.LabelFrame(controls_frame, text="📈 Τύπος Αναφοράς", 
                                  font=FONT_NORMAL, bg=THEMES[self.current_theme]["frame_bg"],
                                  fg=THEMES[self.current_theme]["fg"])
        type_frame.pack(fill="x", padx=15, pady=5)
        
        report_types = [
            ("movements", "📝 Κινήσεις Οχημάτων"),
            ("fuel", "⛽ Κατανάλωση Καυσίμων"),
            ("vehicles", "🚗 Στατιστικά Οχημάτων"),
            ("drivers", "👤 Στατιστικά Οδηγών"),
            ("efficiency", "📊 Αποδοτικότητα"),
            ("costs", "💰 Κόστη & Έξοδα")
        ]
        
        for value, text in report_types:
            tk.Radiobutton(type_frame, text=text, variable=self.report_type_var, 
                          value=value, font=FONT_NORMAL,
                          bg=THEMES[self.current_theme]["frame_bg"],
                          fg=THEMES[self.current_theme]["fg"],
                          selectcolor=THEMES[self.current_theme]["accent"]).pack(anchor="w", padx=10, pady=2)
        
        # Date range selection
        date_frame = tk.LabelFrame(controls_frame, text="📅 Χρονικό Διάστημα", 
                                  font=FONT_NORMAL, bg=THEMES[self.current_theme]["frame_bg"],
                                  fg=THEMES[self.current_theme]["fg"])
        date_frame.pack(fill="x", padx=15, pady=10)
        
        # Start date
        tk.Label(date_frame, text="Από:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.report_start_date_entry = tk.Entry(
            date_frame, 
            textvariable=self.report_start_date_var, 
            font=FONT_NORMAL,
            relief="flat", 
            borderwidth=1, 
            highlightthickness=1,
            highlightbackground=THEMES[self.current_theme]["border"],
            highlightcolor=THEMES[self.current_theme]["accent"]
        )
        self.report_start_date_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        # End date
        tk.Label(date_frame, text="Έως:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        self.report_end_date_entry = tk.Entry(
            date_frame, 
            textvariable=self.report_end_date_var, 
            font=FONT_NORMAL,
            relief="flat", 
            borderwidth=1, 
            highlightthickness=1,
            highlightbackground=THEMES[self.current_theme]["border"],
            highlightcolor=THEMES[self.current_theme]["accent"]
        )
        self.report_end_date_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        date_frame.grid_columnconfigure(1, weight=1)
        
        # Filters section
        filters_frame = tk.LabelFrame(controls_frame, text="🔍 Φίλτρα", 
                                     font=FONT_NORMAL, bg=THEMES[self.current_theme]["frame_bg"],
                                     fg=THEMES[self.current_theme]["fg"])
        filters_frame.pack(fill="x", padx=15, pady=10)
        
        # Vehicle filter
        tk.Label(filters_frame, text="🚗 Όχημα:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.filter_vehicle_combo = SearchableCombobox(
            filters_frame, 
            font=FONT_NORMAL,
            placeholder="Όλα τα οχήματα..."
        )
        self.filter_vehicle_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        # Driver filter
        tk.Label(filters_frame, text="👤 Οδηγός:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        self.filter_driver_combo = SearchableCombobox(
            filters_frame, 
            font=FONT_NORMAL,
            placeholder="Όλοι οι οδηγοί..."
        )
        self.filter_driver_combo.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # Purpose filter
        tk.Label(filters_frame, text="🎯 Σκοπός:", font=FONT_NORMAL,
                bg=THEMES[self.current_theme]["frame_bg"], 
                fg=THEMES[self.current_theme]["fg"]).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        
        self.filter_purpose_combo = SearchableCombobox(
            filters_frame, 
            font=FONT_NORMAL,
            placeholder="Όλοι οι σκοποί..."
        )
        self.filter_purpose_combo.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        
        filters_frame.grid_columnconfigure(1, weight=1)
        
        # Action buttons
        btn_frame = tk.Frame(controls_frame, bg=THEMES[self.current_theme]["frame_bg"])
        btn_frame.pack(pady=20)
        
        ModernButton(btn_frame, text="📊 Δημιουργία Αναφοράς", style="primary", 
                    command=self.generate_report).pack(pady=5, fill="x")
        ModernButton(btn_frame, text="💾 Εξαγωγή CSV", style="success", 
                    command=self.export_report).pack(pady=5, fill="x")
        ModernButton(btn_frame, text="🖨️ Εκτύπωση", style="info", 
                    command=self.print_report).pack(pady=5, fill="x")
    
    def _create_report_results(self, parent):
        """Create the report results section"""
        results_frame = ModernFrame(parent, bg=THEMES[self.current_theme]["frame_bg"])
        results_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=0)
        
        # Title
        title_label = tk.Label(results_frame, text="📋 Αποτελέσματα Αναφοράς", 
                              font=FONT_SUBTITLE, fg=THEMES[self.current_theme]["accent"],
                              bg=THEMES[self.current_theme]["frame_bg"])
        title_label.pack(pady=(15, 10))
        
        # Statistics section
        self._create_statistics_section(results_frame)
        
        # Results tree
        self._create_results_tree(results_frame)
    
    def _create_statistics_section(self, parent):
        """Create the statistics display section"""
        stats_frame = tk.LabelFrame(parent, text="📊 Στατιστικά", 
                                   font=FONT_NORMAL, bg=THEMES[self.current_theme]["frame_bg"],
                                   fg=THEMES[self.current_theme]["fg"])
        stats_frame.pack(fill="x", padx=15, pady=5)
        
        # Create a grid for statistics
        stats_container = tk.Frame(stats_frame, bg=THEMES[self.current_theme]["frame_bg"])
        stats_container.pack(fill="x", padx=10, pady=10)
        
        # Configure grid
        for i in range(3):
            stats_container.grid_columnconfigure(i, weight=1)
        
        # Initialize statistics labels
        stats_items = [
            ("total_movements", "Συνολικές Κινήσεις:", "0"),
            ("total_km", "Συνολικά Χλμ:", "0.0 χλμ"),
            ("total_fuel", "Συνολικά Καύσιμα:", "0.0 L"),
            ("total_cost", "Συνολικό Κόστος:", "0.00 €"),
            ("avg_efficiency", "Μέση Απόδοση:", "0.0 L/100χλμ"),
            ("active_vehicles", "Ενεργά Οχήματα:", "0")
        ]
        
        row = 0
        col = 0
        for key, label, default_value in stats_items:
            # Create label and value display
            label_widget = tk.Label(stats_container, text=label, font=FONT_NORMAL,
                                   bg=THEMES[self.current_theme]["frame_bg"], 
                                   fg=THEMES[self.current_theme]["fg"])
            label_widget.grid(row=row, column=col, sticky="w", padx=5, pady=2)
            
            value_widget = tk.Label(stats_container, text=default_value, font=FONT_NORMAL,
                                   bg=THEMES[self.current_theme]["frame_bg"], 
                                   fg=THEMES[self.current_theme]["accent"])
            value_widget.grid(row=row+1, column=col, sticky="w", padx=5, pady=2)
            
            self.stats_labels[key] = value_widget
            
            col += 1
            if col >= 3:
                col = 0
                row += 2
    
    def _create_results_tree(self, parent):
        """Create the results tree widget"""
        tree_container = tk.Frame(parent, bg=THEMES[self.current_theme]["frame_bg"])
        tree_container.pack(fill="both", expand=True, padx=15, pady=5)
        
        self.tree_reports = ttk.Treeview(tree_container, show="headings", height=15)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree_reports.yview)
        h_scrollbar = ttk.Scrollbar(tree_container, orient="horizontal", command=self.tree_reports.xview)
        self.tree_reports.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.tree_reports.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
    
    # Delegated methods to main app
    def generate_report(self):
        """Generate report - delegate to main app"""
        self.app._generate_report()
    
    def export_report(self):
        """Export report - delegate to main app"""
        self.app._export_report()
    
    def print_report(self):
        """Print report - delegate to main app"""
        self.app._print_report()
    
    def update_statistics(self, stats_data):
        """Update statistics display"""
        for key, value in stats_data.items():
            if key in self.stats_labels:
                self.stats_labels[key].config(text=str(value))
    
    def clear_results(self):
        """Clear current results"""
        if self.tree_reports:
            for item in self.tree_reports.get_children():
                self.tree_reports.delete(item)
        
        # Reset statistics
        default_stats = {
            "total_movements": "0",
            "total_km": "0.0 χλμ",
            "total_fuel": "0.0 L",
            "total_cost": "0.00 €",
            "avg_efficiency": "0.0 L/100χλμ",
            "active_vehicles": "0"
        }
        self.update_statistics(default_stats)
    
    def refresh_data(self):
        """Refresh all data in the tab"""
        # Update vehicle options
        vehicles = self.db.get_vehicles()
        vehicle_options = ["Όλα τα οχήματα..."] + [f"{v[1]} ({v[2]} - {v[3]})" for v in vehicles]
        if self.filter_vehicle_combo:
            self.filter_vehicle_combo.set_values(vehicle_options)
        
        # Update driver options
        drivers = self.db.get_drivers()
        driver_options = ["Όλοι οι οδηγοί..."] + [f"{d[1]} {d[2]}" for d in drivers]
        if self.filter_driver_combo:
            self.filter_driver_combo.set_values(driver_options)
        
        # Update purpose options
        purposes = self.db.get_purpose_names(active_only=True)
        purpose_options = ["Όλοι οι σκοποί..."] + purposes
        if self.filter_purpose_combo:
            self.filter_purpose_combo.set_values(purpose_options)
        
        # Clear current results
        self.clear_results()
