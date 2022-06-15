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
    r = soup.xpath(".//section")[3].text_content()
    if r != "VACCINESVaccines for 5 and under are coming.WE WILL HAVE HAVE THE MODERNA VACCINE IN OUR OFFICE FOR CHILDREN 6 MONTHS THROUGH 5 YEARS OLD.  IT IS A TWO DOSE VACCINE THAT IS 4 WEEKS APART.  WHEN MAKING THE SECOND APPOINTMENT PLEASE ENSURE IT IS AT LEAST 4 WEEKS FROM THE FIRST.APPOINTMENT WILL BE MADE ON MYCHART OR BY CALLING THE OFFICE BUT ARE NOT AVAILABLE YET.  STAYED TUNED FOR UPDATES.WE CONTINUE TO HAVE THE PFIZER VACCINE RIGHT NOW FOR PATIENTS 5 AND UP.  TO SCHEDULE FOR THIS AGE GROUP PLEASE CALL THE OFFICE.  YOU CAN ALSO RECEIVE THE VACCINE AS PART OF ANY UPCOMING VISIT YOU MAY HAVE AT THE OFFICE.AM I UP TO DATE? - CHECK OUT THIS CDC PAGE TO FIND OUT.":
        print(r)
        raise "The website changed."
