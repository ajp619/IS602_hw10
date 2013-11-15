# coding=utf-8
"""
Homework 3

1.Loads in the values from cars.data.csv.  The data can be stored anyway you choose, in any data structure you choose.
  The data should load on start-up by referencing a file path, or even better, a file picker dialog box.


2.In the main portion of your program you should run the following operations and print the result to the console
  (except number 4).  How you achieve this is up to you.  However, operations need to be performed on the data itself
  (don't hard code the solution).

  1.Print to the console the top 10 rows of the data sorted by 'safety' in descending order
  2.Print to the console the bottom 15 rows for the data sorted by 'maint' in ascending order
  3.Print to the console all rows that are high or vhigh in fields 'buying', 'maint', and 'safety', sorted by 'doors'
    in ascending order.  Find these matches using regular expressions.
  4.Save to a file all rows (in any order) that are: 'buying': vhigh, 'maint': med, 'doors': 4, and 'persons': 4 or more.
    The file path can be a hard-coded location or use a dialog box.  Name it output.txt.


3.Your code needs to be able to handle exceptions.  It should handle all data as specified by the data definition
  document from Lesson 2, and throw some kind of error when it encounters data that doesn't match that format.
  To test this, I will add the line 'vlow, vlow, 1, 1, vbig, vhigh' to the .csv file.  Your program should gracefully
  handle this line in all cases from the previous part.


Going forward code style will count a little bit.  So make sure it is readable and I can understand it.  Also, there
are a few ways you can approach this assignment.  Ideally, you will create functions that can return the data in
different ways, not just do what I am asking for in part 2.  For example, consider if I asked for something in a
different order, how hard would it be to make that change in your code?

cars dataset:
Attribute Values:

   buying       v-high, high, med, low
   maint        v-high, high, med, low
   doors        2, 3, 4, 5-more
   persons      2, 4, more
   lug_boot     small, med, big
   safety       low, med, high

Missing Attribute Values: none

Class Distribution (number of instances per class)

   class      N          N[%]
   -----------------------------
   unacc     1210     (70.023 %)
   acc        384     (22.222 %)
   good        69     ( 3.993 %)
   v-good      65     ( 3.762 %)

Homework 6

1. Using your submission of homework 3 as a base, replace as many of the functions as you can with numpy functions.  
   For example, instead of using your sort function that you wrote, use numpy.sort.
2. Using the timeit function measure the execution times of all the sort and search functions you have.  You'll most
   likely need to do a large number of tests on each one to get a meaningful result.  Something like 10000.  
   Your submission will be a single file that has all the functions from homework 3 and the additional approach
   using numpy.  Additionally, you will have the timing of all the functions output to the console. Something like.

   ○ Sort using iteration:  x loops = y seconds
   ○ Sort using built in python: x' loops = y' seconds
   ○ Sort using numpy: x'' loops  = y''seconds
   You fill in all the values for x and y.
"""
__author__ = 'Aaron Palumbo'

#import required libraries:
from Tkinter import *
import csv
import re
import os
import numpy as np
import timeit


class CarEvaluationDataSet():
    """A simple class that represents a car evaluation dataset"""

    columnAttributes = {0: "buyingKeys", 1: "maintKeys", 2: "doorsKeys", 3: "personsKeys", 4: "lug_bootKeys",
                        5: "safetyKeys", 6: "ratingKeys"}

    # Sorting keys: lower value means less desirable so sorting in ascending
    # order will go from less desirable to more desirable.
    buyingKeys = {"vhigh": 1, "high": 2, "med": 3, "low": 4}
    maintKeys = {"vhigh": 1, "high": 2, "med": 3, "low": 4}
    doorsKeys = {"2": 1, "3": 2, "4": 3, "5more": 4}
    personsKeys = {"2": 1, "4": 2, "more": 3}
    lug_bootKeys = {"small": 1, "med": 2, "big": 3}
    safetyKeys = {"low": 1, "med": 2, "high": 3}
    ratingKeys = {"unacc": 1, "acc": 2, "good": 3, "vgood": 4}

    def __init__(self):
        self.data = []
        self.array = []

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return repr(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def add_row(self, buying, maint, doors, persons, lug_boot, safety, rating):
        self.data.append((buying, maint, doors, persons, lug_boot, safety, rating))

    def sort_by_column(self, sort_column, option="asc"):
        """Sort by column number

        :param sort_column:
            0: "buying", 1: "maint", 2: "doors", 3: "persons", 4: "lug_boot"
            5: "safety", 6: "rating"
        :param option:
            "asc": ascending (default)
            "des": descending
        """
        # Get the dictionary for column=sort_column
        key_function = getattr(self, self.columnAttributes[sort_column])
        if option == "asc":
            return sorted(self.data, key=lambda item: key_function[item[sort_column]])
        if option == "des":
            return sorted(self.data, key=lambda item: key_function[item[sort_column]], reverse=True)

    def init_np_array(self):
        self.array = np.array(self.data)

    def generate_column_key(self, column_num):
        """Translates column factors to ranked integers"""
        __key_list = []
        for row in self.data:
            __key_list.append(getattr(self, self.columnAttributes[column_num])[row[column_num]])
        return np.array(__key_list)

    def npsort_by_column(self, column_num=None, filter_values={}, option="asc"):
        """
        npsort_by_column uses Numpy functionality to sort and filter

        filter_values contains columns to filter in keys, and values to filter by as filter_values
        sorting multiple values of a column is an OR function
        sorting across multiple columns is an AND function
        """
        # There are several spots where existence of column_number is checked
        # If blank, the will only filter
        if column_num:
            index = self.generate_column_key(column_num)
        return_array = self.array[:]
        if filter_values:
            n = len(return_array)
            filter_key_and = [True] * n
            filter_key_or = [False] * n
            for k in filter_values.keys():
                for v in filter_values[k]:
                    filter_key_or += (self.generate_column_key(k) == v)
                filter_key_and = filter_key_and * filter_key_or
                filter_key_or = [False] * n
            return_array = return_array[filter_key_and]
            if column_num:
                index = index[filter_key_and]
        if column_num:
            index = np.argsort(index)
            if option == "asc":
                return return_array[index]
            if option == "des":
                return return_array[index[-1::-1]]
        else:
            return return_array


def get_file_name():
    root = Tk()
    root.withdraw()  # This will hide the main window
    import tkFileDialog as tkf
    return tkf.Open().show()


def validate_car_evaluation(raw_data):
    if (len(raw_data) == 7 and
            str(raw_data[0]) in CarEvaluationDataSet.buyingKeys and
            str(raw_data[1]) in CarEvaluationDataSet.maintKeys and
            str(raw_data[2]) in CarEvaluationDataSet.doorsKeys and
            str(raw_data[3]) in CarEvaluationDataSet.personsKeys and
            str(raw_data[4]) in CarEvaluationDataSet.lug_bootKeys and
            str(raw_data[5]) in CarEvaluationDataSet.safetyKeys and
            str(raw_data[6]) in CarEvaluationDataSet.ratingKeys):
        return True
    else:
        return False


def read_file(file_name, car_data_set, bad_data):
    try:
        with open(file_name, 'rb') as csvfile:
            car_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in car_reader:
                #Do some validation here: if meets criteria, append to good list,
                ## if does not meet criteria, append to bad list
                if validate_car_evaluation(row):
                    car_data_set.add_row(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                else:
                    bad_data.append(row)
        car_data_set.init_np_array()  # Added another data container for use with Numpy. Initialize here.
    except IOError:
        print "There was an error reading the file"
        exit()


def sort_n_filter(car_eval_list, col, option, pattern):
    """Created to allow use of timer function"""
    return_list = []
    sorted_list = car_eval_list.sort_by_column(col, option)
    for i in sorted_list:
        if re.search(pattern, "_".join([i[0], i[1], i[5]])):
            return_list.append([i[0], i[1], i[2], i[3], i[4], i[5], i[6]])
    return return_list


def filter_only(car_eval_list, pattern):
    """Created to allow use of timer function"""
    return_list = []
    for i in car_eval_list.data:
        if re.search(pattern, "_".join([i[0], i[1], i[2], i[3]])):
            return_list.append([i[0], i[1], i[2], i[3], i[4], i[5], i[6]])
    return return_list


def wrapper(func, *args, **kwargs):
    """This enables using a function with arguments with timeit"""
    def wrapped():
        return func(*args, **kwargs)
    return wrapped


def timer(func, *args, **kwargs):
    r = 3
    num = 1000
    wrapped = wrapper(func, *args, **kwargs)
    t = timeit.Timer(wrapped)
    return min(t.repeat(r, number=num))/num


def print_header():
    print "buying   | maint    | doors    | # people | luggage  | safety   | rating"
    print "------------------------------------------------------------------------"


def print_separator():
    print "______________________________________________________________________________________"


def print_row(i):
    print "{0: <9}| {1: <9}| {2: <9}| {3: <9}| {4: <9}| {5: <9}| {6}".\
        format(i[0], i[1], i[2], i[3], i[4], i[5], i[6])


def main():
    #Initialize Lists
    car_data = CarEvaluationDataSet()
    bad_data = []

    #Get file name
    file_name = get_file_name()

    #open and read file line by line. store variables. store any unreadable lines. report on num lines read and
    #also show lines not read.
    read_file(file_name, car_data, bad_data)

    print
    print "{0} lines were successfully read from {1}".format(len(car_data), file_name)
    print
    print "The following {0} lines contained invalid data:".format(len(bad_data))
    for i in bad_data:
        print i

    # Part 1 -----------------------------------------------------------------------------------------------------------
    print_separator()
    print_separator()
    print
    print "1.Print to the console the top 10 rows of the data sorted by 'safety' in descending order\n"
    sort1 = car_data.sort_by_column(5, "des")
    print_header()
    for i in sort1[0:10]:
        print_row(i)

    # Time sort1
    print "The time to run the original sorting function is:"
    print timer(car_data.sort_by_column, 5, "des")

    print_separator()
    print "Repeat using Numpy:"
    print
    sort1_numpy = car_data.npsort_by_column(column_num=5, option="des")
    print_header()
    for i in sort1_numpy[0:10]:
        print_row(i)

    # Time numpy approach
    print "The time to run the same sort using numpy is:"
    print timer(car_data.npsort_by_column, column_num=5, option="des")

    # Part 2 -----------------------------------------------------------------------------------------------------------
    print_separator()
    print_separator()
    print
    print "2.Print to the console the bottom 15 rows for the data sorted by 'maint' in ascending order\n"
    sort2 = car_data.sort_by_column(1, "asc")
    print_header()
    for i in sort2[-15:]:
        print_row(i)

    # Time sort2
    print "The time to run the original sorting function is:"
    print timer(car_data.sort_by_column, 1, "asc")

    print_separator()
    print "Repeat using Numpy:"
    print
    sort2_numpy = car_data.npsort_by_column(column_num=1, option="asc")
    print_header()
    for i in sort2_numpy[-15:]:
        print_row(i)

    # Time numpy approach
    print "The time to run the same sort using numpy is:"
    print timer(car_data.npsort_by_column, column_num=1, option="asc")

    # Part 3 -----------------------------------------------------------------------------------------------------------
    print_separator()
    print_separator()
    print
    print "3.Print to the console all rows that are high or vhigh in fields 'buying', 'maint', and 'safety', " \
          "\nsorted by 'doors' in ascending order.  Find these matches using regular expressions.\n"
    pattern = 'v?high_v?high_v?high'
    sort3 = sort_n_filter(car_data, col=2, option="asc", pattern=pattern)
    print_header()
    for i in sort3:
        print_row(i)

    # Time sort3
    print "The time to run the original sorting function is:"
    print timer(sort_n_filter, car_data, col=2, option="asc", pattern=pattern)

    print_separator()
    print "Repeat using Numpy:"
    print
    sort3_numpy = car_data.npsort_by_column(column_num=2, filter_values={0: [1, 2], 1: [1, 2], 5: [3]}, option="asc")
    print_header()
    for i in sort3_numpy:
        print_row(i)

    # Time numpy approach
    print "The time to run the same sort using numpy is:"
    print timer(car_data.npsort_by_column, column_num=2, filter_values={0: [1, 2], 1: [1, 2], 5: [3]}, option="asc")

    # Part 4 -----------------------------------------------------------------------------------------------------------
    print_separator()
    print_separator()
    print
    print "4.Save to a file all rows (in any order) that are: 'buying': vhigh, 'maint': med, 'doors': 4, and\n" \
          "'persons': 4 or more. The file path can be a hard-coded location or use a dialog box.  Name it output.txt.\n"
    logfile = open('output.txt', 'w')
    pattern = 'vhigh_med_4_(?:4|more)'
    sort4 = filter_only(car_data, pattern)
    for i in sort4:
        logfile.write(str(i))
        logfile.write("\n")
    logfile.close()
    print "output written to {0}".format(os.path.join(os.getcwd(), "output.txt"))

    # Time sort4
    print "The time to run the original sorting function is:"
    print timer(filter_only, car_data, pattern=pattern)

    print_separator()
    print "Repeat using Numpy:"
    print
    sort4_numpy = car_data.npsort_by_column(filter_values={0: [1], 1: [3], 2: [3], 3: [2, 3]})
    print_header()
    for i in sort4_numpy:
        print_row(i)

    # Time numpy approach
    print "The time to run the same sort using numpy is:"
    print timer(car_data.npsort_by_column, filter_values={0: [1], 1: [3], 2: [2], 3: [2, 3]})


if __name__ == "__main__":
    main()