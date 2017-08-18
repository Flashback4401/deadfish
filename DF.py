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
br["q"] =  input("Enter: ")
res = br.submit()

link_for_music = br.geturl()
link_for_music = link_for_music[:len(link_for_music) - 1] + '101' #gets the link for the page that only displays files under the audio category
print link_for_music
r = requests.get(link_for_music)
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
    number_of_options = 0
    first_title_name = ""
    for title in soup.find_all("a", {"class": "detLink"}): #searches for titles
        search_results.append(title.text)
        number_of_options += 1
        if number_of_options == 1:
            first_title_name = title.text
    for magnet_link in soup.find_all("a", {"title": "Download this torrent using magnet"}): #searches for links
            magnet_links.append(magnet_link.get('href'))
    for merge in range(0, len(search_results)):
        final_search_results[search_results[merge] ] = magnet_links[merge] #merges the titles and links into a dictionary
    return [final_search_results, first_title_name]
#------------------in progress--------------------
final = find_titles()[0] #the full list of links taken from the site
first_title_name = find_titles()[1] #the title of the very first thing to show up on pirate bay
print(final)
print(first_title_name)
def choose_best_title(final):
    """
       will take the search_results and will find the best title (key), and then will return the link to that title (the value)
       (might make some algorithm later on that takes the top 5 titles that pop up and chooses the best one according to the rating)
    """

    return final.get(first_title_name)#returns final magnet link
print(choose_best_title(final))#prints the magnet link

with open("mechanize_results.html", "w") as f:
     html = soup.prettify("utf-8")
     f.write(html)

"""
Remove all the un-useful page elements. 

Make a algorithm to take all the search result titles in the html and put them into a dictionary, along with the value being the link. 

Put the dictionary trough a bunch of for loops so the best option is chosen. This function should return the 
best title.

"""