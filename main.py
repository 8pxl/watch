import os
def getWebsites():
    return [line.rstrip() for line in open("sites.txt", 'r').readlines()]

print(getWebsites())
