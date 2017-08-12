import mechanize
from bs4 import BeautifulSoup as BS
import requests
url = "https://thepiratebay.org/"
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('user-agent', 'Mozilla/5.0 (X11: U; Linux i686; en-US; rv:1.9,2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3'),
                 ('accept', 'text/html, application/xhtml+hml, application/xml; q = 0.9,*/*;q=0.8')]
br.open(url)

br.select_form(name = "q")
br["q"] = "pink season"
res = br.submit()

new_link = br.geturl()
new_link = new_link[:len(new_link) - 1] + '100'

print new_link
r = requests.get(new_link)
content = r.text
br.close()


#---------------------------------------------------

soup = BS(content, 'html.parser') #a bs4 object (basically makes it easier to get elements from a site)
def remove_elements(element_type_string, key, value):
    for element in soup.find_all(element_type_string, {key: value}): #searches the html
        element.decompose()   #removes those found un-important elements
def remove_the_elements():
    remove_elements("div", "class", "ads")
    remove_elements("div", "id", "sky-right")
    remove_elements("div", "id", "foot")
    remove_elements("h2", "", "")
    remove_elements("a", "class", "img")
    remove_elements("iframe", "id", "sky-center")
    remove_elements("tr", "class", "header")
    remove_elements("thead", "id", "tableHead")
    remove_elements("td", "align", "right")
    remove_elements("style", "type", "text/css")
    remove_elements("font", "class", "detDesc")
remove_the_elements()

def find_titles():
    search_results = []
    magnet_links = []
    final_search_results = {}
    for link in soup.find_all("a", {"class": "detLink"}): #searches for titles
        search_results.append(link.text)
    for magnet_link in soup.find_all("a", {"title": "Download this torrent using magnet"}): #searches for links
            magnet_links.append(magnet_link.get('href'))
    for count in range(0, len(search_results)):
        final_search_results[search_results[count] ] = magnet_links[count] #merges the titles and links into a dictionary
    return final_search_results
#------------------in progress--------------------
final = find_titles()
print(final)
def choose_best_title(final):
    """
       will take the search_results and will find the best title (key), and then will return the link to that title (the value)
    """
    pass
choose_best_title(final)

with open("mechanize_results.html", "w") as f:
     html = soup.prettify("utf-8")
     f.write(html)

"""
Remove all the un-useful page elements.

Make a algorithm to take all the search result titles in the html and put them into a dictionary, along with the value being the link.

Put the dictionary trough a bunch of for loops so the best option is chosen. This function should return the 
best title.

"""