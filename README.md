# CS495_Challenge_5
A simple challenge problem to split a CSV file into two while mapping competition teams to institutions by a created ID.
This was made for the Carroll College CS495 Seminar Class.

In order to run this script, I recommend a bash console. Linux and MacOS have these included; however, on windows, one will either need to download the improved terminal or download GitBash (my personal recommendation and what is guaranteed to work for this program). You will also need a python runtime.

To run the program:
1. Open gitbash and navigate to a file location of your choosing.
2. Run the command "git clone https://github.com/jgrosse01/CS495_Challenge_5_AND_6" without the quotation marks.
3. Enter the folder that was just created.
4. Place any csv files of the proper format that you would like to be split into the data folder (the year 2015 already exists).
5. Use your system's python keyword (mine is simply "python") and pass it the name of the script and the name of the file you placed in the data folder. An example command would be "python MCM_CSV_Split.py 2015.csv" without the quotation marks.
6. Allow the program to run and will note completion and exiting of the program.
7. Your split CSV files can be found in the newly generated build folder.


** This is not intended to split all CSV files, this is particularly for the result csv files from the International Math Modeling Competition into a teams csv and an institutions csv.


# Challenge 6
A simple challenge problem to do some basic analyais of a csv in addition to the function of challenge 5.
This was made for the Carroll College CS495 Seminar Class.

In order to run this script, I recommend a bash console. Linux and MacOS have these included; however, on windows, one will either need to download the improved terminal or download GitBash (my personal recommendation and what is guaranteed to work for this program). You will also need a python runtime.

To run the updated program:
1. Open gitbash and navigate to a file location of your choosing.
2. Run the command "git clone -b Challenge6 --single-branch https://github.com/jgrosse01/CS495_Challenge_5_AND_6" without the quotation marks.
3. Enter the folder that was just created.
4. Place any csv files of the proper format that you would like to be processed into the data folder (the year 2015 already exists).
5. Use your system's python keyword (mine is simply "python") and pass it the name of the script and the name of the file you placed in the data folder. An example command would be "python MCM_CSV_Split.py 2015.csv" without the quotation marks.
6. Allow the program to run and will note completion and exiting of the program.
7. Your processed data can be found in the build folder. The zipped file (a single file) will contain the analysis of the CSV in appropriately named subfiles. The split CSV will also be present in the base level of the build directory.
