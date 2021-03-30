
def get_median(list_of_items):
    """
    Usage: Finds the median from a list of numbers provided
    
    Parameters:
        list_of_items: A list of items(numbers asof now)
    Return:
        median: A float number indicating the median     
    """
    _list = sorted(list_of_items)

    if len(_list) == 0:
        raise ValueError("get_median() arg is empty")  # Exception needs to be raised if len is 0
                                                       # Returning exception will just print the message here

    mid_ele = int(len(_list)//2)

    if len(_list) % 2 == 1:
        return _list[mid_ele] * 1.0
    return (_list[mid_ele] + _list[mid_ele + 1])/2.0


def main():
    # Creating random 5 test cases to see if the program works
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
        except Exception as e:  # Catching the raised exception
            print("Payload", e.args)
            print("Payload {}".format(str(e)))
            continue


if __name__ == '__main__':
    main()
