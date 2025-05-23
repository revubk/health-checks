#!/usr/bin/env python
import os
import sys
import shutil
import socket

def check_reboot():
  """Returns True if the computer hs a pending reboot."""
  return os.path.exists("/run/reboot-required")

def check_disk_full(disk, min_gb, min_percent):
  du = shutil.disk_usage(disk)
  percent_free = 100 * du.free / du.total
  gigabytes_free = du.free / 2**30
  if gigabytes_free < min_gb or percent_free < min_percent:
    return True
  return False

def check_root_full():
    """Reboot True if the root partition is full, False otherwise"""
    return check_disk_full(disk="/", min_gb=2, min_percent=10)

def check_no_network():
    """Return True if it fails to resolve Google's URL, False otherwise"""
    try:
        socket.gethostbyname("www.google.com")
        return False
    except:
        return True
def main():
  checks=[
        (check_reboot, "Pending Reboot."),
        (check_root_full, "Root partition full."),
        (check_no_network, "No working network."),
  ]
  everything_ok= True
  for check, msg in checks:
    if check():
      print(msg)
      sys.exit(1)
  if not everything_ok:
    sys.exit(1)


  print("Everything is OK.")
  sys.exit(0)
main()
