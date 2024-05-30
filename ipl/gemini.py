import vertexai
from vertexai.generative_models import GenerativeModel, Part

# TODO(developer): Update and un-comment below lines
project_id = "ipl-cbre"

vertexai.init(project=project_id, location="us-central1")

model = GenerativeModel(model_name="gemini-1.5-flash-001")


def ai_pdf_to_text(prompt, pdf_file_uri):
    pdf_file = Part.from_uri(pdf_file_uri, mime_type="application/pdf")
    contents = [pdf_file, prompt]
    response = model.generate_content(contents)
    if response:
        return response.text
    else:
        raise f"Error in Gemini Response (ai_text_to_pdf in gemini.py)"


# response = ai_pdf_to_text(,"gs://ipl_schedule_pdfs/pdfs/ipl-2019-schedule-pdf.pdf")
# year = response[-4:]


import csv


def write_csv(rows, filename):
    # Write rows to a CSV file
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)
    print(f"Created {filename}")


PROMPT = """Please extract the IPL schedule data from the provided PDF in the following CSV format:
- Columns: According to data.
- Include only the match schedule details (one row per match).
- Ensure that the year of the season is accurately extracted and included in the last row.
- Extract the winner of the IPL season, placed after the last match record.
- Place the year of the IPL season in the last row so that it can be used to name the CSV file.
- Ensure all fields are accurately populated without extra whitespace or missing values.

Example CSV format:
Date, Year, Time, Teams, Venue, Match Type, Result
March 23, 2019, 8:00 PM IST, Chennai Super Kings vs Royal Challengers Bangalore, MA Chidambaram Stadium, Chepauk, Chennai, League, Chennai Super Kings Won by 7 Wicket(s)
...
...
Winner of season: Mumbai Indians
2019
"""
CSV_DIR = 'csv'  # Directory in which all csv files are stored.

# filename = f"csv/{year}.csv"
# write_csv(response, filename)
