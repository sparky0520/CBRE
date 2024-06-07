import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Returns the html response received after selecting Corp. Action and Clicking submit on 
# bseindia.com/corporates/ann.html
def corp_actions_html():
    try:
        # Replace with the path to your ChromeDriver
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options)

        # Navigate to the website
        driver.get("https://www.bseindia.com/corporates/ann.html")

        # Wait for all elements till submit button to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "submit")))

        category_dropdown = driver.find_element(By.ID, "ddlPeriod")

        # Select "Corp. Action" from the dropdown
        from selenium.webdriver.support.ui import Select

        select_category = Select(category_dropdown)
        select_category.select_by_visible_text("Corp. Action")

        # Find input button with the NAME "submit"
        submit_button = driver.find_element(By.NAME, "submit")

        # Scrolling to the element in case it's outside the viewport
        driver.execute_script("arguments[0].scrollIntoView();", submit_button)

        # Using Actions class for a more controlled click attempt
        actions = ActionChains(driver)
        actions.move_to_element(submit_button).click().perform()

        # Wait after reload till the records td tag is loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "lblann")))

        html_content = driver.page_source
        # Close the browser
        driver.quit()
        return str(html_content)
    except Exception as e:
        print(f"Exception in corp_actions_html (in webscraping.py): {e}")
    finally:
        print("corp_actions_html execution complete")


# Returns the td tag containing all the tables of corp action announcements
def parse_results(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        target_td = soup.find('td', id="lblann")  # This will return the matching td element (main)
        target_td = target_td.table.tbody.contents[6].td  # td tag in which there are announcement tables (descendent)
        if target_td:
            return str(target_td)
        else:
            raise "Parse Results Not Received!"

    except Exception as e:
        print(f"Exception in parse_results (in webscraping.py): {e}")
    finally:
        print("parse_results execution complete")


# Returns a list containing the announcement tables containing dividend or bonus keywords
def dividend_or_bonus_filter(target_td):
    try:
        soup = BeautifulSoup(target_td, "html.parser")
        content = soup.find_all('span', attrs={
            'ng-bind-html': "cann.HEADLINE"
        })

        def filter_func(span_tag):
            lower_text = span_tag.string.lower()
            return "bonus" in lower_text or "dividend" in lower_text

        valid_tables = []
        if content:
            valid_spans = filter(filter_func, content)
            for span in valid_spans:
                valid_tables.append(str(span.find_parent('table')))
            return valid_tables
        else:
            print("No Span tags found (dividend_or_bonus_filter in webscraper.py)")
    except Exception as e:
        print(f"Exception in dividend_or_bonus_filter (in webscraper.py): {e}")
    finally:
        print("dividend_or_bonus_filter execution complete")


# Takes an announcement table html and gives pdf link (param)
def get_pdf_links(announcement_table):
    try:
        soup = BeautifulSoup(announcement_table, "html.parser")
        a_tag = soup.find("a", attrs={
            "target": "_blank",
            "class": "tablebluelink"})
        if a_tag:
            return str("https://www.bseindia.com" + a_tag.get('href'))
    except Exception as e:
        print(f"Exception in get_pdf_links (in webscraping.py): {e}")
    finally:
        print("get_pdf_links execution complete")


# Download Pdf files and save them locally
def download_pdf(url, output_dir):
    try:
        headers = {  # Required to simulate a browser sending a request
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            filepath = os.path.join(output_dir, url.split('/')[-1])
            with open(filepath, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {filepath}")
        else:
            print(f"Error Status Code: {response.status_code}")
    except Exception as e:
        print(f"Exception in download_pdf (in webscraping.py): {e}")
    finally:
        print("download_pdf execution complete")
