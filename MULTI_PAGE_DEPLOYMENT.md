# 📱 Multi-Page Streamlit Deployment Guide

## 🚀 **Multi-Page Architecture Overview**

The BFSI Wealth 360 Analytics Platform has been completely redesigned with a **multi-page architecture** for better navigation, maintainability, and user experience.

### **📁 Project Structure**

```
Stock Analysis/
├── streamlit_app.py                    # Main navigation page
├── utils/
│   └── data_functions.py              # Shared data functions
├── pages/
│   ├── 01_📊_Executive_Dashboard.py   # C-suite level insights
│   ├── 02_👥_Client_Analytics.py     # Customer insights & CRM
│   ├── 03_🎯_Portfolio_Management.py # Risk & performance analytics
│   ├── 04_🤖_AI_Automation.py        # AI-powered features
│   └── 05_🌍_Geographic_Insights.py  # Geospatial analytics
├── environment.yml                     # Snowflake Anaconda packages
├── requirements.txt                    # Local development dependencies
└── requirements-dev.txt               # Development tools
```

---

## 🏔️ **Streamlit in Snowflake Deployment**

### **Step 1: Upload Files**

In Snowsight, create a new Streamlit app and upload ALL the following files:

#### **✅ Required Files:**
1. **`streamlit_app.py`** (main application file)
2. **`environment.yml`** (package dependencies)
3. **`utils/data_functions.py`** (shared utilities)
4. **All page files:**
   - `pages/01_📊_Executive_Dashboard.py`
   - `pages/02_👥_Client_Analytics.py`
   - `pages/03_🎯_Portfolio_Management.py`
   - `pages/04_🤖_AI_Automation.py`
   - `pages/05_🌍_Geographic_Insights.py`

#### **📂 Directory Structure in Snowsight:**
```
Your Streamlit App/
├── streamlit_app.py          # Main file (set as primary)
├── environment.yml           # Package dependencies
├── utils/
│   └── data_functions.py
└── pages/
    ├── 01_📊_Executive_Dashboard.py
    ├── 02_👥_Client_Analytics.py
    ├── 03_🎯_Portfolio_Management.py
    ├── 04_🤖_AI_Automation.py
    └── 05_🌍_Geographic_Insights.py
```

### **Step 2: Set Main File**

In Snowsight Streamlit editor:
- Set **`streamlit_app.py`** as the main file
- Ensure it's marked as the primary application entry point

### **Step 3: Configure Packages**

Upload the `environment.yml` file with these dependencies:

**Option 1: With Python Version (Recommended)**
```yaml
name: sf_env
channels:
  - snowflake
dependencies:
  - python=3.9
  - streamlit
  - snowflake-snowpark-python
  - pandas
  - numpy
  - plotly
  - pydeck
```

**Option 2: Minimal (Let Snowflake choose Python version)**
```yaml
name: sf_env
channels:
  - snowflake
dependencies:
  - pandas
  - numpy
  - plotly
  - pydeck
  - snowflake-snowpark-python
```

### **Step 4: Deploy and Test**

1. Click **"Run"** in Snowsight
2. Navigate through all 5 pages to verify functionality
3. Test sidebar filters and navigation

---

## 💻 **Local Development Deployment**

### **Step 1: Clone and Setup**

```bash
git clone https://github.com/Deepjyoti-ricky/wealth-360-streamlit-snowflake.git
cd wealth-360-streamlit-snowflake

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies (automated)
python install_dependencies.py

# OR manual installation:
pip install -r requirements.txt
```

### **Step 2: Configure Secrets**

```bash
# Copy secrets template
cp .streamlit/secrets.example.toml .streamlit/secrets.toml

# Edit with your Snowflake credentials
nano .streamlit/secrets.toml
```

### **Step 3: Run Application**

```bash
streamlit run streamlit_app.py
```

The application will automatically discover and load all pages from the `pages/` directory.

---

## 🔧 **Multi-Page Features**

### **✨ Enhanced Navigation**

- **Main Page**: Welcome dashboard with platform overview
- **Sidebar Navigation**: Global filters, quick actions, live KPIs
- **Page Discovery**: Automatic detection of all `.py` files in `pages/`
- **Session State**: Shared filters and settings across pages

### **📊 Shared Functionality**

**`utils/data_functions.py` provides:**
- Database connection management
- Shared SQL query functions
- Common data processing utilities
- Global KPI calculations

**Benefits:**
- ✅ No code duplication
- ✅ Consistent data access patterns
- ✅ Centralized connection management
- ✅ Easy maintenance and updates

### **🎯 Page-Specific Features**

Each page is specialized for specific use cases:

| Page | Focus Area | Key Features |
|------|------------|--------------|
| **Executive Dashboard** | C-Suite Insights | KPIs, alerts, executive summary |
| **Client Analytics** | CRM & Engagement | Segmentation, churn, outreach |
| **Portfolio Management** | Risk & Performance | Drift analysis, anomalies, advisor metrics |
| **AI & Automation** | GenAI Features | Wealth narratives, KYC copilot |
| **Geographic Insights** | Geospatial Analytics | 3D maps, climate risk, coverage |

---

## 🚨 **Troubleshooting Multi-Page Issues**

### **Issue 1: Pages Not Loading**

**Symptoms:**
- Pages don't appear in sidebar
- Navigation menu is empty

**Solutions:**
- Ensure all `.py` files are in the `pages/` directory
- Check file naming format: `##_emoji_PageName.py`
- Verify files are uploaded to correct directory in Snowsight

### **Issue 2: Import Errors**

**Symptoms:**
```
ModuleNotFoundError: No module named 'utils.data_functions'
```

**Solutions:**
- Ensure `utils/data_functions.py` is uploaded
- Check directory structure matches exactly
- Verify all imports use relative paths: `from utils.data_functions import ...`

### **Issue 3: Shared State Issues**

**Symptoms:**
- Filters not working across pages
- Session state not persisting

**Solutions:**
- Check `st.session_state` usage in main app
- Ensure filters are stored in session state
- Verify each page accesses shared state correctly

### **Issue 4: Python Version Compatibility**

**Symptoms:**
```
SQL compilation error: Cannot create a Python function with the specified packages.
Please check your packages specification and try again. 'Packages not found: - python==X.Y'
```

**Solutions:**
- **Use Python 3.9** - Currently the most stable version supported by all packages
- **Or remove Python version entirely** and let Snowflake choose automatically
- **Current compatibility matrix (as of latest error):**
  - pandas: 3.8, 3.9, 3.11, 3.12, 3.13
  - snowflake-snowpark-python: 3.8, 3.9, 3.11, 3.12
  - pydeck: 3.8, 3.9, 3.11, 3.12, 3.13
  - plotly: 3.8, 3.9, 3.11, 3.12, 3.13
  - numpy: 3.8, 3.9, 3.11, 3.12, 3.13
- **Recommendation:** Use `python=3.9` as it's supported by ALL packages

### **Issue 5: Performance Issues**

**Symptoms:**
- Slow page loading
- Memory usage warnings

**Solutions:**
- Use `@st.cache_data` decorators appropriately
- Optimize shared functions in `utils/data_functions.py`
- Review database query efficiency

---

## 📈 **Benefits of Multi-Page Architecture**

### **🎯 User Experience**
- **Better Navigation**: Logical grouping of related features
- **Reduced Cognitive Load**: Focused pages instead of overwhelming tabs
- **Professional Appearance**: Enterprise-ready interface

### **👨‍💻 Developer Experience**
- **Modular Code**: Each page is self-contained
- **Easy Maintenance**: Changes isolated to specific pages
- **Team Collaboration**: Multiple developers can work on different pages
- **Scalability**: Easy to add new pages and features

### **🏢 Enterprise Benefits**
- **Specialized Views**: Different roles can focus on relevant pages
- **Performance Optimization**: Load only needed functionality
- **Security**: Page-level access control (future enhancement)
- **Deployment Flexibility**: Deploy subset of pages if needed

---

## 🎯 **Next Steps & Enhancements**

### **Planned Improvements**
- **Role-Based Access**: Different pages for different user roles
- **Custom Themes**: Branded appearance for different organizations
- **Advanced Caching**: Page-level caching strategies
- **Mobile Optimization**: Responsive design for mobile devices

### **Customization Options**
- **Add New Pages**: Simply create new `.py` files in `pages/` directory
- **Modify Navigation**: Update main `streamlit_app.py` sidebar
- **Extend Functionality**: Add new functions to `utils/data_functions.py`
- **Custom Styling**: Modify CSS in individual pages

---

## 📞 **Support & Contact**

For issues with the multi-page deployment:

**Author**: Deepjyoti Dev, Senior Data Cloud Architect, Snowflake GXC Team
**Email**: deepjyoti.dev@snowflake.com
**Phone**: +917205672310

**GitHub Repository**: https://github.com/Deepjyoti-ricky/wealth-360-streamlit-snowflake

---

*This multi-page architecture transforms the BFSI Wealth 360 platform into a truly enterprise-ready solution with professional navigation and specialized analytical views.*
