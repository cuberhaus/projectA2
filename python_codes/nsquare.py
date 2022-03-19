while (True):
    print("choose an n")
    n = int(input())

    for i in range(n):
        j = i+1
        print(str(j) + " : " + str(j*j))