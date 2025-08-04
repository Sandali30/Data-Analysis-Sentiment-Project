import pandas as pd  # For data manipulation
from textblob import TextBlob  # For sentiment analysis
from nltk.sentiment import SentimentIntensityAnalyzer  # For sentiment analysis using NLTK
import nltk

# Download NLTK's VADER lexicon (needed for SentimentIntensityAnalyzer)
nltk.download('vader_lexicon')

# Step 1: Load the Dataset
# Load the dataset created earlier
df = pd.read_csv('Dataset.csv')

# Step 2: Sentiment Analysis Using TextBlob
# Define a function to calculate sentiment polarity and subjectivity
def analyze_sentiment_textblob(review):
    analysis = TextBlob(review)
    return analysis.sentiment.polarity, analysis.sentiment.subjectivity

# Apply the function to the Review column
df['TextBlob_Polarity'], df['TextBlob_Subjectivity'] = zip(*df['Review'].apply(analyze_sentiment_textblob))

# Step 3: Sentiment Analysis Using NLTK's SentimentIntensityAnalyzer
# Initialize SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

# Define a function to calculate sentiment scores using NLTK
def analyze_sentiment_nltk(review):
    sentiment = sia.polarity_scores(review)
    return sentiment['neg'], sentiment['neu'], sentiment['pos'], sentiment['compound']

# Apply the function to the Review column
df['NLTK_Negative'], df['NLTK_Neutral'], df['NLTK_Positive'], df['NLTK_Compound'] = zip(*df['Review'].apply(analyze_sentiment_nltk))

# Step 4: Classify Sentiments
# Define a function to classify sentiment based on compound score (NLTK)
def classify_sentiment(compound_score):
    if compound_score > 0.05:
        return 'Positive'
    elif compound_score < -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# Apply the classification function
df['Sentiment_Class'] = df['NLTK_Compound'].apply(classify_sentiment)

# Step 5: Save the Updated Dataset
# Save the dataset with sentiment analysis results
df.to_csv('Dataset_with_Sentiment.csv', index=False)

# Step 6: Display a Summary of Results
# Print sample data to verify
print(df[['Review', 'TextBlob_Polarity', 'TextBlob_Subjectivity',
          'NLTK_Negative', 'NLTK_Neutral', 'NLTK_Positive',
          'NLTK_Compound', 'Sentiment_Class']].head())
print("Sentiment analysis completed.")
