import string


def bow_dict_dicts(d):
    long_s = ''
    for k, v in d.items():
        for z, y in v.items():
            long_s += (z + ' ')
    long_s.translate(str.maketrans('', '', string.punctuation))
    return long_s

def bow_dict_lists(d):
    long_s = ''
    for k, v in d.items():

        if v is not None:
            for z in v:
                long_s += (z + ' ')
    long_s.translate(str.maketrans('', '', string.punctuation))
    return long_s

def bow_dict_strings(d):
    long_s = ''
    for k, v in d.items():
        long_s += (v + ' ')
    long_s.translate(str.maketrans('', '', string.punctuation))
    return long_s
