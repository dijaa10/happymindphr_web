from bs4 import BeautifulSoup
import re
def strip_empty_tags(soup:BeautifulSoup):
    for item in soup.find_all():
        if not item.get_text(strip=True):
            p = item.parent
            item.replace_with('')
            p.smooth()
            for c in p.find_all(text=True):
                c.replace_with(re.sub(r'\s{2,}$', '\n', c))
    return soup
