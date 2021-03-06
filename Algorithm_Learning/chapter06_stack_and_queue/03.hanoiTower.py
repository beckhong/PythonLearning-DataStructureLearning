def hanoi(n, p1, p2, p3):
    if n == 1:  # recursive exit
        print('ring move from %d to %d' % (p1, p3))

    else:
        hanoi(n - 1, p1, p3, p2)
        print('ring move form %d to %d' % (p1, p3))
        hanoi(n - 1, p2, p1, p3)


j = int(input('please enter the total ring want to move: '))
hanoi(j, 1, 2, 3)

'''
以n=3為例
step 1.
[ 123| | ]

step 2.
[ 23| | 1]

step 3.
[ 3| 2| 1]

step 4.
[ 3| 12| ]

step 5.
[ | 12| 3]

step 6.
[ 1| 2| 3]

step 7.
[ 1| | 23]

step 8.
[ | | 123]
'''