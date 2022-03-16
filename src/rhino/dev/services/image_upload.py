import base64


def test_image_encoded():
    import urllib
    import cStringIO
    import System
    URL = 'https://open-plans.s3.eu-central-1.amazonaws.com/tmp/plan/444f74b2-7667-4dcb-b073-0bc8471afb7b.jpeg'
    file = cStringIO.StringIO(urllib.urlopen(URL).read())
    b64_r = base64.b64encode(file.read()).decode()
    print(b64_r)

    #b64_string = base64.b64encode(img)
    return b64_r
    
    # print(type(file))
    # with open(file, "rb") as img_file:
    #     b64_string = base64.b64encode(img_file.read())
    # return b64_string


def encode_image_b64(img_path):
    with open(img_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read())
    return b64_string
