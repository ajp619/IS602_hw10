# coding=utf-8
"""
Homework 7

What we will be doing here is very similar to the last homework, but now we'll look a bit at scipy.
Do parts 1 and 2.  Part 3 is optional
1. Take what you did on homework 5 as a starting point.  Replace the regression calculation using least squares with a
   curve fitting approach (examples in the reading).  To start, just fit a linear equation.  Output the equation to the
   console.  You don't need to graph anything (we'll look at that in a couple more weeks).
2. Again, using timeit, compare the performance of your solution in homework 5 to the scipy function.  Output the
   results to the console.
3. (Optional)  There are other models that can be fitted to the data we have.  Try to fit other equations, like
   Gaussian, to the data.  Output the equation to the console.

Homework 5

1. Download the new data set on the Lesson 5 page called brainandbody.csv.  This file is a small set of average
   brain weights and average body weights for a number of mammals.  We want to see if a relationship exists between
   the two. (This data set acquired from here).
2. Perform a linear regression using the least squares method on the relationship of brain weight [br] to
   body weight [bo].  Do this using just the built in Python functions (this is really easy using scipy, but we're
   not there yet).  We are looking for a model in the form bo = X * br + Y.  Find values for X and Y and print out the
   entire model to the console.
"""


__author__ = 'Aaron'

# import required modules
from Tkinter import *
import csv
import timeit
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as pyplot

def get_file_name():
    root = Tk()
    root.withdraw()  # This will hide the main window
    import tkFileDialog as tkf
    return tkf.Open().show()


def load_csv(file_name):
    """
    load a csv file

    expects csv file of the form:
        x1, y1, z1, ...
        x2, y2, z2, ...
        ...
    creates return_list of [[X], [Y], [Z], ...]
    returns lines that do not have the same number of arguments as the fist line in a list bad_lines
    """
    return_list = []
    bad_lines = []
    try:
        with open(file_name, 'rb') as csvfile:
            raw_data = csv.reader(csvfile, delimiter=',', quotechar='|')
            num_col_expected = 0
            bad_row_flag = False
            row_num = 0
            for row in raw_data:
                col_num = 0
                for element in row:
                    if row_num == 0:
                        return_list.append(([element]))
                        num_col_expected += 1  # Count the number of columns in the first row
                    else:
                        # All other rows: append if #columns(current_row) = #columns(first row)
                        if len(row) == num_col_expected:
                            return_list[col_num].append(element)
                        else:
                            bad_row_flag = True
                    col_num += 1
                if bad_row_flag: bad_lines.append(row)
                bad_row_flag = False
                row_num += 1
            return return_list, bad_lines
    except IOError:
        print "There was an error reading the file"
        exit()


def load_file_with_numpy(filename):
    return np.loadtxt(filename, skiprows=1, delimiter=',')


def linear_model(x, y, header=True):
    if header:
        x = [float(e) for e in x[1:]]
        y = [float(e) for e in y[1:]]
    else:
        x = [float(e) for e in x]
        y = [float(e) for e in y]

    n = len(x)

    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum([x[i] * y[i] for i in range(0, n)])
    sum_x2 = sum([x[i]**2 for i in range(0, n)])

    slope = (n * sum_xy - sum_x * sum_y)/(n * sum_x2 - sum_x**2)
    intercept = (sum_y * sum_x2 - sum_x * sum_xy)/(n * sum_x2 - sum_x**2)

    return slope, intercept


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
    return min(t.repeat(r, number=num)), num


def linear_func(x, m, b):
    return m * x + b


def gauss_func(x, a, b, c):
    return a*np.exp(-(x-b)**2/(2*c**2))


def print_separator():
    print "______________________________________________________________________________________"


def main():
    # get the path to the data file:
    file_name = get_file_name()

    brain_and_body, bad_data = load_csv(file_name)

    slope, intercept = linear_model(brain_and_body[1], brain_and_body[2])

    #  Original Method
    print_separator()
    print "Original Method"
    print_separator()
    print
    print "According to the provided data set, body weight [bo] is " \
          "related to brain weight [br] by the following equation:"
    print "bo = X * br + Y"
    print "where X = {0: 0.2f} and Y = {1: 0.2f}".format(slope, intercept)
    print
    calc_time, num = timer(load_csv, file_name)
    print "The time to load the data {0} times using csv.reader is {1}".format(num, calc_time)
    calc_time, num = timer(linear_model, brain_and_body[1], brain_and_body[2])
    print "The time to calculate these values {0} times is {1}".format(num, calc_time)
    print
    # Numpy curve_fit, linear model
    print_separator()
    print "Numpy curve_fit, linear model"
    print_separator()
    brain_and_body = load_file_with_numpy(file_name)
    popt, pcov = curve_fit(linear_func, brain_and_body[:, 1], brain_and_body[:, 2])
    print
    print "Using Numpy curve_fit, body weight [bo] is " \
          "related to brain weight [br] by the following equation:"
    print "bo = X * br + Y"
    print "where X = {0: 0.2f} and Y = {1: 0.2f}".format(popt[0], popt[1])
    print
    calc_time, num = timer(load_file_with_numpy, file_name)
    print "The time to load the data {0} times using numpy loadtext is {1}".format(num, calc_time)
    calc_time, num = timer(curve_fit, linear_func, brain_and_body[:, 1], brain_and_body[:, 2])
    print "The time required to calculate these values {0} times using numpy is {1}".format(num, calc_time)
    # Numpy curve_fit, gaussian model
    print_separator()
    print "Numpy curve_fit, gaussian model"
    print_separator()
    brain_and_body = load_file_with_numpy(file_name)
    popt, pcov = curve_fit(gauss_func, brain_and_body[:, 1], brain_and_body[:, 2])
    print
    print "Using Numpy curve_fit, body weight [bo] is " \
          "related to brain weight [br] by the following equation:"
    print "a*np.exp(-(x-b)**2/(2*c**2))"
    print "where a = {0: 0.2f}, b = {1: 0.2f}, and c = {2: 0.2f}".format(popt[0], popt[1], popt[2])
    print
    calc_time, num = timer(curve_fit, gauss_func, brain_and_body[:, 1], brain_and_body[:, 2])
    print "The time required to calculate these values {0} times using numpy is {1}".format(num, calc_time)
    print
    print_separator()
    # Comments
    print
    print "What units are these in? How is it something has a larger brain weight than body weight?"
    print "There's a 1 to 1 ratio with a 91 (lb?) offset? Those outliers are having too much effect."
    print "I think some cleaning is required. =-)"
    print


def dev():
    # This is a way to experiment with sections of code
    #
    # get the path to the data file:
    file_name = get_file_name()
    brain_and_body = load_file_with_numpy(file_name)
    popt, pcov = curve_fit(gauss_func, brain_and_body[:, 1], brain_and_body[:, 2])
    x = np.array(brain_and_body[:,1])
    index = np.argsort(x)
    x = x[index]
    y = gauss_func(x, *popt)

    pyplot.figure()
    pyplot.scatter(x, brain_and_body[:, 2], label='Data', marker='o')
    pyplot.plot(x, y, 'r-', ls='--', label="Fit")
    #pyplot.plot(trialX,   y, label = '10 Deg Poly')
    pyplot.legend()
    pyplot.show()
    pass


if __name__ == "__main__":
    main()
    #dev()
