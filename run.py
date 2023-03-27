from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    url = 'https://www.douyu.com/g_dance'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)
    # input()
    
    # 获取CSS、JS等静态资源链接
    css_links = []
    js_links = []
    for link in soup.find_all('link'):
        if link.get('rel') == ['stylesheet']:
            css_links.append(link.get('href'))
    for script in soup.find_all('script'):
        src = script.get('src')
        if src and re.match(r'.*\.js', src):
            js_links.append(src)
    
    # 拼接CSS、JS链接为绝对路径
    base_url = 'https://www.douyu.com'
    css_links = [base_url + link if not link.startswith('http') else link for link in css_links]
    js_links = [base_url + link if not link.startswith('http') else link for link in js_links]
    
    return render_template('index.html', content=soup.find('div', class_='layout-Module-container layout-Cover ListContent'), css_links=css_links, js_links=js_links)

if __name__ == '__main__':
    app.run(port=8888,debug=True)