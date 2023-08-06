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
