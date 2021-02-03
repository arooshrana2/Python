import time

def func_time(current_time = time.ctime()):
    print(current_time)

def func_list(my_list = []):
    my_list.append('raw data')
    return my_list
    
if __name__ == '__main__':

    func_time() # time1
    time.sleep(5) # sleeping for 5 seconds
    func_time() # should print +5 seconds more than time1. But Not! Why?
    
    list1 = func_list() # add 'raw data' to list1
    list2 = func_list() # add 'raw data' to list2
    print(list1 == list2) # True. Why?  
    print(len(list1), len(list2)) # 2 2. Why?
    print(list1) # ['raw data', 'raw data']. Hmm!
    print(list2) # ['raw data', 'raw data']. Why?
    
    # this is because default arguments are assigned when function is declared.
    # thus current_time doesn't change above
    # similarly, while declaration suppose my_list points to address 1000,
    # raw_data is appended to list, then again when it is called it'll again get appended to it
    
