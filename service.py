import asyncio

import requests

from bs4 import BeautifulSoup as bs


def get_initial_data():
    # getting the total number of articles and the number of articles per scroll
    response = requests.get("https://realpython.com/search/api/v1/?kind=article&level=basics&continue_after=0")

    if response.status_code == 200:
        main_json = response.json()

        try:
            articles_scroll = int(main_json["count"])
            articles_total = int(main_json["total"])
            return articles_scroll, articles_total
        except ValueError:
            print("Invalid data format for number of articles. Check the initial json file")

    else:
        print("Something went wrong, check your json request")
    return False


def get_urls():
    urls = []

    initial_count = get_initial_data()

    if initial_count:
        scroll = initial_count[0]
        total = initial_count[1]

        count = 0

        while count < total:
            urls.append(f"https://realpython.com/search/api/v1/?kind=article&level=basics&continue_after={str(count)}")
            count = count + scroll

        return urls
    return False


# json data is retrieved from website as a list of lists. To enhance readability, we convert a list
# of nested lists containing dictionaries into a single list of dictionaries:
# list(list(dict)) -> list(dict)
async def combine_lists(lists):
    combined = [elem for sublist in lists for elem in sublist]

    try:
        result = []
        for elem in combined:

            info_article = {"id": elem["key"],
                            "title": elem["title"],
                            "url": f"https://realpython.com{elem['url']}",
                            "pub_date": elem["pub_date"],
                            "tags": elem["categories"],
                            "description": elem["description"],
                            }
            result.append(info_article)
        await asyncio.sleep(0)

        return result

    except KeyError:
        print("Invalid key. Check json data")


async def scrape_webpage(div):

    result = {}

    text = {"no headers": ""}

    href = div.find_all('a')
    links = [a["href"] for a in href]

    for p in div.find_all('p', class_=False):

        if p.text == "Unlock This Article":
            result["preview"] = True
            break

        if p.text == "🐍 Python Tricks 💌":
            break

        if p.find_previous("h2"):
            if text.get(p.find_previous("h2").text) is None:
                text[p.find_previous("h2").text] = ""
            text[p.find_previous("h2").text] += p.text

        elif p.find_previous("h3"):
            if text.get(p.find_previous("h3").text) is None:
                text[p.find_previous("h3").text] = ""
            text[p.find_previous("h3").text] += p.text

        else:
            text["no headers"] += p.text

    d = ""
    for key, value in zip(list(text.keys()), list(text.values())):
        d = key + "\n " + value

    await asyncio.sleep(0)

    result["text"] = d
    result["preview"] = False
    result["links"] = links

    return result


async def parse_webpage(html):

    soup = bs(html, 'html.parser')

    div = soup.find("div", {"class": "article-body"})

    if div is None:
        div = soup.find("div", {"class": "col-md-11 col-lg-8 article with-headerlinks"})

    return await scrape_webpage(div)
