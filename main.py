from api.coingecko.price import get_price


def main():
    get_price(ids="solana", vs_currencies="eur")


if __name__ == "__main__":
    main()
