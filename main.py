import os
import pandas as pd
from src import data_loader, metrics, visual

TICKERS = {"BBRI": "BBRI.JK", "BMRI": "BMRI.JK"}

def main():
    data = {}
    for i, (nama, ticker) in enumerate(TICKERS.items()):
        df, _ = data_loader.ambil_data(nama, ticker, seed=i)
        data[nama] = metrics.hitung_return(df)

    stats = [metrics.hitung_statistik(df, nama) for nama, df in data.items()]
    metrics.cetak_statistik(stats)

    visual.buat_plot(data)

    # Simpan ringkasan ke CSV
    pd.DataFrame(stats).to_csv("output/ringkasan_statistik.csv", index=False)
    print("[OK] Ringkasan disimpan: ringkasan_statistik.csv")

if __name__ == "__main__":
    main()







