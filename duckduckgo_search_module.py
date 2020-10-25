import requests
import sys
from bs4 import BeautifulSoup
from result_item import ResultItem

def search(query):
    # Get the Yahoo search result page for the query
    page = requests.get('https://search.yahoo.com/search?p='+query)
    # Prepare a list for returning the search results
    result = list()
    # Check the result page encoding to use it in BeautifulSoup composition
    encoding = page.encoding
    # Analyse the result page using BeautifulSoup
    soup = BeautifulSoup(page.content, "html.parser", from_encoding = encoding)
    # Obtain topics and abstract element by the BeautifulSoup function
    topics = soup.find_all("a", attrs={"ac-algo", "fz-l"})
    abstract = soup.find_all("p", attrs={"lh-16"})
    # Put the results in the list to be returned
    rank = 1
    for title in topics:
        r_item = ResultItem(title.text, title.attrs['href'], "Yahoo!")
        r_item.add_rank(rank)
        result.append(r_item)
        rank += 1
    # Return the result list
    return result

# Main Function
if __name__ == "__main__":
    # Prepare query variable
    query = sys.argv[1]
    # Append multiple query words with "+"
    for arg in sys.argv[2:]:
        query = query + "+" + arg
    # Experiment the search function
    result = search(query)
    # Print the result list to the command line
    for item in result:
        print("[title] "+item.title)
        print("[url] "+item.url)
        print("[rank] "+str(item.rank))
        print("\n")
