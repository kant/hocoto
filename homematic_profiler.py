#!/usr/bin/env python3
'''test'''
# pylint # {{{
# vim: tw=100 foldmethod=marker
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy
# pylint: disable=multiple-statements
# }}}


import sys
import os
import datetime
import sqlite3
import json
import logging
import configargparse

dry_run = False
try:
    from homegear import Homegear
except:
    print ('homegear python module not found; running in dry profile_name')
    dry_run = True

def parseOptions():# {{{
    '''Parse the commandline options'''
# | ID | Name                      | Address | Serial     | Type | Type String |
# |----+---------------------------+---------+------------+------+-------------|
# | 1  | HM Entkleide OEQ1718409   | 63A25E  | OEQ1718409 | 095  | HM-CC-RT-DN |
# | 2  | HM Wohnzimmer OEQ1711775  | 638586  | OEQ1711775 | 095  | HM-CC-RT-DN |
# | 3  | HM Kueche vorn OEQ1711363 | 638718  | OEQ1711363 | 095  | HM-CC-RT-DN |
# | 4  | HM Kueche hinten  OEQ1... | 63A260  | OEQ1718411 | 095  | HM-CC-RT-DN |
# | 5  | HM Gaestezimmer OEQ171... | 63A278  | OEQ1718437 | 095  | HM-CC-RT-DN |
# | 6  | HM Bad OEQ1718406         | 63A255  | OEQ1718406 | 095  | HM-CC-RT-DN |

    path_of_executable = os.path.realpath(sys.argv[0])
    folder_of_executable = os.path.split(path_of_executable)[0]

    config_files = [os.environ['HOME']+'/.config/ldf-interface.conf',
                    folder_of_executable + '/ldf-interface.conf',
                    '/root/configs/ldf-interface.conf']

    parser = configargparse.ArgumentParser(
            default_config_files = config_files,
            description='''test''')
    parser.add('-c', '--my-config', is_config_file=True, help='config file path')
    parser.add_argument('--verbose', '-v', action="count", default=0, help='Verbosity')
    parser.add_argument('all_args', nargs='*')
    parser.add_argument('--logfile', default='/tmp/test-py.log')
    parser.add_argument('--loglevel',                      default='debug')
    parser.add_argument('--device', type=int)
    parser.add_argument('--day', choices = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"])
    parser.add_argument('--profile_name', '--mode', choices = ["fma", "ma", "t", "ta", "a"])
    parser.add_argument('--put', action='store_true', default=False)
    parser.add_argument('--get', action='store_true', default=False)
    parser.add_argument('--db_file', default='homematic_profile.db')

    args = parser.parse_args()
    # print(parser.format_values())
    return args, parser
#}}}
def eventHandler(eventSource, peerId, channel, variableName, value):# {{{
    # This callback method is called on Homegear variable changes
    '''event handler'''
    # Note that the event handler is called by a different thread than the main thread. I. e. thread synchronization is
    # needed when you access non local variables.
    print("Event handler called with arguments: source: " + eventSource + \
            ";\n     peerId: " + str(peerId) + \
            ";\n     channel: " + str(channel) + \
            ";\n     variable name: " + variableName + \
            ";\n     value: " + str(value))
# }}}
def profile_generator(profilename, day_short_name):# {{{
    '''Generate profiles for given weekday'''
    # Global variables
    now = datetime.datetime.now()
    days = {'mon': 'MONDAY',
            'tue': 'TUESDAY',
            'wed': 'WEDNESDAY',
            'thu': 'THURSDAY',
            'fri': 'FRIDAY',
            'sat': 'SATURDAY',
            'sun': 'SUNDAY',
            'today': now.strftime("%A").upper() }
    day_name = days[day_short_name]
    
    t_lo    = 17
    t_med   = 19
    t_high  = 20
    t_hottt = 21
    profiles={}
    profiles['a']={}
    profiles['a']['temp']={}
    profiles['a']['time']={}
    profiles['a']['temp'][0] = t_lo     ; profiles['a']['time'][0] = 60* 16 + 0
    profiles['a']['temp'][1] = t_high   ; profiles['a']['time'][1] = 60* 24 + 0
    profiles['a']['temp'][2] = t_lo     ; profiles['a']['time'][2] = 60* 24 + 0
    profiles['a']['temp'][3] = t_lo     ; profiles['a']['time'][3] = 60* 24 + 0
    profiles['a']['temp'][4] = t_lo     ; profiles['a']['time'][4] = 60* 24 + 0
    profiles['a']['temp'][5] = t_lo     ; profiles['a']['time'][5] = 60* 24 + 0
    profiles['a']['temp'][6] = t_lo     ; profiles['a']['time'][6] = 60* 24 + 0
    profiles['a']['temp'][7] = t_lo     ; profiles['a']['time'][7] = 60* 24 + 0
    profiles['a']['temp'][8] = t_lo     ; profiles['a']['time'][8] = 60* 24 + 0
    profiles['a']['temp'][9] = t_lo     ; profiles['a']['time'][9] = 60* 24 + 0
    profiles['a']['temp'][10]= t_lo     ; profiles['a']['time'][10]= 60* 24 + 0
    profiles['a']['temp'][11]= t_lo     ; profiles['a']['time'][11]= 60* 24 + 0
    profiles['a']['temp'][12]= t_lo     ; profiles['a']['time'][12]= 60* 24 + 0
    profiles['a']['temp'][13]= t_lo     ; profiles['a']['time'][13]= 60* 24 + 0

    profiles['ma']={}
    profiles['ma']['temp']={}
    profiles['ma']['time']={}
    profiles['ma']['temp'][0] = t_lo     ; profiles['ma']['time'][0] = 60*  6 + 0
    profiles['ma']['temp'][1] = t_high   ; profiles['ma']['time'][1] = 60*  8 + 0
    profiles['ma']['temp'][2] = t_lo     ; profiles['ma']['time'][2] = 60* 16 + 0
    profiles['ma']['temp'][3] = t_med    ; profiles['ma']['time'][3] = 60* 23 + 0
    profiles['ma']['temp'][4] = t_lo     ; profiles['ma']['time'][4] = 60* 24 + 0
    profiles['ma']['temp'][5] = t_lo     ; profiles['ma']['time'][5] = 60* 24 + 0
    profiles['ma']['temp'][6] = t_lo     ; profiles['ma']['time'][6] = 60* 24 + 0
    profiles['ma']['temp'][7] = t_lo     ; profiles['ma']['time'][7] = 60* 24 + 0
    profiles['ma']['temp'][8] = t_lo     ; profiles['ma']['time'][8] = 60* 24 + 0
    profiles['ma']['temp'][9] = t_lo     ; profiles['ma']['time'][9] = 60* 24 + 0
    profiles['ma']['temp'][10]= t_lo     ; profiles['ma']['time'][10]= 60* 24 + 0
    profiles['ma']['temp'][11]= t_lo     ; profiles['ma']['time'][11]= 60* 24 + 0
    profiles['ma']['temp'][12]= t_lo     ; profiles['ma']['time'][12]= 60* 24 + 0
    profiles['ma']['temp'][13]= t_lo     ; profiles['ma']['time'][13]= 60* 24 + 0

    profiles['fma']={}
    profiles['fma']['temp']={}
    profiles['fma']['time']={}
    profiles['fma']['temp'][0] = t_lo     ; profiles['fma']['time'][0] = 60*  5 + 00
    profiles['fma']['temp'][1] = t_high   ; profiles['fma']['time'][1] = 60*  9 + 0
    profiles['fma']['temp'][2] = t_lo     ; profiles['fma']['time'][2] = 60* 17 + 0
    profiles['fma']['temp'][3] = t_med    ; profiles['fma']['time'][3] = 60* 21 + 00
    profiles['fma']['temp'][4] = t_high   ; profiles['fma']['time'][4] = 60* 23 + 0
    profiles['fma']['temp'][5] = t_lo     ; profiles['fma']['time'][5] = 60* 24 + 0
    profiles['fma']['temp'][6] = t_lo     ; profiles['fma']['time'][6] = 60* 24 + 0
    profiles['fma']['temp'][7] = t_lo     ; profiles['fma']['time'][7] = 60* 24 + 0
    profiles['fma']['temp'][8] = t_lo     ; profiles['fma']['time'][8] = 60* 24 + 0
    profiles['fma']['temp'][9] = t_lo     ; profiles['fma']['time'][9] = 60* 24 + 0
    profiles['fma']['temp'][10]= t_lo     ; profiles['fma']['time'][10]= 60* 24 + 0
    profiles['fma']['temp'][11]= t_lo     ; profiles['fma']['time'][11]= 60* 24 + 0
    profiles['fma']['temp'][12]= t_lo     ; profiles['fma']['time'][12]= 60* 24 + 0
    profiles['fma']['temp'][13]= t_lo     ; profiles['fma']['time'][13]= 60* 24 + 0

    profiles['t']={}
    profiles['t']['temp']={}
    profiles['t']['time']={}
    profiles['t']['temp'][0] = t_lo     ; profiles['t']['time'][0] = 60*  8 + 0
    profiles['t']['temp'][1] = t_high   ; profiles['t']['time'][1] = 60* 10 + 0
    profiles['t']['temp'][2] = t_med    ; profiles['t']['time'][2] = 60* 18 + 0
    profiles['t']['temp'][3] = t_lo     ; profiles['t']['time'][3] = 60* 24 + 0
    profiles['t']['temp'][4] = t_lo     ; profiles['t']['time'][4] = 60* 24 + 0
    profiles['t']['temp'][5] = t_lo     ; profiles['t']['time'][5] = 60* 24 + 0
    profiles['t']['temp'][6] = t_lo     ; profiles['t']['time'][6] = 60* 24 + 0
    profiles['t']['temp'][7] = t_lo     ; profiles['t']['time'][7] = 60* 24 + 0
    profiles['t']['temp'][8] = t_lo     ; profiles['t']['time'][8] = 60* 24 + 0
    profiles['t']['temp'][9] = t_lo     ; profiles['t']['time'][9] = 60* 24 + 0
    profiles['t']['temp'][10]= t_lo     ; profiles['t']['time'][10]= 60* 24 + 0
    profiles['t']['temp'][11]= t_lo     ; profiles['t']['time'][11]= 60* 24 + 0
    profiles['t']['temp'][12]= t_lo     ; profiles['t']['time'][12]= 60* 24 + 0
    profiles['t']['temp'][13]= t_lo     ; profiles['t']['time'][13]= 60* 24 + 0

    profiles['ta']={}
    profiles['ta']['temp']={}
    profiles['ta']['time']={}
    profiles['ta']['temp'][0] = t_lo     ; profiles['ta']['time'][0] = 60*  8 + 0
    profiles['ta']['temp'][1] = t_med    ; profiles['ta']['time'][1] = 60* 19 + 30
    profiles['ta']['temp'][2] = t_high   ; profiles['ta']['time'][2] = 60* 23 + 50
    profiles['ta']['temp'][3] = t_lo     ; profiles['ta']['time'][3] = 60* 24 + 0
    profiles['ta']['temp'][4] = t_lo     ; profiles['ta']['time'][4] = 60* 24 + 0
    profiles['ta']['temp'][5] = t_lo     ; profiles['ta']['time'][5] = 60* 24 + 0
    profiles['ta']['temp'][6] = t_lo     ; profiles['ta']['time'][6] = 60* 24 + 0
    profiles['ta']['temp'][7] = t_lo     ; profiles['ta']['time'][7] = 60* 24 + 0
    profiles['ta']['temp'][8] = t_lo     ; profiles['ta']['time'][8] = 60* 24 + 0
    profiles['ta']['temp'][9] = t_lo     ; profiles['ta']['time'][9] = 60* 24 + 0
    profiles['ta']['temp'][10]= t_lo     ; profiles['ta']['time'][10]= 60* 24 + 0
    profiles['ta']['temp'][11]= t_lo     ; profiles['ta']['time'][11]= 60* 24 + 0
    profiles['ta']['temp'][12]= t_lo     ; profiles['ta']['time'][12]= 60* 24 + 0
    profiles['ta']['temp'][13]= t_lo     ; profiles['ta']['time'][13]= 60* 24 + 0

    params={}
    for i in range(1,13):
        params["TEMPERATURE_%s_%d"%(day_name, i)] = profiles[profilename]['temp'][i-1]
        params["ENDTIME_%s_%d"%(day_name, i)]     = profiles[profilename]['time'][i-1]
    return(params)
# }}}

################### sqlite ##############
def dict_factory(cursor, row):# {{{
    '''helper for json export from sqlite'''
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
# }}}
def init_sqlite_tables(db_file):# {{{
    '''helper to initialise sql db'''
    # Setup SQL tables
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    try:
        cur.execute('''create table if not exists hp_device_day_profile_map'''
            '''(device INTEGER, weekday TEXT, profile TEXT)''')
        # cur.execute('''create index if not exists name_index ON konto(name)''')
        conn.commit()
        conn.close()

    except sqlite3.OperationalError as e:
        print ("SQL Create error: " + str(e))
        raise
    # self.db_was_initialised = True
# }}}
def store_entry_in_db(db_file, device, day, profile):# {{{
    '''Store profile for given weekday and device'''
    # Setup SQL connection # {{{
    conn = sqlite3.connect(db_file)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    # }}}
    # do sqlite query {{{
    try:
        query = '''delete from hp_device_day_profile_map where device=%s and weekday='%s' ''' %\
                (device, day);
        # print ("Query in store_entry_in_db: " + query)
        cur.execute(query)
        conn.commit()
        query = '''insert into hp_device_day_profile_map values (%d, '%s', '%s')''' %\
                (device, day, profile)
        # print ("Query in store_entry_in_db: " + query)
        cur.execute(query)
        conn.commit()

    except sqlite3.OperationalError as e:
        print ("SQL read error: " + str(e))
        return(False)
    conn.close()
    return(True)
    # }}}
# }}}
def read_entry_from_db(db_file, device, day):# {{{
    '''Read some or all entries from sqlite'''
    # Setup SQL connection # {{{
    conn = sqlite3.connect(db_file)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    # }}}
    # do sqlite query {{{
    try:
        query = '''select * from hp_device_day_profile_map where device=%d and weekday='%s' ''' %\
            (device, day)
        # print ("Query in read_entry_from_db: " + query)
        cur.execute(query)
        conn.commit()
        allentries = cur.fetchall()
        if len(allentries) > 1:
            print ("Warning; Query >>%s<< yielded %d entries; Expected only one. Using last one" %
                (query, len(allentries)))

    except sqlite3.OperationalError as e:
        print ("SQL read error: " + str(e))
    conn.close()
    # print ("SQL Result: %s" % str(allentries))
    return (allentries[-1]['profile'])
    # }}}
# }}}
################### /sqlite ##############


################## MAIN ########################
(args, parser) = parseOptions()
if dry_run:
    args.verbose += 1

# Setup logging
logformat = "{%(asctime)s %(filename)s:%(funcName)s:%(lineno)d} %(levelname)s - %(message)s"
loglevel = logging.getLevelName(args.loglevel.upper())
logging.basicConfig(level=loglevel, format=logformat, filename=args.logfile)
logging.debug('\nhomematirc_profiler- v.0.0.2')

# logging.info(parser.format_values())

init_sqlite_tables(args.db_file)

if args.put:# {{{
    # sanity checking:
    if args.device is None:
        print("device is not specified but required when using --put")
        exit(2)
    if args.day is None:
        print("day is not specified but required when using --put")
        exit(2)
    if args.profile_name is None:
        print("profile_name is not specified but required when using --put")
        exit(1)

    store_entry_in_db(args.db_file, args.device, args.day, args.profile_name)

    if not dry_run:
        hg = Homegear("/var/run/homegear/homegearIPC.sock", eventHandler)

        # in_params = hg.getParamset(1, 0, "MASTER")
        # setattr(params, "TEMPERATURE_MONDAY_4", 11)

        hg.putParamset(args.device, 0, "MASTER", args.profile)
# }}}
if args.get: # {{{
    profile_name = read_entry_from_db(args.db_file, args.device, args.day)
    print (profile_name)

    profile = profile_generator(profile_name, args.day)

    if args.verbose:
        print (json.dumps(profile, sort_keys=False, indent=4, separators=(',', ': ')))

# }}}
