def to_dict(text: str) -> list[dict]:
    result_list = []
    value_dict = text.split('|')
    for i in range(len(value_dict)):
        value_list = value_dict[i].split(':')
        result_dict = {}
        for j in range(0, len(value_list)-1, 2):
            values = value_list[j+1].split(',')
            if len(values) >= 2:
                value = []
                for k in range(len(values)):
                    value.append(values[k])
                result_dict[value_list[j]] = value
            else:
                result_dict[value_list[j]] = value_list[j+1]
        result_list.append(result_dict)
    return result_list

def to_dict_song(text: str) -> list[dict]:
    result_list = []
    value_dict = text.split(':')
    for i in range(len(value_dict)):
        value_list = value_dict[i].split('~|~')
        result_dict = {}
        for j in range(0, len(value_list)-1, 2):
            values = value_list[j+1].split(',')
            if len(values) >= 2:
                value = []
                for k in range(len(values)):
                    value.append(values[k])
                result_dict[value_list[j]] = value
            else:
                result_dict[value_list[j]] = value_list[j+1]
        result_list.append(result_dict)
    return result_list
