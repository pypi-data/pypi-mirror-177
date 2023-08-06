def bubble_sort(input_list):
    """
        Input:
            input_list is the list provided as input.
        Output:
            Returns and changes the original input_list to a sorted list.
    """
    input_list_length = len(input_list)

    for pointer1 in range(input_list_length):

        for pointer2 in range(input_list_length-pointer1-1):

            if input_list[pointer2] > input_list[pointer2 + 1] :

                temp = input_list[pointer2]
                input_list[pointer2] = input_list[pointer2+1]
                input_list[pointer2+1] = temp
    
    return input_list     

