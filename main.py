from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from bs4 import BeautifulSoup
from urllib.request import urlopen
from random import shuffle

app = FastAPI()


def create_world_lst(url: str = "https://launchpad.net/ubuntu/+archivemirrors") -> list:
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    td = soup.find_all("td")

    href: list = []
    # looping through all the things in td
    for t in td:
        # contents
        contents = t.contents
        if contents.__len__() > 1:
            if bool(contents[1].get('href', False)):
                tmp = contents[1].attrs['href']
                if tmp.__contains__("https://") or tmp.__contains__("http://"):
                    href.append(tmp)
    return href


@app.get("/mirror", response_class=PlainTextResponse)
async def main():
    t = create_world_lst()
    shuffle(t)
    output: str = ""
    counter = 0
    for url in t:
        if counter == 20:
            break
        output = output + url + "\n"
        counter = counter + 1
    return output
