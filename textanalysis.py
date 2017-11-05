from textblob import TextBlob
x=TextBlob("you're useless")
print(x.sentiment.polarity)