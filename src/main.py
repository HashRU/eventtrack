#!/usr/bin/python
# vim: set fileencoding=utf8 :

import csv
import datetime
import dateutil.parser
import itertools
import numpy
import math

class Event:
    pass

def read_entries():
    with open('../events.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        row_i = 1
        for row in reader:
            if len(row) != 8:
                print "Warning: unexpected %d rows (expected 8) on line %d" % (len(row), row_i)
                continue

            if row[0] == "naam":
                continue

            e = Event()
            e.naam, e.datum, e.aantal, e.moeite, e.doelmatig, e.sociaal, e.oordeel, e.comment = row
            e.datum = dateutil.parser.parse(e.datum, yearfirst=True, dayfirst=False).date()
            yield e
            row_i += 1

def group(xs, f):
    d = dict()
    for x in xs:
        k = f(x)
        if k not in d:
            d[k] = []

        d[k].append(x)
    return d

def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

d = group(read_entries(), lambda x: x.naam)
now = datetime.datetime.now().date()

for naam, xs in d.items():
    xs.sort(key=lambda x: x.datum)
    dates = map(lambda x: x.datum, xs)

    last_datum = dates[-1]
    date_diffs = map(lambda (x, y): (y - x).days, pairwise(dates))
    mean_diffs = numpy.mean(date_diffs)
    std_diffs = numpy.std(date_diffs)
    approx_next = (now - last_datum).days - int(math.ceil(mean_diffs))

    print "%s (%d)" % (naam, len(xs))
    print "  last time: %s (%d days ago)" % (last_datum, (now - last_datum).days)
    print "  period: %.2f ±%.2f" % (mean_diffs, std_diffs)

    if approx_next < 0:
        print "  approximate next event: %s days" % abs(approx_next)
    else:
        print "  EVENT TOO LATE NOOO: %s days" % approx_next
