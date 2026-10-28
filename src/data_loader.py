import numpy as np
import pandas as pd

TICKERS = {"BBRI": "BBRI.JK", "BMRI": "BMRI.JK"}
START = "2020-01-01"

def download_data(ticker, start=START):
    """"Download Data harian dari Yahoo Finance, dan hanya mengambil kolom Close dalam type data DataFrame"""
    import yfinance as yf
    df = yf.download(ticker, start=start, progress=False, auto_adjust=True)

    if df is None or df.empty:
        raise ValueError(f"Data Kosong untuk {ticker}")

    # yfinance versi baru mengembalikan MultiIndex kolom -> ratakan
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    return df[["Close"]].dropna()


def generate_dummy(ticker, start=START, seed=0):
    """
    Fallback: buat data simulasi kalau internet tidak tersedia.
    Bukan data asli — hanya agar program tetap bisa dijalankan & diuji.
    """
    rng = np.random.default_rng(seed)
    tanggal = pd.bdate_range(start=start, end="2024-12-31")
    harga_awal = 4000 if "BBRI" in ticker else 6500
    # random walk dengan drift kecil
    ret = rng.normal(0.0004, 0.018, len(tanggal))
    harga = harga_awal * np.exp(np.cumsum(ret))
    return pd.DataFrame({"Close": harga}, index=tanggal)


def ambil_data(nama, ticker, seed):
    try:
        df = download_data(ticker)
        print(f"[OK]   {nama}: data asli dari yfinance ({len(df)} baris)")
        return df, True
    except Exception as e:
        print(f"[WARN] {nama}: gagal download ({type(e).__name__}). Pakai data simulasi.")
        return generate_dummy(ticker, seed=seed), False