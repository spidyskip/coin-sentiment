from flask import Flask, render_template, send_file, request
import pandas as pd
import coingecko
from reddit_api.api import RedditApi
from machine_learning.perform import *
import yake

CREDENTIALS_PATH = "../config/credentials/keys.json"

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
    api = RedditApi(CREDENTIALS_PATH)
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

@app.route('/get_sentiment', methods=['GET'])
def get_sentiment():
    input_text = request.args.get('input', '')
    api = RedditApi(CREDENTIALS_PATH)
    hot_posts = api.get_hot_posts(sub=input_text, limit=100)
    reddit_df_clean = clean_data(hot_posts)
    reddit_df_analyzed = analyze_data(reddit_df_clean)
    return reddit_df_analyzed["Insight"].value_counts().to_json()

@app.route('/generate_word_cloud', methods=['GET'])
def create_wordcloud():
    api = RedditApi(CREDENTIALS_PATH)
    input_text = request.args.get('input', '')
    sub = input_text
    hot_posts = api.get_hot_posts(sub=sub, limit=100)
    reddit_df_clean = clean_data(hot_posts)
    reddit_df_analyzed = analyze_data(reddit_df_clean)
    wordcloud_data = get_wordcloud(reddit_df_analyzed)
    wordcloud_image = generate_wordcloud(wordcloud_data)
    word_cloud_image_path = f"static/images/word_cloud.png"
    plot_wordcloud(wordcloud_image, save_path=word_cloud_image_path)
    
    # Use send_file to send the generated image file
    return send_file(word_cloud_image_path, mimetype='image/png')

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
