# schedule.mod
# ============
# any parameter or set marked "USER DEFINED" is specific to every user of the
# scheduler (and thus is student-specific, not Mudd-specific, like the other
# parameters).

# SETS
# ====
# The Classes set keeps track of all available courses
set Classes;

# The Semesters set keeps track of when a course is taken.

# prerequisite parameter to define the Semesters set.
param semesters_left integer > 0;  # USER DEFINED

# The 0th semester refers to any course already taken (and is not subject to
# prereq constraints).  So if you are a sophomore, and have finished core, you'd
# put down *all* core classes as having been taken in semester 0.  See the .dat
# file for more information
set Semesters ordered = 0 .. semesters_left;

# Dependancy tracking.  For each class, keep track of what courses are
# prerequisite
set Prereqs{Classes} within Classes;

# The following subsets of Classes define what courses *must* be taken for
# graduation
set Major_Req within Classes;  # TODO index on Major set, to allow mult. majors
set HSA_Req within Classes;
set Core_Req within Classes;

# TODO allow for desired electives (instead of electives being general)

# PARAMETERS
# ==========
# Note that we use the convention of [class, semester] for doubly indexed
# variables

param offered{Classes, s in Semesters: s > 0};  # TODO this is currently unused
param workload{Classes};
param credit{Classes};

# TODO we need class dependancy tracking! (indexed by classes?)
#
# OPTION 1:
# define a set of prereqs indexed over courses, and then have a
# constraint which uses the sum of these courses (S[c in Classes]
# 
# -----
# 
# I like the set idea, because (a) it will be easier to type and (b) we
# can use AMPL's subset feature to ensure each prereq set will be a
# subset of the course set.  Note that this DOES NOT allow for any
# logical ORs in dependancy tracking.
# 
# TODO are there any instances of courses which have logical OR in their
# prereqs.
# 
# -----
#
# OPTION 2:
# We can also use a matrix of all ones, and then have zeros (would not
# be symetric).  [i,j] represents whether course i depends on course j
#
# to generalize AND, use CS70 <= prerequisite


# TODO we need HSA and major graduation requirements!

# minimum credits allowed in a semester
param min_credits;  # USER DEFINED
# maximum credits allowed in a semester (may cause infeasibility)
param max_credits;  # USER DEFINED

param min_grad_credits;  # minimum credits to graduate

# VARIABLES
# =========
# take class c in semester s?
var take{Classes, Semesters} binary;

# number of credits underloaded (bounded by max_credits)
var underload{Semesters} >= 0, integer;

# number of credits overloaded (bounded by min_credits)
var overload{Semesters} >= 0, integer;

# OBJECTIVE FUNCTION
# ==================

# TODO we still need to finalize this...going to leave this blank for the
# meantime

# this is effectively a min max problem (but we have to linearize it for AMPL):
var Z;
minimize Max_Cost: Z;
subject to Z_def {s in Semesters}:
Z >= sum{c in Classes}workload{c} * take[c,s] + underload[s] + overload[s];


# CONSTRAINTS
# ===========

subject to no_repeats{c in Classes}:
sum{s in Semesters} take[c, s] <= 1;

subject to graduation_credits:
sum{c in Classes, s in Semesters} take[c, s] * credit[c] >= min_grad_credits;

# TODO we need class dependancy tracking!

# TODO we need HSA and major graduation requirements!

# TODO need to constrain underload and overload variables