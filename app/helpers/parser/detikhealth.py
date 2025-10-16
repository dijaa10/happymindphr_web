from .header import headers
import requests
from app.models.Artikel import Artikel
from app.helpers.download_image import download_from_url
from app.config import db
from app.helpers.clean_empty_data import strip_empty_tags
from bs4 import BeautifulSoup as bs


def parse(url: str):
    # return error if url doesn't match
    if "health.detik.com" not in url:
        return False
    try:
        header_list = headers()
        res = requests.request("GET", url, headers=header_list)
        soup = bs(res.text, "html.parser")
        title = soup.find("title").text
        img = soup.find("img", attrs={"class": "p_img_zoomin"})
        filename, status = download_from_url(img["src"])

        # remove figure,a and ul tag
        figure = soup.find_all("figure")
        for figure_tag in figure:
            figure_tag.decompose()
        a = soup.find_all("a")
        for a_tag in a:
            a_tag.replaceWithChildren()
        # a = soup.find_all("a")
        # for a_tag in a:
        #     a_tag.decompose()
        ul = soup.find_all("ul")
        for ul_tag in ul:
            ul_tag.decompose()
        style = soup.find_all("style")
        for style_tag in style:
            style_tag.decompose()
        parallax = soup.find_all("div", attrs={"class": "parallaxindetail"})
        for parallax_element in parallax:
            parallax_element.decompose()
        ads = soup.find_all("div", attrs={"class": "staticdetail_container"})
        for ads_element in ads:
            ads_element.decompose()
        no_content = soup.find_all("div", attrs={"class": "noncontent"})
        for no_content_element in no_content:
            no_content_element.decompose()
        # remove empty tag
        # strip_empty_tags(soup)

        # content = soup.find("div",attrs={"class":"detail__body-text"})
        sections = soup.find_all("section")
        sections = [section_element for section_element in sections]
        content = ""
        for section_element in sections:
            content += f"{section_element}"
        # save to the db
        new_article = Artikel(
            judul=title,
            isi=content,
            sumber="health.detik.com",
            gambar=filename,
        )
        new_article.generate_slug()
        db.session.add(new_article)
        db.session.commit()
        db.session.close()
        # return soup.prettify()
        return True
    except Exception as e:
        raise e
