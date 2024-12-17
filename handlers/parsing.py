import requests
from aiogram import types, Router, F
from aiogram.filters import Command
from bs4 import BeautifulSoup as bs

user_private_goods10parser = Router()


@user_private_goods10parser.message(Command('goods10'))
async def show_top10goods(msg: types.Message):
    url = r"https://mysku.club/blog/aliexpress/coupons"
    h = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
    r = requests.get(url, headers=h)
    soup = bs(r.content, features='html.parser').find_all("div", {"class": "topic"})
    i = 0
    st = '<u><b> ТОП 10 товаров со скидками:</b></u>\n'
    for t in soup:
        i = i + 1
        link = t.find("div", {"class": "topic-title"}).a.attrs['href']
        title = t.find("div", {"class": "topic-title"}).get_text().strip()
        overview = t.find("div", {"class": "wrapper"}).get_text().strip()
        if len(overview) > 160:
            overview = overview[:160]+'...'
        pic = t.find("img", {"class": "product-image"}).attrs['src']
        st = st + f'{i}) <a href="{link}">{title}</a> ({overview})\n'
    # print(len(st))
    await msg.answer(st)
