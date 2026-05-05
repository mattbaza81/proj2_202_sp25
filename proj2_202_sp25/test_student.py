import unittest
from proj2 import *


class TestProject2(unittest.TestCase):
    def test_parse_row_data(self):
        fields = [
            "USA", "2020", "100.5", "0.3",
            "200.5", "0.6", "300.5", "0.9"
        ]
        row = parse_row(fields)

        self.assertEqual(row.country, "USA")
        self.assertEqual(row.year, 2020)
        self.assertEqual(row.electricity_and_heat_co2_emissions, 100.5)
        self.assertEqual(row.energy_co2_emissions, 200.5)

    def test_parse_row_missing_data(self):
        fields = ["Andorra", "2010", "", "", "", "", "", ""]
        row = parse_row(fields)

        self.assertEqual(row.country, "Andorra")
        self.assertEqual(row.year, 2010)
        self.assertIsNone(row.electricity_and_heat_co2_emissions)
        self.assertIsNone(row.total_co2_emissions_excluding_lucf_per_capita)

    def test_read_csv_lines(self):
        data = read_csv_lines("proj2_202_sp25/sample.csv")
        self.assertIsNotNone(data)
        self.assertEqual(data.value.country, "USA")
        self.assertEqual(data.value.year, 2020)
        self.assertEqual(listlen(data), 6)

    def test_listlen_empty(self):
        self.assertEqual(listlen(None), 0)

    def test_listlen_nonempty(self):
        r1 = Row("USA", 2020, None, None, None, None, None, None)
        r2 = Row("Canada", 2020, None, None, None, None, None, None)

        data = Node(r1, Node(r2, None))

        self.assertEqual(listlen(data), 2)

    def test_filter_rows_country_equal(self):
        data = read_csv_lines("proj2_202_sp25/sample.csv")

        result = filter_rows(data, "country", "equal", "USA")

        self.assertEqual(listlen(result), 2)
        self.assertEqual(result.value.country, "USA")
        self.assertEqual(result.next.value.country, "USA")

    def test_filter_rows_year_greater_than(self):
        data = read_csv_lines("proj2_202_sp25/sample.csv")

        result = filter_rows(data, "year", "greater_than", 2019)

        self.assertEqual(listlen(result), 3)

    def test_filter_rows_number_less_than(self):
        data = read_csv_lines("proj2_202_sp25/sample.csv")
        result = filter_rows(
            data,
            "energy_co2_emissions",
            "less_than",
            100.0
        )

        self.assertEqual(listlen(result), 3)

    def test_filter_rows_skipping(self):
        data = read_csv_lines("proj2_202_sp25/sample.csv")
        result = filter_rows(
            data,
            "energy_co2_emissions",
            "greater_than",
            0.0
        )

        self.assertEqual(listlen(result), 5)

    def test_filter_country_invalid_comparison(self):
        data = read_csv_lines("proj2_202_sp25/sample.csv")

        with self.assertRaises(ValueError):
            filter_rows(data, "country", "greater_than", "USA")


if __name__ == "__main__":
    unittest.main()
