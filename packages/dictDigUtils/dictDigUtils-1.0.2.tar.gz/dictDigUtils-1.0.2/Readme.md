# dict dig utils
Some functionality would be quite comfortable to manipulate dicts,
and that we do not have to write them all the time.
Perhaps they already exist, but for any case, here is a simple
version of them for myself.

# flattening
First thing is to turn keys into a flattened string, like
* key1
  * key2
    * key3

turns to key1/key2/key3
Then texts can be easily searched in keys and values withuot
transversing the whole structure


# display
a simple printing function that indents with the levels of the
dict may be intuitive to see what is in a dict.

# search for a key
within the whole tree, and return whatever element is found under it
in a list, allowing for multiple keys.
It searches text in the key, thus using the in operator.

# list keys
run through recursively, and give a list of keys from within.
This is useful for complex, deep dict trees, when one has no idea
where to find a specific key, or how it is spelled.
