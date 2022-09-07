import urllib.request, urllib.parse, os, re
import bs4

OPENER = urllib.request.build_opener()
OPENER.addheaders = [('User-agent', 'Mozilla/5.0')]

def duckduck(word):
    word = urllib.parse.quote(word)
    response = OPENER.open("https://api.duckduckgo.com/?q={}&format=xml".format(word))
#    response = OPENER.open("https://duckduckgo.com/?q={}&t=h_&ia=web".format(word))
    if response:
        soup = bs4.BeautifulSoup(response, "html.parser")
        return soup
#        response = response.read().decode('utf8')
#        soup = bs4.BeautifulSoup(response, 'html5lib')
#        return soup
#        return response.read().decode('utf8')

def google(word):
    word = urllib.parse.quote(word)
    response = OPENER.open("https://www.google.com/search?q={}&oq={}&aqs=chrome..69i57j0i19.9261j0j15&sourceid=chrome&ie=UTF-8".format(word, word))
    if response:
        soup = bs4.BeautifulSoup(response, "html.parser")
        return soup

def abyssinica(word):
    word = urllib.parse.quote(word)
#    definition = "የ{} ትርጉም - ".format(word)
    response = OPENER.open("https://dictionary.abyssinica.com/{}".format(word))
    if response:
        soup = bs4.BeautifulSoup(response, "html.parser")
        definition = soup.find_all('div', 'main-meta')[0].contents[0].split(' - ')[1]
        return definition
    else:
        print("{} not found in Abyssinica")
        
    
