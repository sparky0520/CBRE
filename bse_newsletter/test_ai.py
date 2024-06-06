from gemini import ai_summary, PROMPT
from gcs_upload import upload_to_gcs, PDF_DIR, BUCKET_NAME
import os

gs_links = []
for i in os.listdir(PDF_DIR):
    try:
        if i.endswith(".pdf"):
            print(f"Uploading {i}")
            local_file_path = os.path.join(PDF_DIR, i)
            gcs_uri = upload_to_gcs(local_file_path, BUCKET_NAME, f"{PDF_DIR}/{i}")
            gs_links.append(gcs_uri)

    except Exception as e:
        print(f"Exception in test_ai.py (uploading): {e}")
    finally:
        print("\n*******************")
        print("Operation Completed!")
        print("*******************\n")

for link in gs_links:
    filename = "pdf\\" + link.split('/')[-1]
    try:
        print(f"Getting AI Summary for {filename}")
        ai_response = ai_summary(PROMPT, link)
        with open("GeminiResponseLog.txt", "a") as file:
            file.write(filename + '\n\n')
            file.write(ai_response)
            file.write('\n\n\n')
        print(f"AI Summary Received for {filename}")
    except Exception as e:
        print(f"Exception in test_ai.py (ai_summary): {e}")
    finally:
        print("\n*******************")
        print("Operation Completed!")
        print("*******************\n")
