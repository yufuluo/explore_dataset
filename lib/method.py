"""Methods for processing data.
"""

from typing import List

def sum(num: int, num_list: List[int]) -> int:
    """Methods for calculating the sum of an intger and a list of integer.

    Args:
        num: An integer. The current sum.
        num_list: A list of integer. The new set of data to be added to sum.

    Returns:
        An integer. The new result of sum.
    """
    result = num
    for item in num_list:
        result += item
    return result

def avg(num: int, num_list: List[int], size: int) -> int:
    """With a given size and average of an exising data set, adding a new list of data on top of the set,
    return the average of whole data set.

    Args:
        num: An integer. The current average.
        num_list: A list of integer. New data adding to the set.
        size: An integer. The size of the current data set.

    Returns:
        An integer. The result of new average.
    """
    sum = num * size
    for item in num_list:
        sum += item
    result = int(sum / (size + len(num_list)))
    return result
