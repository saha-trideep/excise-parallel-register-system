# 🔧 Streamlit Cloud Advanced Settings Guide

## 📋 Overview

When deploying on Streamlit Cloud, you have access to advanced settings that can optimize your app's performance, security, and functionality.

---

## ⚙️ Advanced Settings in Streamlit Cloud

### 1. **Python Version**

**Recommended:** Python 3.11

**Options:**
- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11 (recommended)
- Python 3.12

**Why 3.11?**
- Better performance
- Improved error messages
- Full compatibility with all dependencies

---

### 2. **Secrets Management** 🔒

For production apps, you may want to store sensitive data securely.

**How to Add Secrets:**

1. In Streamlit Cloud dashboard, go to your app
2. Click "⚙️ Settings"
3. Click "Secrets"
4. Add your secrets in TOML format:

```toml
# Example secrets for database
[database]
host = "your-db-host.com"
port = 5432
database = "excise_db"
user = "db_user"
password = "your-secure-password"

# Example API keys
[api]
google_sheets_key = "your-api-key"
email_api_key = "your-email-key"

# Example authentication
[auth]
admin_password = "secure-admin-password"
```

**Access Secrets in Code:**

```python
import streamlit as st

# Access secrets
db_host = st.secrets["database"]["host"]
db_password = st.secrets["database"]["password"]
api_key = st.secrets["api"]["google_sheets_key"]
```

---

### 3. **Environment Variables**

You can set environment variables for your app.

**Common Use Cases:**
- Database connection strings
- API endpoints
- Feature flags
- Debug mode settings

**Example:**
```toml
# In Streamlit Cloud Secrets
[env]
DEBUG_MODE = "false"
DATABASE_URL = "postgresql://user:pass@host:5432/db"
APP_ENV = "production"
```

---

### 4. **Resource Limits**

Streamlit Cloud has resource limits:

**Free Tier:**
- 1 GB RAM
- 1 CPU core
- Limited to 3 apps

**Recommendations for Your App:**
- ✅ Use caching (`@st.cache_data`, `@st.cache_resource`)
- ✅ Optimize database queries
- ✅ Lazy load data
- ✅ Use pagination for large datasets

---

### 5. **Custom Domain** 🌐

**Free Domain:**
```
https://your-app-name.streamlit.app
```

**Custom Domain (Paid Plans):**
```
https://excise.yourcompany.com
```

**Setup:**
1. Upgrade to paid plan
2. Add CNAME record in your DNS
3. Configure in Streamlit Cloud settings

---

### 6. **Database Configuration**

### Option A: SQLite (Current - Not Recommended for Production)

**Issues:**
- Data lost on app restart
- Not suitable for production

### Option B: PostgreSQL (Recommended for Production)

**Setup:**

1. **Get PostgreSQL Database:**
   - Use [Supabase](https://supabase.com) (free tier available)
   - Or [ElephantSQL](https://www.elephantsql.com)
   - Or [Neon](https://neon.tech)

2. **Update requirements.txt:**
   ```txt
   streamlit>=1.28.0
   pandas>=2.0.0
   pydantic>=2.0.0
   psycopg2-binary>=2.9.0  # Add this for PostgreSQL
   ```

3. **Add Database URL to Secrets:**
   ```toml
   [database]
   url = "postgresql://user:password@host:5432/database"
   ```

4. **Update Backend Code:**
   ```python
   import os
   import streamlit as st
   
   # Get database URL from secrets or environment
   if "database" in st.secrets:
       DB_URL = st.secrets["database"]["url"]
   else:
       DB_URL = "sqlite:///excise_registers.db"  # Fallback
   ```

---

### 7. **Performance Optimization**

**Add to your code:**

```python
import streamlit as st

# Cache database connections
@st.cache_resource
def get_database_connection():
    # Your database connection code
    return connection

# Cache data loading
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data(date):
    # Your data loading code
    return data

# Use session state for temporary data
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
```

---

### 8. **Authentication** 🔐

**Option A: Simple Password Protection**

```python
import streamlit as st

def check_password():
    """Returns `True` if the user had the correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["auth"]["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password incorrect, show input + error
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct
        return True

# Use in your app
if check_password():
    # Your app code here
    st.write("Welcome to the app!")
```

**Option B: Multi-User Authentication**

```python
import streamlit_authenticator as stauth

# In secrets:
# [credentials]
# usernames = ["admin", "user1", "user2"]
# names = ["Admin User", "User One", "User Two"]
# passwords = ["hashed_pass1", "hashed_pass2", "hashed_pass3"]

authenticator = stauth.Authenticate(
    st.secrets["credentials"]["usernames"],
    st.secrets["credentials"]["names"],
    st.secrets["credentials"]["passwords"],
    "excise_app",
    "auth_key",
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.write(f'Welcome *{name}*')
    # Your app code here
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
```

---

### 9. **Monitoring & Analytics**

**Built-in Analytics:**
- Streamlit Cloud provides basic analytics
- View in app dashboard

**Custom Analytics:**

```python
import streamlit as st
from datetime import datetime

# Log user actions
def log_action(action, user=None):
    timestamp = datetime.now().isoformat()
    # Log to database or file
    st.session_state.setdefault('logs', []).append({
        'timestamp': timestamp,
        'action': action,
        'user': user
    })

# Usage
log_action("Reg-B entry created", user="admin")
```

---

### 10. **Error Handling & Logging**

**Add to your app:**

```python
import streamlit as st
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Error handler
def handle_error(error, context=""):
    """Handle errors gracefully"""
    logger.error(f"{context}: {str(error)}")
    st.error(f"An error occurred: {context}")
    
    # Show details in expander (only in debug mode)
    if st.secrets.get("env", {}).get("DEBUG_MODE") == "true":
        with st.expander("Error Details"):
            st.exception(error)

# Usage
try:
    # Your code
    result = some_operation()
except Exception as e:
    handle_error(e, "Failed to save data")
```

---

### 11. **Backup & Data Export**

**Add Export Functionality:**

```python
import streamlit as st
import pandas as pd
from datetime import datetime

def export_data_to_csv():
    """Export all data to CSV"""
    # Get data from database
    data = get_all_data()
    df = pd.DataFrame(data)
    
    # Create download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name=f"excise_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
```

---

### 12. **App Configuration File**

**Enhanced `.streamlit/config.toml`:**

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 200  # MB
maxMessageSize = 200  # MB

[browser]
gatherUsageStats = false
serverAddress = "your-app.streamlit.app"
serverPort = 443

[runner]
magicEnabled = true
fastReruns = true

[client]
showErrorDetails = false  # Set to true for debugging
toolbarMode = "minimal"

[logger]
level = "info"
messageFormat = "%(asctime)s %(message)s"
```

---

### 13. **Deployment Checklist**

Before deploying, ensure:

**Security:**
- [ ] No hardcoded passwords
- [ ] Secrets configured in Streamlit Cloud
- [ ] Authentication enabled (if needed)
- [ ] Input validation implemented
- [ ] SQL injection protection

**Performance:**
- [ ] Caching implemented
- [ ] Database queries optimized
- [ ] Large datasets paginated
- [ ] Images optimized

**Functionality:**
- [ ] All features tested
- [ ] Error handling implemented
- [ ] User feedback messages
- [ ] Data validation

**Documentation:**
- [ ] README updated
- [ ] User guide available
- [ ] API documentation (if applicable)

---

### 14. **Recommended Secrets for Your App**

```toml
# .streamlit/secrets.toml (Add in Streamlit Cloud)

# Database (if using PostgreSQL)
[database]
url = "postgresql://user:password@host:5432/excise_db"

# Authentication
[auth]
admin_password = "your-secure-password"
allowed_users = ["admin", "user1", "user2"]

# Environment
[env]
DEBUG_MODE = "false"
APP_ENV = "production"

# Email notifications (optional)
[email]
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "your-email@example.com"
sender_password = "your-app-password"

# Backup (optional)
[backup]
enabled = "true"
frequency = "daily"
retention_days = 30
```

---

### 15. **Monitoring App Health**

**Add Health Check:**

```python
import streamlit as st
from datetime import datetime

def check_app_health():
    """Check if app is healthy"""
    health = {
        'database': False,
        'timestamp': datetime.now().isoformat()
    }
    
    try:
        # Test database connection
        conn = get_database_connection()
        health['database'] = True
    except Exception as e:
        st.error(f"Database connection failed: {e}")
    
    return health

# Add to sidebar (for admins)
if st.sidebar.checkbox("Show Health Status", value=False):
    health = check_app_health()
    st.sidebar.json(health)
```

---

## 🎯 Recommended Settings for Your App

### **For Development/Testing:**
- Python: 3.11
- Database: SQLite (current)
- Debug Mode: Enabled
- Authentication: Optional

### **For Production:**
- Python: 3.11
- Database: PostgreSQL (recommended)
- Debug Mode: Disabled
- Authentication: Enabled
- Secrets: Configured
- Backups: Enabled
- Monitoring: Enabled

---

## 📝 Quick Setup Guide

1. **Deploy with Basic Settings:**
   - Use current SQLite setup
   - No secrets needed initially

2. **Add Authentication (Optional):**
   - Add password to secrets
   - Implement check_password() function

3. **Upgrade to PostgreSQL (Recommended):**
   - Get PostgreSQL database
   - Add connection URL to secrets
   - Update backend code
   - Migrate data

4. **Enable Monitoring:**
   - Add logging
   - Implement health checks
   - Set up error tracking

---

## 🆘 Support Resources

- **Streamlit Docs:** https://docs.streamlit.io/
- **Streamlit Community:** https://discuss.streamlit.io/
- **Deployment Guide:** https://docs.streamlit.io/streamlit-community-cloud

---

**Your app is ready to deploy with basic settings. Advanced features can be added later!** 🚀
