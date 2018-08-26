"""Open a URL in different browsers"""

from __future__ import print_function, absolute_import

import sys
import argparse
from workflow import Workflow3, ICON_INFO
from workflow.background import run_in_background, is_running

def main(wf):
    """Run Script Filter."""

    parser = argparse.ArgumentParser()
    parser.add_argument('query', nargs='?', default=None)
    args = parser.parse_args(wf.args)

    url = "http" + args.query

    browsers = wf.cached_data('handlers', None, max_age=0)

    if wf.update_available:
        # Add a notification to top of Script Filter results
        wf.add_item('New version available',
                    'Action this item to install the update',
                    autocomplete='workflow:update',
                    icon=ICON_INFO)

    if not wf.cached_data_fresh('handlers', max_age=600):
        cmd = ['/usr/bin/python', wf.workflowfile('update.py')]
        run_in_background('update', cmd)

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
    wf = Workflow3(update_settings={'github_slug': 'demonbane/alfred-browser-choice'})
    sys.exit(wf.run(main))
