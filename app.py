from flask import Flask
from flask import jsonify

from cloudscraper import CloudScraper
from cloudscraper.exceptions import CloudflareChallengeError
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

scraper = CloudScraper()
URL = "https://nekopoi.care"

def req_nekopoi_or_error_v2(URL):
    try:
        req = scraper.get(URL)
        return req
    except CloudflareChallengeError:
        return jsonify({
            "error": "IP blocked"
        }), 400

@app.route("/")
def home():
    req = req_nekopoi_or_error_v2(URL)
    parse = BeautifulSoup(req.text, "html.parser")

    # Latest posts
    postsElement = parse.find_all(class_="eropost")
    posts = []
    for post in postsElement:
        thumb = post.find(class_="eroimg").find("img").get("src")
        title = post.find(class_="eroinfo").find("h2").text.strip()
        url = post.find(class_="eroinfo").find("h2").find("a")["href"]
    
        posts.append({
            "thumb": thumb,
            "title": title,
            "url": url,
        })

    # Latest hentai
    latestHentaiList = parse.find(class_="animeseries").find_all("li")
    latestHentai = []
    for hentai in latestHentaiList:
        anchor = hentai.find("a")
        thumb = anchor.find("img")["src"]
        title = anchor.find(class_="title").text.strip()
        url = anchor["href"]

        latestHentai.append({
            "thumb": thumb,
            "title": title,
            "url": url,
        })

    # Latest JAV
    latestJavList = parse.find(class_="videoarea").find_all("li")
    latestJav = []
    for jav in latestJavList:
        anchor = jav.find(class_="fuck").find("a")
        thumb = anchor.find("img")["src"]
        title = anchor["title"].strip()
        url = anchor["href"]

        latestJav.append({
            "thumb": thumb,
            "title": title,
            "url": url,
        })

    return jsonify({
        "latest_hentai": latestHentai,
        "latest_posts": posts,
        "latest_jav": latestJav,
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
