import requests
import bs4

game = {
    "FHAG": 0,
    "SHHG": 0,
    "SHAG": 0,
    "HO": 0,
    "DO": 0,
    "AO": 0,

    "FTO 0.5": 0,
    "FTU 0.5": 0,
    "FTO 1.5": 0,
    "FTU 1.5": 0,
    "FTO 2.5": 0,
    "FTU 2.5": 0,
    "FTO 3.5": 0,
    "FTU 3.5": 0,

    "FHO 0.5": 0,
    "FHU 0.5": 0,
    "FHO 1.5": 0,
    "FHU 1.5": 0,
    "FHO 2.5": 0,
    "FHU 2.5": 0,
    "FHO 3.5": 0,
    "FHU 3.5": 0,

    "SHO 0.5": 0,
    "SHU 0.5": 0,
    "SHO 1.5": 0,
    "SHU 1.5": 0,
    "SHO 2.5": 0,
    "SHU 2.5": 0,
    "SHO 3.5": 0,
    "SHU 3.5": 0,

    "NDH": 0,
    "NDA": 0
}


def scrap():
    scrap_year(2018)


# 2018-2019 -> year = 2018
def scrap_year(year):
    # num_pages = 8
    # for i in range(1, num_pages + 1):
    #     scrap_page(year, i)
    scrap_page(year, 1)


def scrap_page(year, page):
    url = "https://www.oddsportal.com/soccer/england/premier-league-{}-{}/results/#/page/{}/".format(year, year + 1, page)
    page = requests.get(url, headers={'User-Agent': 'Custom'})
    soup = bs4.BeautifulSoup(page.content, "html.parser")
    div = soup.find("div", id="tournamentTable")
    print(soup)


# def scrap_game(game_url):


scrap()