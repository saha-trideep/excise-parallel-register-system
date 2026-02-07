# 🗑️ UNINSTALL GUIDE - PDF Dependencies

## ❓ Should You Uninstall?

### Current Situation:
You may have installed these packages:
- ✅ **weasyprint** - Doesn't work on Windows (needs GTK)
- ✅ **jinja2** - Template engine
- ✅ **plotly** - Charting library

### Current PDF System:
Your maintenance project now uses **ReportLab** which is:
- ✅ Already installed (came with reportlab package)
- ✅ Works perfectly on Windows
- ✅ No extra dependencies needed

---

## 💡 RECOMMENDATION

### ❌ UNINSTALL (Save ~60 MB):
**WeasyPrint + Dependencies:**
- weasyprint
- pycairo
- PyGObject  
- cairocffi
- cffi
- pycparser
- tinycss2
- cssselect2
- Pyphen

**Why?** 
- Doesn't work on Windows without GTK
- Takes up space
- Not used by current system

### ✅ KEEP (Useful for future):
**jinja2** (~2.7 MB)
- Templating engine
- Useful for future features
- Many projects use it

**plotly** (~12 MB)
- Interactive charts
- May add charts to PDFs later
- Industry standard

---

## 🚀 HOW TO UNINSTALL

### Option 1: One-Click Uninstall (Recommended)
```
Double-click: UNINSTALL_WEASYPRINT.bat
```

This will:
- ✅ Remove WeasyPrint
- ✅ Remove its dependencies
- ✅ Keep jinja2 and plotly
- ✅ Show confirmation

### Option 2: Manual Command
```cmd
pip uninstall weasyprint pycairo PyGObject cairocffi cffi tinycss2 cssselect2 Pyphen -y
```

### Option 3: Uninstall Everything (If you want)
```cmd
pip uninstall weasyprint jinja2 plotly -y
```

---

## 📊 DISK SPACE SAVINGS

If you uninstall WeasyPrint + dependencies:
- **Save:** ~60 MB
- **Keep:** jinja2 (2.7 MB) + plotly (12 MB) = ~15 MB
- **Total saved:** ~45 MB net

If you uninstall everything:
- **Save:** ~75 MB total
- But you'll need to reinstall jinja2/plotly if needed later

---

## ✅ WHAT YOUR SYSTEM NEEDS NOW

### Currently Required:
- ✅ **reportlab** - Already installed
- ✅ **pandas** - Already installed  
- ✅ **streamlit** - Already installed
- ✅ **sqlite3** - Built into Python

### NOT Required Anymore:
- ❌ weasyprint
- ❌ GTK libraries
- ❌ cairo/pango

---

## 🎯 MY RECOMMENDATION

**Best approach:**

1. **Uninstall WeasyPrint** (doesn't work anyway)
   ```
   Double-click: UNINSTALL_WEASYPRINT.bat
   ```

2. **Keep jinja2 and plotly** (small, useful for future)
   - You might add charts to PDFs later
   - jinja2 is useful for many projects

3. **Result:**
   - Save ~60 MB
   - Keep useful tools
   - Clean system

---

## 🔍 CHECK WHAT'S INSTALLED

To see what you currently have:
```cmd
pip list | findstr "weasyprint jinja2 plotly"
```

---

## ⚠️ IMPORTANT NOTES

1. **Your PDF system works without any of these!**
   - ReportLab handles everything
   - No dependencies needed

2. **Safe to uninstall**
   - Won't break your maintenance app
   - Won't affect other projects

3. **Can reinstall anytime**
   ```
   pip install jinja2 plotly
   ```

---

## 🎉 SUMMARY

| Package | Size | Status | Recommendation |
|---------|------|--------|----------------|
| weasyprint | ~50 MB | ❌ Doesn't work | **UNINSTALL** |
| Dependencies | ~10 MB | ❌ Not needed | **UNINSTALL** |
| jinja2 | ~2.7 MB | ✅ Useful | **KEEP** |
| plotly | ~12 MB | ✅ Useful | **KEEP** |

**Action:** Run `UNINSTALL_WEASYPRINT.bat`

---

## 📝 FILES CREATED

- ✅ `UNINSTALL_WEASYPRINT.bat` - One-click uninstaller
- ✅ `UNINSTALL_GUIDE.md` - This guide

**Ready to clean up!** 🧹
