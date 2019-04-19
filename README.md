# OR Final Project

## set-up
1. `git clone https://github.com/ianrabt/OR-Final-Project.git`
2. make sure `ampl` and `cplex` are in your path

## running AMPL
1. launch an AMPL shell by running `ampl`.  Then, in that shell run the
   following:
2. `option solver cplex;`
3. `model schedule.mod;`
4. `data schedule-hmc.dat;`
4. `data schedule-user.dat;`
5. `solve;`
