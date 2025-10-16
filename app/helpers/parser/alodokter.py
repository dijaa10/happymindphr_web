from .header import headers
import requests
from app.helpers.clean_empty_data import strip_empty_tags
from app.helpers.download_image import download_from_url
from app.models.Artikel import Artikel
from app.config import db,session
from bs4 import BeautifulSoup as bs


def parse(url: str):
    # return error if url doesn't match
    if "alodokter.com" not in url:
        return False
    try:
        header_list = headers()
        res = requests.request("GET", url, headers=header_list)
        soup = bs(res.text, "html.parser")
        title = soup.find("h1", attrs={"id": "post_title"}).text
        # print(title.text)
        a = soup.find_all("a")
        for a_tag in a:
            a_tag.replaceWithChildren()
        content = soup.find("div", attrs={"class": "post-content"})
        img = soup.find(
            "img", attrs={"class": {"alignnone", "size-full", "wp-image-780449"}}
        )
        filename, status = download_from_url(img["src"])
        img = soup.find_all("img")
        for img_tag in img:
            img_tag.decompose()
        # save to the db
        new_article = Artikel(
            judul=title,
            isi=content,
            sumber="alodokter.com",
            gambar=filename,
        )
        new_article.generate_slug()
        session.add(new_article)
        session.commit()
        session.close()

        return True
    except Exception as e:
        print(e)
        raise e
