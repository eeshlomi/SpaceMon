#!/usr/bin/python

import sys
try:
    import psutil
except ImportError:
    msg = "\nPython %s\n\nModule import error:\n%s\n"
    sys.exit(msg % (sys.version, sys.exc_info()[1]))


def main(disks, threshold, email):
    sendmail = False
    for disk in disks:
        try:
            diskinfo = str(psutil.disk_usage(disk).percent)
            if not sendmail and float(diskinfo) >= float(threshold):
                sendmail = True
        except FileNotFoundError:
            diskinfo = "(path not found)"
        except Exception:
            diskinfo = "(unknown error)"
        finally:
            print(disk, diskinfo)

    if sendmail:
        print("\ntoo high values were found")


if __name__ == '__main__':
    try:
        import yaml
    except ImportError:
        msg = "\nPython %s\n\nModule import error:\n%s\n"
        sys.exit(msg % (sys.version, sys.exc_info()[1]))
    configfile = "SpaceMon.yml"
    try:
        with open(configfile, 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        main(cfg['disks'], cfg['threshold'], cfg['email'])
        sys.exit(0)
    except FileNotFoundError:
        sys.exit(configfile+" not found")
