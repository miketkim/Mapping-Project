# SI 330 HW #2
# Michael Kim
# Worked with Cristina, Ankita, Taylor
import csv
import pprint
from collections import defaultdict

def year_from_date(date):
    year = str.split(date, '/')[2]
    return(year)

def output_formatted_float_string(f):
  return "{0:0.2f}".format(f)

# numeric_string_to_float: take a string representing a number as input (which may include commas or quotation marks)
# and convert it to float type so that it can be used in numerical calculations.
def strip_numeric_formatting(s):
    # remove commas and quotation marks from the number
    return s.replace(',', '').replace('\"', '')

# read_region_file: read the regions file and create '
# a dictionary mapping country_name to region
def read_region_file(filename):
    region_mapping = dict()

    with open(filename, 'r', newline='') as input_file:
        region_file_reader = csv.DictReader(input_file, delimiter='\t', quotechar ='"')

        for row in region_file_reader:
            region  = row['Region']
            country = row['Country']
            region_mapping[country] = region

    return region_mapping



def read_directed_graph_from_csv(filename, source_column, dest_column, weight_column):
    graph = defaultdict(list) #returns an empty list if looking up key doesn't exist
    with open(filename, 'r', newline='') as input_file:
        graph_reader = csv.DictReader(input_file, delimiter=',', quotechar='"')
        for row in graph_reader:
            if row[weight_column] == '' or row[weight_column] == "..":
                row[weight_column] = '0'


            tup = ((row[dest_column], (row[weight_column])))
            graph[row[source_column]].append(tup)
            graph[row[source_column]].sort(key= lambda x: float(x[1]), reverse= True)
    return (graph)

migration_outflow_graph = read_directed_graph_from_csv('world_bank_migration.csv', 'Country Origin Name', 'Country Dest Name', '2000 [2000]')



def csv_files(locationCSV):
    with open(locationCSV, 'r', newline='') as input_file:
        location_reader = csv.DictReader(input_file, delimiter=',', quotechar='"')
        with open('si330-hw2-nodes.csv', 'w', newline= '') as output_file:
            location_writer = csv.DictWriter(output_file, fieldnames=['country', 'latitude', 'longitude'], extrasaction = 'ignore', delimiter = ',', quotechar = '"')
            location_writer.writeheader()
            for row in location_reader:
                row['country'] = row['Country Name']
                row['latitude'] = row['Latitude']
                row['longitude'] = row['Longitude']
                location_writer.writerow(row)

csv_files('locations.csv')

def lookUpLocation(country, location):
    with open(location, 'r') as secondfile:
        location_response_reader = csv.DictReader(secondfile)
        for data in location_response_reader:
            try:
             if country == data['Country Name']:
                 someVal = data
                 return someVal
            except:
             pass


def edgeMigrationFiles(edge, locationcsv):

        with open(edge, newline='') as input_file:
            survey_response_reader = csv.DictReader(input_file)

            someDict = []
            with open('si330-hw2-edges.csv', 'w') as output_file:
                survey_response_writer = csv.DictWriter(output_file, fieldnames=['start_country','end_country', 'start_lat', 'start_long', 'end_lat', 'end_long', 'count'], extrasaction='ignore', delimiter=',', quotechar='"')
                survey_response_writer.writeheader()
                limit_row = 0
                for country in survey_response_reader:
                    x = lookUpLocation(country['Country Origin Name'], locationcsv)
                    y = lookUpLocation(country['Country Dest Name'], locationcsv)
                    if country['2000 [2000]'] == '' or  country['2000 [2000]'] == '..':
                        country['2000 [2000]'] = '0'

                    if x and y:
                        someDict.append({'start_country':country['Country Origin Name'], 'end_country': country['Country Dest Name'], 'start_lat': x['Latitude'],'start_long':
                                        x['Longitude'], 'end_lat': y['Latitude'], 'end_long': y['Longitude'], 'count': country['2000 [2000]'] })

                newlist = sorted(someDict, key=lambda k: float(k['count']), reverse= True)

                while limit_row < 1000:
                    survey_response_writer.writerow({'start_country':newlist[limit_row]['start_country'], 'end_country': newlist[limit_row]['end_country'], 'start_lat': newlist[limit_row]['start_lat'],'start_long':
                        newlist[limit_row]['start_long'], 'end_lat': newlist[limit_row]['end_lat'], 'end_long': newlist[limit_row]['end_long'], 'count': newlist[limit_row]['count'] })

                    limit_row+= 1

edgeMigrationFiles("world_bank_migration.csv", "locations.csv" )



def main():

    region_mapping = read_region_file("world_bank_regions.txt")
    destinations = read_directed_graph_from_csv('world_bank_migration.csv', 'Country Origin Name',
                                                'Country Dest Name', '2000 [2000]')
    origins = read_directed_graph_from_csv('world_bank_migration.csv', 'Country Dest Name',
                                           'Country Origin Name', '2000 [2000]')


    # open the tab-delimited input data file
    with open('world_bank_country_data.txt', 'r', newline = '') as input_file:
        # prepare to read the rows of the file using the csv packages' DictReader routines
        country_data_reader = csv.DictReader(input_file, delimiter='\t', quotechar ='"')

        # open a new output file
        with open('world-bank-output-hw2-miketkim.csv', 'w', newline = '') as output_file:
            # Prepare to write out rows to the output file using csv package's DictWriter routines
            # We are going to write out a subset of the original input file's columns, namely, these three:
            country_data_writer = csv.DictWriter(output_file, fieldnames = country_data_reader.fieldnames + ['Destinations', 'Sources'], extrasaction = 'ignore', delimiter = ',', quotechar = '"')
            # write the column header to the output file
            country_data_writer.writeheader()


            row_count = 0
            for row in country_data_reader:
                year = year_from_date(row['Date'])
                # filter for year condition
                if (year != "2000"):
                    continue
                row['Year'] = year

                row['Destinations'] = destinations[row['Country Name']][0:3]
                row['Sources'] = origins[row['Country Name']][0:3]

                country_data_writer.writerow(row)
                row_count = row_count + 1


    print("Done! Wrote a total of %d rows" % row_count)


# This is boilerplate python code: it tells the interpreter to execute main() only
# if this module is being run as the main script by the interpreter, and
# not being imported as a module.
if __name__ == '__main__':
    main()
