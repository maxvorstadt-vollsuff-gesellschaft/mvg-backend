import json
from minio import Minio
import os

minio_client = Minio(
    endpoint="minio.mvg.life",
    access_key="b0Itoi8qNhrPGrqSkIKn",
    secret_key="EKzBso5IwNBvYDW4P5AdOURAfWdI7waNwqbPkZnc",
    secure=True
)

BUCKET_NAME = "recipes"

def upload_recipe_image(file_data, filename: str) -> str:
    """
    Uploads an image to MinIO and returns the permanent public URL
    
    Args:
        file_data: Either bytes or a file-like object
        filename: Original filename with extension
    """
    # Convert to bytes if file_data is a file-like object
    if hasattr(file_data, 'read'):
        file_data = file_data.read()
    
    # Ensure bucket exists
    if not minio_client.bucket_exists(BUCKET_NAME):
        minio_client.make_bucket(BUCKET_NAME)
        # Set bucket policy to public read
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"},
                    "Action": ["s3:GetObject"],
                    "Resource": [f"arn:aws:s3:::{BUCKET_NAME}/*"]
                }
            ]
        }
        minio_client.set_bucket_policy(BUCKET_NAME, json.dumps(policy))

    # Generate unique filename
    import uuid
    file_extension = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"

    # Create BytesIO object for MinIO upload
    from io import BytesIO
    file_data_io = BytesIO(file_data)

    # Upload file
    minio_client.put_object(
        bucket_name=BUCKET_NAME,
        object_name=unique_filename,
        data=file_data_io,
        length=len(file_data),
        content_type=f"image/{file_extension}"
    )

    # Generate permanent URL
    return f"https://minio.mvg.life/{BUCKET_NAME}/{unique_filename}"


def cleanup_bucket():
    objects = minio_client.list_objects(BUCKET_NAME)
    for obj in objects:
        minio_client.remove_object(BUCKET_NAME, obj.object_name)
