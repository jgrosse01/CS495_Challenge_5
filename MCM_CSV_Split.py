import pandas as pd
import os
import sys


# method to execute the process of splitting the CSV
def main(filename: str):
    # read data
    data = pd.read_csv(os.path.abspath(f"./data/{filename}"))
    # split data
    inst, team = split_csv(data)

    # if the build directory does not exist then make it. then write files to that folder
    if not os.path.exists(os.path.abspath("./build")):
        os.mkdir(os.path.abspath("./build"))
    inst.to_csv("build/Institutions.csv", index=False)
    team.to_csv("build/Teams.csv", index=False)


# method to split the dataframe into different
def split_csv(data: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
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

    # take everything except for those columns exclusively required for team into institution
    inst = data.drop(['Team Number', 'Problem', 'Advisor', 'Ranking'], axis=1)
    # make sure there is only one of each institution ID in the CSV
    inst = inst.drop_duplicates(['Institution ID'])

    # select everything except what is required for the team csv
    team = data.drop(['Institution', 'City', 'State/Province', 'Country'], axis=1)

    # selecting all but what is required for the opposite csv file allows for further manipulation without
    # having to re-create any custom columns used to group or sort

    # now that we are done with manipulation, we can drop all of the lowercase columns by regex beginning with 'l_'
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
        try:
            main(str(sys.argv[1]))
            print("Process Complete")
        # if the file is an invalid name, then print to commandline
        except:
            print(f"Invalid file {sys.argv[1]}. Check file name and try again.")

    print("Exiting Program")
