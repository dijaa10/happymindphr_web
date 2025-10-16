from .header import headers
from app.helpers.clean_empty_data import strip_empty_tags
from app.helpers.download_image import download_from_url
import requests
from bs4 import BeautifulSoup as bs
from app.config import db
from app.models.Artikel import Artikel


def parse(url: str):
    # return error if url doesn't match
    if "halodoc" not in url:
        return False
    try:
        header_list = headers()
        res = requests.request("GET", url, headers=header_list)
        soup = bs(res.text, "html.parser")
        img = soup.find("img", attrs={"class": "default-image-style"})

        # TODO Clean the data
        # remove figure,a and ul tag
        figure = soup.find_all("figure")
        for figure_tag in figure:
            figure_tag.decompose()
        a = soup.find_all("a")
        for a_tag in a:
            a_tag.decompose()
        ul = soup.find_all("ul")
        for ul_tag in ul:
            ul_tag.decompose()

        # remove p>strong"Daftar Isi"
        daftar_isi_tag = soup.find_all("strong", string="DAFTAR ISI")
        for daftar_isi in daftar_isi_tag:
            daftar_isi.decompose()

        # remove empty tag
        strip_empty_tags(soup)

        content = soup.find("div", {"id": "articleContent"})
        title = soup.find("title").text

        print(img["src"])
        filename, status = download_from_url(img["src"])

        # save to the db
        new_article = Artikel(
                judul=title,
                isi=content,
                sumber="halodoc.com",
                gambar=filename,
            )
        new_article.generate_slug()
        db.session.add(new_article)
        db.session.commit()
        db.session.close()
        # print(title)
        # print(content)
        return True
    except Exception as e:
        print(e.with_traceback)
        raise e
