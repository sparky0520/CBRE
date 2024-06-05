import vertexai
from vertexai.generative_models import GenerativeModel, Part

# TODO(developer): Update and un-comment below lines
project_id = "bse-newsletter"

vertexai.init(project=project_id, location="us-central1")

model = GenerativeModel(model_name="gemini-1.5-flash-001")


def ai_summary(prompt, pdf_file_uri):
    pdf_file = Part.from_uri(pdf_file_uri, mime_type="application/pdf")
    contents = [pdf_file, prompt]
    response = model.generate_content(contents)
    if response:
        return response.text
    else:
        raise f"Error in Gemini Response (ai_summary in gemini.py)"


PROMPT = """
Please extract the IPL schedule data from the provided PDF and convert it into CSV format:
- Ensure no data in the PDF contains commas. Replace commas with spaces before converting to CSV format.
- Accurately extract and place the year of the season.
- Extract and include the winner of the IPL season, placing this information after the last match record.
- Ensure all fields are accurately populated without extra whitespace or missing values.

Example CSV format:
Date, Year, Time, Teams, Venue, Match Type, Result
March 23 2019, 2019, 8:00 PM IST, Chennai Super Kings vs Royal Challengers Bangalore, MA Chidambaram Stadium Chepauk Chennai, League, Chennai Super Kings Won by 7 Wicket(s)
...
...
Winner of season: Mumbai Indians
2019
"""