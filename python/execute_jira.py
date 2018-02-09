import sys
from rest_client import Downloader

url = sys.argv[1]
filename = sys.argv[2]

downloader = Downloader(url, filename)
downloader.save()
