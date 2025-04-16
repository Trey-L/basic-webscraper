import requests
from bs4 import BeautifulSoup, NavigableString
import json

def element_to_dict(element):
    # If the element is a string (text node), return its content.
    if isinstance(element, NavigableString):
        text = element.strip()
        if text:
            return text
        else:
            return None

    # Process element: tag name, attributes, and recursively process children.
    result = {
        "tag": element.name,
        "attributes": dict(element.attrs)
    }
    # Recursively process element children
    children = []
    for child in element.children:
        child_dict = element_to_dict(child)
        if child_dict is not None:
            children.append(child_dict)
    if children:
        result["children"] = children
    return result

def scrape_entire_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Start from <html> if possible, else the soup object’s root tags
        html_tag = soup.html if soup.html else soup
        root = element_to_dict(html_tag)
        return {
            'url': url,
            'dom': root
        }
    except Exception as e:
        return {'error': str(e)}

def main():
    url = input("Enter the URL to scrape: ")
    result = scrape_entire_page(url)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
