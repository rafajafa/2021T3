import numpy

def drykiss(my_list):
    #use min instead of loop
    my_min = min(my_list)

    #make a new list without the last index and use numpy.prod for the result
    new_list = [my_list[i] for i in range(0,4)]
    result = numpy.prod(new_list)

    new_list = [my_list[i] for i in range(1,5)]
    product = numpy.prod(new_list)

    result = (my_min, result, product)
    
    return result

    
if __name__ == '__main__':
    # put them in the same line
    a, b, c, d, e = input("Enter a: "), input("Enter b: "), input("Enter c: "), input("Enter d: "), input("Enter e: ")
    my_list = int([a, b, c, d, e])
    result = drykiss(my_list)
    # all in one print statement
    print(f'''Minimum: {result[0]} \nProduct of first 4 numbers: {result[1]}\n
    Product of last 4 numbers: {result[2]} ''')

