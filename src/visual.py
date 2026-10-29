""" Visualiasi hasil menggunakan mathplotlib """

import matplotlib
matplotlib.use("Agg")          # supaya bisa jalan tanpa GUI / simpan ke file
import matplotlib.pyplot as plt
from pathlib import Path

def buat_plot(data, outfile="output/analisis_bbri_bmri.png"):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9))

    # -- Grafik 1: Perbandingan harga --
    for nama, df in data.items():
        ax1.plot(df.index, df["Close"], label=nama, linewidth=1.3)
    ax1.set_title("Perbandingan Harga Penutupan: BBRI vs BMRI")
    ax1.set_ylabel("Harga (Rp)")
    ax1.legend()
    ax1.grid(alpha=0.3)

    # -- Grafik 2: Cumulative return --
    for nama, df in data.items():
        ax2.plot(df.index, df["cum_return"] * 100, label=nama, linewidth=1.3)
    ax2.axhline(0, color="black", linewidth=0.8, linestyle="--")
    ax2.set_title("Cumulative Return: BBRI vs BMRI")
    ax2.set_ylabel("Cumulative Return (%)")
    ax2.set_xlabel("Tanggal")
    ax2.legend()
    ax2.grid(alpha=0.3)

    outfile = Path(outfile)
    outfile.parent.mkdir(parents=True, exist_ok=True)
    
    plt.tight_layout()
    plt.savefig(outfile, dpi=120)
    print(f"\n[OK] Grafik disimpan: {outfile}")