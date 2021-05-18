import requests
import urllib
from fake_useragent import UserAgent
import re
from bs4 import BeautifulSoup
  

def search_query(query,number_result):
    query = urllib.parse.quote_plus(query) # Format into URL encoding
    ua = UserAgent()
    google_url = "https://www.google.com/search?q=" + query + 'stackoverflow' +"&num=" + str(number_result)
    response = requests.get(google_url, {"User-Agent": ua.random})
    soup = BeautifulSoup(response.text, "html.parser")
    
    result = soup.find_all('div', attrs = {'class': 'ZINbbc'})
    results=[re.search('\/url\?q\=(.*)\&sa',str(i.find('a', href = True)['href'])) for i in result if "url" in str(i)]
    links=[i.group(1) for i in results if i != None]


    heading_object=soup.find_all( 'h3')
    title=[info.getText() for info in heading_object if info != None]

    text=soup.find_all('div', attrs = {'class': 's3v9rd'})
    desc=[inf.getText() for inf in text if inf != None]
    output=[]
    
    for i in range(0,number_result):

        item = {
            'title': title[i],
            'link':links[i],
            'text': desc[i]
        }
        
        output.append(item)
    return(output)

    






