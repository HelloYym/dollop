from hashlib import sha1
import hmac
import time

def get_unix_time():
    return str(int(time.time()))

def get_login_signature(username, password, timestamp, secret_key=None, is_upper=None):
    msg = "username={username}&password={password}&timestamp={timestamp}".format(username=username, password=password,
                                                                                 timestamp=timestamp)
    if secret_key:
        if is_upper:
            return hmac.new(secret_key, msg, sha1).digest().encode('hex').upper()
        else:
            return hmac.new(secret_key, msg, sha1).digest().encode('hex')
    else:
        if is_upper:
            return hmac.new(password, msg, sha1).digest().encode('hex').upper()
        else:
            return hmac.new(password, msg, sha1).digest().encode('hex')

def get_access_signature(token, timestamp, secret_key, is_upper=None):
    msg = "token={token}&timestamp={timestamp}".format(token=token, timestamp=timestamp)
    if is_upper:
        return hmac.new(secret_key, msg, sha1).digest().encode('hex').upper()
    else:
        return hmac.new(secret_key, msg, sha1).digest().encode('hex')
