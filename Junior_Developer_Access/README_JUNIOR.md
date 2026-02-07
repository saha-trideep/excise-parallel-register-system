# Junior Developer Access - Table of Contents

**Project Location**: `c:\Users\Lenovo\.gemini\antigravity\playground\trideepexcise-parallel-register-system`

Welcome to the **Excise Parallel Register System** testing access folder. This folder contains all the key documents you need to understand, test, and verify the project.

## 📂 Included Documents

### 1. 🧪 [TESTING_GUIDE.md](TESTING_GUIDE.md)
*   **Purpose:** Your primary instruction manual for testing the application.
*   **Contents:** Step-by-step instructions on verifying columns, checking data flow, and validating file storage.
*   **Start Here!** This is your main task list.

### 2. 🔄 [HANDBOOK_DATA_FLOW.md](HANDBOOK_DATA_FLOW.md)
*   **Purpose:** Explains how the Daily Handbook PDF is generated automatically.
*   **Contents:** Detailed mapping of how data moves from Reg-76, Reg-74, Reg-A, and Excise Duty into the final PDF.

### 3. 📚 [HANDBOOK_GENERATOR.md](HANDBOOK_GENERATOR.md)
*   **Purpose:** Technical documentation for the PDF generation engine.
*   **Contents:** Detailed explanation of the `handbook_generator.py` script, including logic for manual vs. auto-filled sections.

### 4. 📋 [Register Format.xlsx](Register Format.xlsx)
*   **Purpose:** The **Source of Truth**.
*   **Contents:** The official physical register format. You must use this file to compare against the digital system and ensure every single column matches.

---

## 🚀 Quick Start
1.  Open `TESTING_GUIDE.md` and read the instructions carefully.
2.  Open `Register Format.xlsx` to see what the official registers look like.
3.  Launch the application using `streamlit run Home.py` (ask for access if you don't have it).
4.  Begin the **Phase 1: Column-by-Column Inspection**.
