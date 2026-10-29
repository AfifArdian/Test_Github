import pandas as pd
import pytest

from src.metrics import hitung_return, hitung_statistik


def test_hitung_return():
    # Arrange: Siapkan data yang hasilnya sudah diketahui
    df = pd.DataFrame({
        "Close": [100, 110, 99]
    })


    # Act: Jalankan fungsi hitung return
    hasil = hitung_return(df)


    # Assert: Periksa hasilnya
    assert hasil["return"].iloc[1] == pytest.approx(0.10)
    assert hasil["return"].iloc[2] == pytest.approx(-0.10)
    assert hasil["cum_return"].iloc[2] == pytest.approx(-0.01)


def test_hitung_statistik():
    # Arrange
    df = pd.DataFrame({
        "Close": [100, 110, 99]
    })

    # Jalankan hitung_return terlebih dahulu
    df = hitung_return(df)

    # Act
    hasil = hitung_statistik(df, "SAHAM_UJI")


    # Assert
    assert hasil["saham"] == "SAHAM_UJI"
    assert hasil["jumlah_hari"] == 2
    assert hasil["total_return"] == pytest.approx(-0.01)
    assert hasil["mean_return_harian"] == pytest.approx(0.0)

    