import bs4
from selenium import webdriver

game = {
    "HT": "",  # HomeTeam
    "AT": "",  # AwayTeam

    "FTHG": 0,  # Final_Time_Home_Goals
    "FTAH": 0,  # Final_Time_Away_Goals
    "FHHG": 0,  # First_Half_Home_Goals
    "FHAG": 0,  # First_Half_Away_Goals
    "SHHG": 0,  # Second_Half_Home_Goals
    "SHAG": 0,  # Second_Half_Away_Goals

    "HO": 0,  # Home_Team_Winning_Odd
    "DO": 0,  # Draw_Odd
    "AO": 0,  # Away_Team_Winning_Odd

    "FTO 0.5": 0,  # Final_Time_Over_0.5_Goals
    "FTU 0.5": 0,  # Final_Time_Under_0.5_Goals
    "FTO 1.5": 0,  # Final_Time_Over_1.5_Goals
    "FTU 1.5": 0,  # Final_Time_Under_1.5_Goals
    "FTO 2.5": 0,  # Final_Time_Over_2.5_Goals
    "FTU 2.5": 0,  # Final_Time_Under_2.5_Goals
    "FTO 3.5": 0,  # Final_Time_Over_3.5_Goals
    "FTU 3.5": 0,  # Final_Time_Under_3.5_Goals

    "FHO 0.5": 0,  # First_Half_Over_0.5_Goals
    "FHU 0.5": 0,  # First_Half_Under_0.5_Goals
    "FHO 1.5": 0,  # First_Half_Over_1.5_Goals
    "FHU 1.5": 0,  # First_Half_Under_1.5_Goals
    "FHO 2.5": 0,  # First_Half_Over_2.5_Goals
    "FHU 2.5": 0,  # First_Half_Under_2.5_Goals

    "SHO 0.5": 0,  # Second_Half_Over_0.5_Goals
    "SHU 0.5": 0,  # Second_Half_Under_0.5_Goals
    "SHO 1.5": 0,  # Second_Half_Over_1.5_Goals
    "SHU 1.5": 0,  # Second_Half_Under_1.5_Goals
    "SHO 2.5": 0,  # Second_Half_Over_2.5_Goals
    "SHU 2.5": 0,  # Second_Half_Under_2.5_Goals

    "NDH": 0,  # No_Draw_Home_Team_Winning_Odd
    "NDA": 0   # No_Draw_Away_Team_Winning_Odd
}

chrome_driver = webdriver.Chrome("C:\\Users\\pcost\\chromedriver_win32\\chromedriver.exe")


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
    chrome_driver.get(url)
    soup = bs4.BeautifulSoup(chrome_driver.page_source, "html.parser")
    table = soup.find("table", id="tournamentTable")
    for tr in table.findAll("tr", {"class": ["odd deactivate", "deactivate"]}):
        game_right_url = tr.find("td", {"class": "name table-participant"}).find("a")["href"]
        game_url = "https://www.oddsportal.com" + game_right_url
        # print(game_url)
        scrap_game(game_url)
        break


def scrap_game(game_url):
    chrome_driver.get(game_url)
    soup = bs4.BeautifulSoup(chrome_driver.page_source, "html.parser")

    # get team names
    teams_names = soup.find("div", id="col-content").find("h1").get_text().split(" - ")
    game["HT"] = teams_names[0]
    game["AT"] = teams_names[1]

    # get number goals
    goals_soup = soup.find("div", id="event-status").find("p", {"class": "result"})
    final_goals_str_list = goals_soup.find("strong").get_text().split(":")
    game["FTHG"] = int(final_goals_str_list[0])
    game["FTAH"] = int(final_goals_str_list[1])

    half_goals_str_list = goals_soup.get_text()[goals_soup.get_text().find("(")+1:goals_soup.get_text().find(")")].split(", ")
    first_half_goals_str_list = half_goals_str_list[0].split(":")
    second_half_goals_str_list = half_goals_str_list[1].split(":")
    game["FHHG"] = int(first_half_goals_str_list[0])
    game["FHAG"] = int(first_half_goals_str_list[1])
    game["SHHG"] = int(second_half_goals_str_list[0])
    game["SHAG"] = int(second_half_goals_str_list[1])

    # get result odds
    result_odds_soup_list = soup.find("div", id="odds-data-table").find("div", {"class": "table-container"}).find("table").find("tfoot").find("tr", {"class": "aver"}).findAll("td", {"class": "right"})
    game["HO"] = float(result_odds_soup_list[0].get_text())
    game["DO"] = float(result_odds_soup_list[1].get_text())
    game["AO"] = float(result_odds_soup_list[2].get_text())

    # get goals odds
    chrome_driver.find_element_by_xpath('//*[@title="Over/Under"]').click()
    soup = bs4.BeautifulSoup(chrome_driver.page_source, "html.parser")

    odds_data_table_soup = soup.find("div", id="odds-data-table").findAll("div", class_="table-container")
    print(odds_data_table_soup)


# def scrap_game_goals_odds(goals_odds_url):



scrap()