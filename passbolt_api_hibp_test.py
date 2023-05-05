#!/usr/bin/env python3
# Author Dario Clavijo 2023

import passboltapi
import json
import pwnedpasswords
import sys
from os.path import exists, getsize
from tqdm import tqdm
import urllib3
from lib.pickling import *

urllib3.disable_warnings()
passbolt = passboltapi.PassboltAPI(config_path="config.ini", new_keys=True)


def load_dict(passbolt):
  """
  loads into a dictionary resources grouped by their passwords
  output: dictionary 
  """
  sys.stderr.write("Gathering resources from passbolt...\n")
  D = {}
  for r in tqdm(passbolt.get(url="/resources.json?api-version=v2")['body']):
    if ((password := passbolt.get_password(r['id'])) != None):
      t = (r['id'], r['name'],r['username'],r['uri'],r['description'])
      if password not in D:
        D[password] = [t]
      else:
        D[password].append(t)
  return D


def proc_dict(passbolt, D):
  """
  Checks every password in the dictionary if its broken.
  input: dictionary
  output: broken_plain_password_list
  """
  sys.stderr.write("Checking new(%d) passwords hashes against HIBP...\n" % len(D))
  return [password for password in tqdm(D) if pwnedpasswords.check(password, plain_text=True) > 0]


def proc_pickle(D, key=None):
  """
  loads a pickle and a dictinary and returns a list of keys that are not in the pickle
  input dictionary
  output: broken_plain_password_list
  """
  filename = ".%s.pkl" % sys.argv[0]
  pkldata = []
  if exists(filename) and getsize(filename) > 16: pkldata = decompress_pickle(filename,key=key)
  newdata = [password for password in D if password not in pkldata]
  compress_pickle(filename, pkldata + newdata, key=key)
  return newdata

def display_broken(broken):
  """
  Display info in the dictionary using elements of broken list as key.
  input: broken_plain_password_list
  """
  sys.stderr.write("Results:\n")
  for password in broken:
    sys.stdout.write("-" * 60 + "\n")
    sys.stdout.write("broken password: %s\n" % password)
    for t in D[password]:
      msg = "id:%s, name:%s, username:%s, uri: %s, description: %s\n" % t
      sys.stdout.write(msg)
    sys.stdout.flush()
  sys.stderr.write("Total broken: %d\n" % len(broken))
  sys.stderr.flush()


if __name__ == "__main__":
  D = load_dict(passbolt)
  D1 = proc_pickle(D,key=passbolt.config["PASSBOLT"]["PASSPHRASE"])
  broken = proc_dict(passbolt, D1)
  display_broken(broken)
