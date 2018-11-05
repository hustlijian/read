#!/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import hashlib
import requests
import urllib
import errno
from HTMLParser import HTMLParser
from urlparse import urljoin, urldefrag


def get_links_from_url(url, html):
    urls = dict()
    try:
        orig_urls = get_links(html)
        for item in orig_urls:
            urls[item] = urljoin(url, remove_fragment(item))
    except Exception as e:
        print('Exception: %s %s' % (e, url))
    return urls


def remove_fragment(url):
    pure_url, frag = urldefrag(url)
    return pure_url


def get_links(html):
    class URLSeeker(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.urls = []

        def handle_starttag(self, tag, attrs):
            # href = dict(attrs).get('href')
            # if href and tag == 'a':
            #     self.urls.append(href)

            if tag == 'img':
                src = dict(attrs).get('data-src') or dict(attrs).get('src')
                if src:
                    self.urls.append(src)

    url_seeker = URLSeeker()
    url_seeker.feed(html)
    return url_seeker.urls


def get_hash_name(input):
    hash_object = hashlib.md5(input)
    return hash_object.hexdigest()


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def get_url(url):
    basepath = get_hash_name(url)
    mkdir_p(basepath)
    rsp = requests.get(url)
    html = rsp.text
    html = html.encode(rsp.encoding)

    urls = get_links_from_url(url, html)
    for orig, url in urls.iteritems():
        filetype = "png"
        name = "%s/%s.%s" % (basepath, get_hash_name(orig), filetype)
        urllib.urlretrieve(url, name)
        html = html.replace(orig, "/" + name)

    main_file = "%s/index.html" % basepath
    with open(main_file, 'w') as fd:
        fd.write(html)

    return main_file


if __name__ == '__main__':
    url = 'https://mp.weixin.qq.com/s/uHtEI_spD2slM-ddVQ9reA'
    if len(sys.argv) > 1:
        url = sys.argv[1]
    print get_url(url)
