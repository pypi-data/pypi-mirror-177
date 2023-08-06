import shortnet


def test_can_access_urllib3_attribute():
    shortnet.packages.urllib3


def test_can_access_idna_attribute():
    shortnet.packages.idna


def test_can_access_chardet_attribute():
    shortnet.packages.chardet
