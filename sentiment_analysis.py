import pickle
import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


with open("models.pkl", "rb") as file:
    models = pickle.load(file)

def show_visualizations(df):
    sentiment_counts = df.value_counts()

    st.subheader("📊 Sentiment Analysis")
    fig_bar, ax_bar = plt.subplots()
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette='pastel', ax=ax_bar)
    ax_bar.set_ylabel("Number of Comments")
    st.pyplot(fig_bar)

    fig_pie, ax_pie = plt.subplots()
    ax_pie.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%', colors=['#66b3ff', '#ff9999'])
    ax_pie.axis('equal')
    st.pyplot(fig_pie)

def analyse_comments(df):
    # df = pd.read_csv(csv_file)

    processed_comments = []
    for comment in df['comment']:

        # Remove all the special characters
        processed_comment = re.sub(r'\W', ' ', str(comment))

        # remove all single characters
        processed_comment= re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_comment)

        # Remove single characters from the start
        processed_comment = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_comment)

        # Substituting multiple spaces with single space
        processed_comment = re.sub(r'\s+', ' ', processed_comment, flags=re.I)

        # Removing prefixed 'b'
        processed_comment = re.sub(r'^b\s+', '', processed_comment)

        # Converting to Lowercase
        processed_comment = processed_comment.lower()
        processed_comments.append(processed_comment)



    # import nltk
    # nltk.download('stopwords')
    # from nltk.corpus import stopwords
    # from sklearn.feature_extraction.text import TfidfVectorizer
    # vectorizer = TfidfVectorizer(max_features=5000, stop_words=stopwords.words('english'))
    vectorizer = models[1]['vectorizer']
    processed_comments = vectorizer.transform(processed_comments).toarray()

    predicted = models[1]['model'].predict(processed_comments)

    df['sentiments'] = predicted
    return(df)
    # result = {'positive':(predicted == 1).sum(),'negative':(predicted == 0).sum()}
    # return(result)

if __name__ == '__main__':
    csv = "mNEUkkoUoIA.csv"
    senti = analyse_comments(csv)
    df = pd.Series(senti)
    print(df.value_counts()[0],df.value_counts()[1])
    # show_visualizations(df)
