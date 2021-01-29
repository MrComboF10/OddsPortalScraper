# OddsPortalScraper
Scrap seasons leagues odds from the site https://www.oddsportal.com/

## Usage
### Scrap one league from season year1 to season year2
- Go to file config.json and edit
- Run application.py
### Scrap multiple leagues or specifics seasons
- Create other application
- Import and use oddsportal.py API
- Run that application

## Input
- The input will be used to create the page link to scrap.<br/>
- All the inputs must be in lower case and have a "-" if it has a space
- "start_season_year" and "last_season_year" must be integers
- It is recommended to go to https://www.oddsportal.com/ and check if the inputs are correct

## Output
- The output will be an Excel with some of the odds from the seasons of the league
- Each page of the Excel Workbook has all the matches of one season
- Each column correspond to the following legend:

### Columns Legend
HomeTeam - HomeTeam
AwayTeam - AwayTeam
FTHG - Final_Time_Home_Goals
FTAH - Final_Time_Away_Goals
FHHG - First_Half_Home_Goals
FHAG - First_Half_Away_Goals
SHHG - Second_Half_Home_Goals
SHAG - Second_Half_Away_Goals
HO - Home_Team_Winning_Odd
DO - Draw_Odd
AO - Away_Team_Winning_Odd
FTO0.5 - Final_Time_Over_0.5_Goals
FTU0.5 - Final_Time_Under_0.5_Goals
FTO1.5 - Final_Time_Over_1.5_Goals
FTU1.5 - Final_Time_Under_1.5_Goals
FTO2.5 - Final_Time_Over_2.5_Goals
FTU2.5 - Final_Time_Under_2.5_Goals
FTO3.5 - Final_Time_Over_3.5_Goals
FTU3.5 - Final_Time_Under_3.5_Goals
FHO0.5 - First_Half_Over_0.5_Goals
FHU0.5 - First_Half_Under_0.5_Goals
FHO1.5 - First_Half_Over_1.5_Goals
FHU1.5 - First_Half_Under_1.5_Goals
FHO2.5 - First_Half_Over_2.5_Goals
FHU2.5 - First_Half_Under_2.5_Goals
SHO0.5 - Second_Half_Over_0.5_Goals
SHU0.5 - Second_Half_Under_0.5_Goals
SHO1.5 - Second_Half_Over_1.5_Goals
SHU1.5 - Second_Half_Under_1.5_Goals
SHO2.5 - Second_Half_Over_2.5_Goals
SHU2.5 - Second_Half_Under_2.5_Goals
NDH - No_Draw_Home_Team_Winning_Odd
NDA - No_Draw_Away_Team_Winning_Odd

