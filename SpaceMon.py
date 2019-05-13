#!/usr/bin/python

__version__ = '1.0'

import sys
import psutil


def spacemon(disks=['.']):
    stats = {}
    for disk in disks:
        print(disk)
        try:
            diskinfo = psutil.disk_usage(disk).percent
        except OSError:  # FileNotFoundError
            disk += '_path_not_found'
            diskinfo = -1
        except Exception:
            # print(sys.exc_info()[1])  # DEBUG
            disk += '_unknown_error'
            diskinfo = -1
        finally:
            stats[disk] = diskinfo
    return stats


def mailMsg(stats, threshold=90):
    values = [v for k, v in stats.items()]
    if max(values) >= threshold:
        return 'disk usage alert'
    elif min(values) == -1:
        return 'could not access some disks'
    else:
        return 0


def mailer(mSubject, stats, mail, logfile):
    mBody1 = str(stats)
    mBody2 = 'The full log is %s' % (logfile)
    m = 'Subject: {}\n\n{}\n{}'.format(mSubject, mBody1, mBody2)
    import smtplib
    server = smtplib.SMTP(mail['server'], 25)
    server.sendmail(mail['sender'], mail['recipients'], m)


def main(cfg):
    import logging
    logging.basicConfig(filename=cfg['logfile'],
                        filemode='a',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%b-%d-%y %H:%M:%S')
    stats = spacemon(cfg['disks'])
    mSubject = mailMsg(stats, cfg['threshold'])
    # Replace Windows systems' escaped slash:
    stats = {k.replace('\\\\', '\\'): v for k, v in stats.items()}
    if mSubject:
        logging.warning(stats)
        if cfg['mail']['server'] != 'None':
            problems = {k: v for k, v in stats.items()
                        if not (-1 < v < cfg['threshold'])}
            mailer(mSubject, problems, cfg['mail'], cfg['logfile'])
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
        mSubject = '%s is not a valid yml file'
        return mSubject % (configfile)
    except KeyError:
        mSubject = 'The key %s is missing in %s'
        return mSubject % (sys.exc_info()[1], configfile)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        configfile = '--help'
    elif len(sys.argv) == 2:
        configfile = sys.argv[1]
    else:
        configfile = 'SpaceMon.yml'
    sys.exit(parseYml(configfile))
