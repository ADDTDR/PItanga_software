from font5x7 import Font5x7_90

def reverse_bits(num):
    num_bits = 5
    reversed_num = 0
    for i in range(num_bits):        
        reversed_num = reversed_num << 1                
        reversed_num = reversed_num | (num & 1)
        
        num = num >> 1

    return reversed_num


if __name__ == "__main__" :
    print('[')
    data  = Font5x7_90
    for ch in data:

        line = []
        for a in ch[::-1]: 
            line.append(int( "0b{0:05b}".format( reverse_bits( a) ), 2))
        
        print(line,',')
    print(']')