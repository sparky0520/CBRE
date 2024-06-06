import os

from google.cloud import storage


def upload_to_gcs(local_file_path, bucket_name, destination_blob_name):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(local_file_path)
        gcs_uri = f'gs://{bucket_name}/{destination_blob_name}'
        print(f"Uploaded PDF to {gcs_uri}")
        os.remove(local_file_path)
        print(f"Removed {local_file_path}")
        return gcs_uri
    except Exception as e:
        print(f"Exception in upload_to_gcs (gcs_upload): {e}")
    finally:
        print("Upload to gcs completed.")


BUCKET_NAME = 'bse-newsletter-test'  # Google Cloud Storage Bucket
PDF_DIR = "pdf"  # Directory in which all pdf files are stored
