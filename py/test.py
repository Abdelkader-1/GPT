
test='''

import pandas as pd

query_result = [{'Month': 1, 'Sales': 1.318139e+08},
                {'Month': 11, 'Sales': 1.861424e+08},
                {'Month': 3, 'Sales': 1.512389e+08},
                {'Month': 4, 'Sales': 1.681386e+08},
                {'Month': 5, 'Sales': 1.496555e+08},
                {'Month': 9, 'Sales': 1.753187e+08},
                {'Month': 12, 'Sales': 1.691831e+08},
                {'Month': 2, 'Sales': 1.217120e+08},
                {'Month': 8, 'Sales': 1.612069e+08},
                {'Month': 6, 'Sales': 1.515772e+08},
                {'Month': 10, 'Sales': 1.813816e+08},
                {'Month': 7, 'Sales': 1.496348e+08}]
result = pd.DataFrame(query_result)
result
'''
exec(test)