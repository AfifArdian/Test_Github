from src.analysis import calculate_return
from src.analysis import calculate_mean_return


def main():
    prices = [100, 105, 102, 110]

    returns = calculate_return(prices)
    mean_returns = calculate_mean_return(returns)

    print("Hasil analisis return saham:")

    for idx, value in enumerate(returns, start=1):
        print(f"Hari {idx}: {value:.2%}")

    print(f"Rata-rata retunr: {mean_returns:.2%}")

if __name__ == "__main__":
    main()