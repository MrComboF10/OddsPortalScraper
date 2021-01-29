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

        half_goals_str_list = goals_soup.get_text()[goals_soup.get_text().find("(")+1:goals_soup.get_text().find(")")].split(", ")
        first_half_goals_str_list = half_goals_str_list[0].split(":")
        second_half_goals_str_list = half_goals_str_list[1].split(":")

        try:
            match["FHHG"] = int(first_half_goals_str_list[0])
        except ValueError:
            print("Failed scrapping first half home goals")

        try:
            match["FHAG"] = int(first_half_goals_str_list[1])
        except ValueError:
            print("Failed scrapping first half away goals")

        try:
            match["SHHG"] = int(second_half_goals_str_list[0])
        except ValueError:
            print("Failed scrapping second half home goals")

        try:
            match["SHAG"] = int(second_half_goals_str_list[1])
        except ValueError:
            print("Failed scrapping second half away goals")

        # get result odds
        # -> full time odds
        result_odds_list = self.__scrap_average_values_list(soup)

        match["FTHO"] = result_odds_list[0]
        match["FTDO"] = result_odds_list[1]
        match["FTAO"] = result_odds_list[2]

        # -> first half odds
        try:
            self.__chrome_driver.find_element_by_link_text("1st Half").click()
        except selenium.common.exceptions.NoSuchElementException:
            print("1st half do not exist")
        else:
            try:
                myElem = WebDriverWait(self.__chrome_driver, self.__delay).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'table-container')))
            except TimeoutException:
                print("Loading odds result first half page took too much time!")
            soup = bs4.BeautifulSoup(self.__chrome_driver.page_source, "html.parser")

            result_odds_list = self.__scrap_average_values_list(soup)

            match["FHHO"] = result_odds_list[0]
            match["FHDO"] = result_odds_list[1]
            match["FHAO"] = result_odds_list[2]

        # -> second half odds
        try:
            self.__chrome_driver.find_element_by_link_text("2nd Half").click()
        except selenium.common.exceptions.NoSuchElementException:
            print("2nd half do not exist")
        else:
            try:
                myElem = WebDriverWait(self.__chrome_driver, self.__delay).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'table-container')))
            except TimeoutException:
                print("Loading odds result second half page took too much time!")
            soup = bs4.BeautifulSoup(self.__chrome_driver.page_source, "html.parser")

            result_odds_list = self.__scrap_average_values_list(soup)

            match["SHHO"] = result_odds_list[0]
            match["SHDO"] = result_odds_list[1]
            match["SHAO"] = result_odds_list[2]

        # get goals odds
        # -> full time odds
        self.__chrome_driver.find_element_by_xpath('//*[@title="Over/Under"]').click()
        try:
            myElem = WebDriverWait(self.__chrome_driver, self.__delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'table-container')))
        except TimeoutException:
            print("Loading odds goals full time page took too much time!")
        soup = bs4.BeautifulSoup(self.__chrome_driver.page_source, "html.parser")
        full_time_odds = self.__scrap_odds_goals_part(soup)

        match["FTO 0.5"] = full_time_odds["O_U 0.5"]["OVER"]
        match["FTU 0.5"] = full_time_odds["O_U 0.5"]["UNDER"]
        match["FTO 1.5"] = full_time_odds["O_U 1.5"]["OVER"]
        match["FTU 1.5"] = full_time_odds["O_U 1.5"]["UNDER"]
        match["FTO 2.5"] = full_time_odds["O_U 2.5"]["OVER"]
        match["FTU 2.5"] = full_time_odds["O_U 2.5"]["UNDER"]
        match["FTO 3.5"] = full_time_odds["O_U 3.5"]["OVER"]
        match["FTU 3.5"] = full_time_odds["O_U 3.5"]["UNDER"]

        # -> first half odds
        try:
            self.__chrome_driver.find_element_by_link_text("1st Half").click()
        except selenium.common.exceptions.NoSuchElementException:
            print("1st half do not exist")
        else:
            try:
                myElem = WebDriverWait(self.__chrome_driver, self.__delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'table-container')))
            except TimeoutException:
                print("Loading odds goals first half page took too much time!")
            soup = bs4.BeautifulSoup(self.__chrome_driver.page_source, "html.parser")
            first_half_odds = self.__scrap_odds_goals_part(soup)

            match["FHO 0.5"] = first_half_odds["O_U 0.5"]["OVER"]
            match["FHU 0.5"] = first_half_odds["O_U 0.5"]["UNDER"]
            match["FHO 1.5"] = first_half_odds["O_U 1.5"]["OVER"]
            match["FHU 1.5"] = first_half_odds["O_U 1.5"]["UNDER"]
            match["FHO 2.5"] = first_half_odds["O_U 2.5"]["OVER"]
            match["FHU 2.5"] = first_half_odds["O_U 2.5"]["UNDER"]

        # -> second half odds
        try:
            self.__chrome_driver.find_element_by_link_text("2nd Half").click()
        except selenium.common.exceptions.NoSuchElementException:
            print("2nd half do not exist")
        else:
            try:
                myElem = WebDriverWait(self.__chrome_driver, self.__delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'table-container')))
            except TimeoutException:
                print("Loading odds goals second half page took too much time!")
            soup = bs4.BeautifulSoup(self.__chrome_driver.page_source, "html.parser")
            second_half_odds = self.__scrap_odds_goals_part(soup)

            match["SHO 0.5"] = second_half_odds["O_U 0.5"]["OVER"]
            match["SHU 0.5"] = second_half_odds["O_U 0.5"]["UNDER"]
            match["SHO 1.5"] = second_half_odds["O_U 1.5"]["OVER"]
            match["SHU 1.5"] = second_half_odds["O_U 1.5"]["UNDER"]
            match["SHO 2.5"] = second_half_odds["O_U 2.5"]["OVER"]
            match["SHU 2.5"] = second_half_odds["O_U 2.5"]["UNDER"]

        # Draw no bet
        # -> full time odds
        self.__chrome_driver.find_element_by_link_text("DNB").click()
        try:
            myElem = WebDriverWait(self.__chrome_driver, self.__delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'table-container')))
        except TimeoutException:
            print("Loading odds no draw page took too much time!")

        soup = bs4.BeautifulSoup(self.__chrome_driver.page_source, "html.parser")
        draw_no_bet_odds_list = self.__scrap_average_values_list(soup)
        match["FTNDH"] = draw_no_bet_odds_list[0]
        match["FTNDA"] = draw_no_bet_odds_list[1]

        # first half odds
        try:
            self.__chrome_driver.find_element_by_link_text("1st Half").click()
        except selenium.common.exceptions.NoSuchElementException:
            print("1st half do not exist")
        else:
            try:
                myElem = WebDriverWait(self.__chrome_driver, self.__delay).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'table-container')))
            except TimeoutException:
                print("Loading odds no draw first half page took too much time!")
            soup = bs4.BeautifulSoup(self.__chrome_driver.page_source, "html.parser")

            draw_no_bet_odds_list = self.__scrap_average_values_list(soup)
            match["FHNDH"] = draw_no_bet_odds_list[0]
            match["FHNDA"] = draw_no_bet_odds_list[1]

        # second half odds
        try:
            self.__chrome_driver.find_element_by_link_text("2nd Half").click()
        except selenium.common.exceptions.NoSuchElementException:
            print("2nd half do not exist")

        else:
            try:
                myElem = WebDriverWait(self.__chrome_driver, self.__delay).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'table-container')))
            except TimeoutException:
                print("Loading odds no draw second half page took too much time!")
            soup = bs4.BeautifulSoup(self.__chrome_driver.page_source, "html.parser")

            draw_no_bet_odds_list = self.__scrap_average_values_list(soup)
            match["SHNDH"] = draw_no_bet_odds_list[0]
            match["SHNDA"] = draw_no_bet_odds_list[1]

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

    def __scrap_odds_goals_part(self, soup):
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
            "O_U 0.5": self.__scrap_odds_over_under(odds_05_div),
            "O_U 1.5": self.__scrap_odds_over_under(odds_15_div),
            "O_U 2.5": self.__scrap_odds_over_under(odds_25_div),
            "O_U 3.5": self.__scrap_odds_over_under(odds_35_div)
        }


    @staticmethod
    def __scrap_odds_over_under(odds_goals_div):
        odds_over_under_span_list = odds_goals_div.findAll("span", class_="avg chunk-odd nowrp")
        odds_dict = {"OVER": 0.0, "UNDER": 0.0}
        try:
            odds_dict = {
                "OVER": float(odds_over_under_span_list[1].find("a").get_text()),
                "UNDER": float(odds_over_under_span_list[0].find("a").get_text())
            }
        except (ValueError, AttributeError):
            print("Failed scrapping odds over/under")
        return odds_dict

    def create_wb(self):

        cols_names = [
            "HT", "AT",
            "DAY", "MONTH", "YEAR",
            "FTHG", "FTAG", "FHHG", "FHAG", "SHHG", "SHAG",
            "FTHO", "FTDO", "FTAO", "FHHO", "FHDO", "FHAO", "SHHO", "SHDO", "SHAO",
            "FTO 0.5", "FTU 0.5", "FTO 1.5", "FTU 1.5", "FTO 2.5", "FTU 2.5", "FTO 3.5", "FTU 3.5",
            "FHO 0.5", "FHU 0.5", "FHO 1.5", "FHU 1.5", "FHO 2.5", "FHU 2.5",
            "SHO 0.5", "SHU 0.5", "SHO 1.5", "SHU 1.5", "SHO 2.5", "SHU 2.5",
            "FTNDH", "FTNDA", "FHNDH", "FHNDA", "SHNDH", "SHNDA"
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
