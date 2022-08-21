from selenium import webdriver
from bs4 import BeautifulSoup
import chromedriver_binary,time

def get_Trending():
    driver = webdriver.Chrome()
    driver.get("https://scratch.mit.edu/explore/projects/all")
    time.sleep(1.5)

    soup = BeautifulSoup(driver.page_source,'html.parser')
    trend = list()

    for i in range(1,17):
        found = soup.select_one(f"#projectBox > div > div > div:nth-of-type({i}) > div > div > a")
        project_data = {'title':found.contents[0], 'id':found.attrs['href'].replace("/","").replace("projects","")}
        trend.append(project_data)
        return trend

if __name__ == "__main__":
    res = get_Trending()
    print(res)
 
