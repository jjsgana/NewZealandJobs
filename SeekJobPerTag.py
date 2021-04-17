from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from matplotlib import pyplot as plt

# OK  1.- Create a list with the URLs to read
#   > Define URL to read
#   > Capture the tags and save them in a list
#   > Function: Create the list with all the URLs with the tags to read
# OK 2.- Scrapp each row of the list and return the number results with that tag
# OK 3.- Save the number returned in a new list: a = [{ python = 13, powerbi = 5}]
#   > Join lists: "jobs results" and "Tags Captured"
# OK 4.- Create a bar chart with the results to compare it with matplotlib


def main():
    CaptureInputFromUser()
    CreateListOfUrls()
    ScrappSeekPage()
    CreatePandasDataFrame()
    CreateChart()


def CaptureInputFromUser():
    global location_to_search
    location_to_search = input(
        'Write location to search (use "-" for spaces):  ')  # location

    # TagstoSearch
    global tags_to_search
    tags_to_search = input(
        'Please enter tags to search separated by comma (,): ').split(sep=',')  # URL tags depending on input of user

    return location_to_search, tags_to_search


def CreateListOfUrls():
    global urls_to_read
    urls_to_read = []
    # URL should look like this: https://www.seek.com.au/data-analyst-jobs/

    # URL tags by default - Not modify
    main_url = "https://www.seek.co.nz/"
    job_in_url = "-jobs"
    location_in_url = "/in-"

    # Concatenate all URL parameters
    for tag in tags_to_search:
        url_to_read = main_url + tag + job_in_url + location_in_url + location_to_search
        urls_to_read.append(url_to_read)

    print(
        f' >>> {len(urls_to_read)} Tag(s) will be searched in {location_to_search}')

    return urls_to_read


def ScrappSeekPage():

    driver = "C://chromedriver.exe"
    chrome = webdriver.Chrome(driver)
    chrome.minimize_window()
    global jobs_per_tag
    jobs_per_tag = []

    for row, tag in zip(urls_to_read, tags_to_search):
        # Open job_page and start scrapping
        chrome.get(row)
        src = chrome.page_source
        soup = BeautifulSoup(src, 'html.parser')
        time.sleep(0.3)
        jobs_numbers_detected_in_url = int(soup.find(
            "span", {"id": "SearchSummary"}).find("h1").find("strong", {"class": "_7ZnNccT"}).get_text().strip().replace(',', ''))

        jobs_per_tag.append(jobs_numbers_detected_in_url)

        print(
            f'##### analyzing... {jobs_numbers_detected_in_url} jobs found in "{location_to_search}" with the tag "{tag}".')

    return jobs_per_tag


def CreatePandasDataFrame():

    global df
    df = pd.DataFrame(
        {'Tag': tags_to_search, 'Jobs': jobs_per_tag, 'Location': location_to_search})
    return df


def CreateChart():
    plt.bar(df.Tag, df.Jobs)
    plt.ylabel('Number of jobs available to apply')
    plt.title(f'Jobs in {location_to_search}, New Zealand')
    plt.show()


main()
