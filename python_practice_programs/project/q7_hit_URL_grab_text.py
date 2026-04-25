import sys
import os

# Add the parent directory (python_practice_programs) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import xml.etree.ElementTree as ET

import requests
from bs4 import BeautifulSoup

from project.read_config import get_config_value


def fetch_url_content(url):
    response = requests.get(url)
    response.raise_for_status()
    html = response.text
    return html


def write_to_file(content):
    output_file = get_config_value('files', 'output_url_content')
    try:
        with open(output_file, "wb") as file:
            file.write(content.encode("utf-8"))
    except Exception as e:
        print(f"An unexpected error occurred while writing the file: {e}")


def fetch_urls_list():
    url = get_config_value('urls', 'rss_url')
    content = ""
    parts = []
    try:

        html = fetch_url_content(url)

        soup = BeautifulSoup(html, "html.parser")
        div = soup.find("div", class_="w3-code notranslate htmlHigh")

        if div is None:
            print("XML block not found")
            exit()

        xml_text = div.get_text(strip=True)

        root = ET.fromstring(xml_text)

        urls = set()

        for link in root.findall(".//link"):
            if link.text:
                urls.add(link.text.strip())

        for url in urls:
            print(f"Unique URLs:{url}")
            parts.append("=======================================================")
            parts.append(url)
            parts.append("=======================================================")
            parts.append(fetch_url_content(url))
            parts.append("\n")

        content = "\n".join(parts)
        write_to_file(content)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")


if __name__ == "__main__":
    fetch_urls_list()
