"""

    Handles everything related to a script output
    Copyright (C) 2019 Hsuan-Ting Lu

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
import statistics


class ScriptOuput:
    def __init__(self, filename: str):
        self.filename = filename

    def avg(self, low_bound: int, high_bound: int) -> float:
        # @todo add more warnings about inclusive/exclusive bound rules
        """ Average:

        [ INCLUSIVE BOUND ]

            parameters:
                low_bound:  valid number low bound
                high_bound: valid number high bound

        opens a file,
        retrieve designated lines according to the filter parameters,
        returns the average value

        """

        with open(self.filename, "r") as f:
            # read and ignore headers
            f.readline()
            f.readline()

            def range_selector(x):  # dynamically defined filter
                """ filter indexes of lines to be within designated range """
                num = int(x.split(' ')[0])
                return high_bound >= num and num >= low_bound

            lines = filter(range_selector, f.readlines())
            val_list = list(map((lambda x: float(x.split(' ')[1])), lines))
            val = statistics.mean(val_list)
            return val
