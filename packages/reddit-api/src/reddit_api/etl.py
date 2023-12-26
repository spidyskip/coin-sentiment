import yake
from .api import RedditApi
from .decorator import save_decorator


@save_decorator
def extract(sub, limit, credentials_path, **kwargs):
    """
    Extract data from the Reddit API.

    Parameters:
    -----------
    sub: str
        Name of the subreddit to extract.
    limit: int (optional)
        Maximum number of posts to extract.
    credentials_path: str (required)
        Path to the credentials file.    
    """
    api = RedditApi(credentials_path)
    if kwargs.get("post_type") == "get_hot_posts":
        df = api.get_hot_posts(sub, limit)
    else:
        df = api.get_new_posts(sub, limit)
    return df


@save_decorator
def transform(df, **kwargs):
    df = df.astype(
        {"Title": "string", "ID": "string", "Author": "string", "URL": "string"}
    )

    df["post_type"] = kwargs["post_type"]

    kw_extractor = yake.KeywordExtractor()
    reddit_and_scores = df["Title"].apply(kw_extractor.extract_keywords)
    scores = reddit_and_scores.apply(lambda x: [i[1] for i in x])
    keywords = reddit_and_scores.apply(lambda x: [i[0] for i in x])
    df["Scores"] = scores
    df["Keywords"] = keywords

    return df

def extract_multiple_subreddits(**kwargs):
    if type(kwargs.get('sub')) == list:
        for _ in kwargs.get('sub'):    
            kwargs['sub'] = _
            extract(**kwargs)
    else:
        extract(**kwargs)


def load(df):
    # Load the data into a database
    return df


def etl(**kwargs):
    """Start the ETL process."""
    df = extract(**kwargs)
    df = transform(df, **kwargs)
    load(df)
    return df
