#!/usr/bin/python

import sys
import psutil


def spacemon(disks=['.']):
    stats = {}
    for disk in disks:
        try:
            diskinfo = psutil.disk_usage(disk).percent
        except OSError:  # FileNotFoundError
            disk += '_path_not_found'
            diskinfo = -1
        except Exception:
            print(sys.exc_info()[1])  # This should go to the log
            disk += '_unknown_error'
            diskinfo = -1
        finally:
            stats[disk] = diskinfo
    return stats


def mailMsg(stats, threshold=90):
    values = [value for key, value in stats.items()]
    if max(values) >= threshold:
        return 'disk usage alert'
    elif min(values) == -1:
        return 'could not access some disks'
    else:
        return 0


def mailer(msg, stats, mail):
    if mail['server'] == 'None':
        print('Should send mail but SMTP sever is set to None')
    else:
        import smtplib
        server = smtplib.SMTP(mail['server'], 25)
        server.sendmail(mail['sender'], mail['recipients'], "msg-body")
    return 0


def main(cfg):
    import logging
    logging.basicConfig(filename=cfg['logfile'],
                        filemode='a',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%b-%d-%y %H:%M:%S')
    stats = spacemon(cfg['disks'])
    msg = mailMsg(stats, cfg['threshold'])
    if msg:
        logging.warning(stats)
        mailer(msg, stats, cfg['mail'])
    else:
        logging.info(stats)
    return 0


def parseYml(configfile='SpaceMon.yml'):
    import yaml
    try:
        with open(configfile, 'r') as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        return main(cfg)
    except IOError:  # FileNotFoundError
        if configfile == '-h' or configfile == '--help':
            return 'Usage: SpaceMon.py [config-file]'
        elif configfile[:1] == '-':
            return 'unknown argument'
        else:
            return 'config/log file access error'
    except (TypeError, yaml.scanner.ScannerError):
        msg = '%s is not a valid yml file'
        return msg % (configfile)
    except KeyError:
        msg = 'The key %s is missing in %s'
        return msg % (sys.exc_info()[1], configfile)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        configfile = '--help'
    elif len(sys.argv) == 2:
        configfile = sys.argv[1]
    else:
        configfile = 'SpaceMon.yml'
    sys.exit(parseYml(configfile))
