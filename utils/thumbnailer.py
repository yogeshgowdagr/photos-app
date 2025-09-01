
import os
from PIL import Image
import pillow_heif
from config import PHOTO_FOLDER, THUMBNAIL_FOLDER, PHOTO_EXTENSIONS, THUMBNAIL_SIZE

def create_thumbnail(filename):
	ext = os.path.splitext(filename)[1].lower()
	src_path = os.path.join(PHOTO_FOLDER, filename)
	thumb_path = os.path.join(THUMBNAIL_FOLDER, filename)
	if not os.path.exists(src_path):
		return
	try:
		if ext == '.heic':
			heif_file = pillow_heif.open_heif(src_path)
			image = Image.fromarray(heif_file[0].data)
		else:
			image = Image.open(src_path)
		image.thumbnail(THUMBNAIL_SIZE)
		image.save(thumb_path, format='JPEG')
	except Exception as e:
		print(f"Error creating thumbnail for {filename}: {e}")

def generate_all_thumbnails():
	for fname in os.listdir(PHOTO_FOLDER):
		ext = os.path.splitext(fname)[1].lower()
		if ext in PHOTO_EXTENSIONS:
			thumb_path = os.path.join(THUMBNAIL_FOLDER, fname)
			if not os.path.exists(thumb_path):
				create_thumbnail(fname)
