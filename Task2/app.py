from flask import Flask, render_template
import requests
import requests
import json
app = Flask(__name__)

@app.route('/')
def index():
    # Example: Fetch data from NewsAPI
    api_key = '7910e9be4c064c4c84324504d39570ac'
    news_api_url = 'https://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey=' + api_key

    response = requests.get(news_api_url)
    data = response.json()

    # print(data)

    return render_template('index.html', articles=data['articles'])
    

if __name__ == '__main__':
    app.run(debug=True)
