import requests
from bs4 import BeautifulSoup
import os
from gemini import ai_pdf_to_text


# Returns the search html response given by google for "filetype:pdf ipl schedule {year}"
def google_search(year):
    url = f"https://www.google.com/search?q=filetype%3Apdf+ipl+schedule+{year}"
    headers = {  # Required to simulate a browser sending a request
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        raise "Error searching on Google (google_search in webscraper.py)"


# Returns the pdf url of ipl schedule doc
def parse_results(search_results_page):
    soup = BeautifulSoup(search_results_page, 'html.parser')
    target_a_tag = soup.find_all('a', jsname="UWckNb")[0]
    if target_a_tag:
        pdf_url = target_a_tag['href']
        return pdf_url
    else:
        raise "Failed to get pdf url from search results (parse_results in webscraper.py)"


# Download Pdf files and save them locally
def download_pdf(url, output_dir):
    response = requests.get(url)
    if response.status_code == 200:
        filepath = os.path.join(output_dir, url.split('/')[-1])
        with open(filepath, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {filepath}")
    else:
        raise f"Failed to download: {url} (download_pdf in webscraper.py)"
