#!/usr/bin/env python36
# coding: utf-8
"""Qiitaの操作を行う."""

import os
from pathlib import Path
import configparser
import requests
import json


def qiita_get_config():
    """設定ファイルを読む."""
    config = configparser.ConfigParser()
    path = Path(os.getenv('HOME'), '.qiita.ini')
    config.read_file(open(path))
    return config


def qiita_get_headers(access_token):
    """カスタムヘッダを得る."""
    return {'Authorization': "Bearer %s" % (access_token)}


def qiita_get_authuser(access_token):
    """公開されたアイテム数を得る."""
    url = 'https://qiita.com/api/v2/authenticated_user'
    headers = qiita_get_headers(access_token)
    resp = requests.get(url, headers=headers)
    return json.loads(resp.text).get('items_count')


def qiita_get_authuser_items(access_token):
    """限定共有を含むすべてのアイテムを得る."""
    PER_PAGE_MAX = 100
    items = []
    url = 'https://qiita.com/api/v2/authenticated_user/items'
    page = 1
    while True:
        params = {'page': page, 'per_page': PER_PAGE_MAX}
        headers = qiita_get_headers(access_token)
        resp = requests.get(url, headers=headers, params=params)
        page_items = json.loads(resp.text)
        if len(page_items) == 0:
            break
        items.extend(page_items)
        page += 1
    return items


def qiita_get_authuser_items2(access_token):
    """限定共有を除く、すべてのアイテムを得る."""
    items = qiita_get_authuser_items(access_token)
    items = filter(lambda x: not x['private'], items)
    return list(items)


def qiita_get_items_item_id(access_token, item_id):
    """記事を取得する."""
    item = None
    url = f'https://qiita.com/api/v2/items/{item_id}'
    headers = qiita_get_headers(access_token)
    resp = requests.get(url, headers=headers)
    return json.loads(resp.text)


def qiita_patch_items_item_id(access_token, item_id, data):
    """記事を更新する."""
    url = f'https://qiita.com/api/v2/items/{item_id}'
    headers = qiita_get_headers(access_token)
    headers['Content-Type'] = 'application/json'
    return requests.patch(url, headers=headers, data=data)
