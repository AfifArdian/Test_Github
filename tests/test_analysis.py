import pytest

from src.analysis import calculate_return, calculate_mean_return

def test_calculate_return():
    prices = [100, 110, 99]

    result = calculate_return(prices)

    assert result == pytest.approx([0.10, -0.10])

def test_calculate_mean_return():
    prices = [100, 105, 102, 110]

    renturn = calculate_return(prices)
    result = calculate_mean_return(renturn)

    assert result == pytest.approx(0.03, abs=0.01)


def test_zero_previous_price():
    with pytest.raises(ValueError):
        calculate_return([0, 100])