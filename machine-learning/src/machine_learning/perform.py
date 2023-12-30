import re
import pandas as pd
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import seaborn as sns
from reddit_api import RedditApi
import click
import numpy as np

plt.style.use('fivethirtyeight')

# Credentials path
credentials_path = "../config/credentials/keys.json"

def get_data(sub="bitcoin", limit=100, credentials_path=credentials_path):
    # Create an instance of the RedditApi class
    reddit_api = RedditApi(credentials_path)
    # Get hot posts from reddit
    hot_posts = reddit_api.get_hot_posts(sub=sub, limit=limit)
    return hot_posts

def clean_data(df):
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

     # Clean the data
    reddit_df = df[['Title', 'Score', 'Created', 'URL']].copy()

    # Cleaning the text
    reddit_df["Title"] = reddit_df["Title"].apply(cleanTxt)

    # Cleaning the text
    reddit_df["Title"] = reddit_df["Title"].apply(remove_emoji)

    return reddit_df

def analyze_data(reddit_df):

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

    reddit_df['Subjectivity'] = reddit_df['Title'].apply(getSubjectivity)
    reddit_df['Polarity'] = reddit_df['Title'].apply(getPolarity)

    # Group the range of Polarity into different categories
    reddit_df["Insight"] = reddit_df["Polarity"].apply(getInsight)

    return reddit_df

def get_sentiment_counts(reddit_df):
    ''' Returns the sentiment counts as a json string'''
    return reddit_df["Insight"].value_counts().to_json()

def get_wordcloud(reddit_df):
    ''' Returns the wordcloud as a json string'''
    wordcloud = generate_wordcloud(reddit_df['Title'])
    return wordcloud.words_

def generate_wordcloud(text_series):
    stopwords = STOPWORDS
    text = ' '.join([twts for twts in text_series])
    wordcloud = WordCloud(font_path=None, width = 1000, height=600,  
            max_words=200,  stopwords=stopwords, background_color='whitesmoke', max_font_size=None, font_step=1, mode='RGB', 
            collocations=True, colormap=None, normalize_plurals=True).generate(text)
    return wordcloud
    
def plot_wordcloud(wordcloud, save_path="images/wordcloud.png"):
    plt.figure( facecolor='k')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(save_path)

def plot_sentiment_bar(sentiment_series, save_path="images/sentiment.png"):
    plt.figure(figsize=(12, 10))
    plt.title("Sentiment Score")
    plt.xlabel("Sentiment")
    plt.ylabel("Scores")
    plt.xticks(rotation=0)
    plt.rcParams['font.size'] = 12
    
    # Use seaborn color palette
    colors = sns.color_palette("viridis", n_colors=len(sentiment_series.unique()))
    
    # Plotting with labels and custom colors
    bar_plot = sentiment_series.value_counts().plot(kind="bar", color=colors)
    for p in bar_plot.patches:
        bar_plot.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                          ha='center', va='center', xytext=(0, 10), textcoords='offset points')
    
    plt.tight_layout()
    plt.savefig(save_path)

def plot_sentiment_counts(sentiment_series, save_path="images/sentiment.png"):
    # Define colors for neutral, positive, and negative sentiments
    colors = ['gray', 'green', 'red']

    # Count the occurrences of each sentiment
    sentiment_counts = sentiment_series.value_counts()

    labels = sentiment_counts.index
    values = sentiment_counts.values

    # Append data and assign color
    labels = np.append(labels, "")
    values = np.append(values, sum(values))  # 50% blank

   # plot
    plt.figure(figsize=(8,6),dpi=100)

    wedges, labels=plt.pie(values, wedgeprops=dict(width=0.4,edgecolor='w'),labels=labels, colors=colors)
    
    # Adjust layout to make the pie chart more centered
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

    # Make the last wedge (blank) invisible to create a semicircle
    wedges[-1].set_visible(False)

    plt.savefig(save_path, bbox_inches='tight', pad_inches=0.1, )

def visualize_data(reddit_df, sub, folder="images"):

    # Plot the values count of sentiment
    plot_sentiment_bar(reddit_df["Insight"], save_path=f"{folder}/{sub}_sentiment.png")

    # Generate and display word cloud
    wordloud = generate_wordcloud(reddit_df['Title'])
    plot_wordcloud(wordloud, save_path=f"{folder}/{sub}_wordcloud.png")

def pipeline(reddit_df, sub,  directory = "images"):
    reddit_df_clean = clean_data(reddit_df)
    reddit_df_analyzed = analyze_data(reddit_df_clean)
    visualize_data(reddit_df_analyzed, sub=sub, folder=directory)

@click.command()
@click.option("--sub", default="bitcoin", help="The subreddit to analyze")
@click.option("--limit", default=100, help="The number of posts to analyze")
@click.option("--save", default = "images", help="Save the data to a csv file")
def main(sub, limit, save):
    reddit_df = get_data(sub=sub, limit=limit)
    pipeline(reddit_df,sub, directory=save)

if __name__ == "__main__":
    main()
