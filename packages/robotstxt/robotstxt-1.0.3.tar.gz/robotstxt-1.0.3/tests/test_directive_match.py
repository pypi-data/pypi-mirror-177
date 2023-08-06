from robotstxt.processor import *


def test_root_and_lower_levels_match():
    assert pattern_match('/', '/anything') == True
    assert pattern_match('/*', '/anything') == True


def test_root_only_match():
    assert pattern_match('/$', '/') == True
    assert pattern_match('/$', '/anything') == False


def test_contains_match():
    assert pattern_match('/fish', '/fish') == True
    assert pattern_match('/fish', '/fish.html') == True
    assert pattern_match('/fish', '/fish/salmon.html') == True
    assert pattern_match('/fish', '/fishheads') == True
    assert pattern_match('/fish', '/fishheads/yummy.html') == True
    assert pattern_match('/fish', '/fish.php?id=anything') == True
    assert pattern_match('/fish', '/Fish.asp') == False
    assert pattern_match('/fish', '/catfish') == False
    assert pattern_match('/fish', '/?id=fish') == False
    assert pattern_match('/fish', '/desert/fish') == False


def test_trailing_wildcard_match():
    assert pattern_match('/fish*', '/fish') == True
    assert pattern_match('/fish**', '/fish') == True
    assert pattern_match('/fish*', '/fish.html') == True
    assert pattern_match('/fish*', '/fish/salmon.html') == True
    assert pattern_match('/fish*', '/fishheads') == True
    assert pattern_match('/fish*', '/fishheads/yummy.html') == True
    assert pattern_match('/fish*', '/fish.php?id=anything') == True
    assert pattern_match('/fish*', '/Fish.asp') == False
    assert pattern_match('/fish*', '/catfish') == False
    assert pattern_match('/fish*', '/?id=fish') == False
    assert pattern_match('/fish*', '/desert/fish') == False


def test_undermatch_match():
    assert pattern_match('/fish/', '/fish/') == True
    assert pattern_match('/fish/', '/fish/?id=anything') == True
    assert pattern_match('/fish/', '/fish/salmon.htm') == True
    assert pattern_match('/fish/', '/fish') == False
    assert pattern_match('/fish/', '/fish.html') == False
    assert pattern_match('/fish/', '/animals/fish/') == False
    assert pattern_match('/fish/', '/Fish/Salmon.asp') == False


def test_leading_wildcard_and_end_of_stringmatch():
    assert pattern_match('/*.php$', '/filename.php') == True
    assert pattern_match('/*.php$', '/folder/filename.php') == True
    assert pattern_match('/*.php$', '/filename.php?parameters') == False
    assert pattern_match('/*.php$', '/filename.php/') == False
    assert pattern_match('/*.php$', '/filename.php5') == False
    assert pattern_match('/*.php$', '/windows.PHP') == False


def test_wildcard_middle_of_string_stringmatch():
    assert pattern_match('/*.php', '/fish.php') == True
    assert pattern_match('/*.php', '/fishheads/catfish.php?parameters') == True
    assert pattern_match('/*.php', '/Fish.PH') == False


def test_missing_leading_slash_or_wildcard_match():
    assert pattern_match('fish', '/fish') == False


def test_end_of_string():
    assert pattern_match('/fish$', '/fish') == True
    assert pattern_match('/fish$', '/fish123') == False


def test_dollar_not_end_of_string():
    assert pattern_match('/ab$cd$', '/ab$cd') == True
    assert pattern_match('/ab$cd$', '/ab$cd$') == False
    assert pattern_match('/ab$cd', '/ab$cd') == True
    assert pattern_match('/ab$', '/ab$cd') == False


def test_leading_wildcard_match():
    assert pattern_match('/*.php', '/index.php') == True
    assert pattern_match('/**.php', '/index.php') == True
    assert pattern_match('/***.php', '/index.php') == True
    assert pattern_match('/*.php', '/filename.php') == True
    assert pattern_match('/*.php', '/folder/filename.php') == True
    assert pattern_match('/*.php', '/folder/filename.php?parameters') == True
    assert pattern_match('/*.php', '/folder/any.php.file.html') == True
    assert pattern_match('/*.php', '/filename.php/') == True
    assert pattern_match('/*.php', '/') == False
    assert pattern_match('/*.php', '/windows.PHP') == False
    assert pattern_match('*.php', '/index.php') == True



def test_generous_wildcard_match():
    assert pattern_match('/*aa-bb', '/aa-aa-bb') == True
    assert pattern_match('/*ab*cd*ab', '/ab-cd-ab') == True
    assert pattern_match('/*aa*bb', '/aa-bb-aa-cc') == True


def test_asterisk_in_path_match():
    assert pattern_match('/a*b', '/a*b') == True


def test_space_in_patterns():
    assert pattern_match('/ b', '/ b') == True


def test_encoded_patterns():
    assert pattern_match('/%20b', '/ b') == True
    assert pattern_match('/ b', '/%20b') == True
    assert pattern_match('/?b', '/%3Fb') == True
    assert pattern_match('/%3Fb', '/?b') == True
    assert pattern_match('/?b', '/%3fb') == True
    assert pattern_match('/%3fb', '/?b') == True

def test_trailing_wildcard_and_endofline():
    assert pattern_match('/blog/*/page/*$', '/blog/en/page/4') == True

