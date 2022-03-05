'''
Utility functions
'''

def add(v1, v2):
    ''' Element-wise vector addition '''
    return [a+b for a, b in zip(v1, v2)]