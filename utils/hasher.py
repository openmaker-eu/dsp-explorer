import hashlib

class HashHelper(object):
    @staticmethod
    def md5_hash(string):
        return hashlib.md5(string.encode("utf")).hexdigest()