from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd

# <COLLECT ALL GAME URLS>

url = "https://www.baseball-reference.com/leagues/MLB/2018-schedule.shtml"
driver = webdriver.Chrome()
driver.get(url)

content_div = None
boxscoreURLs = []
if (driver.find_element_by_id('content')):
    content_div = driver.find_element_by_id('content')

if(content_div.find_elements_by_tag_name('em')):
    boxscoreDriver = content_div.find_elements_by_tag_name('em')
    for boxscoreEM in boxscoreDriver:
        score = boxscoreEM.find_element_by_tag_name('a')
        scoreURL = score.get_attribute('href')
        if ("/boxes/" in scoreURL):
            boxscoreURLs.append(scoreURL)
driver.close()

scoreURL_df = pd.DataFrame(boxscoreURLs)
scoreURL_df.to_csv("boxscore-URL.csv")

# </COLLECT ALL GAME URLS>

# <COLLECT EACH GAME LINEUP AND SCORE>

scoreURL_df = pd.read_csv("boxscore-URL.csv", names=["URL"])
boxscoreURLs = scoreURL_df.URL

startPos = currentPos = 0

for boxscore in boxscoreURLs[startPos:]:
    hrefLists = []
    namesLists = []
    counter = 0
    twoTeams = []
    twoScores = []

    driver = webdriver.Chrome()
    driver.get(boxscore)
    time.sleep(1)

    teamNames = driver.find_elements_by_xpath("//*[contains(@itemprop,'name')]")
    for teamName in teamNames:
        if counter < 2:
            if teamName.text != "":
                twoTeams.append(teamName.text)
                counter = counter + 1

    if driver.find_elements_by_class_name("scores"):
        teamScores = driver.find_elements_by_class_name("scores")
        for scores in teamScores:
            teamScore = scores.find_elements_by_class_name("score")
            for score in teamScore:
                twoScores.append(score.text)

        lineups = driver.find_element_by_id('div_lineups')
        tbodies = lineups.find_elements_by_tag_name('tbody')
        for tbody in tbodies:
            playerhrefs = []
            playerNames = []
            playerCells = tbody.find_elements_by_tag_name('a')
            for playerCell in playerCells:
                playerNames.append(playerCell.text)
                playerhrefs.append(playerCell.get_attribute('href'))
            
            hrefLists.append(playerhrefs)
            namesLists.append(playerNames)

    gameScore = pd.DataFrame([[twoTeams[0], twoTeams[1], twoScores[0], twoScores[1], namesLists[0], namesLists[1], hrefLists[0], hrefLists[1]]], columns=['Team Name', 'Opponent Name', 'Team Score', 'Opponent Score', 'Team Roster', 'Opponent Roster', 'Team Hrefs', 'Opponent Hrefs'])
    with open('baseball-lineups.csv', 'a') as f:
        gameScore.to_csv(f, mode='a', header=False)

    print(currentPos)
    currentPos += 1

    driver.close()

# </COLLECT EACH GAME LINEUP AND SCORE>