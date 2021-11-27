import ssl
import sys
import urllib.request

from urllib.request import urlopen
from urllib.error import HTTPError
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from typing import List


def get_links(url):
    """Find all links on page at the given url.

    Returns:
        a list of all unique hyperlinks on the page,
        without page fragments or query parameters.
    """
    url_list = []
    for url_str in url:
        temp = ""
        if url_str != None:
            for text in url_str:
                if text == "?" or text == "#":
                    break
                temp += text
            if not temp == '':
                url_list.append(temp)
    url_list = list(dict.fromkeys(url_list))
    return url_list


def is_valid_url(url: str):
    """Check the url is reachable.

    Returns:
        True if url reachable or 403, otherwise return False.
    """
    context = ssl._create_unverified_context()
    req = urllib.request.Request(url, method="HEAD")
    try:
        response = urlopen(req, context=context)
        response.close()
    except HTTPError as e:
        if e.code == 403:
            e.close()
            return True
        e.close()
        return False
    else:
        return True


def invalid_urls(urllist: List[str]) -> List[str]:
    """Validate the urls in urllist and return a new list containing
    the invalid or unreachable urls.
    """
    invalid_list = []
    for link in urllist:
        if not is_valid_url(link):
            invalid_list.append(link)
    return invalid_list


def main(websearch):
    # browser: a WebDriver object
    browser = webdriver.Firefox()
    browser.implicitly_wait(3)  # seconds

    # get the duckduckgo search page
    url = websearch
    browser.get(url)

    # get href on that page
    list_link = []
    links = browser.find_elements_by_tag_name("a")
    for link in links:
        if link.tag_name == 'a':
            url_href = link.get_attribute('href')
            list_link.append(url_href)
    list_link = get_links(list_link)
    for link in list_link:
        # all link in the page
        print(link)
    print()
    print("Bad Links:")
    # invalid link in the page
    for link in invalid_urls(list_link):
        print(link)


if __name__ == "__main__":
    web_search = sys.argv[1]
    main(web_search)
