import requests
import hashlib


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
    if sha1(r) != "03aebf8e01acf9720518df6af0422782d70ccaf3":
        raise "The website changed."
