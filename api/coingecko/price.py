import requests
import click


def get_price(ids, vs_currencies):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": ids, "vs_currencies": vs_currencies}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        print(
            "The current price of {} is {} {}".format(
                ids, data[ids][vs_currencies], vs_currencies.upper()
            )
        )
        return data[ids][vs_currencies]
    else:
        print("Failed to retrieve data from the API")
        return None


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
