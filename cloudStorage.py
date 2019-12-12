from config import config

from google.cloud import storage


def uploadImage(image,filename):
    gcs = storage.Client()

    bucket = gcs.get_bucket(config["CLOUD_STORAGE_BUCKET"])

    blob = bucket.blob("avatar/" + filename)

    blob.upload_from_string(image.read(), content_type=image.content_type)

    return blob.public_url
