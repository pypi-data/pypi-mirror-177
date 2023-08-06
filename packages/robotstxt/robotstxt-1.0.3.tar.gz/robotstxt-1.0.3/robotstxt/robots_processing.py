import re

def select_rule_block(rule_blocks, token):
    if token.lower() in rule_blocks:
        return token
    if token.lower() == 'googlebot-news' and 'googlebot' in rule_blocks:
        return 'googlebot'

    elif '*' in rule_blocks:
        return '*'
    else:
        return None

def get_url_path(url):
    url_path_regex = re.compile(r'https?:\/\/.*?(\/.*)')
    url_path = re.search(url_path_regex, url)
    if url_path:
        return url_path[1]
    else:
        return None

def is_valid_url(url):
    import re
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)
