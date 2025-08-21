# 🎥 YouTube Comment Analyzer  

A Streamlit web app that fetches comments from YouTube videos and performs **sentiment analysis** to determine whether the audience reaction is **positive** or **negative**.  

🔗 **Live Demo:** [Click here to try](https://youtubecommentanalyzerusingnlp-ax9k2bealjjcmin3pwmele.streamlit.app/)  

---

## ✨ Features  
- 🔍 Fetch up to **1500 YouTube comments** using the YouTube Data API  
- 👤 **Channel Overview**: channel logo, title, subscribers, total videos, creation date  
- 🎥 **Video Information**: views, likes, and comment count  
- 🎭 **Sentiment Analysis**: classify comments as **Positive** or **Negative**  
- 📊 **Visualizations**:  
  - Bar chart for sentiment counts  
  - Pie chart for sentiment distribution  
- ⏳ Real-time feedback while fetching comments  

---

## 🛠️ Tech Stack  
- **Python**  
- **Streamlit**  
- **YouTube Data API v3**  
- **Pandas, Matplotlib, Seaborn**  
- **NLP (Sentiment Classification)**  

---

## 🚀 How to Run Locally  

1. Clone the repository  
   ```bash
   git clone https://github.com/Shrived28/Youtube_comment_analyzer_using_nlp.git
   cd Youtube_comment_analyzer_using_nlp

2. Install dependencies  

```bash
pip install -r requirements.txt

3. Add your YouTube API key

Open the code and replace "YOUR_API_KEY" with your actual API key.

4. Run the Streamlit app

```bash
streamlit run app.py
