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

def push_into_ResultItems(page: str) -> list:
    '''
    Parameters
    ----------
    page : str
        DuckDuckGo result HTML page which contains the information about the search results
        ex. "<!DOCTYPE html PUBLIC "-//W3C...</body></html>"
    
    Returns
    ----------
    results : list
        The list of search results summarized in the ResultItem objects
        ex. [ResultItem1, ResultItem2, ResultItem3, ...]
    '''
    # Retrieve the necessary results using BeautifulSoup
    soup: BeautifulSoup = BeautifulSoup(page, "html.parser")
    search_results: list = soup.find_all("div", attrs={"result", "result_links", "result_links_deep", "web-result"})
    results: list = []
    rank_count: int = 1
    for item in search_results:
        title = item.find("h2", attrs={"result__title", "result__a"}).get_text()
        url: str = item.find("a", attrs={"result__url"})['href']
        abstract: str = item.find("a", attrs={"result__snippet"}).get_text()
        rank: int = rank_count
        rank_count = rank_count + 1
        result: ResultItem = ResultItem(title, url, "DuckDuckGo")
        result.set_abstract(abstract)
        result.set_rank(rank)
        results.append(result)
    return results

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
