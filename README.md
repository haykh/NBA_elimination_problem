# NBA elimination problem
### _For the application to the 2017 NBA hackaton_


The program can be used as a black box. To get the results of our algorithm described in the `.pdf` file, one needs to run the `main.py` by doing
```
$ python main.py
```
in the terminal. The output is a team title + either "Playoffs" if a team qualifies or the elimination date (or two dates).

#### Description
* `*.csv` files contain the whole data of the season games.
* `main.py` is the main program that contains the numerical algorithm looped over all the teams of Eastern and Western conference.
* `init.py` contains auxiliary functions that read data from `*.csv` and provide necessary values.
* `write_inits.py` pre-evaluate games left between two teams and the results of head-to-head games up to a particular date and save those values to `gamesleft/` and `h2h/` directories. This increases the speed of our algorithm. This should be called once, unless you already have those directories full.
* `helper.py` simply contains a progress bar for `write_inits.py`.