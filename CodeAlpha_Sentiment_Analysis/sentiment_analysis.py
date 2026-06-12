import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk


nltk.download("vader_lexicon")


df = pd.read_csv("IMDB Dataset.csv")

print("Dataset Shape:", df.shape)
print(df.head())


sia = SentimentIntensityAnalyzer()


def predict_sentiment(review):
    score = sia.polarity_scores(str(review))

    compound = score["compound"]

    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"

df["Predicted_Sentiment"] = df["review"].apply(
    predict_sentiment
)


df.to_csv(
    "movie_sentiment_results.csv",
    index=False
)


counts = df["Predicted_Sentiment"].value_counts()

print("\nSentiment Counts:")
print(counts)


plt.figure(figsize=(8,5))

plt.bar(
    counts.index,
    counts.values
)

plt.title("Movie Review Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Number of Reviews")

plt.savefig("movie_sentiment_distribution.png")

plt.show()


plt.figure(figsize=(7,7))

plt.pie(
    counts.values,
    labels=counts.index,
    autopct="%1.1f%%"
)

plt.title("Movie Review Sentiment Breakdown")

plt.savefig("movie_sentiment_pie_chart.png")

plt.show()


positive_reviews = " ".join(
    df[
        df["Predicted_Sentiment"] == "Positive"
    ]["review"].astype(str)
)

if positive_reviews:

    wordcloud = WordCloud(
        width=1000,
        height=500,
        background_color="white"
    ).generate(positive_reviews)

    plt.figure(figsize=(12,6))
    plt.imshow(wordcloud)
    plt.axis("off")

    plt.title("Positive Movie Review Word Cloud")

    plt.savefig("positive_movie_wordcloud.png")

    plt.show()


negative_reviews = " ".join(
    df[
        df["Predicted_Sentiment"] == "Negative"
    ]["review"].astype(str)
)

if negative_reviews:

    wordcloud = WordCloud(
        width=1000,
        height=500,
        background_color="white"
    ).generate(negative_reviews)

    plt.figure(figsize=(12,6))
    plt.imshow(wordcloud)
    plt.axis("off")

    plt.title("Negative Movie Review Word Cloud")

    plt.savefig("negative_movie_wordcloud.png")

    plt.show()

print("\nAnalysis Completed Successfully!")