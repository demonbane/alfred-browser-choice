# encoding: utf-8

from workflow import Workflow3
import sys
import logging

def gethandlers():
    import os
    from LaunchServices import (LSCopyApplicationURLsForURL,
                            kLSRolesAll,
                            CFURLCreateWithString)

    url = CFURLCreateWithString(None, 'http://example.com', None)
    apps = {}

    nsurls = LSCopyApplicationURLsForURL(url, kLSRolesAll)
    paths = set([wf.decode(nsurl.path()).rstrip('/') for nsurl in nsurls])

    for path in paths:
        name = os.path.splitext(os.path.basename(path))[0]
        if name in 'nwjs' 'VLC media player':
            continue
        apps[name] = path
        log.debug('http handler : {} // {}'.format(
                  name, path))

    log.debug('{} handlers cached'.format(len(apps)))

    return apps


def main(wf):
    browsers = wf.cached_data('handlers', gethandlers, max_age=600)

if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    if sys.stdout.isatty():
        log.setLevel(logging.DEBUG)
        log.debug('Running in a terminal')
    wf.run(main)
