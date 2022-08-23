# Description: This program is an implementation of a hash map that utilizes open addressing for
#              collision resolution. The methods included in this program are put - to add a key/value
#              pair to the current map, table load - to determine the current load on the hash table,
#              empty buckets - to determine the number of empty buckets in the current hash table,
#              resize table - to resize the hash table as needed, get - to get the value of a given key
#              in the table, contains key - to determine if a given key is present in the hash table,
#              remove - to remove a key/value pair from the hash table, clear - to clear the current table,
#              and get keys - to get all of the existing keys in the hash table. Functionality of the methods
#              is described in details in their individual doc-strings below.


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Method that updates the key/value pair in the hash map. If the given key already exists, the
        current key's value is replaced with the given value. If the key is not present in the current
        hash table, they key/value pair is added. To deal with collisions, the method utilizes quadratic
        probing to find an empty spot that a key/value pair can be added, if the index that is associated
        with a current key is currently full. At any point, if the table load is greater than or equal to
        0.5, the hash table will be resized and the current key/value pairs will be rehashed into the new
        table. Takes 2 parameters, key to be added to the table and its associated value.
        """

        # check table load, resize if greater than or equal to 0.5
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)                   # resize to 2x current capacity

        bucket_index = self._hash_function(key) % self._capacity    # index of hash of current key
        new_index = self._hash_function(key) % self._capacity       # new index if index already contains key/value pair
        placer = self._buckets[bucket_index]                        # set placer to key at bucket index
        new_spot = 0                                                # used for quadratic probing

        # if placer is not None, probe to an empty spot in the table
        while placer:
            # account for removed values by checking if the current placer is a tombstone
            # if a tombstone is found, replace the the tombstone with the new key/value
            if placer.is_tombstone:
                placer.key = key
                placer.value = value
                placer.is_tombstone = False         #reset tombstone to False
                self._size += 1
                return
            # while probing, if the key to be placed matches an existing key, replace existing keys value
            if placer.key == key:
                placer.value = value
                return
            # if spot is not empty, continue to probe
            new_spot += 1
            new_index = (bucket_index + new_spot**2) % self._capacity
            placer = self._buckets[new_index]

        # reaches here when there is an empty spot, adds key/value to the table
        self._buckets[new_index] = HashEntry(key, value)
        self._size += 1


    def table_load(self) -> float:
        """
        Method that returns a floating point value of the current table load. Takes no parameters.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Method that returns the current integer amount of empty buckets in the hash table.
        Key/value pairs that are tombstones are not considered empty.
        """
        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        Method to resize the current hash table by changing its current capacity to the given new_capacity.
        All existing key/value pairs remain in the new hash table and are rehashed according to the new
        capacity. If the new_capacity parameter is less than 1 or it is less than the current number of
        elements in the hash table, the method does nothing. During resizing, if a key/value pair is found
        to be a tombstone, it is not carried over to the new table.
        """
        if new_capacity < 1 or new_capacity < self._size:
            return

        old_buckets = self._buckets                             # maintain the current buckets in the hash table

        new_map = HashMap(new_capacity, self._hash_function)    # create new hash map that will store the rehashed
                                                                # values
        # iterate through the current buckets
        for bucket in range(old_buckets.length()):
            # skip over a bucket if it is empty or the key/value pair present is a tombstone
            if old_buckets[bucket] is None or old_buckets[bucket].is_tombstone:
                continue
            else:
                # rehash values into the new map accordingly
                new_map.put(old_buckets[bucket].key, old_buckets[bucket].value)

        # set current hash map buckets and capacity to the rehashed buckets based on the new capacity
        self._buckets = new_map._buckets
        self._capacity = new_map._capacity

    def get(self, key: str) -> object:
        """
        Method that takes a key as a parameter and returns the value that is associated with the given
        key. Method quadratically probes to find the key in the hash map.
        """

        bucket_index = self._hash_function(key) % self._capacity  # index of hash of current key
        placer = self._buckets[bucket_index]  # set placer to key at bucket index
        new_spot = 0  # used for quadratic probing

        # if placer is not None, probe to an empty spot in the table
        while placer:
            # while probing, if the key to be placed matches an existing key, replace existing keys value
            if placer.key == key:
                if placer.is_tombstone:
                    return None
                else:
                    return placer.value
            # if spot is not empty, continue to probe
            new_spot += 1
            # maintain original index, utilize new index value to go to the next probe index
            new_index = (bucket_index + new_spot ** 2) % self._capacity
            placer = self._buckets[new_index]


    def contains_key(self, key: str) -> bool:
        """
        Method that determines if a given key is present in the hash table. Quadratically probes
        using the given key to find an initial value in the hash table. Returns True if the key
        is present in the table, returns False if the key is present or if they key is a tombstone
        """
        bucket_index = self._hash_function(key) % self._capacity  # index of hash of current key
        placer = self._buckets[bucket_index]  # set placer to key at bucket index
        new_spot = 0  # used for quadratic probing

        # if placer is not None, probe to an empty spot in the table
        while placer:
            # while probing, if the key to be placed matches an existing key, replace existing keys value
            if placer.key == key:
                if placer.is_tombstone:
                    return False
                else:
                    return True
            # if spot is not empty, continue to probe
            new_spot += 1
            new_index = (bucket_index + new_spot ** 2) % self._capacity
            placer = self._buckets[new_index]

        return False

    def remove(self, key: str) -> None:
        """
        Method that removes a key/value pair from the hash table. Quadratically probes the table starting
        at the index determined by putting the key through the hash function. If a given key is already
        marked as a tombstone, the method will do nothing. Otherwise, if the key is found, the object
        at the given key is marked as a tombstone (is_tombstone = True). They key/value are unchanged.
        """
        bucket_index = self._hash_function(key) % self._capacity  # index of hash of current key
        placer = self._buckets[bucket_index]  # set placer to key at bucket index
        new_spot = 0  # used for quadratic probing

        # if placer is not None, probe to an empty spot in the table
        while placer:
            # while probing, if the key to be placed matches an existing key, replace existing keys value
            if placer.key == key:
                # if key is already a tombstone, exit
                if placer.is_tombstone:
                    return
                else:
                    # make object a tombstone - decrement size of hash map
                    placer.is_tombstone = True
                    self._size -= 1
                    return
            # if spot is not empty, continue to probe
            new_spot += 1
            new_index = (bucket_index + new_spot ** 2) % self._capacity
            placer = self._buckets[new_index]


    def clear(self) -> None:
        """
        Method that clears the contents of the hash table. Takes no parameters.
        """
        new_map = HashMap(self._capacity, self._hash_function)  # create new hash table with same capacity
        self._buckets = new_map._buckets                        # clear buckets of the old hash table
        self._size = 0                                          # reset size of hash table

    def get_keys(self) -> DynamicArray:
        """
        Method that returns a Dynamic Array that is populated with the keys that are present
        in the current hash table. Takes no parameters.
        """
        key_array = DynamicArray()
        # iterate through hash table, append keys to the new array
        for bucket in range(self._buckets.length()):
            # skip over tombstones
            if self._buckets[bucket] is not None and not self._buckets[bucket].is_tombstone:
                key_array.append(self._buckets[bucket].key)

        return key_array



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

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

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
