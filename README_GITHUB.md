# 🚗 Fleet Manager - Modern Vehicle Management System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

*A comprehensive fleet management solution built with Python and modern UI design*

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Screenshots](#-screenshots) • [Contributing](#-contributing)

</div>

## 🌟 Features

### Core Functionality
- **🚙 Vehicle Management**: Complete CRUD operations with photo support
- **👨‍💼 Driver Management**: Comprehensive driver database and analytics
- **🛣️ Movement Tracking**: Detailed trip logging and route management
- **⛽ Fuel Management**: Tank monitoring and consumption tracking
- **📊 Analytics Dashboard**: Real-time performance metrics and insights
- **📋 Report Generation**: PDF reports and data export capabilities

### Advanced Features
- **🎨 Theme System**: 5 professional themes (Light, Dark, Blue, Green, Purple)
- **🔍 Advanced Search**: Fast search and filtering across all modules
- **📱 Modern UI**: Responsive design with custom components
- **💾 Auto-Save**: Automatic settings persistence
- **📈 Driver Analytics**: Performance comparison and efficiency tracking
- **🔒 Data Validation**: Comprehensive input validation and error handling

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/fleet-manager.git
   cd fleet-manager
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python fleet_manager_improved.py
   ```

### Dependencies
```
Pillow>=9.0.0
reportlab>=3.6.0
```

## 📱 Usage

### First Launch
1. The application will automatically create the SQLite database
2. Choose your preferred theme from the toolbar
3. Start by adding vehicles and drivers
4. Begin tracking movements and fuel consumption

### Key Operations
- **Add Vehicle**: Navigate to Vehicles tab → Click "Προσθήκη Οχήματος"
- **Record Movement**: Go to Movements tab → Fill movement details
- **View Analytics**: Check Driver Analytics tab for insights
- **Generate Reports**: Use Reports tab for PDF generation

## 📸 Screenshots

*Screenshots will be added here showing the main interface and features*

## 🏗️ Architecture

### Project Structure
```
fleet-manager/
├── fleet_manager_improved.py     # Main application
├── database.py                   # Database management
├── config.py                     # Configuration and themes
├── ui_components.py              # Custom UI components
├── utils.py                      # Utility functions
├── requirements.txt              # Dependencies
├── tabs/                         # Modular UI tabs
│   ├── drivers_tab.py
│   ├── vehicles_tab.py
│   ├── movements_tab.py
│   └── ...
└── images/                       # UI assets
```

### Database Schema
- **vehicles**: Vehicle information and specifications
- **drivers**: Driver profiles and details
- **movements**: Trip records and routes
- **fuel**: Fuel consumption and costs
- **purposes**: Movement categories
- **system_settings**: Application configuration

## 🔧 Configuration

### Themes
The application supports 5 built-in themes that can be switched from the toolbar:
- Light (default)
- Dark
- Blue Professional
- Green Nature
- Purple Modern

### Database
- SQLite database stored as `fleet.db`
- Automatic backup system
- Data import/export capabilities

## 📊 Analytics Features

### Driver Performance
- Total kilometers driven
- Fuel consumption analysis
- Efficiency metrics (L/100km)
- Monthly performance breakdown
- Comparative analysis between drivers

### Fleet Overview
- Vehicle utilization rates
- Fuel cost analysis
- Movement patterns
- Purpose-based statistics

## 🤝 Contributing

We welcome contributions to improve Fleet Manager!

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -am 'Add some feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

### Coding Standards
- Follow PEP 8 style guidelines
- Add docstrings to functions and classes
- Include error handling for database operations
- Test UI changes with different themes

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Documentation
- [Installation Guide](DEPLOYMENT_CHECKLIST.md)
- [Data Import Templates](DATA_IMPORT_TEMPLATES.md)
- [Production Setup](PRODUCTION_README.md)

### Getting Help
- 🐛 **Bug Reports**: Open an issue with detailed description
- 💡 **Feature Requests**: Discuss in issues before implementing
- 📧 **Questions**: Use GitHub Discussions for general questions

## 🎯 Roadmap

### Upcoming Features
- [ ] Mobile companion app
- [ ] Cloud synchronization
- [ ] API for third-party integrations
- [ ] Advanced reporting templates
- [ ] Multi-language support
- [ ] Role-based access control

### Version History
- **v1.0.0** - Initial release with core features
- **v1.1.0** - Added theme system and analytics
- **v1.2.0** - Enhanced UI and performance improvements

## 🙏 Acknowledgments

- Built with Python and Tkinter
- Icons and UI inspiration from modern design systems
- Database optimization techniques from SQLite best practices

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ for efficient fleet management

</div>
