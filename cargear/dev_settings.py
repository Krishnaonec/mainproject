from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = True
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'static'), ]