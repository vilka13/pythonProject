import re
import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_info_from_page(url):
    """
    Extracts information from a given webpage URL.
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Extracting title
    title = soup.find("h1", class_="sticker__title")
    title = title.text.strip() if title else "NULL"

    # Extracting parameters
    paraminfo = soup.find_all("b", class_="parameters__value")
    city = re.sub(" +", " ", paraminfo[0].text.strip()) if len(paraminfo) >= 1 else "NULL"
    square = paraminfo[1].text.strip() if len(paraminfo) >= 2 else "NULL"
    rooms = paraminfo[2].text.strip() if len(paraminfo) >= 3 else "NULL"
    floor = paraminfo[3].text.strip() if len(paraminfo) >= 4 else "NULL"

    # Extracting built year
    built_in = "NULL"
    if len(paraminfo) >= 5:
        for text in paraminfo:
            built_in_matches = re.findall(r"19[0-9][0-9]|20[0-2][0-9]", text.text)
            if built_in_matches:
                built_in = built_in_matches[0]
                break

    # Extracting update and upload times
    paraminfo = soup.find_all("div", class_="parameters__value")
    update_time = paraminfo[0].text.strip() if len(paraminfo) >= 1 else "NULL"
    upload_time = paraminfo[1].text.strip() if len(paraminfo) >= 2 else "NULL"

    # Extracting price and price per meter
    price = soup.find("span", class_="priceInfo__value")
    price = re.sub(" +", " ", price.text.replace("\n", '').strip()) if price else "NULL"
    price_per_meter = soup.find("span", class_="priceInfo__additional")
    price_per_meter = price_per_meter.text.strip() if price_per_meter else "NULL"

    # Extracting description
    description = soup.find("div", class_="description__container")
    description = description.text.replace("\n", '').replace("\r", '').strip() if description else "NULL"

    return (
        title, city, square, rooms, floor, built_in, update_time, upload_time, price, price_per_meter, description, url)


def get_links_from_page(url):
    """
    Extracts listing links from a given webpage URL.
    """
    links = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    divs = soup.find_all("div", class_="listing__teaserWrapper")
    for div in divs:
        links.append(div.find('a', class_="teaserLink")['href'])
    return links


def get_max_page(url):
    """
    Extracts the maximum page number from pagination links.
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    pagination = soup.find_all('a', class_="pagination__link")
    max_page = max([int(a.text) for a in pagination if a.text.isdigit()], default=1)
    return max_page


def collect_links(base_url, max_page):
    """
    Collects all listing links from the specified number of pages.
    """
    links = []
    for i in range(1, max_page + 1):
        page_links = get_links_from_page(base_url + str(i))
        links.extend(page_links)
        print(f"Loading page {i}/{max_page}")
    return links


def collect_data(links):
    """
    Collects data from each link and stores it in a DataFrame.
    """
    df = pd.DataFrame(
        columns=['Title', 'City', 'Square', 'Rooms', 'Floor', 'Built In', 'Update time', 'Upload time', 'Price',
                 'Price per meter', 'Description', 'Link'])

    for n, link in enumerate(links):
        df.loc[n] = get_info_from_page(link)
        print(f"Fetching data from page {n + 1}/{len(links)}")
    return df


def main():
    base_url = "https://gratka.pl/nieruchomosci/mieszkania?page="
    max_page = 1  # For testing purposes, adjust as necessary

    # Collect links from all pages
    links = collect_links(base_url, max_page)

    # Collect data from each link
    df = collect_data(links)

    # Save to CSV
    df.to_csv("output1.csv", index=True, header=True)
    print("Saved to output1.csv")


if __name__ == "__main__":
    main()
