#!/bin/env python3
import csv
import os
import sys
from jinja2 import Environment, FileSystemLoader, select_autoescape

WORKING_DIR = sys.path[0]  # get path to this script
# all other directories are relative to WORKING_DIR
BUILD_DIR  = os.path.join(WORKING_DIR, 'build')
CONFIG_DIR = os.path.join(WORKING_DIR, 'config') 

# jinja environment
env = Environment(
    loader=FileSystemLoader(os.path.join(WORKING_DIR, 'templates'))
)


class Course:
    """The course object holds all information to a course.  It is
    considered equivalent to a string with the same course code"""

    # list of tuples, (int i, bool b) indicating whether for semester
    # i, the course is pinned to be taken or not taken (given by b)
    pinned_semesters = []

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
            # ignore empty column values
            course = Course(list(filter(lambda x: x, row)))

            # make sure we don't have duplicate entries!
            assert course not in courses

            courses.add(course)
            print("added " + str(course))
    return courses

def read_requirements(req_type):
    # with open(os.path.join())
    pass

def save_template(name, dry_run, **kwargs):
    """generate all necessary dat and mod files.  Prints to standard out
    instead of saving if dry_run is true"""
    
    template = env.get_template(name)
    rendered = template.render(**kwargs)
    if dry_run:
        print('-' * (len(name) + 1))
        print(name + ':')
        print('-' * (len(name) + 1))
        print(rendered)
    else:
        # save the template in the build dir
        print("saving " + name)
        with open(os.path.join(BUILD_DIR, name), 'w') as f:
            f.write(rendered)
            f.close()
    
def main():
    # read csv's necessary to generate the dat files
    courses = read_course_list(os.path.join(CONFIG_DIR,
                                            'course-list.csv'))

    # make build dir, if it doesn't exist
    try:
        os.mkdir(os.path.join(BUILD_DIR))
    except FileExistsError:
        pass  # build dir already exists

    print("\ngenerating templates")
    dry_run = True
    save_template('schedule-hmc.dat', dry_run, courses=courses)

    

if __name__ == "__main__":
    main()
