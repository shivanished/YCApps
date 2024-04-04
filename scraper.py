from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import time
import re
import pandas as pd


def create_dataframe(link):
    filename = create_company_url_list(link)

    df = pd.DataFrame(columns=["Company", "Explanation", "Link", "Company Website", "Founders_Names", "Founder_Emails", "Company Info"])

    companies = open(filename)

    for company in companies:
        new_row = {"Link": company.strip()}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    df = collect_all_company_data(df)

    return df

def create_company_url_list(link):
    driver = webdriver.Chrome()
    driver.get(link)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "_section_1rnar_146")))
    time.sleep(2)

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    div = soup.find('div', class_="_section_1rnar_146 _results_1rnar_327")
    links = div.find_all('a')

    pattern = re.compile(r'/companies/')
    company_urls = [link.get('href') for link in links if pattern.search(link.get('href'))]

    driver.quit()

    filename = 'yc-companies.txt'
    with open(filename, 'w') as file:
        for company in company_urls:
            file.write('https://www.ycombinator.com/' + company + '\n')

    return filename


def collect_all_company_data(df):
    for index, row in df.iterrows():
        url = row['Link']
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            page = soup.find('div', class_="mx-auto max-w-ycdc-page")

            company_name = page.find('h1', class_="font-extralight")
            df.at[index, 'Company'] = company_name.text.strip()

            content_section = page.find('section', class_="relative isolate z-0 border-retro-sectionBorder sm:pr-[13px] ycdcPlus:pr-0 pt-2 sm:pt-4 lg:pt-6 pb-2 sm:pb-4 lg:pb-6")
            content_paragraphs = content_section.find('section', class_="relative isolate z-0 border-retro-sectionBorder sm:pr-[13px] ycdcPlus:pr-0 pt-1 sm:pt-2 lg:pt-3 pb-1 sm:pb-2 lg:pb-3")
            full_content = content_paragraphs.find('p', class_="whitespace-pre-line")
            df.at[index, 'Explanation'] = full_content.text.strip()

            founders_paragraphs = page.find('div', class_="space-y-5")
            if founders_paragraphs:
                founders_names = founders_paragraphs.find_all('h3', class_="text-lg font-bold")
                founders_names_text = [tag.text.strip() for tag in founders_names]
                df.at[index, 'Founders_Names'] = founders_names_text

            # large_div = page.find('div', class_='flex flex-col gap-8 sm:flex-row')
            # website_section = large_div.find('div', class_='my-8 mb-4"')
            website = page.find('div', class_='group flex flex-row items-center px-3 leading-none text-linkColor')
            website_url = website.find('a').get('href')

            domain_regex = r'https?://(?:www\.)?([^/?]+)'
            domain_match = re.search(domain_regex, website_url)
            if domain_match:
                cleaned_website_url = domain_match.group(1)
                df.at[index, 'Company Website'] = cleaned_website_url

    return df