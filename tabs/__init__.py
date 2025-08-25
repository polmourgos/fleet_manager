"""
Tabs package for Fleet Management System
Contains all tab implementations in separate modules
"""

from .movements_tab import MovementsTab
from .vehicles_tab import VehiclesTab
from .drivers_tab import DriversTab
from .fuel_tab import FuelTab
from .purposes_tab import PurposesTab
from .reports_tab import ReportsTab

__all__ = [
    'MovementsTab',
    'VehiclesTab', 
    'DriversTab',
    'FuelTab',
    'PurposesTab',
    'ReportsTab'
]
