def linear_search(input_list, search_key):
    """
        Input: 
            input_list is the list input provided to the function.
            search_key is the element to be searched inside the list.
        Output:
            If search_key not found, return False.
            If search key is  found, return key's position in the list.
    """
    length_of_input_list = len(input_list)
    for current_position in range(length_of_input_list):
        if input_list[current_position] == search_key :
            return current_position
    return False

def binary_search(input_list,search_key,left_pointer,right_pointer):
    """
            Input:
                input_list is the list provided as the input.
                left_pointer acts as the boundary for the left side of the list.
                right pointer acts as the boundary for the right side of the list.
                search_key is the element to be searched.
            Output:
                if search key is  found, returns the position of the search_key.
                if search key not found, returns False.
    """

    if right_pointer >=1 :
        mid_point = left_pointer + (right_pointer - left_pointer)//2

        if input_list[mid_point] == search_key :
            return mid_point
        elif input_list[mid_point] > search_key :
            return binary_search(input_list, search_key, left_pointer, mid_point - 1)
        else:
            return binary_search(input_list, search_key, mid_point + 1, right_pointer)
    else:
        return False
