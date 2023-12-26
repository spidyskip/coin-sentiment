from flask import Flask, render_template
import pandas as pd
import coingecko
from reddit_api.api import RedditApi
import yake

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Replace this function with your actual data retrieval logic
def get_crypto_data():
    # Get trending coins
    df = coingecko.price.get_trending()
    return df

def get_comments():
    trending_coins = get_crypto_data()[['name', 'price_usd']]
    trending_coins['name'] = trending_coins['name'].str.lower()
    # Get trending coins
    api = RedditApi("/home/antonio/Projects/coin-sentiment/config/credentials/keys.json")
    comments = pd.DataFrame()
    for _ in trending_coins['name']:
        try:
            df = api.get_sub_comments(_, 1)
            df['price_usd'] = trending_coins[trending_coins['name'] == _]['price_usd'].values[0]
            kw_extractor = yake.KeywordExtractor()
            reddit_and_scores = df["Content"].apply(kw_extractor.extract_keywords)
            scores = reddit_and_scores.apply(lambda x: [i[1] for i in x])
            keywords = reddit_and_scores.apply(lambda x: [i[0] for i in x])
            df["Scores"] = scores
            df["Keywords"] = keywords
            comments = comments.append(df, ignore_index=True)
        except:
            pass
    return comments

@app.route('/')
def index():
    # Get DataFrame
    df = get_crypto_data()
    comments = get_comments()

    # Convert DataFrame to HTML
    df_html = df.to_html(classes='table table-striped', index=False)

    # Render the template with the DataFrame HTML
    return render_template('index.html', df=df, df_html=df_html, comments=comments)

if __name__ == '__main__':
    app.run(debug=True)
