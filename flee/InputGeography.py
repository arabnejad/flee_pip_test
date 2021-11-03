import csv
import os
import sys
from functools import wraps
from typing import List

from flee.SimulationSettings import SimulationSettings

if os.getenv("FLEE_TYPE_CHECK") is not None and os.environ["FLEE_TYPE_CHECK"].lower() == "true":
    from beartype import beartype as check_args_type
else:

    def check_args_type(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper


class InputGeography:
    """
    Class which reads in Geographic information.
    """

    def __init__(self):
        self.locations = []
        self.links = []
        self.conflicts = {}

    @check_args_type
    def ReadFlareConflictInputCSV(self, csv_name: str) -> None:
        """
        Reads a Flare input file, to set conflict information.

        Args:
            csv_name (str): Description
        """
        self.conflicts = {}

        row_count = 0
        headers = []

        with open(csv_name, newline="", encoding="utf-8") as csvfile:
            values = csv.reader(csvfile)

            for row in values:
                # print(row)
                if row_count == 0:
                    headers = row
                    for i in range(1, len(headers)):  # field 0 is day.
                        headers[i] = headers[i].strip()
                        if len(headers[i]) > 0:
                            self.conflicts[headers[i]] = []
                else:
                    for i in range(1, len(row)):  # field 0 is day.
                        # print(row[0])
                        self.conflicts[headers[i]].append(int(row[i].strip()))
                row_count += 1

        # print(self.conflicts)
        # TODO: make test verifying this in test_csv.py

    @check_args_type
    def getConflictLocationNames(self) -> List[str]:
        """
        Summary

        Returns:
            List[str]: Description
        """
        if len(SimulationSettings.FlareConflictInputFile) == 0:
            conflict_names = []
            for l in self.locations:
                if "conflict" in l[4].lower():
                    conflict_names += [l[0]]
            print(conflict_names, file=sys.stderr)
            return conflict_names

        return list(self.conflicts.keys())

    @check_args_type
    def ReadLocationsFromCSV(self, csv_name: str, columns: List[str] = None) -> None:
        """
        Converts a CSV file to a locations information table

        Args:
            csv_name (str): Description
            columns (List[str], optional): Description
        """
        self.locations = []

        c = {}  # column map

        c["location_type"] = 0
        c["conflict_date"] = 0
        c["country"] = 0
        c["region"] = 0

        if columns is None:
            columns = [
                "name",
                "region",
                "country",
                "gps_x",
                "gps_y",
                "location_type",
                "conflict_date",
                "pop/cap",
            ]

        for i in range(0, len(columns)):
            c[columns[i]] = i

        with open(csv_name, newline="", encoding="utf-8") as csvfile:
            values = csv.reader(csvfile)

            for row in values:
                if row[0][0] == "#":
                    pass
                else:
                    # print(row)
                    self.locations.append(
                        [
                            row[c["name"]],
                            row[c["pop/cap"]],
                            row[c["gps_x"]],
                            row[c["gps_y"]],
                            row[c["location_type"]],
                            row[c["conflict_date"]],
                            row[c["region"]],
                            row[c["country"]],
                        ]
                    )

    @check_args_type
    def ReadLinksFromCSV(
        self, csv_name: str, name1_col: int = 0, name2_col: int = 1, dist_col: int = 2
    ) -> None:
        """
        Converts a CSV file to a locations information table

        Args:
            csv_name (str): Description
            name1_col (int, optional): Description
            name2_col (int, optional): Description
            dist_col (int, optional): Description
        """
        self.links = []

        with open(csv_name, newline="", encoding="utf-8") as csvfile:
            values = csv.reader(csvfile)

            for row in values:
                if row[0][0] == "#":
                    pass
                else:
                    # print(row)
                    self.links.append([row[name1_col], row[name2_col], row[dist_col]])

    @check_args_type
    def ReadClosuresFromCSV(self, csv_name: str) -> None:
        """
        Read the closures.csv file. Format is:
        closure_type,name1,name2,closure_start,closure_end

        Args:
            csv_name (str): Description
        """
        self.closures = []

        with open(csv_name, newline="", encoding="utf-8") as csvfile:
            values = csv.reader(csvfile)

            for row in values:
                if row[0][0] == "#":
                    pass
                else:
                    # print(row)
                    self.closures.append(row)

    def StoreInputGeographyInEcosystem(self, e):
        """
        Store the geographic information in this class in a FLEE simulation,
        overwriting existing entries.

        Args:
            e (Ecosystem): Description

        Returns:
            Tuple[Ecosystem, Dict]: Description
        """
        lm = {}
        num_conflict_zones = 0
        for l in self.locations:

            name = l[0]
            # if population field is empty, just set it to 0.
            if len(l[1]) < 1:
                population = 0
            else:
                population = int(l[1]) // SimulationSettings.PopulationScaledownFactor

            x = float(l[2]) if len(l[2]) > 0 else 0.0
            y = float(l[3]) if len(l[3]) > 0 else 0.0

            # if country field is empty, just set it to unknown.
            if len(l[7]) < 1:
                country = "unknown"
            else:
                country = l[7]

            # print(l, file=sys.stderr)
            location_type = l[4]
            if "conflict" in location_type.lower():
                num_conflict_zones += 1
                if int(l[5]) > 0:
                    location_type = "town"

            if "camp" in location_type.lower():
                lm[name] = e.addLocation(
                    name=name,
                    location_type=location_type,
                    capacity=population,
                    x=x,
                    y=y,
                    country=country,
                )
            else:
                lm[name] = e.addLocation(
                    name=name,
                    location_type=location_type,
                    pop=population,
                    x=x,
                    y=y,
                    country=country,
                )

        for l in self.links:
            if len(l) > 3:
                if int(l[3]) == 1:
                    e.linkUp(
                        endpoint1=l[0],
                        endpoint2=l[1],
                        distance=float(l[2]),
                        forced_redirection=True,
                    )
                if int(l[3]) == 2:
                    e.linkUp(
                        endpoint1=l[1],
                        endpoint2=l[0],
                        distance=float(l[2]),
                        forced_redirection=True,
                    )
                else:
                    e.linkUp(
                        endpoint1=l[0],
                        endpoint2=l[1],
                        distance=float(l[2]),
                        forced_redirection=False,
                    )
            else:
                e.linkUp(
                    endpoint1=l[0],
                    endpoint2=l[1],
                    distance=float(l[2]),
                    forced_redirection=False,
                )

        e.closures = []
        for l in self.closures:
            e.closures.append([l[0], l[1], l[2], int(l[3]), int(l[4])])

        if num_conflict_zones < 1:
            print(
                "Warning: location graph has 0 conflict zones (ignore if conflicts.csv is used).",
                file=sys.stderr,
            )

        return e, lm

    @check_args_type
    def AddNewConflictZones(self, e, time: int, Debug: bool = False) -> None:
        """
        Adds new conflict zones according to information about the current time step.
        If there is no Flare input file, then the values from locations.csv are used.
        If there is one, then the data from Flare is used instead.
        Note: there is no support for *removing* conflict zones at this stage.

        Args:
            e (Ecosystem): Description
            time (int): Description
            Debug (bool, optional): Description
        """
        if len(SimulationSettings.FlareConflictInputFile) == 0:
            for l in self.locations:
                if "conflict" in l[4].lower() and int(l[5]) == time:
                    if e.print_location_output:
                        print(
                            "Time = {}. Adding a new conflict zone [{}] with pop. {}".format(
                                time, l[0], int(l[1])
                            ),
                            file=sys.stderr,
                        )
                    e.add_conflict_zone(name=l[0])
        else:
            confl_names = self.getConflictLocationNames()
            # print(confl_names)
            for l in confl_names:
                if Debug:
                    print("L:", l, self.conflicts[l], time, file=sys.stderr)
                if self.conflicts[l][time] == 1:
                    if time > 0:
                        if self.conflicts[l][time - 1] == 0:
                            print(
                                "Time = {}. Adding a new conflict zone [{}]".format(time, l),
                                file=sys.stderr,
                            )
                            e.add_conflict_zone(name=l)
                    else:
                        print(
                            "Time = {}. Adding a new conflict zone [{}]".format(time, l),
                            file=sys.stderr,
                        )
                        e.add_conflict_zone(name=l)
                if self.conflicts[l][time] == 0 and time > 0:
                    if self.conflicts[l][time - 1] == 1:
                        print(
                            "Time = {}. Removing conflict zone [{}]".format(time, l),
                            file=sys.stderr,
                        )
                        e.remove_conflict_zone(name=l)
