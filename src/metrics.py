import numpy as np

TRADING_DAYS = 252             # jumlah hari bursa dalam setahun
RISK_FREE_ANNUAL = 0.06        # asumsi risk-free rate Indonesia ~6% per tahun


# Hitung return harian
def hitung_return(df):
    df = df.copy()
    df["return"] = df["Close"].pct_change()
    df["cum_return"] = (1 + df["return"].fillna(0)).cumprod() - 1
    return df


# Statistik
def hitung_statistik(df, nama, risk_free=RISK_FREE_ANNUAL):
    r = df["return"].dropna()

    mean_harian = r.mean()
    std_harian = r.std()

    # Annualisasi
    mean_tahunan = mean_harian * TRADING_DAYS
    std_tahunan = std_harian * np.sqrt(TRADING_DAYS)

    # Sharpe ratio sederhana = (return tahunan - risk free) / volatilitas tahunan
    sharpe = (mean_tahunan - risk_free) / std_tahunan

    total_return = df["cum_return"].iloc[-1]

    return {
        "saham": nama,
        "mean_return_harian": mean_harian,
        "std_return_harian": std_harian,
        "mean_return_tahunan": mean_tahunan,
        "volatilitas_tahunan": std_tahunan,
        "sharpe_ratio": sharpe,
        "total_return": total_return,
        "jumlah_hari": len(r),
    }

def cetak_statistik(stats):
    print("\n" + "=" * 60)
    print("STATISTIK RETURN")
    print("=" * 60)
    for s in stats:
        print(f"\n{s['saham']}  ({s['jumlah_hari']} hari bursa)")
        print(f"  Mean return harian    : {s['mean_return_harian']*100:.4f}%")
        print(f"  Std dev harian        : {s['std_return_harian']*100:.4f}%")
        print(f"  Mean return tahunan   : {s['mean_return_tahunan']*100:.2f}%")
        print(f"  Volatilitas tahunan   : {s['volatilitas_tahunan']*100:.2f}%")
        print(f"  Sharpe ratio          : {s['sharpe_ratio']:.3f}")
        print(f"  Total return periode  : {s['total_return']*100:.2f}%")

    terbaik_sharpe = max(stats, key=lambda s: s["sharpe_ratio"])
    terbaik_return = max(stats, key=lambda s: s["total_return"])

    print("\n" + "-" * 60)
    print(f"Sharpe ratio tertinggi (risk-adjusted): {terbaik_sharpe['saham']} "
          f"({terbaik_sharpe['sharpe_ratio']:.3f})")
    print(f"Total return tertinggi (absolut)      : {terbaik_return['saham']} "
          f"({terbaik_return['total_return']*100:.2f}%)")
    print("-" * 60)







