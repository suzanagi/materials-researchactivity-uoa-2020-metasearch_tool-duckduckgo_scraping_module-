import sys
import json
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
from result_item import ResultItem

def retrieve_result_page(query: str) -> str:
    '''
    Parameters
    ----------
    query : str
        search query string to be sent to DuckDuckGo
        can contain space character and no need to concatenate with '+'
        ex. "hello world"

    Returns
    ----------
    result_page : str
        obtained HTML result page in string
        ex. "<!DOCTYPE html PUBLIC "-//W3C...</body></html>"
    '''
    # Put the query into the form data (post parameter) and it should be encoded binary
    # Look at "Data" section on the page https://docs.python.org/3.7/howto/urllib2.html
    data = parse.urlencode({
        "q": query,
    }).encode('ascii')

    # To access their result without using web browser just use html version of their page
    url = "https://html.duckduckgo.com/html/"

    # Method should be POST to retrieve their result page correctly
    request_to_throw = request.Request(url, data, method="POST")

    # In case it fails to retrieve the result, return an empty string
    result_page = ""

    with request.urlopen(request_to_throw) as response:
        result_page = response.read().decode('utf-8')

    return result_page

def search(query):
    # Get the DuckDuckGo search result page for the query
    page = retrieve_result_page(query)
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
