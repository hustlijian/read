#!/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import requests
import urllib
from HTMLParser import HTMLParser
from urlparse import urljoin, urldefrag

url = 'https://mp.weixin.qq.com/s/2wnIRBpj0keOnScHVUexZg'
main_file = 'index.html'


def get_links_from_url(url, html):
    """Download the page at `url` and parse it for links.

    Returned links have had the fragment after `#` removed, and have been made
    absolute so, e.g. the URL 'gen.html#tornado.gen.coroutine' becomes
    'http://www.tornadoweb.org/en/stable/gen.html'.
    """
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
                print attrs
                src = dict(attrs).get('data-src') or dict(attrs).get('src')
                if src:
                    self.urls.append(src)

    url_seeker = URLSeeker()
    url_seeker.feed(html)
    return url_seeker.urls


def get_hash_name(input):
    hash_object = hashlib.md5(input)
    return hash_object.hexdigest()


def test(url):
    rsp = requests.get(url)
    print rsp
    html = rsp.text
    html = html.encode(rsp.encoding)

    urls = get_links_from_url(url, html)
    for orig, url in urls.iteritems():
        filetype = "png"
        name = "%s.%s" % (get_hash_name(orig), filetype)
        print name
        urllib.urlretrieve(url, name)
        html = html.replace(orig, "/" + name)

    with open(main_file, 'w') as fd:
        fd.write(html)


if __name__ == '__main__':
    url = 'https://mp.weixin.qq.com/s/2wnIRBpj0keOnScHVUexZg'
    test(url)
