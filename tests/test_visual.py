import pandas as pd
import matplotlib.pyplot as plt

from src.visual import buat_plot


def test_buat_plot_menyimpan_gambar(tmp_path):
    # Arrange: siapkan data buatan
    tanggal = pd.to_datetime([
        "2024-01-01",
        "2024-01-02",
        "2024-01-03",
    ])

    data = {
        "BBRI": pd.DataFrame(
            {
                "Close": [100, 110, 105],
                "cum_return": [0.00, 0.10, 0.05],
            },
            index=tanggal,
        ),
        "BMRI": pd.DataFrame(
            {
                "Close": [200, 210, 220],
                "cum_return": [0.00, 0.05, 0.10],
            },
            index=tanggal,
        ),
        
    }


    # Simpan gambar di folder sementara milik pytest
    outfile = tmp_path / "hasil_grafik.png"


    # Act: Jalankan function yang diuji
    buat_plot(data, outfile=str(outfile))


    # Assert: pastikan file gambar berhasil dibuat
    assert outfile.exists()
    assert outfile.stat().st_size > 0


    # Bersihkan figure Matplotlib yang masih terbuka
    plt.close("all")


def test_buat_plot_menghasilkan_dua_grafik(tmp_path):
    tanggal = pd.date_range("2024-01-01", periods=3)

    data = {
            "BBRI": pd.DataFrame(
                {
                    "Close": [100, 110, 105],
                    "cum_return": [0.00, 0.10, 0.05],
                },
                index=tanggal,
            ),
            "BMRI": pd.DataFrame(
                {
                    "Close": [200, 210, 220],
                    "cum_return": [0.00, 0.05, 0.10],
                },
                index=tanggal,
        ),    
    }


    outfile = tmp_path / "hasil_grafik.png"

    try:
        buat_plot(data, outfile=str(outfile))

        # Ambil figure yang baru saja dibuat
        fig = plt.gcf()
        axes = fig.axes

        # Harus ada dua area grafik
        assert len(axes) == 2

        
        # Periksa judul kedua grafik
        assert axes[0].get_title() == (
            "Perbandingan Harga Penutupan: BBRI vs BMRI"
        )
        assert axes[1].get_title() == (
            "Cumulative Return: BBRI vs BMRI"
        )


        # Setiap grafik memiliki dua garis data:
        # satu untuk BBRI dan satu untuk BMRI.
        assert len(axes[0].lines) == 2
        assert len(axes[1].lines) == 3 # 2 garis saham dan 1 garis nol

        assert outfile.exists()
        assert outfile.stat().st_size > 0
        
    finally:
        plt.close("all")