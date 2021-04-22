#!/usr/bin/env python
# -*- mode: python -*- -*- coding: utf-8 -*-
import argparse
import os
import pathlib

import contentful
from dotenv import load_dotenv
#import html2markdown
from rich_text_renderer import RichTextRenderer
#import tomd

APP_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = pathlib.Path(APP_DIR).parent

dotenv_path = os.path.join(PROJECT_DIR, '.env')
load_dotenv(dotenv_path)


def check_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--fetch', action='store_true')
    parser.add_argument('-d', '--deploy', action='store_true')

    return parser.parse_args()


def fetch():
    renderer = RichTextRenderer()
    client = contentful.Client(space_id=os.getenv(
        'CONTENTFUL_SPACE'), access_token=os.getenv('CONTENTFUL_TOKEN'))
    locales = [x.strip() for x in os.getenv(
        'CONTENTFUL_LOCALES', 'ja-JP,en-US').split(',')]
    default_locale = locales[0]

    entries = dict()
    for i, locale in enumerate(locales):
        entries[locale] = dict()
        try:
            for entry in client.entries({
                'content_type': os.getenv('CONTENTFUL_CONTENT_TYPE', 'post'),
                    'order': '-fields.title', 'locale': locale}):
                data = dict()
                entry_id = entry.sys['id']
                if hasattr(entry, 'title'):
                    data.update({'title': entry.title})
                else:
                    continue
                data.update({'slug': entry.slug})
                data.update(
                    {'date': entry.pub_date.strftime('%Y-%m-%dT%H:%M:%S+09:00')})
                # if 'second' in entry.slug:
                #    print(entry.body)
                body = renderer.render(entry.body)
                #data.update({'body': html2markdown.convert(body)})
                #data.update({'body': tomd.convert(body)})
                data.update({'body': body})
                if hasattr(entry, 'categories'):
                    data.update({'categories': entry.categories.title})
                if hasattr(entry, 'tags'):
                    tags = [x.title for x in entry.tags]
                    data.update({'tags': tags})
                if hasattr(entry, 'images'):
                    images = list()
                    for image in entry.images:
                        if image.url():
                            images.append(
                                {'title': image.title, 'url': image.url()})
                    if locale != default_locale:
                        if entries[default_locale].get(entry_id):
                            images = entries[default_locale][entry_id].get(
                                'images')
                    if images:
                        data.update({'images': images})

                entries[locale][entry_id] = data
        except contentful.errors.BadRequestError as e:
            print(e)
    # print(entries)

    HUGO_CONTENT_DIR = os.path.join(
        PROJECT_DIR, os.getenv('HUGO_CONTENT_DIR', 'content/blog'))
    os.makedirs(HUGO_CONTENT_DIR, exist_ok=True)
    for locale, x in entries.items():
        suffix = f'.{locale[:2]}' if locale != default_locale else ''

        for entry_id, y in x.items():
            if locale == default_locale and 'english' in y['title'].lower():
                continue
            body = adjust(y['body'])
            output = f'''\
---
title: {y["title"]}
slug: {y["slug"]}
date: {y["date"]}
draft: false'''
            if y.get('categories'):
                output += f'\ncategories: {y["categories"]}'
            if y.get('tags'):
                output += '\ntags:'
                for tag in y['tags']:
                    output += f'\n  - {tag}'
            if y.get('images'):
                output += '\nimages:'
                for image in y['images']:
                    output += f'\n  - alt: {image["title"]}'
                    output += f'\n    src: {image["url"]}'
            output += '\n---'
            output += f'\n{body}\n'

            with open(os.path.join(HUGO_CONTENT_DIR, f'{entry_id}{suffix}.md'), 'w') as f:
                f.write(output)
            # print(output)


def adjust(s, sep='\n'):
    l = s.split(sep)
    for i, x in enumerate(l):
        if i:
            if l[i] and l[i-1]:
                l[i-1] += '<br />'
    result = sep.join(l)
    return result.replace('</p><br />', '</p>')


def adjust_md(s, sep='\n'):
    l = s.split(sep)
    for i, x in enumerate(l):
        if i:
            if l[i] and l[i-1]:
                l[i-1] += '  '
    return sep.join(l)


def main():
    args = check_args()
    if args.fetch:
        fetch()
    if args.deploy:
        print('waoo')


if __name__ == "__main__":
    main()
