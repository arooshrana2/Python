# let's create a list of lists
a = [[1, 2], [3, 4]]

# copy the list to a new list
b = a[:]

b is a # prints False. Great objects are different

b[0] is a[0] # prints True. Huh?

b[0] = [6, 7]

b[0] is a[0] # prints False. Great!

# let's append to b[1] list
b[1].append(4)

b[1] # prints [3, 4, 4] great. its added

# check a[1]
a[1] # prints [3, 4, 4]. Uh-Oh, What?

"""
[:] or .copy() methods do create a copy but 
inner items are mutable objects, and only their
parents address is changed
a -> 1000 address [1,2] and [3,4]
b -> 2000 address [1,2] and [3,4]
where address of [1,2] and [3,4] doesn't changes
"""
