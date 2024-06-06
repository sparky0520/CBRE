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


PROMPT = """
Instructions:

Using the provided corporate action details in the PDF, extract the relevant information and create a summary in the format shown in the example. Ensure each section is concise, informative, and prompts the reader to click for more information. Maintain a consistent tone and structure throughout.

Here is an example summary for the provided PDF:

<html>
    <head></head>
    <body>
        <p><strong>Saurashtra Cement Limited: Corporate Actions Update</strong></p>
        <p><strong>Date:</strong> June 05, 2024</p>
        <p><strong>Key Corporate Announcements:</strong></p>
        <ul>
            <li><strong>66th Annual General Meeting (AGM)</strong></li>
            <ul>
                <li><strong>Date:</strong> Wednesday, 21st August 2024</li>
                <li><strong>Book Closure:</strong> 15th August 2024 - 21st August 2024</li>
                <li><strong>Record Date for Final Dividend:</strong> 14th August 2024</li>
                <li><strong>Purpose:</strong> Conduct AGM and approve final dividend for FY 2023-24</li>
            </ul>
        </ul>
        <p>For detailed information, click the below link.</p>
        <p>Stay tuned for more updates and ensure your contact details are up to date to receive timely notifications. Thank you for staying informed with our updates.</p>
    </body>
</html>
"""
