#!/usr/bin/env python36
# coding: utf-8
"""Qiitaのまとめ記事を更新する."""

import argparse
import re
import json


from qiitalib import \
    qiita_get_config, \
    qiita_get_items_item_id, \
    qiita_get_authuser_items2, \
    qiita_patch_items_item_id


if __name__ == '__main__':
    # 引数を解析する
    parser = argparse.ArgumentParser()
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()

    # 設定を読む
    config = qiita_get_config()
    access_token = config['DEFAULT']['access_token']
    summary_id = config['summary']['id']

    # 投稿を得る
    item = qiita_get_items_item_id(access_token, summary_id)
    body = item['body']
    payload = {
        'title': item['title'],
        'tags': item['tags'],
        'private': item['private'],
    }

    # 本文にリンクが見つからなければ加える
    changed = False
    for i in qiita_get_authuser_items2(access_token):
        # まとめ記事へのリンクは気にしない
        if summary_id == re.escape(i.get('id')):
            continue

        # URL無ければリンクを加える
        pattern = re.escape(i.get('url'))
        if not re.search(pattern, body):
            url = i.get('url')
            title = i.get('title')
            if not changed:
                body += "\n"
            body += f"* [{title}]({url})\n"
            changed = True

    # タイトルに相違があれば置き換える
    for i in qiita_get_authuser_items2(access_token):
        # まとめ記事へのリンクは気にしない
        if summary_id == re.escape(i.get('id')):
            continue

        # URL無ければリンクを加える
        pattern = "\[[^]]+\]\(" + re.escape(i.get('url')) + "\)"
        url = i.get('url')
        title = i.get('title')
        repl = f"[{title}]({url})"
        body_orig = body
        body = re.sub(pattern, repl, body)
        if body != body_orig:
            changed = True

    payload['body'] = body

    # 変更あれば更新する
    if changed:
        if args.force:
            print("changed=True")
            argv = {
                'access_token': access_token,
                'item_id': summary_id,
                'data': json.dumps(payload),
            }
            r = qiita_patch_items_item_id(**argv)
            # 即座に結果は繁栄されないため、次のコードは使わない
            # assert(r.text == body)
        else:
            print("changed=True (dry run)")
    else:
        print("changed=False")
