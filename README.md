# Data-Extraction-and-Text-Analysis

Web Scraped 114 websites and did text analysis.
Calcualted Positive, Negative, Polarity and Subjectivity Score.
Also did Normalization using PortStemmer

Install following dependencies

For Web Scraping:
import bs4, 
import urllib,
import pandas as pd,
import html5lib,
import requests,
import urllib.request,
from bs4 import BeautifulSoup.

For Text Analysis:
import nltk,
from nltk.corpus import stopwords,
from nltk.tokenize import word_tokenize,
from nltk.tokenize import sent_tokenize,
import re,
nltk.download('stopwords'),
nltk.download('punkt').

For Normalization using PortStemmer:
from nltk.stem.porter import PorterStemmer.
