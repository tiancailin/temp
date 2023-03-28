from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import dy_url


app = Flask(__name__)

@app.route('/')
def index():
    # 舞蹈区url
    url = 'https://www.douyu.com/g_dance'
    # 伪装成浏览器发送请求
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    css_links = []
    js_links = []

    # 获取CSS和JS的链接
    for link in soup.find_all('link'):
        if link.get('href') and '.css' in link.get('href'):
            css_links.append(link.get('href'))
    for link in soup.find_all('script'):
        if link.get('src') and '.js' in link.get('src'):
            js_links.append(link.get('src'))

    # 获取CSS和JS的内容
    css_content = []
    js_content = []
    for link in css_links:
        css_content.append(requests.get(link).text)
    for link in js_links:
        js_content.append(requests.get(link).text)

    # 找到直播间列表所在的div
    room_list = soup.find('div', {'class': 'layout-Module-container layout-Cover ListContent'})
    # room_list = soup.select('div.layout-Module-container.layout-Cover.ListContent ul.layout-Cover-list li.layout-Cover-item')

    # 重写a标签链接地址
    # for room in room_list.find_all('li'):
    #     a_tag = room.find('a', {'class': 'DyListCover-wrap'})
    #     if a_tag is not None and 'href' in a_tag.attrs:
    #         href = a_tag['href']
    #         new_href = f"https://www.douyu.com{href}"
    #         a_tag['href'] = new_href

    return render_template('index.html', css=css_content, js=js_content, html=room_list)

if __name__ == '__main__':
    app.run(port=8888,debug=True)
