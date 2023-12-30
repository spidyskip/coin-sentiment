from coingecko.price import (
    get_price,
    get_price_hocl,
    get_coin_markets,
    get_trending,
)
from reddit_api.api import RedditApi
from machine_learning.perform import *

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

def main_ML():
    sub = "solana"
    api = RedditApi(CREDENTIALS)
    hot_posts = api.get_hot_posts(sub=sub, limit=100)
    reddit_df_clean = clean_data(hot_posts)
    reddit_df_analyzed = analyze_data(reddit_df_clean)
    wordcloud_data = get_wordcloud(reddit_df_analyzed)
    wordcloud_image = generate_wordcloud(wordcloud_data)
    word_cloud_image_path = f"data/word_cloud.png"
    plot_wordcloud(wordcloud_image, save_path=word_cloud_image_path)
    plot_sentiment_bar(reddit_df_analyzed["Insight"], save_path=f"data/sentiment.png")

if __name__ == "__main__":
    main_ML()
