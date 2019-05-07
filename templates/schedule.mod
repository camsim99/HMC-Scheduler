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
set Major_Req within Classes;  
set HSA_Req within Classes;
set Core_Req within Classes;

# The following subsets of classes define what courses are to be
# pinned or unpinned for a given semester
set Pin_Take{Semesters} within Classes;
set Pin_No_Take{Semesters} within Classes;

# PARAMETERS
# ==========
# Note that we use the convention of [class, semester] for doubly indexed
# variables

param offered_fall{Classes} binary;  
param offered_spring{Classes} binary;  
param workload{Classes};
param credit{Classes};

# minimum credits allowed in a semester
param min_credits integer >= 0;  # USER DEFINED
# maximum credits allowed in a semester (may cause infeasibility)
param max_credits integer > 0;  # USER DEFINED

param already_taken{Classes} binary;  # USER DEFINED

param next_semester_fall binary;  # USER DEFINED

param min_grad_credits integer > 0;  # minimum credits to graduate

param pin_take{Classes, Semesters};
param pin_no_take{Classes, Semesters};

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

# this is effectively a min max problem (but we have to linearize it for AMPL):
var Z;
minimize Max_Cost: Z + sum{s in Semesters} (1000*underload[s] + 1000*overload[s]);
subject to Z_def {s in Semesters}:
Z >= sum{c in Classes} workload[c] * take[c,s];


# CONSTRAINTS
# ===========

subject to no_repeats{c in Classes}:
sum{s in Semesters} take[c, s] <= 1;

subject to graduation_credits:
sum{c in Classes, s in Semesters} take[c, s] * credit[c] >= min_grad_credits;

subject to taken_courses{c in Classes}:
take[c, 0] = already_taken[c];

# Class dependancy tracking.  This constraint applies to all `prereq's of all
# classes `c'.  Note that `s' is for all members of the `Semesters' set, except
# for the 0th semester (and take advantage of arithmetic expressions).
subject to prerequisite_courses{c in Classes, s in 1 .. semesters_left,
                                prereq in Prereqs[c]}:
sum{temp_s in 0 .. (s - 1)} take[prereq, temp_s] >= take[c,s];

# course graduation requirements:
subject to major_req{c in Major_Req}:
sum{s in Semesters} take[c,s] = 1;

subject to hsa_req{c in HSA_Req}:
sum{s in Semesters} take[c,s] = 1;

subject to core_req{c in Core_Req}:
sum{s in Semesters} take[c,s] = 1;

# underload and overload constraints (see min_credits and max_credits).
subject to underloading{s in 1 .. semesters_left}:
sum{c in Classes} credit[c] * take[c,s] + underload[s] >= min_credits;

subject to overloadingloading{s in 1 .. semesters_left}:
sum{c in Classes} credit[c] * take[c,s] + overload[s] <= max_credits;

subject to pinned_classes_take{s in Semesters, c in Pin_Take[s]}:
take[c,s] = 1;

subject to pinned_classes_no_take{s in Semesters, c in Pin_No_Take[s]}:
take[c,s] = 0;

subject to fall{c in Classes, s in Semesters : s mod 2 = next_semester_fall and s != 0}:
take[c,s] <= offered_fall[c];

subject to spring{c in Classes, s in Semesters : s mod 2 != next_semester_fall and s!= 0}:
take[c,s] <= offered_spring[c];
