import math

Dec = "0123456789"
Hex = "0123456789ABCDEF"
Bin = "01"
plaintextlist=[]


def XOR(x,y):
    xorans=""
    for dd in range(len(y)):
        if(x[dd]==y[dd]):
            xorans+="0"
        else:
            xorans+="1"
    return xorans


pc1 = [56, 48, 40, 32, 24, 16, 8,
         0, 57, 49, 41, 33, 25, 17,
         9, 1, 58, 50, 42, 34, 26,
         18, 10, 2, 59, 51, 43, 35,
         62, 54, 46, 38, 30, 22, 14,
         6, 61, 53, 45, 37, 29, 21,
         13, 5, 60, 52, 44, 36, 28,
         20, 12, 4, 27, 19, 11, 3
         ]

pc2 = [
    13, 16, 10, 23, 0, 4,
    2, 27, 14, 5, 20, 9,
    22, 18, 11, 3, 25, 7,
    15, 6, 26, 19, 12, 1,
    40, 51, 30, 36, 46, 54,
    29, 39, 50, 44, 32, 47,
    43, 48, 38, 55, 33, 52,
    45, 41, 49, 35, 28, 31
]

ip = [57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7,
        56, 48, 40, 32, 24, 16, 8, 0,
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6
        ]

expansion_table = [
    31, 0, 1, 2, 3, 4,
    3, 4, 5, 6, 7, 8,
    7, 8, 9, 10, 11, 12,
    11, 12, 13, 14, 15, 16,
    15, 16, 17, 18, 19, 20,
    19, 20, 21, 22, 23, 24,
    23, 24, 25, 26, 27, 28,
    27, 28, 29, 30, 31, 0
]


sbox = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

pafters = [
    15, 6, 19, 20, 28, 11,
    27, 16, 0, 14, 22, 25,
    4, 17, 30, 9, 1, 7,
    23, 13, 31, 26, 2, 8,
    18, 12, 29, 5, 21, 10,
    3, 24
]


def sboxnumber(listitem):
    if(listitem[0]+listitem[-1]=="00"):
        row=0
    elif (listitem[0]+listitem[-1]=="01"):
        row=1
    elif (listitem[0] + listitem[-1] == "10"):
        row=2
    elif (listitem[0] + listitem[-1] == "11"):
        row=3

    if(listitem[1:5]=="0000"):
        column=0
    elif(listitem[1:5]=="0001"):
        column=1
    elif(listitem[1:5]=="0010"):
        column=2
    elif(listitem[1:5]=="0011"):
        column=3
    elif(listitem[1:5]=="0100"):
        column=4
    elif(listitem[1:5]=="0101"):
        column=5
    elif(listitem[1:5]=="0110"):
        column=6
    elif(listitem[1:5]=="0111"):
        column=7
    elif(listitem[1:5]=="1000"):
        column=8
    elif(listitem[1:5]=="1001"):
        column=9
    elif(listitem[1:5]=="1010"):
        column=10
    elif(listitem[1:5]=="1011"):
        column=11
    elif(listitem[1:5]=="1100"):
        column=12
    elif(listitem[1:5]=="1101"):
        column=13
    elif(listitem[1:5]=="1110"):
        column=14
    elif(listitem[1:5]=="1111"):
        column=15
    return row,column



def hextobin(hexnumber):
    ans=""
    for i in range(len(hexnumber)):
        if(hexnumber[i]=="0"):
            ans+="0000"
        elif (hexnumber[i] == "1"):
            ans+="0001"
        elif (hexnumber[i] == "2"):
            ans+="0010"
        elif (hexnumber[i] == "3"):
            ans+="0011"
        elif (hexnumber[i] == "4"):
            ans+="0100"
        elif (hexnumber[i] == "5"):
            ans+="0101"
        elif (hexnumber[i] == "6"):
            ans+="0110"
        elif (hexnumber[i] == "7"):
            ans+="0111"
        elif (hexnumber[i] == "8"):
            ans+="1000"
        elif (hexnumber[i] == "9"):
            ans+="1001"
        elif (hexnumber[i] == "A"):
            ans+="1010"
        elif (hexnumber[i] == "B"):
            ans+="1011"
        elif (hexnumber[i] == "C"):
            ans+="1100"
        elif (hexnumber[i] == "D"):
            ans+="1101"
        elif (hexnumber[i] == "E"):
            ans+="1110"
        elif (hexnumber[i] == "F"):
            ans+="1111"
    return ans


def setD(j, k,num):  # Convert from decimal
    l = int(j)
    n = ""
    while (l > 0):
        n = k[l % len(k)] + n
        l = math.floor(l / len(k))
    if(k==Bin):
        while(len(n)<num):
            n="0"+n
    return (n)

fp = [
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25,
    32, 0, 40, 8, 48, 16, 56, 24
]


def shiftone(element):
    return element[1:]+element[:1]

def shifttwo(element):
    return element[2:]+element[:2]


def keycreation(key):


    tobin=hextobin(key)
    key2=""
    for i in range(len(pc1)):
        index=pc1[i]
        key2+=str(tobin[index])

    left=key2[:28]
    right=key2[28:]

    leftlist=[]
    rightlist=[]
    finallist=[]


    j=1
    for i in range(16):
        if(j==1):
            keyee=left[1:]+left[:1]
            leftlist.append(keyee)
            keyee=right[1:]+right[:1]
            rightlist.append(keyee)
        elif(j==2 or j==9 or j==16):
            keyee=shiftone(leftlist[i-1])
            leftlist.append(keyee)
            keyee=shiftone(rightlist[i-1])
            rightlist.append(keyee)
        else:
            keyee=leftlist[i-1][2:]+leftlist[i-1][:2]
            keyee=shifttwo(leftlist[i-1])
            leftlist.append(keyee)
            keyee = shifttwo(rightlist[i-1])
            rightlist.append(keyee)
        j=j+1
        keyee=""

    for x in range(len(rightlist)):
        keyfin=leftlist[x]+rightlist[x]
        finallist.append(keyfin)

    key3=""
    finalkeylist=[]

    for c in range(len(finallist)):
        for d in range(len(pc2)):
            index = pc2[d]
            key3 += str(finallist[c][index])
        finalkeylist.append(key3)
        key3=""
    return finalkeylist



def enc(numberofenc,plaintextlist,finalkeylist):
    for numb in range(numberofenc):
        mtobin=hextobin(plaintextlist[-1])
        message1=""

        for f in range(len(ip)):
            index=ip[f]
            message1+=str(mtobin[index])

        leftm=message1[:32]
        rightm=message1[32:]

        leftmessage=[]
        rightmessage=[]

        leftmessage.append(leftm)
        rightmessage.append(rightm)

        number=16
        jj=1

        for no in range(number):
            rseq = ""
            sboxx = []
            befors = []
            sboxapp = ""
            leftmessage.append(rightmessage[jj-1])
            for ff in range(len(expansion_table)):
                index = expansion_table[ff]
                rseq += str(rightmessage[jj-1][index])

            xorkey=XOR(rseq,finalkeylist[jj-1])


            for xx in range(8):
                ind = xx * 6
                befors.append(xorkey[ind:ind + 6])

            for z in range(len(befors)):
                x, y = sboxnumber(befors[z])
                sboxx.append(sbox[z][x][y])

            for f in range(len(sboxx)):
                sett=setD(sboxx[f],Bin,4)
                sboxapp+=sett
            mafters=""
            for ss in range(len(pafters)):
                index = pafters[ss]
                mafters += str(sboxapp[index])
            finalxor=XOR(mafters,leftmessage[jj-1])
            rightmessage.append(finalxor)
            jj+=1



        finalmbin= rightmessage[-1]+leftmessage[-1]

        finalmessagebin=""
        for ss1 in range(len(fp)):
            index = fp[ss1]
            finalmessagebin += str(finalmbin[index])


        finalmdec=int(finalmessagebin,2)
        finalmhex=hex(finalmdec)[2:].upper()

        plaintextlist.append(finalmhex)
    return plaintextlist


def main():
    print("-------------WELCOME TO DES-------------")
    print("please enter the key: ")
    keyin=str(input()).upper()
    print("please enter the plaintext: ")
    plaintext=str(input()).upper()
    print("please enter the number on encryptions: ")
    numberofenc=int(input())
    print("encrypt or decrypt?? ")
    y=str(input())

    finalkeylist=[]
    finalkeylist=keycreation(keyin)

    #plaintext="355550B2150E2451"
    list1=[]
    if(y.lower()=="encrypt"):
        plaintextlist.append(plaintext)
        list1=enc(numberofenc,plaintextlist,finalkeylist)
        print("the message after encryption is:",list1[-1])
    elif(y.lower()=="decrypt"):
        finalkeyinverse=[]
        finalkeyinverse=finalkeylist[::-1]
        leftchar=plaintext[:16]
        rightchar=plaintext[16:]
        messagefinal1=rightchar+leftchar
        plaintextlist.append(messagefinal1)
        list1=enc(numberofenc,plaintextlist,finalkeyinverse)
        print("the message after decryption is:",list1[-1])
    print("press any key to close")
    x=input()


if __name__ == "__main__":
    main()
















