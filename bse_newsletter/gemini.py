import vertexai
from vertexai.generative_models import GenerativeModel, Part


# TODO(developer): Update and un-comment below lines
project_id = "bse-newsletter"

vertexai.init(project=project_id, location="us-central1")

model = GenerativeModel(model_name="gemini-1.5-flash-001")


def ai_summary(prompt, pdf_file_uri):
    try:
        pdf_file = Part.from_uri(pdf_file_uri, mime_type="application/pdf")
        contents = [pdf_file, prompt]
        response = model.generate_content(contents)
        if response:
            print("Generated content successfully")
            return response.text
    except Exception as e:
        print(f"Error in Gemini Response (ai_summary in gemini.py): {e}")
    finally:
        print("Finished ai_summary")


PROMPT = """Instructions:

You will be given details of corporate actions from various companies, provided as PDF documents. Your task is to extract the relevant information from the PDF and create a brief summary for each corporate action, formatted for a newsletter. Each summary should include the essential details and a brief closing remark, prompting the reader to click for more information. Ensure that the response is consistent in format and tone. The "click here" button should be a hyperlink to https://www.bseindia.com/xml-data/corpfiling/AttachLive/ followed by the name of the PDF file.

Your Task:

Using the provided corporate action details in the PDF, extract the relevant information and create a summary in the format shown in the example. Ensure each section is concise, informative, and prompts the reader to click for more information. Maintain a consistent tone and structure throughout. Use https://www.bseindia.com/xml-data/corpfiling/AttachLive/ followed by the name of the PDF file for the "click here" hyperlink.

Here is an example summary for the provided PDF:

Saurashtra Cement Limited: Corporate Actions Update
Date: June 05, 2024

Key Corporate Announcements:
66th Annual General Meeting (AGM)
Date: Wednesday, 21st August 2024
Book Closure: 15th August 2024 - 21st August 2024
Record Date for Final Dividend: 14th August 2024
Purpose: Conduct AGM and approve final dividend for FY 2023-24
For detailed information, click the below link.

Stay tuned for more updates and ensure your contact details are up to date to receive timely notifications. Thank you for staying informed with our updates.

"""
