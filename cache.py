import os
from hashlib import sha1

class Cache:
    def __init__(self, websites):
        self.hashes = dict()
        self.hashMap = dict()
        self.websites = websites
        self.createCache()

    def getHash(self, url):
        if url not in self.hashes.keys():
            newHash = sha1(url.encode()).hexdigest()
            self.hashes[url] = newHash
            self.hashMap[newHash] = url
        return self.hashes[url]
    def createCache(self):
        for url in self.websites:
            path = f"data/{self.getHash(url)}"
            if not os.path.isfile(path):
                open(path, 'x')
    def readCache(self):
        content = []
        for url in self.websites:
            path = f"data/{self.getHash(url)}"
            f = open(path, 'r')
            content.append(f.read())

