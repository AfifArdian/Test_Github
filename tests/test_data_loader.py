import pandas as pd
import pytest
from src import data_loader


def test_generate_dummy_returns_valid_dataframe():
    df = data_loader.generate_dummy(
        ticker="BBRI.JK",
        start="2024-12-27",
        seed=0
    )

    # 1. Hasilnya harus berupa DataFrame
    assert isinstance(df, pd.DataFrame)

    # 2. Harus ada kolom Close
    assert "Close" in df.columns

    # 3. Data tidak boleh kosong
    assert not df.empty

    # 4. Semua harga harus positif
    assert (df["Close"] > 0).all()


def test_generate_dummy_is_reproducible():
    df1 = data_loader.generate_dummy(
        ticker="BBRI.JK",
        start="2024-12-27",
        seed=42
    )

    df2 = data_loader.generate_dummy(
            ticker="BBRI.JK",
            start="2024-12-27",
            seed=42,
        )

    # Seed yang sama seharusnya dapat menghasilkan data yang sama
    pd.testing.assert_frame_equal(df1, df2)


def test_ambil_data_success(monkeypatch):
    data_asli = pd.DataFrame(
        {"Close": [100, 105, 110]},
        index=pd.to_datetime([
            "2024-01-01",
            "2024-01-02",
            "2024-01-03",
        ]),
    )

    # Simulasikan unduhan yang berhasil
    def fake_download(ticker, start=data_loader.START):
        return data_asli

    monkeypatch.setattr(
        data_loader,
        "download_data",
        fake_download,
    )

    df, is_real = data_loader.ambil_data(
        "BBRI",
        "BBRI.JK",
        seed=0,
    )

    pd.testing.assert_frame_equal(df, data_asli)
    assert is_real is True



def test_ambil_data_fallback(monkeypatch):
    data_simulasi = pd.DataFrame(
        {"Close": [100, 101, 102]},
        index=pd.date_range(
            "2024-01-01",
            periods=3
        ),
    )

    # Simulasi ketika gagal mendownload data
    def fake_download(ticker, start=data_loader.START):
        raise RuntimeError("Simulasi kegagalan unduhan")

    # Simulasi data dummy berhasil dibuat
    def fake_dummy(ticker, start=data_loader.START, seed=0):
        return data_simulasi

    monkeypatch.setattr(
        data_loader,
        "download_data",
        fake_download,
    )

    monkeypatch.setattr(
        data_loader,
        "generate_dummy",
        fake_dummy,
    )

    df, is_real = data_loader.ambil_data(
        "BBRI",
        "BBRI.JK",
        seed=0,
    )

    pd.testing.assert_frame_equal(df, data_simulasi)
    assert is_real is False