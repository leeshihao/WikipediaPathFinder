import requests
import re
startArticle = "https://en.wikipedia.org/wiki/Stanford_University"
endArticle = "https://en.wikipedia.org/wiki/Samsung"

r = requests.get(startArticle)
content = str(r.content)

print(set(re.findall("\"/wiki/([^\":]*)\"",content)))