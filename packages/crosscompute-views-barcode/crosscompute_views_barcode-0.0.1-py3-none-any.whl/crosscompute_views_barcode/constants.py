from pathlib import Path


PACKAGE_FOLDER = Path(__file__).parent
TEMPLATES_FOLDER = PACKAGE_FOLDER / 'templates'


BARCODE_JS_URI = 'https://unpkg.com/html5-qrcode'
FRAMES_PER_SECOND = 25
SCANNER_WIDTH_IN_PIXELS = 256
SCANNER_HEIGHT_IN_PIXELS = 256
