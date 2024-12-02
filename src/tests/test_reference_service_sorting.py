import unittest

from services.reference_service import ReferenceService


class MockReference:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def __eq__(self, value: object):
        if isinstance(value, MockReference):
            return (
                self.title == value.title
                and self.author == value.author
                and self.year == value.year
            )
        return False


class TestReferenceService(unittest.TestCase):
    def setUp(self):
        self.reference_service = ReferenceService()
        self.reference_service.references = [
            MockReference("Classical mechanics", "Leonard Susskind", 2014),
            MockReference("An Analysis of Example", "John Smith and Jane Doe", 2022),
            MockReference("An Analysis of Example", "xyz", 2022),
            MockReference("Toimitusketjujen optimointi", "Joulupukki", 2023),
            MockReference("Aamunsarastus", "Joulupukki", 2023),
        ]

    def test_sort_references_by_title(self):
        result = self.reference_service.sort_references_by_title()
        expected = [
            MockReference("Aamunsarastus", "Joulupukki", 2023),
            MockReference("An Analysis of Example", "John Smith and Jane Doe", 2022),
            MockReference("An Analysis of Example", "xyz", 2022),
            MockReference("Classical mechanics", "Leonard Susskind", 2014),
            MockReference("Toimitusketjujen optimointi", "Joulupukki", 2023),
        ]

        self.assertEqual(result, expected)

    def test_sort_references_by_author(self):
        result = self.reference_service.sort_references_by_author()
        expected = [
            MockReference("An Analysis of Example", "John Smith and Jane Doe", 2022),
            MockReference("Aamunsarastus", "Joulupukki", 2023),
            MockReference("Toimitusketjujen optimointi", "Joulupukki", 2023),
            MockReference("Classical mechanics", "Leonard Susskind", 2014),
            MockReference("An Analysis of Example", "xyz", 2022),
        ]

        self.assertEqual(result, expected)

    def test_sort_references_by_year(self):
        result = self.reference_service.sort_references_by_year()
        expected = [
            MockReference("Classical mechanics", "Leonard Susskind", 2014),
            MockReference("An Analysis of Example", "John Smith and Jane Doe", 2022),
            MockReference("An Analysis of Example", "xyz", 2022),
            # if primary and secondary sorting values are the same the order is the
            # default what is given when called from the data base
            MockReference("Toimitusketjujen optimointi", "Joulupukki", 2023),
            MockReference("Aamunsarastus", "Joulupukki", 2023),
        ]

        self.assertEqual(result, expected)
