def get_data(dict, key):
    if dict['succeeded']:
        return dict[key]
    else:
        try:
            print(dict['error'])
        except:
            print('failed without error message')
