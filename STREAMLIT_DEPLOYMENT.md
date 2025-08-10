# 🏔️ Streamlit in Snowflake Deployment Guide

## 🚨 Fixing: `ModuleNotFoundError: No module named 'plotly'`

When deploying to **Streamlit in Snowflake**, you need to use the `environment.yml` file instead of `requirements.txt` to specify dependencies.

### ✅ **Solution: Upload environment.yml**

1. **Create environment.yml** (already provided in this repo):
   ```yaml
   name: sf_env
channels:
  - snowflake
dependencies:
  - python=3.10
  - streamlit
     - snowflake-snowpark-python
     - pandas
     - numpy
     - plotly
     - pydeck
   ```

2. **Deploy to Snowflake**:
   - Go to Snowsight → Projects → Streamlit
   - Create New Streamlit App
   - **Upload BOTH files**:
     - `streamlit_app.py` (main file)
     - `environment.yml` (dependencies)

3. **Key Requirements**:
   - ✅ `channels: - snowflake` (mandatory)
   - ✅ Both files at same directory level
   - ✅ Use Snowflake Anaconda Channel packages only
   - ❌ Don't use `requirements.txt` in Streamlit in Snowflake

---

## 📋 **Step-by-Step Deployment**

### **Option A: Snowsight UI Deployment**

1. **Login to Snowsight**
   - Navigate to your Snowflake account
   - Go to **Projects** → **Streamlit**

2. **Create New App**
   ```
   App Name: BFSI Wealth 360 Analytics
   Database: FSI_DEMOS (or your database)
   Schema: WEALTH_360 (or your schema)
   Warehouse: COMPUTE_WH (or your warehouse)
   ```

3. **Upload Files**
   - **Main File**: Upload `streamlit_app.py`
   - **Additional Files**: Upload `environment.yml`
   - Ensure both files are at the root level

4. **Configure Packages** (Alternative to environment.yml)
   - Click "Packages" in Snowsight editor
   - Add packages manually:
     ```
     plotly
     pandas
     numpy
     pydeck
     ```

5. **Run Application**
   - Click "Run" in Snowsight
   - App will automatically install packages from Snowflake Anaconda Channel

### **Option B: SQL Deployment**

```sql
-- Create Streamlit app using SQL
CREATE OR REPLACE STREAMLIT "FSI_DEMOS"."WEALTH_360"."BFSI_WEALTH_360"
FROM '@MY_STAGE'
MAIN_FILE = '/streamlit_app.py';

-- Grant permissions
GRANT USAGE ON STREAMLIT "FSI_DEMOS"."WEALTH_360"."BFSI_WEALTH_360" TO ROLE YOUR_ROLE;
```

---

## 🔧 **Troubleshooting Common Issues**

### **Issue 1: Import Error After Deployment**
```
ModuleNotFoundError: No module named 'plotly'
```

**Solution**:
- Verify `environment.yml` is uploaded
- Check package name spelling: `plotly` (not `plotly.express`)
- Ensure `channels: - snowflake` is specified

### **Issue 2: Environment File Not Recognized**
```
Environment file not found
```

**Solution**:
- File must be named exactly `environment.yml`
- Must be at same level as `streamlit_app.py`
- Use YAML format (not JSON/TOML)

### **Issue 3: Package Not Available**
```
Package 'somepackage' not found in Snowflake channel
```

**Solution**:
- Check [Snowflake Anaconda Channel](https://repo.anaconda.com/pkgs/snowflake/)
- Use only packages available in Snowflake channel
- Remove unavailable packages from environment.yml

### **Issue 4: Python Version Mismatch**
```
Python version conflict
```

**Solution**:
- Specify Python version in environment.yml: `python=3.11`
- Use supported versions: 3.8, 3.9, 3.10, 3.11
- Default is 3.11 (recommended)

---

## ✅ **Verification Steps**

After deployment, verify the app works:

1. **Check Import Success**
   ```python
   import plotly.express as px
   print("✅ Plotly imported successfully")
   ```

2. **Test Visualizations**
   - Executive Dashboard should load
   - Charts should render properly
   - No import errors in logs

3. **Monitor Performance**
   - Check warehouse usage
   - Verify data queries execute
   - Confirm PyDeck maps load

---

## 📊 **Production Deployment Checklist**

- [ ] `streamlit_app.py` uploaded
- [ ] `environment.yml` uploaded with correct packages
- [ ] Database/schema permissions configured
- [ ] Warehouse selected and active
- [ ] All imports working without errors
- [ ] Charts and visualizations rendering
- [ ] PyDeck 3D maps loading
- [ ] Performance optimized for user load

---

## 🎯 **Expected Results**

After following this guide:
- ✅ No `ModuleNotFoundError` for plotly
- ✅ All visualizations working
- ✅ Executive dashboard loading
- ✅ PyDeck 3D maps functional
- ✅ Real-time data analytics operational

For additional support, see the main [README.md](README.md) or contact the development team.
