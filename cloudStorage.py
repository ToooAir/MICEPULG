from config import config

from google.cloud import storage


def uploadImage(image, filename):
    gcs = storage.Client()

    bucket = gcs.get_bucket(config["CLOUD_STORAGE_BUCKET"])

    blob = bucket.blob("avatar/" + filename)

    blob.upload_from_string(image.read(), content_type=image.content_type)

    return blob.public_url


def deleteImage(url):
    gcs = storage.Client()

    bucket = gcs.get_bucket(config["CLOUD_STORAGE_BUCKET"])

    filename = url.split("/")[-1]

    blob = bucket.blob("avatar/" + filename)
    print(blob.exists())
    if blob.exists():
        blob.delete()
