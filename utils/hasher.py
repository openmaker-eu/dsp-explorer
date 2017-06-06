import hashlib

class HashHelper(object):
    @staticmethod
    def md5_hash(email):
        return hashlib.md5(email.encode("utf")).hexdigest()