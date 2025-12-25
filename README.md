# 📊 Excise Parallel Register System

**Comprehensive Digital Register Management for SIP 2 LIFE DISTILLERIES**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)

---

## 🎯 Overview

The Excise Parallel Register System is a comprehensive digital solution for managing excise-related registers in distillery operations. Built with Streamlit, it provides an intuitive interface for tracking production, fees, inventory, and excise duty.

---

## ✨ Features

### 📦 **Reg-B - Issue of Country Liquor in Bottles**
- Production fees account (₹3 per bottle)
- Multi-size bottle tracking (750ml, 600ml, 500ml, 375ml, 300ml, 180ml)
- Multi-strength tracking (50°, 60°, 70°, 80° U.P.)
- Auto-fill from Reg-A production data
- Automatic BL/AL calculations
- Wastage/breakage tracking
- Daily summary generation

### 💰 **Excise Duty Register**
- Personal ledger account of excise duty for IML
- Strength-based duty rates:
  - 50° U.P. (28.5% v/v) → ₹50/BL
  - 60° U.P. (22.8% v/v) → ₹50/BL
  - 70° U.P. (17.1% v/v) → ₹20/BL
  - 80° U.P. (11.4% v/v) → ₹17/BL
- Auto-fill from Reg-B issued bottles
- Financial account tracking with E-Challan
- Transport permit tracking
- Duty breakdown by strength
- Balance validation

### � **Integration**
- Seamless data flow between registers
- Automatic calculations across modules
- Real-time validation
- Consolidated reporting

---

## � Quick Start

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/saha-trideep/excise-parallel-register-system.git
   cd excise-parallel-register-system
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run Home.py
   ```

4. **Access the app:**
   - Open your browser to `http://localhost:8501`

---

## 🌐 Deployment

### Streamlit Cloud

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

**Quick Deploy:**
1. Push code to GitHub
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Connect your repository
4. Deploy with `Home.py` as the main file

---

## 📁 Project Structure

```
excise-parallel-register-system/
├── Home.py                          # Main landing page
├── pages/
│   ├── 1_📦_Reg_B.py               # Reg-B register
│   ├── 2_💰_Excise_Duty.py         # Excise Duty register
│   └── 6_📚_Daily_Handbook.py      # Daily Handbook Generator
├── regb_schema.py                   # Reg-B data models
├── regb_backend.py                  # Reg-B database operations
├── regb_utils.py                    # Reg-B utilities
├── excise_duty_schema.py            # Excise Duty data models
├── excise_duty_backend.py           # Excise Duty database operations
├── excise_duty_utils.py             # Excise Duty utilities
├── requirements.txt                 # Python dependencies
├── .streamlit/
│   └── config.toml                  # Streamlit configuration
├── .gitignore                       # Git ignore rules
├── DEPLOYMENT.md                    # Deployment guide
└── README.md                        # This file
```

---

## 🛠️ Technology Stack

- **Frontend:** Streamlit
- **Backend:** Python 3.11+
- **Database:** SQLite (local) / PostgreSQL (production)
- **Data Validation:** Pydantic
- **Data Processing:** Pandas

---

## 📋 Requirements

- Python 3.11 or higher
- Streamlit >= 1.28.0
- Pandas >= 2.0.0
- Pydantic >= 2.0.0

See [requirements.txt](requirements.txt) for complete list.

---

## � Usage

### Daily Workflow:

1. **Reg-A (Production)** → Record production and bottling operations
2. **Reg-78** → Track production fees on bulk litres
3. **Reg-B** → Record bottle issues and production fees
4. **Excise Duty Register** → Calculate and track excise duty

### Navigation:

- Use the sidebar to switch between registers
- Each register has Data Entry and Summary views
- Enable auto-fill options for streamlined entry

---

## 🧮 Key Calculations

### Bottle to BL Conversion:
```
BL = (bottles × bottle_size_ml) / 1000
```

### BL to AL Conversion:
```
AL = BL × (strength / 100)
```

### Production Fees (Reg-B):
```
Fees = bottles × ₹3.00
```

### Excise Duty:
```
Duty = BL × Duty Rate (based on strength)
```

---

## ✅ Features Checklist

- [x] Multi-page Streamlit app
- [x] SQLite database integration
- [x] Pydantic data validation
- [x] Auto-fill from related registers
- [x] Automatic calculations (BL, AL, fees, duty)
- [x] Real-time validation
- [x] Summary views
- [x] Premium UI with gradients
- [x] Responsive design
- [x] Export-ready data tables
- [x] PDF export (Daily Handbook)
- [ ] Digital signatures (planned)
- [ ] Multi-user authentication (planned)

---

## 🔒 Security

- Input validation on all fields
- Parameterized database queries
- No hardcoded credentials
- Balance validation
- Data integrity checks

**For production deployment:**
- Implement user authentication
- Use Streamlit Secrets for sensitive data
- Consider external database (PostgreSQL)
- Regular backups

---

## 📊 Database Schema

### Reg-B Tables:
- `regb_production_fees` - Financial tracking
- `regb_bottle_stock` - Inventory tracking
- `regb_daily_summary` - Consolidated summaries

### Excise Duty Tables:
- `excise_duty_ledger` - Financial account
- `excise_duty_bottles` - Bottle issues
- `excise_duty_summary` - Daily summaries

---

## 🐛 Troubleshooting

### Common Issues:

**Database not found:**
- Database is created automatically on first run
- Check file permissions

**Import errors:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version`

**Calculation errors:**
- Verify input data types
- Check for negative values
- Ensure proper decimal precision

---

## 📝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## � License

This project is proprietary software for SIP 2 LIFE DISTILLERIES.

---

## 👥 Authors

- **Development Team** - SIP 2 LIFE DISTILLERIES
- **Repository:** https://github.com/saha-trideep/excise-parallel-register-system

---

## 📞 Support

For issues or questions:
- Create an issue on GitHub
- Contact the development team

---

## 🎉 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by Python
- Designed for SIP 2 LIFE DISTILLERIES

---

## 📈 Version History

### v1.0.0 (Current)
- ✅ Reg-B implementation
- ✅ Excise Duty Register implementation
- ✅ Auto-integration between registers
- ✅ Multi-page app structure
- ✅ Streamlit Cloud ready

---

**Ready for deployment!** 🚀

For deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)
