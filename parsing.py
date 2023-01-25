import requests
from bs4 import BeautifulSoup as BS
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from urllib.parse import urljoin
import csv

disable_warnings(InsecureRequestWarning)

def get_html(url):
    response = requests.get(url, verify=False)
    response.encoding = 'utf-8'
    return response.content.decode('utf-8')

def get_soup(html):
    soup = BS(html, 'lxml', from_encoding="utf-8")
    soup.original_encoding = "utf-8"
    return soup

def get_data(soup):
    catalog = soup.find('div', class_='content-cols container')
    books = catalog.find_all('div', class_='last-books-item full-window')
    if books:
        for book in books:
           
            try:
                title = book.find('h4').text.strip()
                print(title)
            except AttributeError:
                del title
                # title = ''
            try:
                url = book.find('a', class_='books-list-image').get('href')
                url = urljoin('https://samolit.com/books', url)
            except:
                del url
                # url = ''
                
                
            if title == '' or url =='':
                continue
                
            write_csv({
                'title': title,
                'url': url
            })
            
    else:
        raise AttributeError('Error')
    
    
def write_csv(data):
    with open('books.csv', 'a') as f:
        names = ['title', 'url']
        write = csv.DictWriter(f, delimiter=',', fieldnames=names)
        write.writerow(data)
        
        
def main():
    try:
        URL = 'https://samolit.com/books/'
        html = get_html(URL)
        soup = get_soup(html)
        get_data(soup)
    except AttributeError:
        print('Error')        
            



    