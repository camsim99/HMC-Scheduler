#!/bin/env python3
import csv
import os
import sys
from jinja2 import Environment, FileSystemLoader, select_autoescape

WORKING_DIR = sys.path[0]  # get path to this script
# all other directories are relative to WORKING_DIR
BUILD_DIR  = os.path.join(WORKING_DIR, 'build')
CONFIG_DIR = os.path.join(WORKING_DIR, 'config') 

all_courses = None

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
        self.in_fall   = bool(int(row[1]))
        self.in_spring = bool(int(row[2]))
        self.credits   = float(row[3])
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
        next(reader)
        for row in reader:
            # ignore empty column values
            course = Course(list(filter(lambda x: x, row)))

            # make sure we don't have duplicate entries!
            assert course not in courses

            courses.add(course)
            print("added " + str(course))
    return courses

def read_taken_courses(path):
    taken = set()
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) # ignore header row
        for row in reader:
            taken_course = row[0]
            if taken_course:  # ignore empty strings
                assert taken_course in all_courses
                taken.add(taken_course)
    return taken

def read_misc_user_config(path):
    """returns semesters_left, minimum_credits, maximum_credits"""
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # ignore the first header line
        settings = next(reader)
        return int(settings[1]), int(settings[2]), int(settings[3]), bool(int(settings[4]))

def read_pinned_courses(path, semesters_left):
    """returns the dict mapping semester number [0...semesters_left] (as
    an int) to a set of tuples of the form (str code, bool take?)
    """
    pinned = {}
    for i in range(0, semesters_left + 1):
        pinned[i] = set()
    start = 5  # where do pinned courses start in user-config.csv?
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) # ignore header row
        for row in reader:
            course = row[start + 0]
            if course:  # ignore empty strings
                # now read pinned settings for this course
                semester = int(  row[start + 1] )
                take     = bool( int(row[start + 2]) )

                assert course in all_courses
                # it doesn't make sense to pin courses in past semesters
                assert semester != 0
                pinned[semester].add( (course, take) )
    return pinned

def read_requirements(path):
    major_reqs = set()
    hsa_reqs = set()
    core_reqs = set()

    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) # ignore header row
        for row in reader:
            major = row[0]
            hsa = row[1]
            core = row[2]

            if major:
                major_reqs.add(row[0])
            if hsa:
                hsa_reqs.add(row[1])
            if core:
                core_reqs.add(row[2])

    return major_reqs, hsa_reqs, core_reqs

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
    global all_courses
    all_courses = read_course_list(os.path.join(CONFIG_DIR,
                                                'course-list.csv'))
    user_config_path = os.path.join(CONFIG_DIR, 'user-config.csv')
    taken_courses = read_taken_courses(user_config_path)
    semesters_left, minimum_credits, maximum_credits, next_semester_fall = read_misc_user_config(user_config_path)

    pinned = read_pinned_courses(user_config_path, semesters_left)
    print(pinned)

    major_reqs, hsa_reqs, core_reqs = read_requirements(os.path.join(CONFIG_DIR, 'requirements.csv'))


    # make build dir, if it doesn't exist
    try:
        os.mkdir(os.path.join(BUILD_DIR))
    except FileExistsError:
        pass  # build dir already exists

    print("\ngenerating templates")
    dry_run = False
    save_template('schedule-hmc.dat', dry_run, courses=all_courses,
                  major_reqs=major_reqs,
                  hsa_reqs=hsa_reqs,
                  core_reqs=core_reqs
    )
    save_template('schedule-user.dat', dry_run,
                  courses=all_courses,
                  taken=taken_courses,
                  semesters_left=semesters_left,
                  minimum_credits=minimum_credits,
                  maximum_credits=maximum_credits,
                  pinned=pinned,
                  next_semester_fall=int(next_semester_fall)
                  )
    save_template('schedule.mod', dry_run, pinned=pinned)

    

if __name__ == "__main__":
    main()
