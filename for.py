class IterationLimitReached(Exception):
    '''Throws when limit is hit'''

class controlled:
    def __init__(
        self, 
        iterator, 
        index = False, 
        starts_at = 0, 
        incrementor = None,
        bound = True,
        limit = 10000
    ):
        if not hasattr(object,'__iter__'):
            iterator = iter(iterator) 

        self.value = next(iterator)
        self.iterator = iterator
        self.stop = False
        self.index = starts_at
        self.use_index = index
        self.incrementor = incrementor
        self.bound = bound
        self.limit = limit
        self.limit_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.stop:
            raise StopIteration

        if self.limit != None and self.limit == self.limit_index:
            raise IterationLimitReached

        self.limit_index += 1

        if self.use_index:
            next_value = [self.index, self.value, self.iterate]
            if not self.bound:
                self.index = self.increment()
        else:
            next_value = [self.value, self.iterate]

        return next_value

    def iterate(self):
        try:
            self.value = next(self.iterator)

            if self.bound:
                self.index = self.increment()
        except StopIteration:
            self.stop = True
    
    def increment(self):
        if self.incrementor == None:
            return self.index + 1
        else: 
            return self.incrementor(self.index)  

my_list = [1,2,3,4,5]

for index, val, iterate in controlled(my_list, index=True):
    iterate()
    print(index, val)

print()

for index, val, iterate in controlled(my_list, index=True, bound=False):
    if index % 2 == 1:
        iterate()
    print(index, val)

print()

for index, val, iterate in controlled(
    my_list[::-1], 
    index=True,
    starts_at=len(my_list) * 2 - 1,
    incrementor=lambda index: index -1, 
    bound=False
):
    if index % 2 == 0:
        iterate()
    print(index, val)

print()
    
try:
    for index, val, iterate in controlled(my_list, index=True, limit=50):
        pass
except IterationLimitReached:
    print("At Limit")
