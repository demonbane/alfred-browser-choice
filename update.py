# encoding: utf-8

from workflow import Workflow3

def gethandlers():
    import os
    import re
    rexps = [
        re.compile('^\s*(bundle)\s*id:\s*(\d*)'),
        re.compile('^\s*(path):\s*(.*)'),
        re.compile('^\s*(name):\s*(.*)'),
        re.compile('^\s*(bindings):\s*(.*)')
    ]
    handlers = {}
    bundle = ""
    name = ""
    path = ""

    dump = os.popen("/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/LaunchServices.framework/Versions/A/Support/lsregister -dump")

    for line in dump.readlines():
        for rexp in rexps:
            m = rexp.match(line)
            if not m:
                continue

            key = m.group(1)
            value = m.group(2)

            if key == "bundle":
                if bundle != value:
                    bundle = value
                    name = ""
                    path = ""

            if key == "name" and not name:
                name = value

            if key == "path" and not path:
                path = value

            if key == "bindings" and 'http:' in value.split(","):
                handlers[name] = path

    dump.close()
    handlers.pop('nwjs', None)
    handlers.pop('VLC media player', None)
    return handlers

def main(wf):
    browsers = wf.cached_data('handlers', gethandlers, max_age=600)
    # Record our progress in the log file
    wf.logger.debug('{} handlers cached'.format(len(browsers)))

if __name__ == '__main__':
    wf = Workflow3()
    wf.run(main)
