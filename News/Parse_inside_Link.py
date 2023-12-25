import requests
from bs4 import BeautifulSoup
import json

def parse_and_get_text(url):
    css_selector = "#__next > div > div.LayoutChild__Container-sc-1n20zw8-0.eWjRGN > div > div > div.id__Content-bhuaj0-13.jjcxHY > div > div:nth-child(1) > article > div.EditorContent__EditorContentWrapper-ygblm0-0.dzgBwY"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        content = soup.select_one(css_selector)
        if content is not None:
            paragraphs = content.find_all('p')
            paragraphs_text = ",".join([p.get_text().replace('"', "'") for p in paragraphs])

            return paragraphs_text
        else:
            print(f"Failed to fetch {url}")
            return "shesacvlelia"
    else:
        print("")


with open("./News/last.json", encoding='utf-8') as json_file:
    data = json.load(json_file)
hrefs = data[0]["hrefs"][:-1]



parsed_text_list = []
for href in hrefs:
    full_url = f"https://mtavari.tv{href}"
    parsed_text = parse_and_get_text(full_url)
#
    if parsed_text:
        parsed_text_list.append(parsed_text)

data[0]["text"] = parsed_text_list

with open("./News/last.json", 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

