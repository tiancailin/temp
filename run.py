import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    url = 'https://www.douyu.com/g_dance'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    div = soup.find('div', {'class': 'layout-Module-container layout-Cover ListContent'})
    return render_template_string(str(div))

if __name__ == '__main__':
    app.run(port=8888)
