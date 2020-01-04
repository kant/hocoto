#!/usr/bin/env python3
'''homematic day profile'''
# pylint
# vim: tw=100 foldmethod=indent
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy
# pylint: disable=multiple-statements
import logging
from hocoto.parse_options_manager import args
from hocoto.homematic_day_profile import HomematicDayProfile
from hocoto.weekdays import weekdays, days, daynames

logger = logging.getLogger(__name__)

class HomematicProfile():
    '''Class to capture homematic profiles'''
    def __init__(self, profile=None, days=None):
        '''init'''
        self.hm_day_profiles = {}
        if profile is not None:
            self.set_profile(profile, days)
    def set_profile(self, profile, days=None):
        '''add profile to class instance'''
        if days is not None:
            days = ensure_is_list (days)
        else:
            days = weekdays

        for day in days:
            self.hm_day_profiles[day] = HomematicDayProfile()
            # self.profile_dict[day]={}
            # self.profile_dict[day]['temp']=[]
            # self.profile_dict[day]['time']=[]
            day_name = daynames[day]
            for num in range (1, 14):
                # profile_dict[day][temp][num] = profile["TEMPERATURE_%s_%d"%(day_name, num)]
                # profile_dict[day][time][num] = profile["ENDTIME_%s_%d"%(day_name, num)]
                self.hm_day_profiles[day].add_step(profile["TEMPERATURE_%s_%d"%(day_name, num)],
                                                   profile["ENDTIME_%s_%d"%(day_name, num)])
    def get_profile(self, days=None):
        '''Get homematic profile for given weekday(s)'''
        output_dict = {}
        if days is not None:
            days = ensure_is_list (days)
        else:
            days = weekdays
        for day in days:
            if not self.profile_dict[day]:
                continue
            day_name = daynames[day]
            for num in range (1, 14):
                # output_dict["TEMPERATURE_%s_%d"%(day_name, num)] = self.profile_dict[day]['temp'][num]
                # output_dict["ENDTIME_%s_%d"%(day_name, num)]     = self.profile_dict[day]['time'][num]
                (time, temp) = self.hm_day_profiles[day].get_step(num)
                output_dict["ENDTIME_%s_%d"%(day_name, num)]     = time
                output_dict["TEMPERATURE_%s_%d"%(day_name, num)] = temp
    def __repr_table__(self, days=None):
        '''Table view of the profile'''
        rv = ''
        if days is not None:
            days = ensure_is_list (days)
        else:
            days = weekdays
        for day in days:
            rv += F"{daynames[day]}\n"
            rv += self.hm_day_profiles[day].__repr_table__()
        return rv
    def __repr_table_dedup__(self):
        '''Table view of the profile'''
        rv = ''
        days = weekdays
        for day_num in range (0,7):
        # for day in days:
            # rv += F"{daynames[day]}\n"
            # rv += self.hm_day_profiles[day].__repr_table__()
            day = weekdays[day_num]
            dupe_found = False
            dupe_name = ""
            cur_day_profile = self.hm_day_profiles[day].__repr_table__()
            for prev_day_num in range (0,day_num):
                prev_day = weekdays[prev_day_num]
                prev_day_profile = self.hm_day_profiles[prev_day].__repr_table__()
                if cur_day_profile == prev_day_profile:
                    dupe_found = True
                    dupe_name  = prev_day
                    break
            print (F"{daynames[day]}")
            if not dupe_found:
                print (self.hm_day_profiles[day].__repr_table__())
            else:
                print (F"Same as {daynames[dupe_name]}\n")
            

        return rv
    def __repr_tables_multi__(self):
        rv = ''
        plots = {}
        lines = {}
        # convert plots to lines
        for day in weekdays:
            plots[day] = hm_profile.__repr_table__(days=day)
            lines[day] = plots[day].split('\n')

        maxlines = 0
        for day in weekdays:
            if len(lines[day]) > maxlines:
                maxlines = len(lines[day]) 

        for i in range (0, maxlines-1):
            for day in weekdays:
                try:
                    entry = lines[day][i].rstrip('\n')
                    rv += F"{entry:<15}| "
                except IndexError:
                    rv += "{:<15}| ".format(" ")

            rv += "\n"
        return rv
    def __repr_plot__(self, width=40, days=None):
        '''Table view of the profile'''
        rv = ''
        if days is not None:
            days = ensure_is_list (days)
        else:
            days = weekdays
        for day in days:
            rv += F"{daynames[day]}\n"
            rv += self.hm_day_profiles[day].__repr_plot__(width = width)
        return rv
    def __repr_plots_multi__(self, width, plots_per_row=3):
        '''mutliple plots in a row'''
        plots = {}
        lines = {}
        do_summary = False
        if plots_per_row == 3:
            do_summary = True
        plots_per_row  -= 1
        blocks_to_plot = int (7 / plots_per_row - 0.1)+1
        rv = ''

        # convert plots to lines
        for day in weekdays:
            plots[day] = hm_profile.__repr_plot__(width=args.width, days=day)
            lines[day] = plots[day].split('\n')

        for blocks in range (0, blocks_to_plot*plots_per_row, plots_per_row+1):
            for i in range (blocks, blocks + plots_per_row + 1):
                try:
                    rv += (("   {:<%d}" % width).format(daynames[weekdays[i]]) )
                except IndexError:
                    pass
            rv += ('\n')
            for line in range (1, len(lines[weekdays[-1]])):
                for i in range (blocks, blocks + plots_per_row + 1):
                    if i < len(lines):
                        rv += (F"{lines[weekdays[i]][line]}  ")
                rv += ("\n")
        return rv
    def __repr_dump__(self, day_in=None, day_out=None):
        if day_in is not None:
            return (self.hm_day_profiles[day_in].__repr_dump__(day_out))
        rv={}
        for day in weekdays:
            temp = self.hm_day_profiles[day].__repr_dump__(day)
            for entry in temp:
                rv[entry] = temp[entry]
                # print (F"  entry: {entry}")
        return rv


