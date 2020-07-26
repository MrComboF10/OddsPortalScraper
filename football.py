import bs4
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import openpyxl


chrome_driver = webdriver.Chrome("C:\\Users\\pcost\\chromedriver_win32\\chromedriver.exe")
delay = 3  # delay to load page


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
    try:
        myElem = WebDriverWait(chrome_driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'table-participant')))
        print("Page is ready!")
    except TimeoutException:
        print("Loading page took too much time!")

    soup = bs4.BeautifulSoup(chrome_driver.page_source, "html.parser")
    table = soup.find("table", id="tournamentTable")
    for tr in table.findAll("tr", {"class": ["odd deactivate", "deactivate"]}):
        game_right_url = tr.find("td", {"class": "name table-participant"}).find("a")["href"]
        game_url = "https://www.oddsportal.com" + game_right_url
        scrap_game(game_url)
        break


def scrap_game(game_url):
    game = {
        "HT": "",  # HomeTeam
        "AT": "",  # AwayTeam

        "FTHG": 0,  # Final_Time_Home_Goals
        "FTAH": 0,  # Final_Time_Away_Goals
        "FHHG": 0,  # First_Half_Home_Goals
        "FHAG": 0,  # First_Half_Away_Goals
        "SHHG": 0,  # Second_Half_Home_Goals
        "SHAG": 0,  # Second_Half_Away_Goals

        "FTHO": 0,  # Final_Time_Home_Team_Winning_Odd
        "FTDO": 0,  # Final_Time_Draw_Odd
        "FTAO": 0,  # Final_Time_Away_Team_Winning_Odd

        "FHHO": 0,  # First_Half_Home_Team_Winning_Odd
        "FHDO": 0,  # First_Half_Draw_Odd
        "FHAO": 0,  # First_Half_Away_Team_Winning_Odd

        "SHHO": 0,  # Second_Half_Home_Team_Winning_Odd
        "SHDO": 0,  # Second_Half_Draw_Odd
        "SHAO": 0,  # Second_Half_Away_Team_Winning_Odd

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

        "FTNDH": 0,  # Final_Time_No_Draw_Home_Team_Winning_Odd
        "FTNDA": 0,  # Final_Time_No_Draw_Away_Team_Winning_Odd

        "FHNDH": 0,  # First_Half_No_Draw_Home_Team_Winning_Odd
        "FHNDA": 0,  # First_Half_No_Draw_Away_Team_Winning_Odd

        "SHNDH": 0,  # Second_Half_No_Draw_Home_Team_Winning_Odd
        "SHNDA": 0   # Second_Half_No_Draw_Away_Team_Winning_Odd
    }

    chrome_driver.get(game_url)
    try:
        myElem = WebDriverWait(chrome_driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'result')))
        myElem = WebDriverWait(chrome_driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'table-container')))
        print("Game page is ready!")
    except TimeoutException:
        print("Loading game page took too much time!")

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
    # -> full time odds
    result_odds_list = scrap_average_values_list(soup)

    game["FTHO"] = result_odds_list[0]
    game["FTDO"] = result_odds_list[1]
    game["FTAO"] = result_odds_list[2]

    # -> first half odds
    chrome_driver.find_element_by_link_text("1st Half").click()
    try:
        myElem = WebDriverWait(chrome_driver, delay).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'table-container')))
        print("Odds result first half page is ready!")

    except TimeoutException:
        print("Loading odds result first half page took too much time!")
    soup = bs4.BeautifulSoup(chrome_driver.page_source, "html.parser")

    result_odds_list = scrap_average_values_list(soup)

    game["FHHO"] = result_odds_list[0]
    game["FHDO"] = result_odds_list[1]
    game["FHAO"] = result_odds_list[2]

    # -> second half odds
    chrome_driver.find_element_by_link_text("2nd Half").click()
    try:
        myElem = WebDriverWait(chrome_driver, delay).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'table-container')))
        print("Odds result second half page is ready!")

    except TimeoutException:
        print("Loading odds result second half page took too much time!")
    soup = bs4.BeautifulSoup(chrome_driver.page_source, "html.parser")

    result_odds_list = scrap_average_values_list(soup)

    game["SHHO"] = result_odds_list[0]
    game["SHDO"] = result_odds_list[1]
    game["SHAO"] = result_odds_list[2]

    # get goals odds
    # -> full time odds
    chrome_driver.find_element_by_xpath('//*[@title="Over/Under"]').click()
    try:
        myElem = WebDriverWait(chrome_driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'table-container')))
        print("Odds goals full time page is ready!")

    except TimeoutException:
        print("Loading odds goals full time page took too much time!")
    soup = bs4.BeautifulSoup(chrome_driver.page_source, "html.parser")
    full_time_odds = scrap_odds_goals_part(soup)

    # -> first half odds
    chrome_driver.find_element_by_link_text("1st Half").click()
    try:
        myElem = WebDriverWait(chrome_driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'table-container')))
        print("Odds goals first half page is ready!")

    except TimeoutException:
        print("Loading odds goals first half page took too much time!")
    soup = bs4.BeautifulSoup(chrome_driver.page_source, "html.parser")
    first_half_odds = scrap_odds_goals_part(soup)

    # -> second half odds
    chrome_driver.find_element_by_link_text("2nd Half").click()
    try:
        myElem = WebDriverWait(chrome_driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'table-container')))
        print("Odds goals second half page is ready!")

    except TimeoutException:
        print("Loading odds goals second half page took too much time!")
    soup = bs4.BeautifulSoup(chrome_driver.page_source, "html.parser")
    second_half_odds = scrap_odds_goals_part(soup)

    game["FTO 0.5"] = full_time_odds["O_U 0.5"]["OVER"]
    game["FTU 0.5"] = full_time_odds["O_U 0.5"]["UNDER"]
    game["FTO 1.5"] = full_time_odds["O_U 1.5"]["OVER"]
    game["FTU 1.5"] = full_time_odds["O_U 1.5"]["UNDER"]
    game["FTO 2.5"] = full_time_odds["O_U 2.5"]["OVER"]
    game["FTU 2.5"] = full_time_odds["O_U 2.5"]["UNDER"]
    game["FTO 3.5"] = full_time_odds["O_U 3.5"]["OVER"]
    game["FTU 3.5"] = full_time_odds["O_U 3.5"]["UNDER"]

    game["FHO 0.5"] = first_half_odds["O_U 0.5"]["OVER"]
    game["FHU 0.5"] = first_half_odds["O_U 0.5"]["UNDER"]
    game["FHO 1.5"] = first_half_odds["O_U 1.5"]["OVER"]
    game["FHU 1.5"] = first_half_odds["O_U 1.5"]["UNDER"]
    game["FHO 2.5"] = first_half_odds["O_U 2.5"]["OVER"]
    game["FHU 2.5"] = first_half_odds["O_U 2.5"]["UNDER"]

    game["SHO 0.5"] = second_half_odds["O_U 0.5"]["OVER"]
    game["SHU 0.5"] = second_half_odds["O_U 0.5"]["UNDER"]
    game["SHO 1.5"] = second_half_odds["O_U 1.5"]["OVER"]
    game["SHU 1.5"] = second_half_odds["O_U 1.5"]["UNDER"]
    game["SHO 2.5"] = second_half_odds["O_U 2.5"]["OVER"]
    game["SHU 2.5"] = second_half_odds["O_U 2.5"]["UNDER"]

    # Draw no bet
    # -> full time odds
    chrome_driver.find_element_by_link_text("DNB").click()
    try:
        myElem = WebDriverWait(chrome_driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'table-container')))
        print("Odds no draw page is ready!")

    except TimeoutException:
        print("Loading odds no draw page took too much time!")

    soup = bs4.BeautifulSoup(chrome_driver.page_source, "html.parser")
    draw_no_bet_odds_list = scrap_average_values_list(soup)
    game["FTNDH"] = draw_no_bet_odds_list[0]
    game["FTNDA"] = draw_no_bet_odds_list[1]

    # first half odds
    chrome_driver.find_element_by_link_text("1st Half").click()
    try:
        myElem = WebDriverWait(chrome_driver, delay).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'table-container')))
        print("Odds no draw first half page is ready!")

    except TimeoutException:
        print("Loading odds no draw first half page took too much time!")
    soup = bs4.BeautifulSoup(chrome_driver.page_source, "html.parser")

    draw_no_bet_odds_list = scrap_average_values_list(soup)
    game["FHNDH"] = draw_no_bet_odds_list[0]
    game["FHNDA"] = draw_no_bet_odds_list[1]

    # second half odds
    chrome_driver.find_element_by_link_text("2nd Half").click()
    try:
        myElem = WebDriverWait(chrome_driver, delay).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'table-container')))
        print("Odds no draw second half page is ready!")

    except TimeoutException:
        print("Loading odds no draw second half page took too much time!")
    soup = bs4.BeautifulSoup(chrome_driver.page_source, "html.parser")

    draw_no_bet_odds_list = scrap_average_values_list(soup)
    game["SHNDH"] = draw_no_bet_odds_list[0]
    game["SHNDA"] = draw_no_bet_odds_list[1]

    print(game)


def scrap_average_values_list(soup):
    result_odds_soup_list = soup.find("div", id="odds-data-table").find("div", {"class": "table-container"}).find("table").find("tfoot").find("tr", {"class": "aver"}).findAll("td", {"class": "right"})
    result_odds_list = []
    for odd_soup in result_odds_soup_list:
        result_odds_list.append(float(odd_soup.get_text()))
    return result_odds_list


def scrap_odds_goals_part(soup):
    odds_data_list_soup = soup.find("div", id="odds-data-table").findAll("div", class_="table-container")

    odds_05_div, odds_15_div, odds_25_div, odds_35_div = "", "", "", ""

    for div in odds_data_list_soup:
        if "Over/Under +0.5" in str(div):
            odds_05_div = div
        elif "Over/Under +1.5" in str(div):
            odds_15_div = div
        elif "Over/Under +2.5" in str(div):
            odds_25_div = div
        elif "Over/Under +3.5" in str(div):
            odds_35_div = div

    return {
        "O_U 0.5": scrap_odds_over_under(odds_05_div),
        "O_U 1.5": scrap_odds_over_under(odds_15_div),
        "O_U 2.5": scrap_odds_over_under(odds_25_div),
        "O_U 3.5": scrap_odds_over_under(odds_35_div)
    }


def scrap_odds_over_under(odds_goals_div):
    odds_over_under_span_list = odds_goals_div.findAll("span", class_="avg chunk-odd nowrp")
    return {"OVER": float(odds_over_under_span_list[1].find("a").get_text()), "UNDER": float(odds_over_under_span_list[0].find("a").get_text())}


# def scrap_game_goals_odds(goals_odds_url):



scrap()