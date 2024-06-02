import requests
from google.cloud import storage
import os


def upload_to_gcs(local_file_path, bucket_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_file_path)
    gcs_uri = f'gs://{bucket_name}/{destination_blob_name}'
    print(f"Uploaded PDF to {gcs_uri}")
    return gcs_uri


BUCKET_NAME = 'ipl_schedule_pdfs_test'   # Google Cloud Storage Bucket
PDF_DIR = "pdfs"    # Directory in which all pdf files are stored


# local_file_path = 'pdfs/ipl-2019-schedule-pdf.pdf'
# upload_to_gcs(local_file_path,"ipl_schedule_pdfs","pdfs/ipl-2019-schedule-pdf.pdf")
# os.remove(local_file_path)
