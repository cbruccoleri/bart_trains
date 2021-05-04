#!/usr/bin/env python
#
# Author: Christian Bruccoleri
# Email: cbruccoleri@gmail.com
# Date: 5/5/2021
#
# License: MIT License

"""Queries BART to get the time of next departures from the origin station.

- Times are given in minutes from now.
- 0 replaces 'Leaving' when a train is leaving at the time of request
- Errors are handled (to the extent possible)

Usage:
    $ python departures.py [ORIGIN]

    List all south-bound departures from the ORIGIN station. If ORIGIN is 
    omitted, selects El Cerrito Plaza (default). ORIGIN can be any string 
    allowed by the BART API station abbreviations. If instead the string 
    `testing` is provided as argument, it runs the local example tests for
    debugging.
"""

import sys
import json
import glob
try:
    import requests
except:
    print('Please install the `requests` library from PyPI.\nE.g.:\n\t$ pip install requests')
    sys.exit(-1)

# Example API:
# http://api.bart.gov/api/etd.aspx?cmd=etd&orig=RICH&key=MW9S-E7SL-26DU-VV8V&json=y

bartURL = 'http://api.bart.gov/api/etd.aspx'


def get_departures(
    origin: str='RICH',
    direction: str='s',
    testcase: object=None,
    verbose: bool=False) -> list:
    """Get a list of south-bound departures from the desired station.
    
    Each element of the list is a dictionary containing the information
    on that departure. Departures are separated by destination.

    Input:
        origin      Departing station abbreviation (see BART abbreviations).
        testcase    Use the provided response as test case.
        verbose     If True, print additional output for debugging.

    Output:
        A list of departure times from the specified origin. 
        `None` if an error occurrs.
    """

    try:
        if testcase is None:
            # prepare a dictionary with the arguments to the API
            reqParams = {
                 "cmd": "etd",
                "orig": origin,
                 "dir": direction,
                 "key": "MW9S-E7SL-26DU-VV8V",
                "json": "y"
            }
            # make the actual request
            r = requests.get(bartURL, params=reqParams)
            r.raise_for_status() # raise exception on HTTP Errors
            
            if verbose:
                print(r.url)
            # Note: this is a blocking request. In an App, one would use a 
            # non-blocking request through the asincio module.
            resp = r.json()
            # TODO: check error codes
        else:
            # use the provided testcase
            resp = testcase

        if verbose:
            print(json.dumps(resp, sort_keys=True, indent=4))

        # get a list of departures; note: we know we have only one station
        # by requirements, otherwise must loop over the departing stations too.
        try:
            depList = resp['root']['station'][0]['etd']
        except:
            # service is closed or no trains available.
            depList = []
        minutesList = []
        for dep in depList:
            for depData in dep['estimate']:
                try:
                    m = int(depData['minutes'])
                except ValueError as ex:
                    #print('ValueError:', depData['minutes'], file=sys.stderr) # debug
                    m = 0
                minutesList.append(m)

        return minutesList
    except requests.exceptions.RequestException as ex:
        # print error on stderr for debugging
        # this should be removed in production and use a logging system instead.
        print('[!] Error: could not complete the request.', file=sys.stderr)
        print(ex, file=sys.stderr)
        return None


def do_tests():
    """Run all the test cases in the current folder."""
    test_files = sorted(glob.glob('./test*.json'))
    for fname in test_files:
        with open(fname) as ftest:
            print(fname)
            jsonobj = json.load(ftest)
            print(get_departures(origin='PLZA', testcase=jsonobj, verbose=False))       
            print('-----')


if __name__=='__main__':
    if len(sys.argv) > 1:
        org = sys.argv[1]
        if org == 'testing':
            # special origin: run the local tests
            dep_list = None
            do_tests()
        else:
            # Get the origin from the argument list
            # See abbreviations at:
            # https://api.bart.gov/docs/overview/abbrev.aspx
            dep_list = get_departures(origin=org)
    else:
        # Use default origin
        dep_list = get_departures(origin='PLZA')
    if dep_list is not None:
        print(dep_list)
