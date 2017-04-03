#!/usr/bin/python

import fileinput
from datetime import datetime
import sys

if len(sys.argv) == 1:
    # @todo: logging
    print "argv[1]: acceptDelta in days is required"
    sys.exit(2)

today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
acceptDelta = int(sys.argv[1])

for line in sys.stdin:
    lineDate = datetime.strptime(line.strip(), "%d.%m.%Y")
    if ((today-lineDate).total_seconds()/24/60/60) > acceptDelta:
        # Delta reached, we can stop downloading more pages
        sys.exit(1)
    