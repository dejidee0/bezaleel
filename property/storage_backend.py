import uuid
from django.core.files.storage import Storage
from io import BytesIO
from supabase import create_client
from django.conf import settings
import mimetypes

class SupabaseStorage(Storage):
    def __init__(self):
        self.client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        self.bucket = settings.SUPABASE_STORAGE_BUCKET

    def _open(self, name, mode="rb"):
        try:
            response = self.client.storage.from_(self.bucket).download(name)
            return BytesIO(response)  # Convert to file-like object
        except Exception as e:
            raise FileNotFoundError(f"File not found in Supabase: {name}") from e

    def _save(self, name, content):
        file_data = content.read()  # Read file as bytes
        directory, filename = name.rsplit("/", 1)

        # Generate unique filename
        new_filename = f"{filename.split('.')[0]}_{uuid.uuid4()}.{filename.split('.')[-1]}"
        new_name = f"{directory}/{new_filename}"

        # Determine content type (MIME type)
        content_type, _ = mimetypes.guess_type(filename)
        if not content_type:
            content_type = "application/octet-stream"  # Default MIME type

        # Upload to Supabase
        response = self.client.storage.from_(self.bucket).upload(
            path=new_name,
            file=file_data,  # File in bytes
            file_options={"content-type": content_type}
        )

        if not response:
            raise ValueError("File upload failed.")

        return new_name  # Return stored filename

    def exists(self, name):
        directory = "/".join(name.split("/")[:-1])  # Extract directory
        files = self.client.storage.from_(self.bucket).list(path=directory)  # List only relevant files

        return any(file['name'] == name for file in files)

    def url(self, name):
        return f"{settings.SUPABASE_URL}/storage/v1/object/public/{self.bucket}/{name}"
