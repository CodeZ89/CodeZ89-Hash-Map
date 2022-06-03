# Name: Zach Chaloner
# OSU Email: chalonez@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date:06/03/2022
# Description: This program is the implementation of the Hash Map data structure using chaining
#              for collision resolution. The HashMap is initialized as a dynamic array of empty
#              singly linked lists and contains methods to add, remove, and adjust items depending
#              on input from the user. A separate function is included outside of the HashMap class,
#              find_mode, that allows a user to find the mode (most occurring) value of a dynamic array.
#              The find_mode function utilizes the HashMap data structure for storage and keeping track
#              of occurrences of the values in the dynamic array.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Method that places a key value pair in the HashMap. The function utilizes the given
        hash function to determine where the key/value pair is to be placed in the map. If the
        key already exists in the map, the key is maintained but the value of the key is changed
        to the value that is input into the function. If the key is not present, the key/value pair
        is added to the HashMap. Takes two parameters, key - a string to be used in the hash function,
        and the value that is associated with that key.
        """
        bucket_index = self._hash_function(key) % self._capacity    # determine DA index to place key/value pair
        new_bucket = self._buckets[bucket_index]
        check_contains = new_bucket.contains(key)                   # determine if a key is present in the SLL

        if check_contains:
            check_contains.value = value                            # replace value if key is already present in map
        else:
            self._buckets[bucket_index].insert(key, value)          # otherwise add key/value pair to corresponding
            self._size += 1                                         # SLL in the map

    def empty_buckets(self) -> int:
        """
        Method that determines the amount of empty buckets that are left in the
        HashMap. Takes no parameters, returns the integer value of empty buckets
        in the map.
        """
        num_empty = 0                   # initialize count

        # iterate through the map, increase count if a bucket is empty
        for bucket in range(self._buckets.length()):
            if self._buckets[bucket].length() == 0:
                num_empty += 1
        return num_empty

    def table_load(self) -> float:
        """
        Method that determines the current table load given by the equation:
        table load = current # of elements in the HashMap / current capacity of the HashMap.
        Takes no parameters, returns a floating point value of the current table load.
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Method that clears the current HashMap. It does not take any parameters and does not change
        the underlying capacity of the current map.
        """
        # iterate through current table, if an index contains any key/value pairs
        # initialize an empty linked list to replace the current SLL
        for bucket in range(self._buckets.length()):
            if self._buckets[bucket].length() != 0:
                self._buckets[bucket] = LinkedList()
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Method that resizes the current hash table based on the input parameter, new_capacity.
        If the new capacity is less than 1, the method does nothing. Otherwise the method resizes
        the current hash table and rehashes the existing values. All existing key/value pairs are
        rehashed into the new map utilizing the given hash_function. Takes one parameter new_capacity.
        """
        if new_capacity < 1:
            return

        old_map = self._buckets

        # create new HashMap to rehash values of the current map with the new capacity
        new_map = HashMap(new_capacity, self._hash_function)

        # iterate through the old hash table, rehash values if SLL is not empty
        for bucket in range(old_map.length()):
            # if bucket contains a SLL with key/value pairs, iterate through and rehash as necessary
            if old_map[bucket].length() != 0:
                iterator = old_map[bucket].__iter__()
                current_node = iterator.__next__()
                while current_node is not None:
                    new_map.put(current_node.key, current_node.value)
                    current_node = current_node.next

        # set values of the original HashMap to the rehashed values with the new capacity
        self._buckets = new_map._buckets
        self._capacity = new_capacity



    def get(self, key: str) -> object:
        """
        Method that returns the value of a given key. Takes one parameter the key
        that is being searched for. If the key is not present in the hash table,
        the method returns None.
        """
        bucket_index = self._hash_function(key) % self._capacity    # find index of given key
        target = self._buckets[bucket_index].contains(key)
        if target:                                                  # if key is in the table
            return target.value
        else:
            return None


    def contains_key(self, key: str) -> bool:
        """
        Method that determines if the current hash table contains a given key. The given key
        is run through the hash function, if it is present the method returns true, if it is
        not present it returns false.
        """
        bucket_index = self._hash_function(key) % self._capacity    # determine index of given key
        target = self._buckets[bucket_index].contains(key)          # determine if SLL contains given key

        if target:
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Method that removes a key/value pair from the hash table. Takes one parameter
        the key to be removed. If the key is not found, the method does nothing. If the
        key is found, the key/value pair is removed and the size of the hash table is
        decremented.
        """
        bucket_index = self._hash_function(key) % self._capacity
        target = self._buckets[bucket_index].contains(key)

        if target:
            self._buckets[bucket_index].remove(key)
            self._size -= 1
        else:
            return


    def get_keys(self) -> DynamicArray:
        """
        Method that returns a dynamic array with all the keys stored in the current hash map.
        Does not take any parameters.
        """

        key_array = DynamicArray()

        for bucket in range(self._buckets.length()):
            # if a bucket is not empty, append all keys to the new DA
            if self._buckets[bucket].length() != 0:
                iterator = self._buckets[bucket].__iter__()             # initialize iterator
                current_node = iterator.__next__()
                while current_node is not None:
                    key_array.append(current_node.key)                  # append key to DA
                    current_node = current_node.next
        return key_array


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Function outside of the HashMap class that finds the mode of a given dynamic array.
    The function utilizes the HashMap class to store the objects of the dynamic array
    with the object being the key and the value being the number of occurrences of that
    object in the original dynamic array. Takes one parameter, a dynamic array. Returns a tuple
    of a dynamic array containing the most occurring value(s)  and the count of how many
    times they occurred.
    """

    map = HashMap(da.length() // 3, hash_function_1)
    mode_array = DynamicArray()                         # new dynamic array that will contain mode value(s)
    count = 0                                           # initialize mode count

    # iterate through DA, determine the count of each object in the array
    for index in range(da.length()):
        # if value has already been seen, increment value
        if map.contains_key(da[index]):
            map.put(da[index], map.get(da[index]) + 1)
            # if current object matches the current mode, append current object to mode_array
            if count == map.get(da[index]):
                mode_array.append(da[index])
            # if current object has been seen more than current mode, create new DA with current object
            # increment the count
            elif count < map.get(da[index]) + 1:
                mode_array = DynamicArray()
                mode_array.append(da[index])
                count += 1
        else:
            # if a value has not been seen, place it in the hash map
            map.put(da[index], 1)
            # if mode_array is empty, put first value in the array, increment count
            if mode_array.length() == 0:
                mode_array.append(da[index])
                count += 1
            # if the current mode count is 1, append the new value to the mode array
            elif count == 1:
                mode_array.append(da[index])

    return mode_array, count

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")
