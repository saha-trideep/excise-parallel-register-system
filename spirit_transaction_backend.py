import os
import sqlite3
from datetime import datetime, date
from typing import Dict, Optional

import pandas as pd
import streamlit as st

import desktop_storage
from reg78_schema import SST_VATS, BRT_VATS
from spirit_transaction_schema import (
    SPIRIT_TRANSACTION_COLUMNS,
    DEFAULT_RECON_TOLERANCE_AL,
)
from spirit_transaction_sqlite_schema import (
    CREATE_SPIRIT_TRANSACTION_TABLE,
    CREATE_SPIRIT_TRANSACTION_INDEXES,
)

CSV_PATH = "backup_data/spirit_transaction_data.csv"
DB_PATH = "excise_registers.db"


def _ensure_backup_dir():
    backup_dir = os.path.dirname(CSV_PATH)
    if backup_dir:
        os.makedirs(backup_dir, exist_ok=True)


def _as_date(value) -> Optional[date]:
    if value is None:
        return None
    if isinstance(value, date):
        return value
    try:
        return pd.to_datetime(value).date()
    except Exception:
        return None


def _as_date_str(value) -> Optional[str]:
    value_date = _as_date(value)
    return value_date.isoformat() if value_date else None


def init_sqlite_db():
    """Initialize SQLite database and tables if they don't exist"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.executescript(CREATE_SPIRIT_TRANSACTION_TABLE)
        cursor.executescript(CREATE_SPIRIT_TRANSACTION_INDEXES)
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"SQLite initialization error: {e}")


def get_data_from_sqlite() -> pd.DataFrame:
    """Load data from SQLite database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(
            "SELECT * FROM spirit_transaction_daily ORDER BY txn_date DESC", conn
        )
        conn.close()
        return df
    except Exception as e:
        st.warning(f"SQLite read error: {e}")
        return pd.DataFrame(columns=SPIRIT_TRANSACTION_COLUMNS)


def save_to_sqlite(data_dict: Dict) -> bool:
    """Save record to SQLite database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        columns = list(data_dict.keys())
        placeholders = ", ".join(["?" for _ in columns])
        column_names = ", ".join(columns)
        values = [data_dict[col] for col in columns]

        query = (
            f"INSERT OR REPLACE INTO spirit_transaction_daily "
            f"({column_names}) VALUES ({placeholders})"
        )
        cursor.execute(query, values)

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"SQLite save error: {e}")
        return False


def get_data_local() -> pd.DataFrame:
    """Load local CSV fallback"""
    if os.path.exists(CSV_PATH):
        try:
            return pd.read_csv(CSV_PATH)
        except Exception:
            return pd.DataFrame(columns=SPIRIT_TRANSACTION_COLUMNS)
    return pd.DataFrame(columns=SPIRIT_TRANSACTION_COLUMNS)


def get_data() -> pd.DataFrame:
    """Load data - prioritized from SQLite database"""
    init_sqlite_db()
    return get_data_from_sqlite()


def _safe_sum(series: pd.Series) -> float:
    if series is None:
        return 0.0
    return float(series.fillna(0).sum())


def _load_reg76_daily(conn: sqlite3.Connection, target_date: str) -> Dict[str, float]:
    reg76_df = pd.read_sql_query(
        "SELECT * FROM reg76_receipts WHERE date_receipt = ?",
        conn,
        params=(target_date,),
    )
    if reg76_df.empty:
        return {
            "received_al": 0.0,
            "transit_increase_al": 0.0,
            "transit_wastage_al": 0.0,
        }

    received_al = 0.0
    if "rec_al" in reg76_df.columns:
        received_al = _safe_sum(reg76_df["rec_al"])
    if received_al == 0.0 and "adv_al" in reg76_df.columns:
        received_al = _safe_sum(reg76_df["adv_al"])

    if "transit_increase_al" in reg76_df.columns and "transit_wastage_al" in reg76_df.columns:
        transit_increase = _safe_sum(reg76_df["transit_increase_al"])
        transit_wastage = _safe_sum(reg76_df["transit_wastage_al"])
    else:
        adv = reg76_df.get("adv_al", pd.Series(dtype=float)).fillna(0)
        rec = reg76_df.get("rec_al", pd.Series(dtype=float)).fillna(0)
        diff = rec - adv
        transit_increase = float(diff[diff > 0].sum())
        transit_wastage = float((-diff[diff < 0]).sum())

    return {
        "received_al": float(received_al),
        "transit_increase_al": float(transit_increase),
        "transit_wastage_al": float(transit_wastage),
    }


def _load_rega_daily(conn: sqlite3.Connection, target_date: str) -> Dict[str, float]:
    rega_df = pd.read_sql_query(
        "SELECT * FROM rega_production WHERE production_date = ?",
        conn,
        params=(target_date,),
    )
    if rega_df.empty:
        return {
            "mfm2_al": 0.0,
            "production_increase": 0.0,
            "production_wastage": 0.0,
            "total_bottles": 0,
            "total_cases": 0,
            "bottled_al": 0.0,
            "allowable_wastage": 0.0,
        }

    mfm2_al = _safe_sum(rega_df.get("mfm2_reading_al"))
    bottled_al = _safe_sum(rega_df.get("bottles_total_al"))
    if mfm2_al == 0.0:
        mfm2_al = bottled_al

    production_increase = _safe_sum(rega_df.get("production_increase_al"))
    production_wastage = _safe_sum(rega_df.get("wastage_al"))
    total_bottles = int(_safe_sum(rega_df.get("total_bottles")))
    total_cases = int(_safe_sum(rega_df.get("total_cases")))

    allowable_wastage = 0.0
    if "allowable_limit" in rega_df.columns:
        limits = rega_df["allowable_limit"].fillna(0)
        if limits.sum() > 0:
            if limits.max() <= 1.0:
                allowable_wastage = float(mfm2_al * (limits.mean() / 100.0))
            else:
                allowable_wastage = float(limits.sum())
    if allowable_wastage == 0.0:
        allowable_wastage = float(mfm2_al * 0.001)

    return {
        "mfm2_al": float(mfm2_al),
        "production_increase": float(production_increase),
        "production_wastage": float(production_wastage),
        "total_bottles": total_bottles,
        "total_cases": total_cases,
        "bottled_al": float(bottled_al),
        "allowable_wastage": float(allowable_wastage),
    }


def _load_reg78_sample(conn: sqlite3.Connection, target_date: str) -> float:
    try:
        reg78_df = pd.read_sql_query(
            "SELECT sample_drawn_al FROM reg78_synopsis WHERE synopsis_date = ?",
            conn,
            params=(target_date,),
        )
        if reg78_df.empty:
            return 0.0
        return float(reg78_df.iloc[-1].get("sample_drawn_al") or 0.0)
    except Exception:
        return 0.0


def _get_latest_vat_balance(reg74_df: pd.DataFrame, vat: str, target_date: date) -> float:
    if reg74_df.empty:
        return 0.0
    df = reg74_df.copy()
    df["operation_date_dt"] = pd.to_datetime(df["operation_date"]).dt.date
    df = df[
        (df["operation_date_dt"] <= target_date)
        & ((df["source_vat"] == vat) | (df["destination_vat"] == vat))
    ]
    if df.empty:
        return 0.0
    df = df.sort_values("operation_date_dt")
    latest = df.iloc[-1]
    return float(latest.get("closing_al") or 0.0)


def _get_opening_vat_balance(reg74_df: pd.DataFrame, vat: str, target_date: date) -> float:
    if reg74_df.empty:
        return 0.0
    df = reg74_df.copy()
    df["operation_date_dt"] = pd.to_datetime(df["operation_date"]).dt.date
    df = df[
        (df["operation_date_dt"] < target_date)
        & ((df["source_vat"] == vat) | (df["destination_vat"] == vat))
    ]
    if df.empty:
        return 0.0
    df = df.sort_values("operation_date_dt")
    latest = df.iloc[-1]
    return float(latest.get("closing_al") or 0.0)


def _compute_vat_totals(reg74_df: pd.DataFrame, vats, target_date: date) -> Dict[str, float]:
    opening_total = 0.0
    closing_total = 0.0
    for vat in vats:
        opening_total += _get_opening_vat_balance(reg74_df, vat, target_date)
        closing_total += _get_latest_vat_balance(reg74_df, vat, target_date)
    return {"opening": float(opening_total), "closing": float(closing_total)}


def compute_spirit_transaction_row(target_date) -> Dict[str, float]:
    target_date_obj = _as_date(target_date)
    if not target_date_obj:
        raise ValueError("Invalid target_date supplied to compute_spirit_transaction_row")
    target_date_str = target_date_obj.isoformat()

    conn = sqlite3.connect(DB_PATH)

    reg74_df = pd.read_sql_query("SELECT * FROM reg74_operations", conn)
    reg76_summary = _load_reg76_daily(conn, target_date_str)
    rega_summary = _load_rega_daily(conn, target_date_str)
    sample_drawn = _load_reg78_sample(conn, target_date_str)

    conn.close()

    vat_totals_sst = _compute_vat_totals(reg74_df, SST_VATS, target_date_obj)
    vat_totals_brt = _compute_vat_totals(reg74_df, BRT_VATS, target_date_obj)

    reg74_day = reg74_df.copy()
    if not reg74_day.empty:
        reg74_day["operation_date_dt"] = pd.to_datetime(reg74_day["operation_date"]).dt.date
        reg74_day = reg74_day[reg74_day["operation_date_dt"] == target_date_obj]

    transfer_mask = (
        (reg74_day.get("source_vat", pd.Series()).isin(SST_VATS))
        & (reg74_day.get("destination_vat", pd.Series()).isin(BRT_VATS))
    )
    transfer_al = _safe_sum(reg74_day.loc[transfer_mask, "issue_al"]) if not reg74_day.empty else 0.0

    strong_increase = 0.0
    blended_increase = 0.0
    blended_wastage = 0.0
    if not reg74_day.empty and "storage_wastage_al" in reg74_day.columns:
        strong_rows = reg74_day[reg74_day["source_vat"].isin(SST_VATS)]
        blended_rows = reg74_day[reg74_day["source_vat"].isin(BRT_VATS)]
        strong_increase = float((-strong_rows["storage_wastage_al"]).clip(lower=0).sum())
        blended_increase = float((-blended_rows["storage_wastage_al"]).clip(lower=0).sum())
        blended_wastage = float(blended_rows["storage_wastage_al"].clip(lower=0).sum())

    credits = (
        vat_totals_sst["opening"]
        + reg76_summary["received_al"]
        + reg76_summary["transit_increase_al"]
        + strong_increase
        + vat_totals_brt["opening"]
        + transfer_al
        + blended_increase
        + rega_summary["production_increase"]
    )
    debits = (
        reg76_summary["transit_wastage_al"]
        + transfer_al
        + blended_wastage
        + sample_drawn
        + rega_summary["mfm2_al"]
        + rega_summary["production_wastage"]
    )
    expected_closing = credits - debits
    actual_closing = vat_totals_sst["closing"] + vat_totals_brt["closing"]
    net_difference = actual_closing - expected_closing

    actual_wastage = (
        reg76_summary["transit_wastage_al"]
        + blended_wastage
        + rega_summary["production_wastage"]
    )
    chargeable_excess = max(0.0, actual_wastage - rega_summary["allowable_wastage"])

    row = {
        "txn_date": target_date_str,
        "strong_spirit_opening_balance": vat_totals_sst["opening"],
        "strong_spirit_received_unloaded": reg76_summary["received_al"],
        "in_transit_unloading_increase": reg76_summary["transit_increase_al"],
        "in_transit_unloading_wastage": reg76_summary["transit_wastage_al"],
        "strong_spirit_transferred_to_blending": transfer_al,
        "operational_increase_strong_spirit": strong_increase,
        "strong_spirit_closing_balance": vat_totals_sst["closing"],
        "blended_spirit_opening_balance": vat_totals_brt["opening"],
        "blended_spirit_received_from_strong": transfer_al,
        "operational_increase_blended_spirit": blended_increase,
        "operational_wastage_blended_spirit": blended_wastage,
        "sample_drawn": sample_drawn,
        "spirit_passed_to_bottling": rega_summary["mfm2_al"],
        "blended_spirit_closing_balance": vat_totals_brt["closing"],
        "production_increase": rega_summary["production_increase"],
        "production_wastage": rega_summary["production_wastage"],
        "total_bottles_produced": rega_summary["total_bottles"],
        "total_cases_produced": rega_summary["total_cases"],
        "spirit_accounted_in_bottled_production": rega_summary["bottled_al"],
        "net_difference": net_difference,
        "total_allowable_wastage": rega_summary["allowable_wastage"],
        "chargeable_excess_wastage": chargeable_excess,
    }

    recon_status, recon_note = validate_reconciliation(row, target_date_obj)
    row["recon_status"] = recon_status
    row["recon_note"] = recon_note

    return row


def validate_reconciliation(row: Dict[str, float], target_date) -> (str, str):
    target_date_obj = _as_date(target_date)
    if not target_date_obj:
        return "warning", "Invalid date for reconciliation"

    conn = sqlite3.connect(DB_PATH)
    reg74_df = pd.read_sql_query("SELECT * FROM reg74_operations", conn)
    conn.close()

    vat_totals_sst = _compute_vat_totals(reg74_df, SST_VATS, target_date_obj)
    vat_totals_brt = _compute_vat_totals(reg74_df, BRT_VATS, target_date_obj)

    strong_diff = abs(row.get("strong_spirit_closing_balance", 0.0) - vat_totals_sst["closing"])
    blended_diff = abs(row.get("blended_spirit_closing_balance", 0.0) - vat_totals_brt["closing"])

    issues = []
    if strong_diff > DEFAULT_RECON_TOLERANCE_AL:
        issues.append(f"SST closing mismatch {strong_diff:.3f} AL")
    if blended_diff > DEFAULT_RECON_TOLERANCE_AL:
        issues.append(f"BRT closing mismatch {blended_diff:.3f} AL")

    if issues:
        return "warning", "; ".join(issues)
    return "ok", "Balances reconciled"


def save_record(data_dict: Dict) -> Optional[str]:
    """Save record to SQLite (primary), Desktop Excel, CSV (backup)"""
    txn_date = _as_date_str(data_dict.get("txn_date"))
    if not txn_date:
        st.error("Invalid txn_date for Spirit Transaction save")
        return None

    data_dict["txn_date"] = txn_date
    data_dict["created_at"] = data_dict.get("created_at") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_dict["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_dict["status"] = data_dict.get("status", "draft")

    if "recon_status" not in data_dict or "recon_note" not in data_dict:
        recon_status, recon_note = validate_reconciliation(data_dict, txn_date)
        data_dict["recon_status"] = recon_status
        data_dict["recon_note"] = recon_note

    init_sqlite_db()
    success_sqlite = save_to_sqlite(data_dict)
    if not success_sqlite:
        st.error("Failed to save Spirit Transaction to SQLite")
        return None

    try:
        success_excel, message_excel, _ = desktop_storage.add_spirit_transaction_record_to_excel(
            data_dict
        )
        if not success_excel:
            st.warning(f"Desktop Excel save failed: {message_excel}")
    except Exception as e:
        st.warning(f"Desktop Excel save failed: {e}")

    try:
        _ensure_backup_dir()
        df_local = get_data_local()
        df_local = df_local[df_local["txn_date"].astype(str) != txn_date] if not df_local.empty else df_local
        df_local = pd.concat([df_local, pd.DataFrame([data_dict])], ignore_index=True)
        df_local.to_csv(CSV_PATH, index=False)
    except Exception as e:
        st.warning(f"CSV backup failed: {e}")

    return txn_date


def refresh_for_date(target_date) -> Optional[str]:
    row = compute_spirit_transaction_row(target_date)
    return save_record(row)


def get_spirit_transaction(date_from=None, date_to=None) -> pd.DataFrame:
    df = get_data()
    if df is None or df.empty:
        return pd.DataFrame(columns=SPIRIT_TRANSACTION_COLUMNS)

    if "txn_date" in df.columns:
        df["txn_date_dt"] = pd.to_datetime(df["txn_date"]).dt.date
        if date_from:
            df = df[df["txn_date_dt"] >= date_from]
        if date_to:
            df = df[df["txn_date_dt"] <= date_to]
    return df
