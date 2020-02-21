#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: geekTimeSpider.py
# Author: Liweijian
# Date: 2020/2/21

import requests
from selenium import webdriver
import time
import json
import re
import html2text as ht
import random
import sys

headers = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36",
    "Referer": "https://time.geekbang.org/column/article/39972",
    "Host": "time.geekbang.org",
    "Content-Type": "application/json",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
}


class geekTimeSpider:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.text_maker = ht.HTML2Text()

    def login(self, username, password):
        self.driver.get("https://account.geekbang.org/signin?redirect=https%3A%2F%2Ftime.geekbang.org%2F")
        self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div[3]/a").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div[1]/div[1]/input").send_keys(
            username)
        self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div[2]/input").send_keys(password)
        self.driver.find_element_by_class_name("mybtn").click()
        self.write_cookie()

    def get_content(self, id):
        """获取专栏具体文章内容"""

        data = {"id": id, "include_neighbors": "true", "is_freelyread": "true"}
        content_json = requests.session().post("https://time.geekbang.org/serv/v1/article", headers=headers,
                                               cookies=self.read_cookie(),
                                               data=json.dumps(data)).json()

        title = content_json["data"]["article_title"]
        audio_download_url = content_json["data"]["audio_download_url"]
        article_content = content_json["data"]["article_content"]
        self.download_markdown(title=title, audio_download_url=audio_download_url, article_content=article_content)

    def download_markdown(self, title, audio_download_url, article_content):
        """ 下载成markdown """

        title = re.sub(r'[\?\\/\:\*"<>\|]', "", title)
        with open(title + ".md", "w") as f:
            f.write("## " + title + "\n")
            f.write("> 音频地址：" + audio_download_url + "\n")
            f.write(self.text_maker.handle(re.sub(r"[\xa5]", "", article_content)))

    def get_articles(self, cid):
        """获取文章id列表"""
        time.sleep(3)
        data = {"cid": cid, "size": 100, "prev": 0, "order": "earliest", "sample": "false"}

        url = "https://time.geekbang.org/serv/v1/column/articles"
        articles_json = requests.session().post(url=url, headers=headers, cookies=self.read_cookie(),
                                                data=json.dumps(data)).json()

        ids = []
        for list in articles_json["data"]["list"]:
            ids.append(list["id"])

        return ids

    # =============== cookie 操作 start ===============================
    def refresh_cookie(self, id):
        """打开专栏，刷新cookie，不刷新cookie会无权限"""
        # self.driver.get("https://time.geekbang.org/column/article/%s" % id)
        self.driver.get("https://time.geekbang.org/column/intro/%s" % id)
        self.write_cookie()

    def read_cookie(self):
        with open("cookies.txt", "r")as f:
            cookies = f.read()
            cookies = json.loads(cookies)
        return cookies

    def write_cookie(self):
        cookie = {}
        for i in self.driver.get_cookies():
            cookie[i["name"]] = i["value"]
        with open("cookies.txt", "w") as f:
            f.write(json.dumps(cookie))

    # =============== cookie 操作 end. ===============================

    def run(self, cid, phone, password, count=None):
        self.login(phone, password)
        self.refresh_cookie(cid)
        ids = self.get_articles(cid)
        for index, id in enumerate(ids):
            if count is not None and index < int(count):
                continue
            print(id)
            self.get_content(id)
            time.sleep(random.randint(3, 10))


if __name__ == '__main__':
    cid = sys.argv[1]  # 专栏id
    phone = sys.argv[2]  # 手机号
    password = sys.argv[3]  # 密码
    count = None
    if len(sys.argv) > 4:
        count = sys.argv[4]  # 从第几篇开始下载
    print("%s = %s = %s = %s" % (cid, phone, password, count))
    geekTimeSpider().run(cid=cid, phone=phone, password=password, count=count)
