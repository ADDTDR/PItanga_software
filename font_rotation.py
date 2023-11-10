from font5x7 import Font5x7_full as Font5x7

def rotate_90(a):
        b = []
        for k in range(0, 7):       	
            q = [(x & (1 << k)) >> k for x in a ]
            qi = 0
            for bit in q:    
                qi = (qi << 1) | bit
            b.append(qi)
        return b


if __name__ == '__main__':
    print('Font5x7_90 = [')
    for e in Font5x7:
        print(rotate_90(e),',')
    print(']')