def calculate_return(prices):
    returns = []

    for i in range(1, len(prices)):
        previous_price = prices[i - 1]
        current_price = prices[i]

        if previous_price == 0:
            raise ValueError("Harga sebelumnya tidak boleh nol.")

        daily_return = (
            current_price - previous_price
        ) / previous_price

        returns.append(daily_return)

    return returns

def calculate_mean_return(prices):
    return sum(prices) / len(prices)