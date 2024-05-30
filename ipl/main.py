from webscraper import google_search, parse_results, download_pdf
from gcs_upload import upload_to_gcs,BUCKET_NAME,PDF_DIR
import os
from gemini import ai_pdf_to_text,write_csv,CSV_DIR,PROMPT

# To get records of all years
for year in range(2008,2025):
    try:
        html_response = google_search(year)     # Returns html of search result page
        pdf_url = parse_results(html_response)  # Gets the pdf url from html returned
        download_pdf(pdf_url,output_dir=PDF_DIR)    # Downloads the pdf
    except Exception as e:
        print(e)
    finally:
        print("PDF Download Phase Completed.")

filenames = os.listdir(PDF_DIR)
for i in filenames:
    try:
        local_file_path = f"{PDF_DIR}/{i}"       # pdfs/file.pdf - format
        # Uploading to bucket
        gcs_uri = upload_to_gcs(local_file_path,BUCKET_NAME,destination_blob_name=local_file_path)
        os.remove(local_file_path)              # Remove pdf from local storage after uploading

        csv_response = ai_pdf_to_text(PROMPT,gcs_uri)   # Getting csv summary from Gemini 1.5 flash
        year = csv_response[-4:]            # year - which is name of created csv file
        filename = f"{CSV_DIR}/{year}.csv"  # csv/year.csv - format
        write_csv(csv_response,filename)    # write AI response to csv file with formatting
    except Exception as e:
        print(e)
    finally:
        print("AI response and processing Phase Completed.")
