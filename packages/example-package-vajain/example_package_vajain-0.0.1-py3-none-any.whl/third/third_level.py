from  ..second import second_level

if __name__ == "__main__":
    print('third level file')

def subtract_one_multiply_two_add_three(number):
    num = second_level.subtract_one_multiply_two(number)
    return num + 3