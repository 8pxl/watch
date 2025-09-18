import os
from hashlib import sha1

class Cache:
    def __init__(self, websites):
        self.hashes = dict()
        self.urlMap = dict()
        self.websites = websites
        # self.populateUrlMap()
        for url in websites:
            print(url)
            newHash = self.createHash(url)
            self.hashes[url] = newHash
            self.urlMap[newHash] = url
        self.createCache()

    def createHash(self, string):
        return sha1(string.encode()).hexdigest()

    def addUrl(self, url):
        newHash = self.createHash(url)
        self.hashes[url] = newHash
        self.urlMap[newHash] = url

    def getHash(self, url):
        if url not in self.hashes.keys():
            print("invalid hash")
            newHash = self.createHash(url)
            self.hashes[url] = newHash
            self.urlMap[newHash] = url
        return self.hashes[url]

    def getUrl(self, hash):
        return self.urlMap[hash]
    
    def pathFromUrl(self, url):
        return f"data/{self.getHash(url)}"

    # def populateUrlMap(self):
    #     for url in self.websites:
    #         self.urlMap[url] = self.getHash(url)
            
    def createCache(self):
        if not os.path.isdir("data/"):
            os.makedirs("data/")
        for url in self.websites:
            path = self.pathFromUrl(url)
            if not os.path.isfile(path):
                open(path, 'x')

    def updateCache(self, url, new):
        f = open(self.pathFromUrl(url), 'w')
        f.write(new)

    def readCache(self):
        content = dict()
        for url in self.websites:
            path = self.pathFromUrl(url)
            f = open(path, 'r')
            content[url] = f.read()
            f.close()
        return content

