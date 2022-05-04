import math
import numpy as np
import os
import pandas as pd
import sys
import zipfile as zip


# method to execute the process of splitting the CSV
def main(filename: str):
    # read data
    data = pd.read_csv(os.path.abspath(f"./data/{filename}"))
    # clean data
    data = clean_csv(data)
    # get stats list from data to save
    avg, num_teams, outstanding, US_meritorious = stats(data)
    # split data
    inst, team = split_csv(data)

    # if the build directory does not exist then make it. then write files to that folder
    if not os.path.exists(os.path.abspath("./build")):
        os.mkdir(os.path.abspath("./build"))

    # write stats files
    # average teams per inst.
    f = open("Average Teams per Institution.txt", 'w')
    f.write(f"The Average Number of Teams per Institution is: {round(avg, 3)}")
    f.close()
    # institution by number of teams
    num_teams.to_csv("Institutions_By_Number_Of_Entered_Teams.csv", index=False)
    # all outstanding teams
    outstanding.to_csv("Institutions_With_Outstanding.csv", index=False)
    # all US teams meritorious or above
    US_meritorious.to_csv("US_Meritorious_Or_Above.csv", index=False)

    # zip stats files into one file (THIS IS "AN output file")!!!!!
    zippy = zip.ZipFile("build/MCM_Stats.zip", 'w')
    zippy.write("Average Teams per Institution.txt")
    zippy.write("Institutions_By_Number_Of_Entered_Teams.csv")
    zippy.write("Institutions_With_Outstanding.csv")
    zippy.write("US_Meritorious_Or_Above.csv")
    zippy.close()

    # delete old files that have been moved
    os.remove("Average Teams per Institution.txt")
    os.remove("Institutions_By_Number_Of_Entered_Teams.csv")
    os.remove("Institutions_With_Outstanding.csv")
    os.remove("US_Meritorious_Or_Above.csv")

    # write split files
    inst.to_csv("build/Institutions_Table.csv", index=False)
    team.to_csv("build/Teams_Table.csv", index=False)


# method to clean up the data given
def clean_csv(data: pd.DataFrame) -> pd.DataFrame:
    # get rid of the bom symbol on the institution header
    data['Institution'] = data['ï»¿Institution']
    data = data.drop(['ï»¿Institution'], axis=1)

    # add a lowercase column for each string column in the data and strip the lowercase column of whitespace
    for col in data:
        if data.dtypes[col] == object:
            data[f"l_{col}"] = data[col].str.lower().str.strip()

    # give a unique Institution ID to every unique pair of institution and city
    # this allows for multiple cities with the same named university or multiple university names in the same city
    data['Institution ID'] = data.groupby(['l_Institution', 'l_City']).ngroup()

    # do not drop duplicates here because it reduces each institution to one row which interferes with further use

    return data


# method to return the necessary list and dataframes to write to files (from a clean dataframe)
def stats(data: pd.DataFrame) -> (float, pd.DataFrame, pd.DataFrame, pd.DataFrame):
    # find the average number of teams submitted per institution
    avg_df = data[['Institution ID', 'Institution', 'Team Number']]
    # add a count column for the number of rows taken by each institution by ID
    avg_df = avg_df.groupby('Institution ID').size().reset_index(name='count_teams')
    # now we have the average value
    avg_teams = float(np.mean(avg_df['count_teams']))

    # now we find the ordered list of the institutions that entered the most teams,
    # including the number of teams that they entered (ordered by number of teams)
    rank_n_teams = data.groupby(['Institution', 'Institution ID'])\
        .size().reset_index(name='num_teams')\
        .sort_values('num_teams', ascending=False)
    rank_n_teams = rank_n_teams.drop_duplicates('Institution ID').drop('Institution ID', axis=1)
    # we now found the thing that Ted gave an obscenely long description

    # now we find the list of all institutions ranked 'outstanding' ordered by name
    outst = data[data['l_Ranking'] == "outstanding winner"].sort_values('Institution')
    outst = outst.drop_duplicates("Institution ID")
    outst = outst[['Institution', 'Ranking']]
    # and we found it!

    # now we find US teams with meritorious or higher rank
    # mask to see if ranking is in the valid range and country is united states
    mask = data['l_Ranking'].isin(['meritorious', 'finalist', 'outstanding winner']) & data['l_Country'].isin(["us", "usa"])
    # apply mask to get all rows that fit the criterion
    usmerit = data[mask]
    usmerit.drop_duplicates("Institution ID")
    usmerit = usmerit[['Institution', 'Country', 'Ranking']]
    # and were done!

    # return them
    return avg_teams, rank_n_teams, outst, usmerit


# method to split the dataframe into different
def split_csv(data: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    # take everything except for those columns exclusively required for team into institution
    inst = data.drop(['Team Number', 'Problem', 'Advisor', 'Ranking'], axis=1)

    # select everything except what is required for the team csv
    team = data.drop(['Institution', 'City', 'State/Province', 'Country'], axis=1)

    # selecting all but what is required for the opposite csv file allows for further manipulation without
    # having to re-create any custom columns used to group or sort

    # now that we are done with manipulation, we can drop all the lowercase columns by regex beginning with 'l_'
    inst = inst[inst.columns.drop(list(inst.filter(regex='l_')))]
    team = team[team.columns.drop(list(team.filter(regex='l_')))]

    # sort by institution ID/Team number for the respective CSV files to make it pretty
    inst = inst.sort_values(['Institution ID'])
    team = team.sort_values(['Team Number'])

    return inst, team


if __name__ == '__main__':
    # get number of command line arguments passed
    n = len(sys.argv)
    # if it's more than just the name of the python file
    if n > 1:
        # run the program
        #try:
        print(f"Running MCM CSV Analysis Tool on {sys.argv[1]}")
        main(str(sys.argv[1]))
        print("Process Complete. Exiting.")
        # if the file is an invalid name, then print to commandline
        #except:
        #    print(f"Invalid file {sys.argv[1]}. Check file name and try again.")

    print("Exiting Program")
