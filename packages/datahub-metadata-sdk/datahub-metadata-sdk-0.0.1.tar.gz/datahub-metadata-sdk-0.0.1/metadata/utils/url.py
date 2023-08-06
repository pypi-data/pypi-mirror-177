# -*- encoding: utf-8 -*-

import urllib.parse


def build_url(base, path, args_dict):
    url_parts = list(urllib.parse.urlparse(base))
    url_parts[2] = path
    url_parts[4] = urllib.parse.urlencode(args_dict)
    return urllib.parse.urlunparse(url_parts)