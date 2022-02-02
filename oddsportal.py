import bs4
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import openpyxl
import json


class OddsPortal:

    def __init__(self):

        self.__config_path = "config.json"

        self.__sport = ""
        self.__country = ""
        self.__league = ""
        self.__start_season_year = 0  # 2018-2019 -> year = 2018
        self.__last_season_year = 0  # 2019-2020 -> year = 2019
        self.__wb_name = ""

        self.__current_year = 0
        self.__current_match = 1

        self.__seasons = []

        self.__chrome_driver = webdriver.Chrome("C:\\Users\\pcost\\chromedriver_win32\\chromedriver.exe")
        self.__delay = 10
        self.__number_pages_season = 8

    def close(self):
        self.__chrome_driver.close()

    def load(self, sport, country, league, start_season_year, last_season_year, wb_name):
        self.__sport = sport
        self.__country = country
        self.__league = league
        self.__start_season_year = start_season_year
        self.__last_season_year = last_season_year
        self.__wb_name = wb_name + ".xlsx"

    def load_file(self):

        with open(self.__config_path) as f:
            config = json.load(f)
            self.__sport = config["sport"]
            self.__country = config["country"]
            self.__league = config["league"]
            self.__start_season_year = config["start_season_year"]
            self.__last_season_year = config["last_season_year"]
            self.__wb_name = config["workbook_name"] + ".xlsx"

    def scrap_seasons(self):
        for year in range(self.__start_season_year, self.__last_season_year + 1):
            self.__seasons.append(self.scrap_season(year))
        return self.__seasons

    def scrap_season(self, year):
        matches = []

        self.__current_year = year
        self.__current_match = 0

        for page in range(1, self.__number_pages_season + 1):
            matches_page = self.__scrap_page(page)
            for match in matches_page:
                matches.append(match)

        return {"Year": self.__current_year, "Matches": matches}

    def __scrap_page(self, page):
        matches_page = []
        url = "https://www.oddsportal.com/{}/{}/{}-{}-{}/results/#/page/{}/".format(self.__sport, self.__country, self.__league, self.__current_year, self.__current_year + 1, page)
        self.__chrome_driver.get(url)
        try:
            myElem = WebDriverWait(self.__chrome_driver, self.__delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'table-participant')))
        except TimeoutException:
            print("Loading page took too much time!")

        soup = bs4.BeautifulSoup(self.__chrome_driver.page_source, "html.parser")
        table = soup.find("table", id="tournamentTable")
        for tr in table.findAll("tr", {"class": ["odd deactivate", "deactivate"]}):
            match_right_url = tr.find("td", {"class": "name table-participant"}).find("a")["href"]
            match_url = "https://www.oddsportal.com" + match_right_url
            matches_page.append(self.__scrap_match(match_url))
        return matches_page

    def __scrap_match(self, game_url):
        match = {
            "HT": "",  # HomeTeam
            "AT": "",  # AwayTeam

            "DAY": 0,    # Game day
            "MONTH": 0,  # Game Month
            "YEAR": 0,   # Game Year

            "FTHG": 0,  # Final_Time_Home_Goals
            "FTAG": 0,  # Final_Time_Away_Goals

            "FTHO": 0,  # Final_Time_Home_Team_Winning_Odd
            "FTDO": 0,  # Final_Time_Draw_Odd
            "FTAO": 0,  # Final_Time_Away_Team_Winning_Odd
        }

        self.__chrome_driver.get(game_url)
        try:
            myElem = WebDriverWait(self.__chrome_driver, self.__delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'result')))
            myElem = WebDriverWait(self.__chrome_driver, self.__delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'table-container')))
        except TimeoutException:
            print("Loading match page took too much time!")

        soup = bs4.BeautifulSoup(self.__chrome_driver.page_source, "html.parser")

        # get team names
        teams_names = soup.find("div", id="col-content").find("h1").get_text().split(" - ")
        match["HT"] = teams_names[0]
        match["AT"] = teams_names[1]

        # get match date
        date_list = soup.find("div", id="col-content").find("p", class_="date").get_text().replace(",", " ").split()
        try:
            match["DAY"] = int(date_list[1])
            match["MONTH"] = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"].index(date_list[2]) + 1
            match["YEAR"] = int(date_list[3])
        except ValueError:
            print("Failed scrapping date")
            match["DAY"] = 0
            match["MONTH"] = 0
            match["YEAR"] = 0

        # get number goals
        goals_soup = soup.find("div", id="event-status").find("p", {"class": "result"})
        final_goals_str_list = goals_soup.find("strong").get_text().split(":")

        try:
            match["FTHG"] = int(final_goals_str_list[0])
        except ValueError:
            print("Failed scrapping final time home goals")
        try:
            match["FTAG"] = int(final_goals_str_list[1])
        except ValueError:
            print("Failed scrapping final time away goals")

        # get result odds
        result_odds_list = self.__scrap_average_values_list(soup)

        match["FTHO"] = result_odds_list[0]
        match["FTDO"] = result_odds_list[1]
        match["FTAO"] = result_odds_list[2]

        self.__current_match += 1
        print("Year: {}, Match: {}".format(self.__current_year, self.__current_match))
        print(match)
        return list(match.values())


    @staticmethod
    def __scrap_average_values_list(soup):
        result_odds_soup_list = soup.find("div", id="odds-data-table").find("div", {"class": "table-container"}).find("table").find("tfoot").find("tr", {"class": "aver"}).findAll("td", {"class": "right"})
        result_odds_list = []
        for odd_soup in result_odds_soup_list:
            try:
                result_odds_list.append(float(odd_soup.get_text()))
            except (ValueError, AttributeError):
                print("Failed scrapping odds average")
                result_odds_list.append(0)
        return result_odds_list

    def create_wb(self):

        cols_names = [
            "HT", "AT",
            "DAY", "MONTH", "YEAR",
            "FTHG", "FTAG",
            "FTHO", "FTDO", "FTAO",
        ]

        wb = openpyxl.Workbook()
        current_ws = wb.active

        first_season = True

        for season in self.__seasons:

            if first_season:
                first_season = False
                current_ws.title = season["Year"]
            else:
                current_ws = wb.create_sheet(season["Year"])

            current_column = 1
            for name in cols_names:
                current_ws.cell(row=1, column=current_column, value=name)
                current_column += 1

            current_row = 2
            current_column = 1
            for match in season["Matches"]:
                for key in match:
                    current_ws.cell(row=current_row, column=current_column, value=key)
                    current_column += 1
                current_row += 1
                current_column = 1

        wb.save(self.__wb_name)
        wb.close()
