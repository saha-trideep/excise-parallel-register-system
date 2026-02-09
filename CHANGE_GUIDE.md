# Change Guide: How to Modify the Existing Project

This guide explains **where to make changes** in the current codebase and how the pieces fit together. It’s designed to help you (or any developer) quickly implement new requirements without re‑learning the whole project.

---

## 1) Start With the Requirement
Before editing code, write the change in a single sentence:
> “I want to change X in register Y and have it appear in Z (UI, Excel, handbook).”

This helps identify exactly which files you need to touch.

---

## 1.1) Storage Architecture (Important!)

The system uses a **3-tier storage strategy**:

1. **PRIMARY**: Desktop Excel files  
   - Location: `C:\Users\Lenovo\Desktop\Excise_Register_Data\`
   - Files: `Reg76_Data.xlsx`, `Reg74_Data.xlsx`, `RegA_Data.xlsx`, `RegB_Data.xlsx`, `Reg78_Data.xlsx`, `Excise_Duty_Data.xlsx`
   - Purpose: Main operational storage for manual presentation to officers

2. **BACKUP**: CSV files in `backup_data/` folder  
   - Location: `backup_data/` (git-ignored)
   - Files: `reg76_data.csv`, `reg74_data.csv`, `rega_data.csv`, `reg78_data.csv`
   - Purpose: Disaster recovery, portable backups

3. **SYNC**: Google Sheets (optional)  
   - Purpose: Cloud backup and remote access

**Export Script** (`export_register_format.py`) reads from **CSV backups** to populate the official `Register Format.xlsx` template.

---

## 2) Common Change Scenarios (and Where to Edit)

### ✅ Add a new field to a register
You usually need to update **three** layers:

1) **Schema** (data definition)
- `reg76_schema.py`, `reg74_schema.py`, `rega_schema.py`, `regb_schema.py`, `excise_duty_schema.py`

2) **UI form** (Streamlit input)
- `reg76.py`, `reg74.py`, `rega.py`, `regb.py`, `excise_duty_register.py`
- Or `pages/` if the register lives in a page module

3) **Storage / backend** (save + read)
- `reg76_backend.py`, `reg74_backend.py`, `rega_backend.py`, `regb_backend.py`, `excise_duty_backend.py`

If the field must appear in **Register Format.xlsx**, also update:
- `export_register_format.py`

---

### ✅ Change how Reg‑78 is generated
Reg‑78 is auto‑generated from upstream registers. The generation logic lives in:
- `export_register_format.py`
- `reg78_backend.py`

When you change Reg‑78 logic, confirm it still reads from **Reg‑76 + Reg‑74 + Reg‑A**.

---

### ✅ Change the Excel export layout
The export logic is centralized in:
- `export_register_format.py`

Before editing, open:
- `Register Format.xlsx` (template)
- `REGISTER_FORMAT_MAPPING.md` (mapping guide)

Update the mapping, then update the export write logic for the specific sheet.

---

### ✅ Change the Daily Handbook output
The handbook uses data from multiple registers and is generated in:
- `handbook_generator.py`
- `handbook_generator_v2.py`

If you add a new field, ensure it is fetched and rendered into the PDF sections.

---

## 3) Recommended Change Workflow (Safe + Predictable)

1) **Confirm the requirement** (exact column name, unit, or Excel location).
2) **Update schema** (add field + validation).
3) **Update UI form** (input field + help text).
4) **Update backend save logic** (write to CSV/DB/Excel).
5) **Update export to template** (if needed).
6) **Run a manual test** for the register you changed.

---

## 3.1) Export the Official Workbook (Quick Command)

Run the export tool after changing data mappings or register fields:

```bash
python export_register_format.py
```

Optional: set a custom output or template path:

```bash
python export_register_format.py --output "C:\\path\\to\\Register Format.xlsx" --template "Register Format.xlsx"
```

---

## 3.2) Push Changes to Your Repository (Git Workflow)

After you update code or documentation, use this quick sequence to push changes to your remote repository:

```bash
git status
git add <files>
git commit -m "Your commit message"
git push origin <branch-name>
```

If you are using a fork, replace `origin` with your fork’s remote name. If you don’t know the branch name, run:

```bash
git branch --show-current
```

---

## 4) Example: Add a “Permit Expiry Date” to Reg‑76

1) Add a field in `reg76_schema.py`.
2) Add a date input in `reg76.py`.
3) Save it in `reg76_backend.py`.
4) Add a column mapping in `REGISTER_FORMAT_MAPPING.md`.
5) Export to Excel in `export_register_format.py`.

---

## 5) How I Can Help You Directly

You can tell me any specific change in plain language, and I will:
- Locate the exact files to edit
- Implement the change
- Update the export mapping if needed
- Provide a commit and PR summary

**Example request:**
> “Add a new column to Reg‑74 for `Temperature at Transfer`, and export it into the official Excel sheet.”

---

## 6) Quick File Map (Most‑Edited Files)

- **UI Pages**: `reg76.py`, `reg74.py`, `rega.py`, `regb.py`, `excise_duty_register.py`, `pages/`
- **Schemas**: `*_schema.py`
- **Backends**: `*_backend.py`
- **Export**: `export_register_format.py`
- **Template Mapping**: `REGISTER_FORMAT_MAPPING.md`
- **Handbook**: `handbook_generator.py`

---

If you share the change you want, I’ll implement it and keep the template export aligned.
