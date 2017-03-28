#!/usr/bin/env python

import pandas as pd

from namereader import *

dirname = 'PML_NAME_output'

fs = fileset.Fileset(dirname)

#files = fs.weeks[19]
#files = fs.months['5']
files = fs.years['2015']

print files

n = name.Name(files[0])
n.add_all()

m = n.trimmed()
m = m.rename(columns={'subtotal': 'total'})

for f in files[1::]:
    print 'Loading: ', f
    n2 = name.Name(f)
    n2.add_all()
    m2 = n2.trimmed()
    m = pd.merge(m, m2, how='outer', on=['Longitude', 'Latitude'])
    m = m.fillna(0)

    m.total = m.total + m.subtotal
    m = m.drop('subtotal', 1)

    t = m.total
    print t.loc[t > 0.0].count()

p = m.total
print p.loc[ p > 1e-5 ]
  

