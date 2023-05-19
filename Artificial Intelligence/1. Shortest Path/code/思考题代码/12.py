import requests
from bs4 import BeautifulSoup

url = 'https://gutenberg.org/cache/epub/70165/pg70165-images.html'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57'}
# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57

strhtml = requests.get(url, headers=headers)  # Get方式获取网页数据
soup = BeautifulSoup(strhtml.text, 'lxml')  # 将请求到的数据解析为lxml格式
info = soup.select('body')  # 筛选数据，这里需要加一个参数

word_list = []
count = 0
with open("12.txt", 'w', encoding='utf-8') as file:
    for item in info:
        ss = item.get_text().lower()
        count += ss.count('the')
        word_list.extend(ss.split())
        file.write(item.get_text())
print('大约一共有 ' + str(len(word_list)) + ' 个单词')
print('大约一共有 ' + str(count) + '个单词the')

print("------------------------------------------------------------")
for item in info:
    print(item.get_text())
