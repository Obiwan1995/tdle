# -*- coding: utf-8 -*-
# !/usr/bin/python3
from bs4 import BeautifulSoup

def main():
    text = """</div>
                <div class="left phone"><sup>(843)</sup> 222-000-3 | 003 <small>(телефон в г.Казани) </small></div>
                <div class="right buttons">
                    <div class="button last-child">
                        <div class="left"><a id="requestCall11" href="#"><img src="/content/img/icon-phone.png"></a></div>
                        <div class="left name"><a href="#" id="requestCall">Заказать<br>звонок</a></div>
                    </div>
                    <div class="button">
                        <div class="left"><a id="questionToOperator11" href="#"><img src="/content/img/icon-questions.png"></a></div>
                        <div class="left name"><a href="#" id="questionToOperator">Задать вопрос<br>специалисту</a></div>
                    </div>
                    <div class="button">
                        <div class="left"><a href="/opinions"><img src="/content/img/icon-opinions.png"></a></div>
                        <div class="left name"><a href="/opinions">Ваши отзывы</a></div>
                    </div>"""
    text2 = """
        <a
        href="test">Toto</a>
    """
    soup = BeautifulSoup(open("test"), "html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    res = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in res.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    res = '\n'.join(chunk for chunk in chunks if chunk)

    #print(soup)
    #print("\n")
    for link in soup.find_all('a'):
        print(link.get('href'))

if __name__ == '__main__':
    main()