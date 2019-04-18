# SETS
# ====
set Classes;
set Semesters;

# PARAMETERS
# ==========
# Note that we use the convention of [class, semester] for doubly indexed
# variables

param offered{Classes, Semesters};
param workload{Classes};
param credit{Classes};

# TODO we need class dependancy tracking! (indexed by classes?)

param min_credits; # minimum credits allowed in a semester
param max_credits; # maximum credits allowed in a semester (may cause
                   # infeasibility)

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

# CONSTRAINTS
# ===========

subject to no_repeats{c in Classes}:
sum{s in Semesters} take[c, s] <= 1;

subject to graduation_credits:
sum{c in Classes, s in Semesters} take[c, s] * credit[c] >= min_grad_credits;

# TODO we need class dependancy tracking!