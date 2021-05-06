#!/usr/bin/env python
# -*- mode: python -*- -*- coding: utf-8 -*-
import argparse
import datetime
import json
import os
import pathlib
import re
import urllib.request

from dotenv import load_dotenv

APP_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = pathlib.Path(APP_DIR).parent
HUGO_CONTENT_DIR = os.path.join(PROJECT_DIR, 'content')
UPDATE_SEC = int(os.getenv('UPDATE_SEC', '300'))

dotenv_path = os.path.join(PROJECT_DIR, '.env')
load_dotenv(dotenv_path)


class GraphcmsManager(object):
    def __init__(self, endpoint, token):
        self.endpoint = endpoint
        self.headers = {'Authorization': f'Bearer {token}'}

    def format_query(self, s):
        s = re.sub(r'\s+', '' ' ', s).replace('\n', ' ')
        return {'query': f'{s}'}

    def query(self, data=None, is_raw=True):
        if not data:
            data = self.__query_statement()
        if is_raw:
            data = self.format_query(data)

        req = urllib.request.Request(self.endpoint,
                                     data=json.dumps(data).encode(),
                                     headers=self.headers)
        status_code = 500
        try:
            with urllib.request.urlopen(req) as response:
                payload = json.loads(response.read())
                status_code = response.getcode()
                # print ('url:', response.geturl())
                # print ('Content-Type:', response.info()['Content-Type'])
        except urllib.error.HTTPError as e:
            payload = {'error': e.reason}
        except urllib.error.URLError as e:
            payload = {'error': e.reason}
        except Exception as e:
            payload = {'error': str(e)}
        return status_code, payload

    def __query_statement(self):
        return '''\
        {
          jpecPosts(locales: [ja, en], orderBy: updatedAt_DESC) {
            localizations(includeCurrent: true) {
              locale
              id
              slug
              date
              title
              body {
                markdown
              }
              image {
                url
                fileName
                mimeType
              }
              japanese
              updatedAt
            }
            category {
              localizations(includeCurrent: true) {
                locale
                title
              }
            }
            tag {
              ... on JpecTag {
                localizations(includeCurrent: true) {
                  locale
                  title
                }
              }
            }
          }
          jpecPages(locales: [ja, en]) {
            localizations(includeCurrent: true) {
              locale
              id
              title
              body {
                markdown
              }
              path
              layout
              updatedAt
            }
          }
        }'''

    def __time_diff(self, date_str, fmt='%Y-%m-%dT%H:%M:%S.%f+00:00'):
        updatetime = datetime.datetime.strptime(date_str, fmt)
        return (datetime.datetime.now() - datetime.timedelta(hours=9) - updatetime).seconds

    def gen_hugo_contents(self, payload):
        result = list()
        data = (payload.get('data'))
        for model, content_list in data.items():
            locale = 'en'
            if model == 'jpecPosts':
                for content in content_list:
                    # generate category_map
                    category = content.get('category')
                    category_map = dict((x['locale'], x['title']) for x in category.get('localizations')) if category else {}
                    # generate tags_map
                    tags = content.get('tag')
                    tags_map = {}
                    if tags:
                        for tag in tags:
                            for x in tag.get('localizations'):
                                tag_list = tags_map.get(x['locale'], [])
                                tag_list.append(x['title'])
                                tags_map[x['locale']] = tag_list
                    # parse
                    for x in content.get('localizations'):
                        data_map = dict()
                        locale = x['locale']
                        # skip japanese only post
                        if locale == 'en' and x['japanese']:
                            continue
                        front_matter = f'title: "{x["title"]}"\n'
                        front_matter += f'slug: "{x["slug"]}"\n'
                        front_matter += f'date: {x["date"]}\n'
                        if category_map:
                            front_matter += f'categories: "{category_map[locale]}"\n'
                        if tags_map:
                            front_matter += 'tags:\n'
                            for y in tags_map.get(locale):
                                front_matter += f'  - \"{y}\"\n'
                        image = x.get('image')
                        if image:
                            # add save image action in here
                            front_matter += 'images:\n'
                            front_matter += f'  - alt: {image["fileName"]}\n'
                            front_matter += f'    src: {image["url"]}\n'
                        data_map['front_matter'] = front_matter
                        data_map['body'] = x['body']['markdown']
                        data_map['filepath'] = f'news/{x["slug"]}.{locale}.md'.replace('.ja', '')
                        data_map['update_sec'] = self.__time_diff(x['updatedAt'])
                        result.append(data_map)
            elif model == 'jpecPages':
                for content in content_list:
                    for x in content.get('localizations'):
                        data_map = dict()
                        locale = x['locale']
                        front_matter = f'title: "{x["title"]}"\n'
                        layout = x.get('layout')
                        if layout:
                            front_matter += f'layout: "{x["layout"]}"\n'
                        data_map['front_matter'] = front_matter
                        data_map['body'] = x['body']['markdown'].replace('\n\n', '  \n')
                        data_map['filepath'] = f'{x["path"]}/_index.{locale}.md'.replace('.ja', '')
                        data_map['update_sec'] = self.__time_diff(x['updatedAt'])
                        result.append(data_map)
        return result

    def write(self, data, update_sec=UPDATE_SEC):
        for x in data:
            fullpath = os.path.join(HUGO_CONTENT_DIR, x['filepath'])
            os.makedirs(os.path.dirname(fullpath), exist_ok=True)

            if os.path.exists(fullpath) and x["update_sec"] > update_sec:
                # skip old posts
                continue

            with open(fullpath, 'w') as f:
                text = f'---\n{x["front_matter"]}---\n{x["body"]}'
                f.write(text)


def check_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--fetch', action='store_true')
    parser.add_argument('-d', '--deploy', action='store_true')

    return parser.parse_args()


def main():
    endpoint = os.getenv('GRAPHCMS_ENDPOINT', 'http://localhost')
    token = os.getenv('GRAPHCMS_TOKEN', 'my-token')
    G = GraphcmsManager(endpoint=endpoint, token=token)
    args = check_args()
    if args.fetch:
        status_code, payload = G.query()
        if status_code != 200:
            print(payload)
            return
        data = G.gen_hugo_contents(payload)
        G.write(data)
    if args.deploy:
        pass


if __name__ == "__main__":
    main()
