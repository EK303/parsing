import requests


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


def create_urls():
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
