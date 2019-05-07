#!/usr/bin/python

import sys
try:
    import psutil
    import yaml
except ImportError:
    msg = "\nPython %s\n\nModule import error:\n%s\n"
    sys.exit(msg % (sys.version, sys.exc_info()[1]))


def main(drives):
    sendmail = False
    for drive in drives:
        try:
            driveinfo = str(psutil.disk_usage(drive).percent)
            if not sendmail and float(driveinfo) >= 90:
                sendmail = True
        except FileNotFoundError:
            driveinfo = "(path not found)"
        except Exception:
            driveinfo = "(unknown error)"
        finally:
            print(drive, driveinfo)

    if sendmail:
        print("\ntoo high values were found")


if __name__ == '__main__':
    main(["\\\\jlm-pc-shlomi\\c$", "\\\\jlm-fs-8\\e$"])
    sys.exit(0)
