import os
from PIL import Image
import pillow_heif
from config import PHOTO_FOLDER, THUMBNAIL_FOLDER, PHOTO_EXTENSIONS, THUMBNAIL_SIZE

# Register HEIF/HEIC opener once at startup
pillow_heif.register_heif_opener()

def create_thumbnail(filename):
    ext = os.path.splitext(filename)[1].lower()
    src_path = os.path.join(PHOTO_FOLDER, filename)
    thumb_path = os.path.join(THUMBNAIL_FOLDER, filename)

    if not os.path.exists(src_path):
        return

    try:
        # Pillow will now handle .heic files too
        image = Image.open(src_path)
        image.thumbnail(THUMBNAIL_SIZE)

        # Always save thumbnails as JPEG
        thumb_path = os.path.splitext(thumb_path)[0] + ".jpg"
        image.save(thumb_path, format="JPEG")

    except Exception as e:
        print(f"Error creating thumbnail for {filename}: {e}")

def generate_all_thumbnails():
    for fname in os.listdir(PHOTO_FOLDER):
        ext = os.path.splitext(fname)[1].lower()
        if ext in PHOTO_EXTENSIONS:
            thumb_path = os.path.join(THUMBNAIL_FOLDER, fname)
            if not os.path.exists(thumb_path):
                create_thumbnail(fname)
