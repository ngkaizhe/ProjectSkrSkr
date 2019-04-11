from decimal import Decimal

# recursive function below
round_answer = True
digit_round = 4

def len_decimal(num : (Decimal, float, int)) -> (int, int):
    split_string = "{0:f}".format(num).split('.')
    length = [0, 0]
    length[0] = len(split_string[0])
    if len(split_string) == 2: length[1] = len(split_string[1])
    return (length[0], length[1])

def get_string(element: list, current_line: int, ndim: int, seperate_string: str, isFormal: bool) -> str:
    if isinstance(element, list) is False:
        #return str(round(Decimal(element),2) + 0)
        return "{0:.4f}".format(element + 0)

    else:
        answer = '['
        var = 1
        for x in element:
            answer += get_string(x, current_line - 1, ndim, seperate_string, isFormal)
            if var is not len(element):
                answer += seperate_string + '\n' * current_line
                if isFormal and isinstance(element[0], list):
                    answer += ' ' * (6 + ndim - current_line)
                elif isFormal is False and isinstance(element[0], list):
                    answer += ' ' * (ndim - current_line)
            var += 1

    return answer + ']'


def cut_array(element: list, shape: list, index: int) -> list:
    # index is index of shape
    if index == len(shape) - 1:
        return element
    else:
        new_list = []
        total_divided_part = shape[index]
        start = 0
        rangee = int(len(element) / total_divided_part)
        for i in range(total_divided_part):
            new_list.append(cut_array(element[start: start+rangee], shape, index + 1))
            start += rangee

        return new_list


def combine_array(element: list) -> list:
    if isinstance(element[0], list) is False:
        return element

    else:
        new_list = []
        for i in element:
            new_list += combine_array(i)

        return new_list