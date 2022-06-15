import requests
import hashlib
from lxml.html import fromstring


def sha1(s):
    """Return the sha1sum of a string.

    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    ! This algorithm is obsolete for most purposes. Its !
    ! usage is discouraged. Please use SHA256 instead.  !
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    :param s: The data to hash. Ideally bytes, but if unicode is passed in, it
    will convert it to bytes first.
    :return: a hexadecimal SHA1 hash of the data
    """
    if isinstance(s, str):
        s = s.encode()
    sha1sum = hashlib.sha1()
    sha1sum.update(s)
    return sha1sum.hexdigest()



if __name__ == '__main__':
    url = "https://www.westcambridgepediatrics.com/covid19"
    r = requests.get(url).content
    soup = fromstring(r)
    r = soup.xpath(".//body")[0].text_content()
    if sha1(r) != "58169a993e530ef69df77093369174ca9824c4e8":
        print(sha1(r), "!=", "58169a993e530ef69df77093369174ca9824c4e8")
        raise "The website changed."
