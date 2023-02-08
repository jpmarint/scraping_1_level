import requests
from bs4 import BeautifulSoup

def obtainSourceCode(url: str) -> bytes:
    """Obtain Source Code
    
    Function to obtain the source code of a website
    
    Args:
        url (str): link to the website where to obtain the source code

    Returns:
        html_content (bytes): html content of the page
    """
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    page = requests.get(url, headers=header)
    html_content = page.content
    print(page.status_code)
    return html_content


def extractLinksFromHtml(html_content: bytes) -> list:
    """Extract Links From html

    Obtains the list of links that are located in the html of the website
    
    Args:
        html_content (bytes): html content obtained from the request of website

    Returns:
        links (list): list of links stored in the html of the website
    """
    soup = BeautifulSoup(html_content, "html.parser")
    links = [link.get("href") for link in soup.find_all("a")]
    return links






if __name__ == "__main__":
    url = "https://www.classcentral.com"
    main_page = obtainSourceCode(url)
    #print(main_page)
    links_list = extractLinksFromHtml(main_page)
    print(links_list)






