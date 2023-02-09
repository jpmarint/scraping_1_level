import os
import requests
from bs4 import BeautifulSoup
from googletrans import Translator

translator = Translator()

def obtainSourceCode(url: str) -> bytes:
    """Obtain Source Code
    
    Function to obtain the source code of a website
    
    Args:
        url (str): link to the website where to obtain the source code

    Returns:
        html_content (bytes): html content of the page
    """
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    page = requests.get(url, headers=header, timeout=(2, 4.1))
    print(page)
    html_content = page.content
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


def translatePageToHindi(html_content: bytes) -> bytes:
    """Translate Page

    Translates the content of a website to a specified language
    
    Args:
        html_content (bytes): html content of the website

    Returns:
        translated_html (bytes): translated html content of the website
    """
    soup = BeautifulSoup(html_content, "html.parser")
    text_to_translate = soup.get_text()
    try:
        translated_text = translator.translate(text_to_translate, dest='hi').text
    except Exception as e:
        print("An error occurred while translating the text:", e)
        translated_text = ""
    translated_html = str(soup).replace(text_to_translate, translated_text)
    return translated_html.encode("utf-8")
    


if __name__ == "__main__":
    url = "https://www.classcentral.com"
    main_page = obtainSourceCode(url)
    
    links_list = extractLinksFromHtml(main_page)
    
    pages = []
    for link in links_list:
        if link.startswith("/"):
            link = url + link
        print(link)
        page_content = obtainSourceCode(link)
        translated_content = translatePageToHindi(page_content)
        pages.append(translated_content)
        print(f"{link} obtained, translated and appended! \n")

    # Create the directory to store the translated pages
    print("\n\n")
    print("**"*10)
    print("Directory creation")
    directory = "translated_pages"
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory {directory} created!")
        
    # Store the translated pages in the directory
    print("\n\n")
    print("**"*10)
    print("Translated pages in the directory")
    for i, page in enumerate(pages):
        file_name = f"{directory}/page_{i}.html"
        with open(file_name, "wb") as f:
            f.write(page)
            print(f"{i} stored in {file_name}")

    # Change the original hrefs to the new ones inside the directories
    print("\n\n")
    print("**"*10)
    print("original hrefs to the new ones")
    for i, page in enumerate(pages):
        soup = BeautifulSoup(page, "html.parser")
        for link in soup.find_all("a"):
            print(f"Original link: {link}")
            original_href = link.get("href")
            if original_href and original_href.startswith("/"):
                original_href = url + original_href
            if original_href and original_href in links_list:
                new_link = f"page_{links_list.index(original_href)}.html"
                link["href"] = new_link
                print(f"New link: { new_link }")
        with open(f"{directory}/page_{i}.html", "wb") as file:
            file.write(str(soup).encode("utf-8"))






