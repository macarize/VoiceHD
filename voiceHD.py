import numpy as np

def genRandomHv(d):
    return np.random.randint(2, size=d)

def genFrequencyHv(n, d):
    frequencyHv = np.empty((1, d), dtype=int)

    for i in range(n):
        item = np.array([genRandomHv(d)])
        frequencyHv = np.append(frequencyHv, item, axis=0)

    frequencyHv = np.delete(frequencyHv, [0, 0], axis=0)
    return frequencyHv

def genLevelHv(m, d):
    flipBitsNum = int(d/(m-1))
    flipstart = 0
    levelHv = np.empty((1, d), dtype=int)
    item = np.array([genRandomHv(d)])
    levelHv = np.append(levelHv, item, axis=0)
    for i in range(0, m-1):
        lastItem = len(levelHv)-1
        item = levelHv[lastItem]
        flipedItem = np.array(flipBits(flipstart, flipBitsNum, item))
        levelHv = np.append(levelHv, [flipedItem], axis=0)
        flipstart = flipstart + flipBitsNum
    levelHv = levelHv[1:, :]
    return levelHv

def flipBits(f, n, a):
    temp = np.copy(a)
    for i in range(f, f+n):
        temp[i] = np.logical_not(temp[i]).astype(int)
    return temp

def encoding(data, m, d, f, l):
    n = data.shape[0]
    bins = np.arange(0, 20, 20/m)
    ci = np.zeros(d, dtype=int)

    for i in range(n):
        si = np.zeros(d, dtype=int)
        for j in range(617):
            levelIndex = np.digitize((data[i][j]+1)*10, bins)-1
            #print("levelIndex {}".format(levelIndex))
            temp = vectorXOR(f[j],l[levelIndex], d)
            #print("temp {}".format(temp))
            si = si + temp
        si = boundling(si, j)
        ci = ci + si
    ci = boundling(ci, n)
    return ci

def encodingSample(data, m, d, f, l):
    n = data.shape[0]
    bins = np.arange(0, 20, 20/m)
    for i in range(n):
        si = np.zeros(d, dtype=int)

        for j in range(617):
            levelIndex = np.digitize((data[i][j]+1)*10, bins)-1
            #print("levelIndex {}".format(levelIndex))
            temp = vectorXOR(f[j],l[levelIndex], d)
            #print("temp {}".format(temp))
            si = si + temp
        si = boundling(si, j)
    return si

def vectorXOR(A, B, d):
    newHv = genRandomHv(d)
    for i in range(d):
        if A[i] == B[i]:
            newHv[i] = 0
        else:
            newHv[i] = 1
    return newHv

def boundling(a, n):
    for i in range(a.shape[0]):
        if a[i]/n > 0.5:
            a[i] = 1
        else :
            a[i] = 0
    return a

def similartyCheck(a, b):
    acc = 0
    d = a.shape[0]

    for i in range(d):
        s1 = a[i]
        s2 = int(b[i])
        if s1 == s2:
            acc = acc + 1
    return acc

# GENERATE ID, LEVEL HV
# np.savetxt("10000_HDFQ.csv", genFrequencyHv(617, 10000), delimiter=",")
# np.savetxt("10000_HDLV.csv", genLevelHv(10, 10000), delimiter=",")

# LOAD DATASET
# rawData = np.loadtxt("isoletT.data", delimiter=",")
# frequencyHv = np.loadtxt('10000_HDFQ.csv', delimiter=",")
# levelHv = np.loadtxt('10000_HDLV.csv', delimiter=",")

# SEPERATE CLASES
# for k in range(1,27):
#     ar = np.zeros((1, 618))
#     print(k)
#     for i in range(len(rawData)):
#         classIndex = int(rawData[i][rawData.shape[1]-1])
#         if k == classIndex:
#             ar = np.append(ar, np.array([rawData[i]]), axis=0)
#
#     ar = np.delete(ar, 0, 0)
#     ar = np.delete(ar, ar.shape[1]-1, 1)
#     np.savetxt("TEST_ISOLET{}.csv".format(k),ar, delimiter=",")

# GENERATE CLASS HV
# for i in range(8,27):
#     print(i)
#     alphabetClass = np.loadtxt('ISOLET{}.csv'.format(i), delimiter=",")
#     n = alphabetClass.shape
#     d = 10000
#     m = 10
#
#     ClassHV = encoding(alphabetClass, m, d, frequencyHv, levelHv)
#     np.savetxt("10000_ClassHV{}.csv".format(i), ClassHV, delimiter=",")

# SIMIRARITY CHECK PER CLASS
# accNumArr = np.zeros(26)
# for k in range(1, 27):
#     similarty = np.zeros(26, dtype=int)
#     quary = np.loadtxt("TEST_ISOLET{}.csv".format(k), delimiter=",")
#     accNum = 0
#     print(k)
#     for j in range(quary.shape[0]):
#         quaryItem = np.array([quary[j]])
#         quaryHv = encodingSample(quaryItem, 10, 10000, frequencyHv, levelHv)
#         for i in range(1,27):
#             classHV = np.loadtxt("10000_ClassHV{}.csv".format(i), delimiter=",")
#             similarty[i-1] = similartyCheck(quaryHv, classHV)
#         AlphabetClass = np.argmax(similarty)
#         if AlphabetClass == k-1:
#             accNum += 1
#         accNumArr[k-1] = accNum
#
# print(accNumArr)
