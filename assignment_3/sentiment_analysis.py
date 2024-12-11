#%%
import pprint
import boto3

import pandas as pd
import numpy as np
import re
import string
import nltk
import matplotlib.pyplot as plt
import seaborn as sns

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer

from textblob import TextBlob
from textblob.sentiments import PatternAnalyzer, NaiveBayesAnalyzer
from textblob.tokenizers import WordTokenizer, SentenceTokenizer
from nrclex import NRCLex

from scipy import stats
from collections import Counter
from pathlib import Path
# %%
# Load transcript
TRANSCRIPT_FILE_PATH = Path(__file__).parent / "debate_transcript.txt"
# print(TRANSCRIPT_FILE_PATH)

# read the transcript line by line
transcript = []
with open(TRANSCRIPT_FILE_PATH, 'r') as file:
    for line in file:
        if line.strip():    # skip the empty lines
            transcript.append(line.rstrip())
# %%
# Data preprocessing
## Step 1: Extract relevant parts of the data
# separate transcript by each candidate
harris_transcript = [line for line in transcript if line.startswith('VICE PRESIDENT KAMALA HARRIS:')]
trump_transcript = [line for line in transcript if line.startswith('FORMER PRESIDENT DONALD TRUMP:')]

# extract only the speeches of each candidate
# harris
start_pattern = r'VICE PRESIDENT KAMALA HARRIS:\s+'
harris_transcript = [re.sub(start_pattern, '', line) for line in harris_transcript]

# trump
start_pattern = r'FORMER PRESIDENT DONALD TRUMP:\s+'
trump_transcript = [re.sub(start_pattern, '', line) for line in trump_transcript]
# %%
# use comprehend to compare the overall sentiment between the 2 candidates
# Initialize pretty printer for better output formatting
pp = pprint.PrettyPrinter(indent=2)

# Create Comprehend client
comprehend = boto3.client(service_name="comprehend", region_name="eu-west-1")

# %%
# Detect sentiment of Harris over time
# using max batch size of 25
MAX_BATCH_SIZE = 25

harris_sentiment_scores = []
for i in range(0, len(harris_transcript), MAX_BATCH_SIZE):
    batch_response = comprehend.batch_detect_sentiment(TextList=harris_transcript[i:min(i+MAX_BATCH_SIZE, len(harris_transcript))], LanguageCode='en')
    
    for response in batch_response['ResultList']:
        sentiment_score = response['SentimentScore']
        harris_sentiment_scores.append(sentiment_score)

# Detect sentiment of Trump over time
trump_sentiment_scores = []
for i in range(0, len(trump_transcript), MAX_BATCH_SIZE):
    batch_response = comprehend.batch_detect_sentiment(TextList=trump_transcript[i:min(i+MAX_BATCH_SIZE, len(trump_transcript))], LanguageCode='en')
    
    for response in batch_response['ResultList']:
        sentiment_score = response['SentimentScore']
        trump_sentiment_scores.append(sentiment_score)
# %%
# Compare Harris and Trump sentiment score distribution for each sentiment
SENTIMENT_LIST = harris_sentiment_scores[0].keys()

fig, axes = plt.subplots(1, 4, figsize=(20, 5))
# axes.sharey()

for ax, sentiment in zip(axes.flatten(), SENTIMENT_LIST):
    harris_ = [i[sentiment] for i in harris_sentiment_scores]
    trump_ = [i[sentiment] for i in trump_sentiment_scores]

    # plot cumulative distribution
    sns.ecdfplot(harris_, label='Harris', color='b', ax=ax)
    sns.ecdfplot(trump_, label='Trump', color='r', ax=ax)
    # add labels and titles
    ax.set_xlabel(f'{sentiment}', fontsize=16)
    ax.set_ylabel('CDF', fontsize=16)
    # add annotation box for results of KS-test
    ks = stats.ks_2samp(harris_, trump_)
    d_stat, p_val = ks.statistic, ks.pvalue
    # Add a text box with the D-statistic and p-value
    textstr = f'D-statistic: {d_stat:.4f}\np-value: {p_val:.4f}'
    props = dict(boxstyle='round', facecolor='none', alpha=0.5, edgecolor='none')
    ax.text(0.65, 0.2, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)
    ax.legend()

plt.tight_layout()
plt.show()
# %%
# average sentiment score of Harris and Trump over time

