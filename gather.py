import functools

# taken from class notes
def memoize(bad_f):
    # note we're attaching the memo
    # dictionary to our function
    # here. It becomes part of the
    # data attached to our function
    # this way, if we want, we can
    # clear our memoized values if we
    # are concerned about htis dictionary
    # growing too large
    bad_f.memo = {}

    # functools.wraps is a decorator
    # we can use to take all the meta data
    # from bad_f (like the function name and
    # docstring) add it to good_f.
    # This way we don't lose our doctests,
    # doctests, function name
    # and other good meta data
    @functools.wraps(bad_f)
    def good_f(*args, **kwargs):
        # Remember that *args and **kwargs allow
        # us to accept a variable number of input arguments
        # args is a tuple with all input values
        # and kwargs is a dictionary with all key = value
        # pairs provided as arguements for our function.
        my_key = repr(args) + repr(kwargs)
        # repr is like str in that it gives us a representation
        # of our object. However, str is for human reading
        # and repr is intended for "python" reading.
        # it is guaranteed to be a unique, immutable
        # representation of our args.
        if my_key not in bad_f.memo:
            # Note that we need to use *args andk **kwargs
            # when calling bad_f so that our args tuple and
            # kwargs dictionary get re-expanded into useful
            # inputs to our function
            bad_f.memo[my_key] = bad_f(*args, **kwargs)
        return bad_f.memo[my_key]
    return good_f


def gather(transport, unit_list, value):
    """
    Finds the maximum possible "value" of troops that can be loaded
    in to the remaining space of a transport.

    Input:
     transport - The transport unit to be loaded.
     unit_list - The list of units that can be loaded onto transport.
       You may assume that these units are non-transport ground units
       that are already on the same team as the transport, have not
       moved this turn, and can reach the transport with a single move.
     value - a function that maps a unit to some value

    Output:
     A list of units from unit_list. Do NOT load them into the transport
     here, just compute the list of units with maximum possible value whose
     total size is at most the remaining capacity of the transport.

     The calling function from gui.py will take care of loading them.

    Target Complexity:
     It is possible to implement this method to run in time
     O(n * C) where n is the number of units in unit_list and C
     is the remaining capacity in the transport. Remember, the capacity
     of a transport and the sizes of the units are all integers.
    """
    
    # the unused capacity of the transport
    remain = transport.capacity

    @memoize
    def best_value(index, max_size):
        """
        best_value returns the best sequence for the first index elements
        weight must add up to less than max_size.

        The inital function call runs at O(C) where C is the transport capacity.
        It will run at O(max_size).

        Doctests are complicated to create for this function since we
        need an active unit list, therefore we just tested in in game.
        """
        next_index = index - 1
        if index == 0:
            return 0
        val = value(unit_list[next_index])  # the current unit value
        weight = unit_list[next_index].unit_size  # the current unit weight

        if weight > max_size:  # if the unit weights more than the avaiable room
            # check if any other units can fit the size remaining
            return best_value(next_index, max_size)
        else:
            # return the best result between the current unit combination and
            # the unit combination that includes the next unit
            return max(best_value(next_index, max_size),
                       best_value(next_index, max_size - weight) + val)

    gathered = []
    # for every unit in unit_list (n), iterating backwards in order to exclude
    # dupicates in the possibility tree
    unit_range = range(len(unit_list), 0, -1)
    for i in unit_range:
        if best_value(i, remain) != best_value(i-1, remain):
            gathered.append(unit_list[i-1])
            remain -= unit_list[i-1].unit_size

    # return the list of units from an optimal solution
    # note, in particular, that we have not actually loaded them here
    return gathered
