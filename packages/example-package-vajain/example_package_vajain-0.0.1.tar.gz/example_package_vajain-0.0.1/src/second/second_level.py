from  example_package_vajain.first import first_level

if __name__ == "__main__":
    print('second level file')

def subtract_one_multiply_two(number):
    num = first_level.subtract_one(number)
    return num * 2