#!/usr/bin/python

import sys
try:
    import psutil
    # import traceback
except ImportError:
    msg = "\nPython %s\n\nModule import error:\n%s\n"
    sys.exit(msg % (sys.version, sys.exc_info()[1]))


def main(disks):
    results = {}
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
            results[disk] = diskinfo
    return results


def mailer(msg, results):
    print(msg)
    print(results)
    return 0


def mail_run(results, threshold):
    values = [value for key, value in results.items()]
    maxval = max(values)
    minval = min(values)
    if maxval >= threshold:
        return mailer("disk usage alert", results)
    elif minval == -1:
        return mailer("could not acccess some disks", results)
    else:
        return 0


def yaml_run(configfile="SpaceMon.yml"):
    try:
        import yaml
    except ImportError:
        msg = "\nPython %s\n\nModule import error:\n%s\n"
        sys.exit(msg % (sys.version, sys.exc_info()[1]))
    try:
        with open(configfile, 'r') as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        return mail_run(main(cfg['disks']), cfg['threshold'])
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
    sys.exit(yaml_run(configfile))
