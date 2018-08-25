"""Open a URL in different browsers"""

from __future__ import print_function, absolute_import

import sys
import argparse
from workflow import Workflow3, ICON_INFO
from workflow.background import run_in_background, is_running

def main(wf):
    """Run Script Filter."""

    # build argument parser to parse script args and collect their
    # values
    parser = argparse.ArgumentParser()
    # add an optional query and save it to 'query'
    parser.add_argument('query', nargs='?', default=None)
    # parse the script's arguments
    args = parser.parse_args(wf.args)

    url = "http" + args.query

    browsers = wf.cached_data('handlers', None, max_age=0)

    # Start update script if cached data are too old (or doesn't exist)
    if not wf.cached_data_fresh('handlers', max_age=600):
        cmd = ['/usr/bin/python', wf.workflowfile('update.py')]
        run_in_background('update', cmd)

    # Notify the user if the cache is being updated
    if is_running('update'):
        wf.add_item('Refreshing installed browsers',
                    valid=False,
                    icon=ICON_INFO)

    for b in sorted(browsers):
        it = wf.add_item(title='Open in ' + b,
                    subtitle=browsers[b],
                    arg=url,
                    icon=browsers[b],
                    icontype='fileicon',
                    valid=True,
            )
        it.setvar('browser', browsers[b])
        it.setvar('url', url)

    wf.send_feedback()


if __name__ == '__main__':
     wf = Workflow3()
     sys.exit(wf.run(main))
