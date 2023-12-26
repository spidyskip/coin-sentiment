import pandas as pd
import click
from pycoingecko import CoinGeckoAPI


def get_price(ids, vs_currencies):
    cg = CoinGeckoAPI()
    data = cg.get_price(ids=ids, vs_currencies=vs_currencies)
    print(
        "@ The current price of {} is {} {}".format(
            ids, data[ids][vs_currencies], vs_currencies.upper()
        )
    )
    return data[ids][vs_currencies]


def get_price_hocl(ids, vs_currencies, days):
    def to_df(data):
        df = pd.DataFrame(data)
        df.columns = ["date", "open", "high", "low", "close"]
        df["date"] = pd.to_datetime(df["date"], unit="ms")
        df.set_index("date", inplace=True)
        return df

    cg = CoinGeckoAPI()
    ohlc = cg.get_coin_ohlc_by_id(id=ids, vs_currency=vs_currencies, days=days)
    return to_df(ohlc)


def get_coin_markets(
    vs_currency, order, per_page, page, sparkline, price_change_percentage
):
    def to_df(data):
        df = pd.DataFrame(data)
        df = df.drop(
            [
                "id",
                "symbol",
                "image",
                "high_24h",
                "low_24h",
                "price_change_24h",
                "price_change_percentage_24h",
                "market_cap_change_24h",
                "market_cap_change_percentage_24h",
                "fully_diluted_valuation",
                "ath_date",
                "ath_change_percentage",
                "atl_change_percentage",
                "atl_date",
                "roi",
            ],
            axis=1,
        )
        return df

    cg = CoinGeckoAPI()
    data = cg.get_coins_markets(
        vs_currency=vs_currency,
        order=order,
        per_page=per_page,
        page=page,
        sparkline=sparkline,
        price_change_percentage=price_change_percentage,
    )
    return to_df(data)


def get_trending():
    def to_df(data):
        # Extract relevant fields from the JSON data (coins section)
        coin_data = []
        for coin in data.get("coins", []):
            coin_item = coin.get("item", {})
            coin_data.append(
                {
                    "id": coin_item.get("id", ""),
                    "name": coin_item.get("name", ""),
                    "symbol": coin_item.get("symbol", ""),
                    "market_cap_rank": coin_item.get("market_cap_rank", 0),
                    "score": coin_item.get("score", 0),
                }
            )
        # Create a DataFrame from the extracted data
        df = pd.DataFrame(coin_data)
        return df

    cg = CoinGeckoAPI()
    data = cg.get_search_trending()
    return to_df(data)


# def get_price(ids, vs_currencies):
#    url = "https://api.coingecko.com/api/v3/simple/price"
#    params = {"ids": ids, "vs_currencies": vs_currencies}
#    response = requests.get(url, params=params)
#    if response.status_code == 200:
#        data = response.json()
#        print(
#            "The current price of {} is {} {}".format(
#                ids, data[ids][vs_currencies], vs_currencies.upper()
#            )
#        )
#        return data[ids][vs_currencies]
#    else:
#        print("Failed to retrieve data from the API")
#        return None


def cli():
    """A simple CLI for getting the current price of a cryptocurrency"""
    get_price_cli()


@click.command()
@click.option("--ids", default="bitcoin", help="The coin id")
@click.option("--vs_currencies", default="usd", help="The currency")
def get_price_cli(ids, vs_currencies):
    get_price(ids, vs_currencies)


if __name__ == "__main__":
    cli()
