from coingecko.price import (
    get_price,
    get_price_hocl,
    get_coin_markets,
    get_trending,
)
from reddit_api.api import RedditApi

CREDENTIALS = "config/credentials/keys.json"

def main():
    sub = "solana"
    print(get_trending())
    
    api = RedditApi(CREDENTIALS)
    api.get_sub_comments(sub = "solana", limit = 10).to_csv(f"data/comments_posts_{sub}.csv")
    new_posts = api.get_new_posts(sub = "solana", limit=100)
    new_posts.to_csv(f"data/new_posts_{sub}.csv")
    for post in new_posts['ID'][:2]:
        api.get_comments(id_post = post, limit = 10).to_csv(f"data/comments_new_posts_{post}.csv")



if __name__ == "__main__":
    main()
