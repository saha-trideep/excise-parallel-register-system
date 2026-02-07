# 📨 DEVELOPER MESSAGE - Critical Fixes Required

## 3 Issues Found in Reg-76 → Handbook Flow

### 🚨 ISSUE #1: Missing Fields (Add to Reg-76)
- Weight of Empty Tanker
- Date of Dispatch  
- Indication field

### 🟡 ISSUE #2: BL at 20°C Must Be Manual Entry
Change from auto-calc to input field

### 🔴 ISSUE #3: CRITICAL - Handbook Shows Wrong Vat Data
**Problem**: When tanker unloads into SST-5, ALL vats show same value
**Fix**: Each vat row must show ONLY what it received (0 if none)

Example:
```
SST-5: Received = 28,725 AL (tanker went here)
SST-6: Received = 0 AL (nothing received)
SST-7: Received = 0 AL (nothing received)
```

**See BUG_REPORT_FOR_DEVELOPER.md for complete code fixes**
