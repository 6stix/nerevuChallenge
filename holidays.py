"""
AN9cn1faxv
ijUEs7STn8plCOBq7HENHaNSumw

secret: KjpP6annnePfpKA93Twd

https://api.xmltime.com/holidays?country=us
&year=2011&version=2&out=json&prettyprint=1
&accesskey={KEY}&expires={TIMESTAMP}&signature={SIGNATURE}

2019-07-20T02:23:07+00:00
"""

import requests
import html.parser
import bs4

import csv
import datetime

def main():
    """
    This main function can be used to create the CSV.
    """
    # write_holidays_csv("holidays.csv")
    holidays_arr = holidays_to_arr("holidays2019-sheets.csv")
    next_ten_holidays = upcoming_holidays(10, holidays_arr)

def holidays(number_of_holidays, holiday_type=None):
    holidays_arr = holidays_to_arr("holidays2019-sheets.csv", holiday_type)
    next_holidays = upcoming_holidays(number_of_holidays, holidays_arr)

    return next_holidays

def upcoming_holidays(number_of_holidays, holidays_arr):
    """
    This function returns the next "number_of_holidays" worth of holidays.
    """
    month_mappings = {1:'January', 2:'February', 3:'March',
        4:'April', 5:'May', 6:'June', 7:'July',
        8:'August', 9:'September', 10:'October',
        11:'November', 12:'December'}

    reverse_month_mappings = reverse_mappings(month_mappings)

    curr_date = datetime.datetime.now()
    curr_month = month_mappings[curr_date.month]
    curr_day = curr_date.day

    starting_index = find_date(holidays_arr, curr_month, curr_day, reverse_month_mappings)
    upcoming = holidays_arr[starting_index : starting_index + number_of_holidays]

    return upcoming

def find_date(arr, month, day, month_map):
    """
    Finds location of either the first holiday listed for today or the next holiday
    coming up. Returns the index of this holiday.
    """
    month_found = False
    month_index = 0

    i = 0
    arr_len = len(arr)
    while i < arr_len and month_found == False:
        row = arr[i]
        date = row['date']

        if month in date:
            month_found = True
            month_index = i

        i += 1

    if month_found == False:
        exit("Something must be wrong with the holidays calendar.")

    starting_index = month_index
    day_found = False
    day_index = 0

    i = starting_index
    month = month_map[month]
    while i < arr_len and day_found == False:
        row = arr[i]
        date = row['date'].split()
        date_day = date[2]
        date_month = month_map[date[1]]

        if date_month == month and int(date_day) >= day:
            day_found = True
            day_index = i

        elif date_month > month:
            day_found = True
            day_index = i

        i += 1

    if day_found == False:
        exit("Something might be wrong with the holidays calendar.")

    return day_index

def reverse_mappings(mappings):
    """
    Function to reverse the key-value pairs of a dictionary.
    Used to reverse months and numbers in this program.
    """
    new_map = {}
    for key in mappings:
        value = mappings[key]
        new_map[value] = key

    return new_map

def holidays_to_arr(fname, holiday_type=None):
    """
    Converts CSV file to an array of dictionaries.
    """
    csv_arr = []
    with open(fname, 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        for row in csv_reader:
            if all_values_empty(row) == False:
                csv_arr.append(row)

    fields = csv_arr.pop(0)
    fields[1] = 'Extra Date'

    # "date": "Sunday, July 14, 2019",
    month_mappings = {'Jan':'January', 'Feb':'February', 'Mar':'March',
        'Apr':'April', 'May':'May', 'Jun':'June', 'Jul':'July',
        'Aug':'August', 'Sep':'September', 'Oct':'October',
        'Nov':'November', 'Dec':'December'}

    holidays_arr = []
    for row in csv_arr:
        curr_dict = {'name':row[2], 'type':row[3], 'details':row[4]}

        month_day = row[0].strip().split()
        month = month_mappings[month_day[0]]
        day = month_day[1]
        date = row[1] + ", " + month + " " + day

        curr_dict['date'] = date
        holidays_arr.append(curr_dict)

    if holiday_type != None:
        holidays_arr = [x for x in holidays_arr if x['type'] == holiday_type]

    return holidays_arr

def all_values_empty(array):
    """
    Checks if all values in an array are blank.
    """
    all_blank = True
    for item in array:
        if item != "" and item != None:
            all_blank = False

    return all_blank

def write_holidays_csv(fname):
    """
    Web-scrape timeanddate.com for holiday data.
    """
    response = requests.get("https://www.timeanddate.com/holidays/us/")
    content = response.text

    soup = bs4.BeautifulSoup(content, features="html.parser")

    table_tag = soup.table
    fields_soup = table_tag.contents[0]
    fields_soup = fields_soup.contents[0].contents
    fields = []
    for field in fields_soup:
        temp_field = field.contents[0]
        temp_field = temp_field.replace(u'\xa0', u' ')
        if temp_field != None and temp_field != " ":
            fields.append(temp_field)
        else:
            fields.append("Extra " + fields[-1])

    # Fields: date, extra date, name, type, details

    holidays_table = table_tag.contents[1]
    # print(holidays_table.contents[21]) # -> entry of hol_feb

    holidays_table = holidays_table.contents

    for entry in holidays_table:
        pass

    # print(len(holidays_table))
    stripped = []
    for a in holidays_table:
        if "hol_" not in str(a):
            stripped.append(a)

    num_fields = len(fields)

    holidays_array = []
    for block in stripped:
        holiday_string = ""
        curr_block = block.th

        for i in range(num_fields):
            to_iterate = curr_block.contents
            iter_str = to_iterate
            #iter_str = " ".join(to_iterate)

            print("To iter:", iter_str)

            holiday_string += str(curr_block.contents[0]) + ","
            curr_block = curr_block.next_sibling

        holidays_array.append(holiday_string)

    print("Holiday Info:\n",holidays_array[-1])

if __name__ == '__main__':
    main()
