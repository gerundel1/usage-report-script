#!/usr/bin/env python3

import os
import sys
import argparse
import time

def read_login_rec(filelist):
    ''' docstring for this function
    get records from given filelist
    open and read each file from the filelist
    filter out the unwanted records
    add filtered record to list (login_recs)''' 
    login_recs = []
    for i in filelist:
        file = open(i, 'r')
        for line in file:
            line = line.strip()
            login_recs.append(line)
        file.close()
    login_recs = sorted(login_recs)
    return login_recs

def cal_daily_usage(subject,login_recs):
    ''' docstring for this function
    generate daily usage report for the given 
    subject (user or remote host)'''
    print ("Daily usage report for {}".format(subject))
    temp = "Daily usage report for " + subject
    temp1 = ""
    for i in range(len(temp)):
        temp1 += '='
    print (temp1)
    recs = []
    for i in range(len(login_recs)):
        rec = login_recs[i].split()
        if user == 1:
            if subject == rec[0]:
                recs.append(login_recs[i])
        else:
            if subject == rec[2]:
                recs.append(login_recs[i])
    daily_usage = {}
    total_usage = 0
    for i in range(len(recs)):
        rec = recs[i].split()
        norm_recs = normalized_rec(rec)
        for j in range(len(norm_recs)):
            norm_rec = norm_recs[j]
            login_time = ' '.join(norm_rec[4:8])
            logout_time = ' '.join(norm_rec[10:14])
            usage_in_sec = int(time.mktime(time.strptime(logout_time, "%b %d %H:%M:%S %Y")) - time.mktime(time.strptime(login_time, "%b %d %H:%M:%S %Y")))
            total_usage += usage_in_sec
            year_month_day = str(time.strptime(login_time, "%b %d %H:%M:%S %Y").tm_year) + ' ' + str(time.strptime(login_time, "%b %d %H:%M:%S %Y").tm_mon) + ' ' + str(time.strptime(login_time, "%b %d %H:%M:%S %Y").tm_mday)
            if year_month_day in daily_usage:
                daily_usage[year_month_day] += usage_in_sec
            else:
                daily_usage[year_month_day] = usage_in_sec
    daily_usage["Total"] = total_usage
    return daily_usage

def cal_weekly_usage(subject,login_recs):
    ''' docstring for this function
    generate weekly usage report for the given 
    subject (user or remote host)'''
    print ("Weekly usage report for {}".format(subject))
    temp = "Weekly usage report for " + subject
    temp1 = ""
    for i in range(len(temp)):
        temp1 += '='
    print (temp1)
    recs = []
    for i in range(len(login_recs)):
        rec = login_recs[i].split()
        if user == 1:
            if subject == rec[0]:
                recs.append(login_recs[i])
        else:
            if subject == rec[2]:
                recs.append(login_recs[i])
    weekly_usage = {}
    total_usage = 0
    for i in range(len(recs)):
        rec = recs[i].split()
        norm_recs = normalized_rec(rec)
        for j in range(len(norm_recs)):
            norm_rec = norm_recs[j]
            login_time = ' '.join(norm_rec[4:8])
            logout_time = ' '.join(norm_rec[10:14])
            usage_in_sec = int(time.mktime(time.strptime(logout_time, "%b %d %H:%M:%S %Y")) - time.mktime(time.strptime(login_time, "%b %d %H:%M:%S %Y")))
            week = int(time.strptime(login_time, "%b %d %H:%M:%S %Y").tm_yday)
            if week % 7 == 0:
                week = int(time.strptime(login_time, "%b %d %H:%M:%S %Y").tm_yday / 7 ) 
            else:
                week = int(time.strptime(login_time, "%b %d %H:%M:%S %Y").tm_yday / 7 ) + 1
            total_usage += usage_in_sec
            year_week = str(time.strptime(login_time, "%b %d %H:%M:%S %Y").tm_year) + ' ' + str(week)
            if year_week in weekly_usage:
                weekly_usage[year_week] += usage_in_sec
            else:
                weekly_usage[year_week] = usage_in_sec
    weekly_usage["Total"] = total_usage
    return weekly_usage

def list_by_subject(subject, login_recs):
    if subject == 'user':
        print ("User list for", end=' ')
        temp = ""
        for i in args.files:
            print(i, end =' ')
            temp = temp + i
        temp1 = ""
        for i in range(len(temp + "User list for ")):
            temp1 += '='
        print('\n' + temp1)
        temp = ''
        for i in range(len(login_recs)):
            rec = login_recs[i].split()
            if rec[0] == temp:
                continue
            else:
                print(rec[0])
            temp = rec[0]
    else:
        print ("Host list for", end=' ')
        temp = ""
        for i in args.files:
            print(i, end =' ')
            temp = temp + i
        temp1 = ""
        for i in range(len(temp + "Host list for ")):
            temp1 += '='
        print('\n' + temp1)
        temp = []
        for i in range(len(login_recs)):
            rec = login_recs[i].split()
            temp.append(rec[2])
        temp=sorted(temp)
        for i in range(len(temp)):
            if temp[i] == temp[i-1]:
                continue
            else:
                print(temp[i])

def normalized_rec(rec):
    norm_rec = []
    login_day = ' '.join(rec[4:6]+rec[7:8])
    logout_day = ' '.join(rec[10:12]+rec[13:14])
    day_format = '%b %d %Y'
    sec_t_in = time.mktime(time.strptime(login_day,day_format))
    sec_t_out = time.mktime(time.strptime(logout_day,day_format))

    n_day = int((sec_t_out - sec_t_in)/86400)
    if n_day == 0:
       norm_rec.append(rec.copy())
    else:
       rec1 = rec.copy()
       rec1[12] = '23:59:59'
       rec1[9] = rec1[3]
       rec1[10] = rec1[4]
       rec1[11] = rec1[5]
       norm_rec.append(rec1.copy())
       for x in range(n_day):
           new_rec = rec.copy()
           t_next = sec_t_in + (x+1)*86400
           next_day = time.strftime('%a %b %d %H:%M:%S %Y', time.strptime(time.ctime(t_next))).split()
           new_rec[3] = next_day[0]
           new_rec[4] = next_day[1]
           new_rec[5] = next_day[2]
           new_rec[6] = next_day[3]
           new_rec[7] = next_day[4]
           if (x+1) != n_day:
               new_rec[12] = '23:59:59'
               new_rec[9] = new_rec[3]
               new_rec[10] = new_rec[4]
               new_rec[11] = new_rec[5]
               new_rec[13] = new_rec[7]
           norm_rec.append(new_rec.copy())
    return norm_rec

parser = argparse.ArgumentParser(description="Usage Report based on the last command",epilog="Copyright 2020 - Taras Sosnovsky",)
parser.add_argument("-l", "--list", type=str, choices=['user','host'], help="generate user name or remote host IP from the given files")
parser.add_argument("-r", "--rhost", help="usage report for the given remote host IP")
parser.add_argument("-t","--type", type=str, choices=['daily','weekly'], help="type of report: daily or weekly")
parser.add_argument("-u", "--user", help="usage report for the given user name")
parser.add_argument("-v","--verbose", action="store_true",help="turn on output verbosity")
parser.add_argument("files",metavar='F', type=str, nargs='+',help="list of files to be processed")
args=parser.parse_args()
if args.verbose:
    print('Files to be processed:', args.files)
    print('Type of args for files',type(args.files))
    if args.list:
        print('processing usage report for the following:')
        print('reading login/logout record files ', args.files)
        if args.user:
            print('Generating list for user')
        if args.rhost:
            print('Generating list for host')
    if args.user:
        print('usage report for user: ',args.user)
        print('usage report type: ', args.type)
        print('processing usage report for the following:')
        print('reading login/logout record files ', args.files)
    if args.rhost:
        print('usage report for remote host:',args.rhost)
        print('usage report type: ', args.type)
        print('processing usage report for the following:')
        print('reading login/logout record files ', args.files)
if args.list:
    if args.list == 'user':
        list_by_subject('user', read_login_rec(args.files))
    if args.list == 'host':
        list_by_subject('host', read_login_rec(args.files))
if args.user:
    user = 1
    if args.type == 'daily':
        daily_usage = cal_daily_usage(args.user, read_login_rec(args.files))
        print("{}\t\t{}".format("Date", "Usage In Sec"))
        for k in sorted(daily_usage):
            if k != "Total":
                print("{}\t{}".format(k, daily_usage[k]))
        print("Total", '\t\t', daily_usage.get("Total"))
    if args.type == 'weekly':
        weekly_usage = cal_weekly_usage(args.user, read_login_rec(args.files))
        print("{}\t\t{}".format("Week #", "Usage In Sec"))
        for k in sorted(weekly_usage):
            if k != 'Total':
                print("{}\t\t{}".format(k, weekly_usage[k]))
        print("Total", '\t\t', weekly_usage.get("Total"))
if args.rhost:
    user = 0
    if args.type == 'daily':
        daily_usage = cal_daily_usage(args.rhost, read_login_rec(args.files))
        print("{}\t\t{}".format("Date", "Usage In Sec"))
        for k in sorted(daily_usage):
            if k != "Total":
                print("{}\t{}".format(k, daily_usage[k]))
        print("Total", '\t\t', daily_usage.get("Total"))
    if args.type == 'weekly':
        weekly_usage = cal_weekly_usage(args.rhost, read_login_rec(args.files))
        print("{}\t\t{}".format("Week #", "Usage In Sec"))
        for k in sorted(weekly_usage):
            if k != 'Total':
                print("{}\t\t{}".format(k, weekly_usage[k]))
        print("Total", '\t\t', weekly_usage.get("Total"))