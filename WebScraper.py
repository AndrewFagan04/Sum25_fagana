from urllib.request import urlopen

url = "https://sunypoly.edu/library/hours-spaces/library-hours.html"

page = urlopen(url)

html_bytes = page.read()
html = html_bytes.decode("utf-8")

print(html)