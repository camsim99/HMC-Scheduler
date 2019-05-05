#!/bin/env python3
import csv
import os
import sys
from jinja2 import Environment, FileSystemLoader, select_autoescape

WORKING_DIR = sys.path[0]  # get path to this script

# jinja environment
env = Environment(
    loader=FileSystemLoader(os.path.join(WORKING_DIR, 'templates'))
)


class Course:
    def __init__(self, row):
        """create a course object from a row from a course list csv which is a
        list of strings with the following ordering:

        course code, offered in fall? (0 or 1), in spring?, credits,
        workload, prereqs ...
        """

        self.code      = row[0]
        self.in_fall   = bool(row[1])
        self.in_spring = bool(row[2])
        self.credits   = int(row[3])
        self.workload  = int(row[4])
        self.prereqs   = row[5:]

    def __repr__(self):
        return "<{}: {} - {}>".format(self.code, self.workload, self.prereqs)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.code == other
        else:
            return self.code == other.code
    
    def __hash__(self):
        return hash(self.code)

def read_course_list(path):
    courses = set()
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(row)
            courses.add(Course(row))
    return courses
    
def main():
    # read csv's necessary to generate the dat files
    courses = read_course_list(os.path.join(WORKING_DIR, 'dat',
                                            'course-list.csv'))
    
    # test
    for course in courses:
        print(course)
    print("CS-70" in courses)
    print( courses.get("CS-70").prereqs )

    # template = env.get_template('schedule-hmc.dat')
    # print ( template.render(courses=courses) )
    

if __name__ == "__main__":
    main()
