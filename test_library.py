import os
import unittest
from companieshouse import CompaniesHouseClient

class TestCompaniesHouseClient(unittest.TestCase):
    """
    Unit tests for the Companies House API client.
    Requires the COMPANIES_HOUSE_API_KEY environment variable to be set.
    """

    def setUp(self):
        """Set up the test client before each test."""
        self.api_key = os.environ.get("COMPANIES_HOUSE_API_KEY")
        if not self.api_key:
            self.fail("COMPANIES_HOUSE_API_KEY environment variable not set.")
        self.client = CompaniesHouseClient(api_key=self.api_key)

    def test_search_companies(self):
        """Test searching for companies."""
        query = "BBC"
        response = self.client.search_companies(query)
        self.assertIn("items", response)
        self.assertIsInstance(response["items"], list)
        print(f"\nFound {len(response['items'])} companies for query: '{query}'")
        # So we can see some results
        for company in response["items"][:5]:
            print(f"  - {company.get('title')} ({company.get('company_number')})")


    def test_get_company_profile(self):
        """Test retrieving a specific company profile."""
        # Using a known company number for a well-known entity
        company_number = "06500244" # BARCLAYS PLC
        response = self.client.get_company_profile(company_number)
        self.assertIn("company_name", response)
        self.assertEqual(response["company_number"], company_number)
        self.assertEqual(response["company_name"], "BBC LIMITED")
        print(f"\nSuccessfully retrieved profile for {response['company_name']}")
        print(f"  - Company Number: {response['company_number']}")
        print(f"  - Status: {response['company_status']}")
        print(f"  - Creation Date: {response['date_of_creation']}")


    def test_get_company_officers(self):
        """Test retrieving company officers."""
        company_number = "06500244" # BARCLAYS PLC
        response = self.client.get_company_officers(company_number)
        self.assertIn("items", response)
        self.assertIsInstance(response["items"], list)
        print(f"\nFound {len(response['items'])} officers for company number: {company_number}")
        # So we can see some results
        for officer in response["items"][:5]:
            print(f"  - {officer.get('name')}")


if __name__ == '__main__':
    unittest.main()
