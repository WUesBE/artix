def w_counter(s):
    '''
    :param s: string
    :return: dict {k: word, v:number}
    '''
    d = {}
    splitted = s.split()
    for i in splitted:
        if i not in d.keys():
            d[i] = 1
        else:
            d[i] += 1
    d = {k: v for k, v in sorted(d.items(), key=lambda item: item[1])}
    return d




