import requests


class Downloader:
    def __init__(self, url, filename):
        self.url = url
        self.filename = filename

    def save(self):
        response = requests.get(self.url)
        file = open(self.filename, "w", encoding="utf-8")
        result = response.text

        result = result.replace("&amp;", "&")
        result = result.replace("&quot;", "\"")
        result = result.replace("&apos;", "\'")
        result = result.replace("&lt;", "<")
        result = result.replace("&gt;", ">")
        result = result.replace("&nbsp;", " ")

        file.write(result)
        file.close()


#url = "https://jira.spring.io/sr/jira.issueviews:searchrequest-xml/temp/SearchRequest.xml?jqlQuery=project+%3D+SPR&tempMax=1000"
#filename = "jira.xml"
#downloader = Downloader(url, filename)
#downloader.save()