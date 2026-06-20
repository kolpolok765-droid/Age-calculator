import unittest
from datetime import date
from app import app, add_years, add_months, get_zodiac_info

class TestAgeCalculator(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_add_years_leap_year(self):
        # Leap year Feb 29 to non-leap year (e.g., 2000 to 2001) should fall back to Feb 28
        leap_day = date(2000, 2, 29)
        self.assertEqual(add_years(leap_day, 1), date(2001, 2, 28))
        self.assertEqual(add_years(leap_day, 4), date(2004, 2, 29))

    def test_add_months(self):
        # Normal month addition
        d = date(2023, 1, 15)
        self.assertEqual(add_months(d, 1), date(2023, 2, 15))
        # Month addition over year boundary
        self.assertEqual(add_months(d, 12), date(2024, 1, 15))
        # Day capping (e.g. Aug 31 + 1 month -> Sep 30)
        self.assertEqual(add_months(date(2000, 8, 31), 1), date(2000, 9, 30))

    def test_zodiac_info(self):
        self.assertEqual(get_zodiac_info(3, 21), ("Aries", "♈"))
        self.assertEqual(get_zodiac_info(12, 25), ("Capricorn", "♑"))
        self.assertEqual(get_zodiac_info(6, 15), ("Gemini", "♊"))

    def test_calculate_age_api(self):
        # Test calculation with a custom target date
        # 1990-05-15 to 2025-06-20 should be 35 years, 1 month, 5 days
        response = self.app.post('/calculate', json={
            "birthdate": "1990-05-15",
            "targetdate": "2025-06-20"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["years"], 35)
        self.assertEqual(data["months"], 1)
        self.assertEqual(data["days"], 5)
        self.assertEqual(data["zodiac_name"], "Taurus")

    def test_calculate_age_birthdate_after_targetdate(self):
        response = self.app.post('/calculate', json={
            "birthdate": "2026-06-20",
            "targetdate": "2025-06-20"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["error"], "Birthdate cannot be after target date")

    def test_calculate_age_missing_date(self):
        response = self.app.post('/calculate', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

if __name__ == "__main__":
    unittest.main()
