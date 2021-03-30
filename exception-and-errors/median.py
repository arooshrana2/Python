def get_median(list_of_items):
    _list = sorted(list_of_items)

    if len(_list) == 0:
        raise ValueError("get_median() arg is empty")

    mid_ele = int(len(_list)//2)

    if len(_list) % 2 == 1:
        return _list[mid_ele] * 1.0
    return (_list[mid_ele] + _list[mid_ele + 1])/2.0


def main():
    x = 5
    twoD_array = [
        [4,6,1,7,9,10],
        [6,3,2,9,1],
        [],
        [5,8,4,0,1],
        []
    ]
    while x > 0:
        x -= 1
        try:
            median = get_median(twoD_array[x])
            print("Here => ", median)
        except Exception as e:
            print("Payload", e.args)
            print("Payload {}".format(str(e)))
            continue


if __name__ == '__main__':
    main()