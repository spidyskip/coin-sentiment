from packages.coingecko.price import (
    get_price,
    get_price_hocl,
    get_coin_markets,
    get_trending,
)


def main():
    get_price(ids="solana", vs_currencies="usd")
    print(get_price_hocl(ids="solana", vs_currencies="usd", days="1"))
    print(
        get_coin_markets(
            vs_currency="usd",
            order="market_cap_desc",
            per_page="10",
            page="1",
            sparkline="false",
            price_change_percentage="1h,24h,7d",
        )
    )
    print(get_trending())


if __name__ == "__main__":
    main()
