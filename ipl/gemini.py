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


def write_csv(data, filename):
    # Split the data into rows
    rows = [row.split(",") for row in data.split("\n")]
    # Write rows to a CSV file
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)
    print(f"Created {filename}")


PROMPT = """Turn data inside this pdf into csv format with headers best suiting the data. 
            Give me the winner of the tournament. At the last give only the year in the last row."""
CSV_DIR = 'csv'  # Directory in which all csv files are stored.

# filename = f"csv/{year}.csv"
# write_csv(response, filename)
