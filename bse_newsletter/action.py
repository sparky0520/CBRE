from webscraper import corp_actions_html, parse_results, dividend_or_bonus_filter, get_pdf_links, download_pdf
import os
from gcs_upload import upload_to_gcs, PDF_DIR, BUCKET_NAME
from gemini import ai_summary, PROMPT
from mail import send_email, SENDER, APP_PASSWORD, SUBJECT


# All tasks to be performed to send info through newsletter
def send_news():
    print("Sending News....")

    # Downloading pdf of matching announcement
    announcements = dividend_or_bonus_filter(parse_results(corp_actions_html()))
    for announcement in announcements:
        link = get_pdf_links(announcement)
        download_pdf(link, PDF_DIR)

    # Uploading the files to Google Cloud Storage
    gs_links = []
    for file in os.listdir(PDF_DIR):
        if file.endswith(".pdf"):
            filename = os.path.join(PDF_DIR, file)
            link = upload_to_gcs(filename, BUCKET_NAME, destination_blob_name=f"{PDF_DIR}/{file}")
            gs_links.append(link)

    # Asking Gemini 1.5 Flash for pdf summary
    mail_body = ''
    for link in gs_links:
        ai_result = ai_summary(PROMPT, link)
        link = "https://www.bseindia.com/xml-data/corpfiling/AttachLive/" + link.split("/")[-1]
        summary = ai_result + link
        # Logging response
        with open('text/GeminiResponseLog.txt', 'a', encoding='utf-8') as file:
            file.write('')
            file.write(summary + '\n\n')
        mail_body += f"{summary}\n\n\n\n"

    # Mailing the mail_body to target
    if mail_body:
        send_email(SENDER, APP_PASSWORD, SENDER, SUBJECT, mail_body)
    else:
        print("\n***No updates to mail.***\n")