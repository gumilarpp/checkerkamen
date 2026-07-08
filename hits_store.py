"""
Persistent hit storage — appends every valid hit to a JSON-Lines file.
Thread-safe; safe to call from asyncio via run_in_executor or directly.
"""
import json
import threading
from datetime import datetime, timezone, timedelta

JAKARTA_TZ = timezone(timedelta(hours=7))

from pathlib import Path

HITS_FILE = Path(__file__).parent / "hits.jsonl"

_lock = threading.Lock()


def save_hit(result: dict, raw: str) -> None:
    """Append one hit record to the hits file."""
    record = {
        "ts":           datetime.now(JAKARTA_TZ).strftime("%Y-%m-%d %H:%M:%S WIB"),
        "status":       result.get("status", "hit"),
        "email":        result.get("email") or "",
        "password":     result.get("password") or "",
        "plan":         result.get("plan_name") or "",
        "country":      result.get("country") or "",
        "quality":      result.get("quality") or "",
        "max_streams":  result.get("max_streams") or "",
        "price":        result.get("price") or "",
        "member_since": result.get("member_since") or "",
        "next_billing": result.get("next_billing") or "",
        "payment":      result.get("payment") or "",
        "card_type":    result.get("card_type") or "",
        "card_last4":   result.get("card_last4") or "",
        "netflix_id":   result.get("netflix_id") or "",
        "source":       result.get("_source") or "",
        "raw":          raw,
    }
    with _lock:
        with open(HITS_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_hits() -> list[dict]:
    """Return all saved hits as a list of dicts (newest first)."""
    if not HITS_FILE.exists():
        return []
    records = []
    with _lock:
        with open(HITS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
    return list(reversed(records))


def hits_count() -> int:
    """Return total number of saved hits without loading all data."""
    if not HITS_FILE.exists():
        return 0
    count = 0
    with _lock:
        with open(HITS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    count += 1
    return count


def clear_hits() -> int:
    """Delete all saved hits. Returns the number of records that were cleared."""
    count = hits_count()
    with _lock:
        if HITS_FILE.exists():
            HITS_FILE.unlink()
    return count


def export_txt() -> str:
    """
    Export all hits as a human-readable text file.
    Each hit is a block separated by a divider line.
    """
    records = load_hits()
    if not records:
        return "No hits saved yet.\n"

    lines = [f"Netflix Cookie Checker — Saved Hits ({len(records)} total)\n",
             "=" * 60 + "\n\n"]
    for i, r in enumerate(records, 1):
        lines.append(f"[{i}] {r['ts']}\n")
        lines.append(f"  Status    : {r['status'].upper()}\n")
        if r["email"]:
            lines.append(f"  Email     : {r['email']}\n")
        if r["password"]:
            lines.append(f"  Password  : {r['password']}\n")
        if r["plan"]:
            lines.append(f"  Plan      : {r['plan']}\n")
        if r["country"]:
            lines.append(f"  Country   : {r['country']}\n")
        if r["quality"]:
            lines.append(f"  Quality   : {r['quality']}\n")
        if r["max_streams"]:
            lines.append(f"  Streams   : {r['max_streams']}\n")
        if r["price"]:
            lines.append(f"  Price     : {r['price']}\n")
        if r["member_since"]:
            lines.append(f"  Member    : {r['member_since']}\n")
        if r["next_billing"]:
            lines.append(f"  Billing   : {r['next_billing']}\n")
        if r["card_type"] or r["card_last4"]:
            card = r["card_type"]
            if r["card_last4"]:
                card += f" ···· {r['card_last4']}"
            lines.append(f"  Card      : {card}\n")
        if r["netflix_id"]:
            lines.append(f"  Netflix ID: {r['netflix_id']}\n")
        lines.append("-" * 60 + "\n\n")
    return "".join(lines)
