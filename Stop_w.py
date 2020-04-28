def stop_word(string_, word_list):
    for i in word_list:
        string_ = string_.lower()
        string_ = string_.replace(i, '')
        string_ = string_.replace('ï', 'i')
        string_ = string_.strip()
    return string_


