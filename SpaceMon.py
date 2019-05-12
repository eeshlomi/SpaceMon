#!/usr/bin/python

import sys
try:
    import psutil
    # import traceback
except ImportError:
    msg = "\nPython %s\n\nModule import error:\n%s\n"
    sys.exit(msg % (sys.version, sys.exc_info()[1]))


def spacemon(disks=['.']):
    stats = {}
    for disk in disks:
        try:
            diskinfo = psutil.disk_usage(disk).percent
        except OSError:  # FileNotFoundError
            disk += "_path_not_found"
            diskinfo = -1
        except Exception:
            # print(traceback.format_exc())
            disk += "_unknown_error"
            diskinfo = -1
        finally:
            stats[disk] = diskinfo
    return stats


def mailer(msg, stats):
    return 0


def mailMsg(stats, threshold):
    values = [value for key, value in stats.items()]
    if max(values) >= threshold:
        return "disk usage alert"
    elif min(values) == -1:
        return "could not acccess some disks"
    else:
        return 0


def main(cfg):
    stats = spacemon(cfg['disks'])
    msg = mailMsg(stats, cfg['threshold'])
    print(stats)  # DEBUG
    if msg:
        print(msg)  # call mailer
    return 0


def parseYml(configfile="SpaceMon.yml"):
    try:
        import yaml
    except ImportError:
        msg = "\nPython %s\n\nModule import error:\n%s\n"
        sys.exit(msg % (sys.version, sys.exc_info()[1]))
    try:
        with open(configfile, 'r') as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        return main(cfg)
    except IOError:  # FileNotFoundError
        if configfile == "-h" or configfile == "--help":
            sys.exit("Usage: %s [config-file]" % (sys.argv[0]))
        elif configfile[:1] == "-":
            sys.exit("unknown argument")
        else:
            msg = "\n%s not found\n"
            sys.exit(msg % (configfile))
    except KeyError:
        msg = "\nThe key %s is missing in %s\n"
        sys.exit(msg % (sys.exc_info()[1], configfile))


if __name__ == '__main__':
    if len(sys.argv) > 2:
        configfile = "--help"
    elif len(sys.argv) == 2:
        configfile = sys.argv[1]
    else:
        configfile = "SpaceMon.yml"
    sys.exit(parseYml(configfile))
