from datetime import datetime

def high_value(amount, threshold=50000):
    try:
        return float(amount) > threshold
    except Exception:
        return False

def odd_hour(timestamp_str, start=0, end=5):
    try:
        h = datetime.fromisoformat(str(timestamp_str)).hour
        return start <= h < end
    except Exception:
        return False

def fast_upi_sequences(df, window_seconds=120):
    seq_ids = set()
    if df.empty:
        return []
    df_sorted = df.sort_values("Timestamp")
    for i in range(1, len(df_sorted)):
        try:
            t1 = datetime.fromisoformat(str(df_sorted.iloc[i-1]["Timestamp"]))
            t2 = datetime.fromisoformat(str(df_sorted.iloc[i]["Timestamp"]))
            if (t2 - t1).total_seconds() < window_seconds:
                seq_ids.add(df_sorted.iloc[i-1]["TransactionID"])
                seq_ids.add(df_sorted.iloc[i]["TransactionID"])
        except Exception:
            continue
    return list(seq_ids)
