import re
import pandas as pd
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from reddit_api import RedditApi

plt.style.use('fivethirtyeight')

# Credentials path
credentials_path = "../config/credentials/keys.json"

# Create an instance of the RedditApi class
reddit_api = RedditApi(credentials_path)
subreddit = "solana"

def get_data(sub="bitcoin", limit=100):
    # Get hot posts from r/bitcoin
    hot_posts = reddit_api.get_hot_posts(sub=sub, limit=limit)
    return hot_posts

def clean_data():
    #Create a function to clean the tweets
    def cleanTxt(text):
        text = re.sub(r'@[A-Za-z0–9]+', '', text) #Remove @mentions replace with blank
        text = re.sub(r'#', '', text) #Remove the '#' symbol, replace with blank
        text = re.sub(r'RT[\s]+', '', text) #Removing RT, replace with blank
        text = re.sub(r'https?:\/\/\S+', '', text) #Remove the hyperlinks
        text = re.sub(r':', '', text) # Remove :
        return text
    
    #Next we have to remove emoji & Unicode from the Tweet data.
    def remove_emoji(string):
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F" # emoticons
            u"\U0001F300-\U0001F5FF" # symbols & pictographs
            u"\U0001F680-\U0001F6FF" # transport & map symbols
            u"\U0001F1E0-\U0001F1FF" # flags (iOS)
            u"\U00002500-\U00002BEF" # chinese char
            u"\U00002702-\U000027B0"
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            u"\U0001f926-\U0001f937"
            u"\U00010000-\U0010ffff"
            u"\u2640-\u2642"
            u"\u2600-\u2B55"
            u"\u200d"
            u"\u23cf"
            u"\u23e9"
            u"\u231a"
            u"\ufe0f" # dingbats
            u"\u3030"
            "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', string)
    
    def getSubjectivity(text):
            return TextBlob(text).sentiment.subjectivity
        #Create a function to get Polarity
    def getPolarity(text):
        return TextBlob(text).sentiment.polarity
    
    def getInsight(score):
        if score < 0:
            return "Negative"
        elif score == 0:
            return "Neutral"
        else:
            return "Positive"

     # Clean the data
    df = get_data(subreddit)
    reddit_df = df[['Title', 'Score', 'Created', 'URL']].copy()

    # Cleaning the text
    reddit_df["Title"] = reddit_df["Title"].apply(cleanTxt)

    # Cleaning the text
    reddit_df["Title"] = reddit_df["Title"].apply(remove_emoji)

    reddit_df['Subjectivity'] = reddit_df['Title'].apply(getSubjectivity)
    reddit_df['Polarity'] = reddit_df['Title'].apply(getPolarity)

    # Group the range of Polarity into different categories
    reddit_df["Insight"] = reddit_df["Polarity"].apply(getInsight)

    reddit_df.head(10)

    # Plot the values count of sentiment
    plot_sentiment_counts(reddit_df["Insight"])

    # Generate and display word cloud
    generate_word_cloud(reddit_df['Title'])

def plot_sentiment_counts(sentiment_series):
    plt.title("Crypto Sentiment Score")
    plt.xlabel("Sentiment")
    plt.ylabel("Scores")
    plt.rcParams["figure.figsize"] = (12, 10)
    plt.rcParams['font.size'] = 12
    sentiment_series.value_counts().plot(kind="bar", color="#2078B4")
    plt.savefig("images/sentiment.png")

def generate_word_cloud(text_series):
    stopwords = STOPWORDS
    text = ' '.join([twts for twts in text_series])
    wordcloud = WordCloud(width=1000, height=600, max_words=100, stopwords=stopwords, background_color="black").generate(text)
    
    # Display the generated image:
    plt.figure(figsize=(20, 10), facecolor='k')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig("images/wordcloud.png")

if __name__ == "__main__":
    clean_data()
