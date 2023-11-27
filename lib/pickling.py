import bz2
import pickle
import _pickle as cPickle
from lib.aes256 import AESCipher

# Pickle a file and then compress it into a file with extension 
def compress_pickle(filename, data, key = None):
  if key is None:
    with bz2.BZ2File(filename, 'w') as f: 
      cPickle.dump(data, f)
  else:
    with open(filename, "wb") as f:
      aes = AESCipher(key)
      f.write(aes.encrypt(bz2.compress(cPickle.dumps(data))))
      f.flush()

# Load any compressed pickle file
def decompress_pickle(filename, key = None):
  if key is None:
    data = bz2.BZ2File(filename, 'rb')
    data = cPickle.load(data)
    return data
  else:
    with open(filename, "rb") as f:
      aes = AESCipher(key)
      return cPickle.loads(bz2.decompress(aes.decrypt(f.read())))
