#!/usr/bin/env python36
# coding: utf-8
"""Qiitaの自身の限定共有以外の投稿を一覧表示する."""

import yaml

from qiitalib import \
    qiita_get_config, \
    qiita_get_authuser_items2


def filter_items(items):
    """タイトルとURLを抽出する."""
    ret = []
    for i in items:
        item = {'title': i['title'], 'url': i['url']}
        ret.append(item)
    return ret


def print_yaml(items):
    """YAMLで出力する."""
    args = {'allow_unicode': True, 'default_flow_style': False}
    print(yaml.dump(items, **args))


if __name__ == '__main__':
    # 設定を読む
    config = qiita_get_config()
    access_token = config['DEFAULT']['access_token']

    # 処理する
    items = qiita_get_authuser_items2(access_token)
    items = filter_items(items)
    print_yaml(items)
