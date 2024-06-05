import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_pdf_links():
    try:
        # Replace with the path to your ChromeDriver
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options)

        # Navigate to the website
        driver.get("https://www.bseindia.com/corporates/ann.html")

        # Wait for the category dropdown to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "btnSubmit")))

        category_dropdown = driver.find_element(By.ID, "ddlPeriod")

        # Select "Corp. Action" from the dropdown
        from selenium.webdriver.support.ui import Select

        select_category = Select(category_dropdown)
        select_category.select_by_visible_text("Corp. Action")

        # Find all elements with the ID "btnSubmit"
        submit_buttons = driver.find_elements(By.ID, "btnSubmit")

        # We want the first button (Submit button):
        if len(submit_buttons) > 0:
            first_submit_button = submit_buttons[0]

            # Scrolling to the element in case it's outside the viewport
            driver.execute_script("arguments[0].scrollIntoView();", first_submit_button)

            # Using Actions class for a more controlled click attempt
            actions = ActionChains(driver)
            actions.move_to_element(first_submit_button).click().perform()

        # Wait after reload till the records td tag is loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "lblann")))

        # Get the HTML content of the entire page
        html_content = driver.page_source

        # Close the browser
        driver.quit()

        # Processing the HTML content further using Beautiful Soup
        target_td = parse_results(html_content)
        announcement_tables = target_td.table.tbody.contents[6]  # tr tag in which there are announcement tables

        # print(announcement_tables)

        a_tags = announcement_tables.find_all("a", attrs={
            "target": "_blank",
            "class": "tablebluelink"})  # A list of pdf params like: bseindia.com{/xml-data... for eg.}
        return a_tags

    except Exception as e:
        print(f"Exception in get_pdf_links (in webscraping.py): {e}")
    finally:
        print("get_pdf_links execution complete")


# Returns the td tag containing the table for all announcement records
def parse_results(search_results_page):
    try:
        soup = BeautifulSoup(search_results_page, 'html.parser')
        target_td = soup.find('td', id="lblann")  # This will return the matching td element
        if target_td:
            print("Parse Results Received!")
            return target_td
        else:
            raise "Parse Results Not Received!"

    except Exception as e:
        print(f"Exception in parse_results (in webscraping.py): {e}")
    finally:
        print("parse_results execution complete")


# Download Pdf files and save them locally
def download_pdf(url, output_dir):
    try:
        response = requests.get(f"https://www.bseindia.com{url}")
        if response.status_code == 200:
            filepath = os.path.join(output_dir, url.split('/')[-1])
            with open(filepath, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {filepath}")
        else:
            raise f"Failed to download: {url} (download_pdf in webscraper.py)"

    except Exception as e:
        print(f"Exception in download_pdf (in webscraping.py): {e}")
    finally:
        print("download_pdf execution complete")
