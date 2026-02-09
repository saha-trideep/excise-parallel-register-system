# Troubleshooting: `desktop_storage.py` SyntaxError ("invalid decimal literal")

## Symptom
When starting the app, you see an error like:

```
SyntaxError: File "...\desktop_storage.py", line 2
  index 720187c39e30e222115c8cf3ddf9e7dc2d62ed3f..8daab635109c0309a9f126214540510d7964ef5b 100644
             ^
SyntaxError: invalid decimal literal
```

And then Reg‑78 fails to load because it imports `desktop_storage.py`.

---

## ✅ Root Cause
Git *diff headers* (such as `diff --git` and `index ...`) were accidentally pasted into `desktop_storage.py`. These lines are not valid Python, so the interpreter stops immediately.

---

## ✅ Fix (Recommended)
From the repo root, restore the clean file from git:

```bash
git checkout -- desktop_storage.py
```

This removes the invalid `index ...` diff line and restores the correct Python file.

---

## ✅ Fix (Manual Alternative)
Open `desktop_storage.py` and **delete any diff header lines**, including:

- `diff --git ...`
- `index ...`
- `---` / `+++`

The file must begin with normal imports, e.g.:

```python
import os
import pandas as pd
from datetime import datetime
from pathlib import Path
```

---

## ✅ After Fix
Re-run the app:

```bash
streamlit run Home.py
```

The Reg‑78 page should load normally because `desktop_storage.py` will import correctly.

---

## ✅ Prevention Tip
If you ever copy code from a git diff, **never paste the `diff --git` / `index` headers** into `.py` files.

---

If you want, we can add a small validation script to automatically detect diff headers inside `.py` files before app start.
