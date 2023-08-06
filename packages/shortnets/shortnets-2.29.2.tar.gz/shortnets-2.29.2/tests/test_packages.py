import shortnets


def test_can_access_urllib3_attribute():
    shortnets.packages.urllib3


def test_can_access_idna_attribute():
    shortnets.packages.idna


def test_can_access_chardet_attribute():
    shortnets.packages.chardet
