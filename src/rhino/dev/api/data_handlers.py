import cookielib
import urllib2


def get_data(dict, key):
    if dict['succeeded']:
        return dict[key]
    else:
        try:
            print(dict['error'])
        except:
            print('failed without error message')


def cookie_processor(func):

    def wrapper(*args, **kwargs):
        cj = cookielib.CookieJar()
        # Use the HTTPCookieProcessor object of the urllib2 library to create a cookie processor
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)

        val = func(*args, **kwargs)
        return val

    return wrapper
