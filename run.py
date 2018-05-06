"""This script loads data from a given wiki page for retrieving a list of
universities in the bay area, organizes the data, and displays the ones near a
given location.
"""
import urllib
import googlemaps
import geopy.distance
import pandas as pd
from bs4 import BeautifulSoup

KEY_FILENAME = "key"
OUTPUT_FILENAME = "output.csv"
BAY_AREA_UNIVERSITIES_WIKI = ("https://en.wikipedia.org/wiki/"
                              "List_of_colleges_and_universities_in_the_"
                              "San_Francisco_Bay_Area")
MY_LOCATION = (37.388282, -122.030361)


def main():
    """Main function of the script. It reads a given WikiPedia page, parses the
    names of universities, retrieves the goelocation information using Google
    Map API, calculates the distance, then saves the sorted result into a CSV
    file.
    """
    def __get_university_names():

        with urllib.request.urlopen(BAY_AREA_UNIVERSITIES_WIKI) as url:
            soup = BeautifulSoup(url.read(), "lxml")

        return [
            link.text.strip()
            for link in soup.select("div#mw-content-text "
                                    "> div.mw-parser-output "
                                    "> table tr ul li a")
        ]

    def __get_gmaps():

        def __get_api_key():
            with open(KEY_FILENAME) as fin:
                return fin.read().strip()

        return googlemaps.Client(key=__get_api_key())

    def __get_location(gmaps, name):
        location = gmaps.geocode(name)[0]["geometry"]["location"]
        return location["lat"], location["lng"]

    # Initializes the variables
    names = __get_university_names()
    gmaps = __get_gmaps()
    table = pd.DataFrame(columns=["distance"])
    table.index.name = "name"

    # Parses and logs each university
    for name in names:
        location = __get_location(gmaps, name)
        distance = geopy.distance.vincenty(location, MY_LOCATION).km
        table.set_value(name, "distance", distance)
        print(name, location, distance)

    # Saves the final result
    table.sort_values(by=["distance"], inplace=True)
    table.to_csv(OUTPUT_FILENAME)
    print(table)


if __name__ == "__main__":
    main()
