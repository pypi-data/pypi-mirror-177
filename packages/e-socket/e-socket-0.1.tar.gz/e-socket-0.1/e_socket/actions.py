
def str_to_list(text: str,key=' '):
    '''
    Use for converting string to list
    Input:
    text: str
    key: str # only 1 character
    Output:
    list

    Examples:

    a = "0 hello 3 63 57"
    print(str_to_list(text=a, key = " "))
    ['0', 'hello', '3', '63', '57']

    b = "hello0540321"
    print(str_to_list(text=b, key = "0"))
    ['hello', '54', '321']

    '''
    message = []
    val = 0
    for letter in range(len(text)):
        if text[letter] != key:
            if len(message) == val:
                message.append(text[letter])
            else:
                message[val] += text[letter]
        else:
            message.append('')
            val += 1
    return message