'''
Function to do parameter checking in application.
'''

# --------------------------------------------------------------------
'''
Imports
'''

from typing import List, Union

# --------------------------------------------------------------------
'''
Function Definition
'''

def required(para:Union[List[str], set]) -> Union[str, None]:

    '''
    Check that the required parameters have been passed into the request. 

    If parameters are not passed in requests, Flask.request.args.get("parameter_name") should return None.
    '''

    for name in para:
        val = locals()[name]
        if val == None:
            return f"Input Parameter Error: {name}. Parameter Not Found.\nThe parameter was not found in the submitted request."