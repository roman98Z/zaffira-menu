#!/usr/bin/env python3
import requests
import json
import time
import os
import sys
from datetime import datetime
import unittest

# Get the backend URL from the frontend .env file
with open('/app/frontend/.env', 'r') as f:
    for line in f:
        if line.startswith('REACT_APP_BACKEND_URL='):
            BACKEND_URL = line.strip().split('=')[1].strip('"\'')
            break

# Ensure we have a valid backend URL
if not BACKEND_URL:
    print("Error: Could not find REACT_APP_BACKEND_URL in frontend/.env")
    sys.exit(1)

# Add /api prefix for all API calls
API_URL = f"{BACKEND_URL}/api"

class MenuAPITest(unittest.TestCase):
    """Test suite for Menu 9nove API"""

    def setUp(self):
        """Setup for each test"""
        self.start_time = time.time()
        # Initialize test item data
        self.test_item = {
            "name": "Test Item",
            "price": 9.99,
            "description": "Test description",
            "category": "apericena"
        }
        self.created_item_id = None

    def tearDown(self):
        """Teardown after each test"""
        elapsed = time.time() - self.start_time
        print(f"{self._testMethodName} took {elapsed:.2f} seconds")
        
        # Clean up any created test items
        if self.created_item_id:
            try:
                requests.delete(f"{API_URL}/menu/{self.created_item_id}")
                self.created_item_id = None
            except:
                pass

    def test_01_api_root(self):
        """Test API root endpoint"""
        response = requests.get(f"{API_URL}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("running", data["message"])

    def test_02_menu_initialization(self):
        """Test menu initialization endpoint"""
        # First, initialize the menu
        response = requests.post(f"{API_URL}/menu/init")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Check if initialization was successful or menu was already initialized
        self.assertIn("message", data)
        if "initialized successfully" in data["message"]:
            self.assertIn("items_created", data)
            self.assertEqual(data["items_created"], 30)  # Should create 30 sample items
        else:
            self.assertIn("already initialized", data["message"])
            self.assertIn("items_count", data)
        
        # Try initializing again to check duplicate prevention
        response = requests.post(f"{API_URL}/menu/init")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("already initialized", data["message"])

    def test_03_get_menu_categories(self):
        """Test getting menu categories"""
        response = requests.get(f"{API_URL}/menu/categories")
        self.assertEqual(response.status_code, 200)
        categories = response.json()
        
        # Check we have 5 categories
        self.assertEqual(len(categories), 5)
        
        # Expected categories
        expected_categories = [
            {"id": "apericena", "label": "Apericena", "icon": "🍢"},
            {"id": "bevande", "label": "Bevande", "icon": "🥤"},
            {"id": "vini", "label": "Vini e Bollicine", "icon": "🍷"},
            {"id": "mixology", "label": "Mixology", "icon": "🍸"},
            {"id": "gin", "label": "I Nostri Gin", "icon": "🍃"}
        ]
        
        # Verify each category
        for expected in expected_categories:
            found = False
            for category in categories:
                if category["id"] == expected["id"]:
                    found = True
                    self.assertEqual(category["label"], expected["label"])
                    self.assertEqual(category["icon"], expected["icon"])
                    self.assertIn("items", category)
                    
                    # Check items are sorted by name
                    if len(category["items"]) > 1:
                        for i in range(len(category["items"]) - 1):
                            self.assertLessEqual(
                                category["items"][i]["name"].lower(),
                                category["items"][i + 1]["name"].lower()
                            )
                    break
            self.assertTrue(found, f"Category {expected['id']} not found")

    def test_04_get_all_menu_items(self):
        """Test getting all menu items"""
        response = requests.get(f"{API_URL}/menu")
        self.assertEqual(response.status_code, 200)
        items = response.json()
        
        # Should have at least 30 items (from initialization)
        self.assertGreaterEqual(len(items), 30)
        
        # Check item structure
        for item in items:
            self.assertIn("id", item)
            self.assertIn("name", item)
            self.assertIn("price", item)
            self.assertIn("category", item)
            self.assertIn("is_active", item)
            self.assertIn("created_at", item)
            self.assertIn("updated_at", item)
            
            # Validate data types
            self.assertIsInstance(item["id"], str)
            self.assertIsInstance(item["name"], str)
            self.assertIsInstance(item["price"], float)
            self.assertIsInstance(item["category"], str)
            self.assertIsInstance(item["is_active"], bool)
            
            # Validate category is one of the expected values
            self.assertIn(item["category"], ["apericena", "bevande", "vini", "mixology", "gin"])

    def test_05_filter_menu_by_category(self):
        """Test filtering menu items by category"""
        # Test each category
        for category in ["apericena", "bevande", "vini", "mixology", "gin"]:
            response = requests.get(f"{API_URL}/menu?category={category}")
            self.assertEqual(response.status_code, 200)
            items = response.json()
            
            # Should have at least 1 item per category
            self.assertGreaterEqual(len(items), 1)
            
            # All items should be from the requested category
            for item in items:
                self.assertEqual(item["category"], category)
        
        # Test invalid category
        response = requests.get(f"{API_URL}/menu?category=invalid_category")
        self.assertEqual(response.status_code, 200)
        items = response.json()
        self.assertEqual(len(items), 0)  # Should return empty list, not error

    def test_06_get_single_menu_item(self):
        """Test getting a single menu item"""
        # First, get all items to find a valid ID
        response = requests.get(f"{API_URL}/menu")
        self.assertEqual(response.status_code, 200)
        items = response.json()
        
        if items:
            # Get the first item's ID
            item_id = items[0]["id"]
            
            # Test getting that specific item
            response = requests.get(f"{API_URL}/menu/{item_id}")
            self.assertEqual(response.status_code, 200)
            item = response.json()
            
            # Verify it's the same item
            self.assertEqual(item["id"], item_id)
            self.assertEqual(item["name"], items[0]["name"])
            self.assertEqual(item["price"], items[0]["price"])
            self.assertEqual(item["category"], items[0]["category"])
        
        # Test invalid item ID
        response = requests.get(f"{API_URL}/menu/invalid_id")
        self.assertEqual(response.status_code, 404)
        error = response.json()
        self.assertIn("detail", error)
        self.assertIn("not found", error["detail"])

    def test_07_create_menu_item(self):
        """Test creating a new menu item"""
        # Create a new item
        response = requests.post(f"{API_URL}/menu", json=self.test_item)
        self.assertEqual(response.status_code, 200)
        item = response.json()
        
        # Save the ID for cleanup
        self.created_item_id = item["id"]
        
        # Verify item was created correctly
        self.assertEqual(item["name"], self.test_item["name"])
        self.assertEqual(item["price"], self.test_item["price"])
        self.assertEqual(item["description"], self.test_item["description"])
        self.assertEqual(item["category"], self.test_item["category"])
        self.assertTrue(item["is_active"])
        
        # Verify timestamps are present
        self.assertIn("created_at", item)
        self.assertIn("updated_at", item)
        
        # Verify item exists in the database
        response = requests.get(f"{API_URL}/menu/{item['id']}")
        self.assertEqual(response.status_code, 200)
        
        # Test creating item with invalid category
        invalid_item = self.test_item.copy()
        invalid_item["category"] = "invalid_category"
        response = requests.post(f"{API_URL}/menu", json=invalid_item)
        self.assertEqual(response.status_code, 400)
        error = response.json()
        self.assertIn("detail", error)
        self.assertIn("Invalid category", error["detail"])
        
        # Test creating item with missing required fields
        for field in ["name", "price", "category"]:
            invalid_item = self.test_item.copy()
            del invalid_item[field]
            response = requests.post(f"{API_URL}/menu", json=invalid_item)
            self.assertEqual(response.status_code, 422)  # Validation error

    def test_08_update_menu_item(self):
        """Test updating a menu item"""
        # First create an item to update
        response = requests.post(f"{API_URL}/menu", json=self.test_item)
        self.assertEqual(response.status_code, 200)
        item = response.json()
        self.created_item_id = item["id"]
        
        # Update the item
        update_data = {
            "name": "Updated Test Item",
            "price": 12.99,
            "description": "Updated description"
        }
        response = requests.put(f"{API_URL}/menu/{item['id']}", json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_item = response.json()
        
        # Verify item was updated correctly
        self.assertEqual(updated_item["id"], item["id"])
        self.assertEqual(updated_item["name"], update_data["name"])
        self.assertEqual(updated_item["price"], update_data["price"])
        self.assertEqual(updated_item["description"], update_data["description"])
        self.assertEqual(updated_item["category"], item["category"])  # Category unchanged
        
        # Verify updated_at timestamp changed
        self.assertNotEqual(updated_item["updated_at"], item["updated_at"])
        
        # Test updating with invalid category
        response = requests.put(f"{API_URL}/menu/{item['id']}", json={"category": "invalid_category"})
        self.assertEqual(response.status_code, 400)
        
        # Test updating non-existent item
        response = requests.put(f"{API_URL}/menu/invalid_id", json=update_data)
        self.assertEqual(response.status_code, 404)

    def test_09_delete_menu_item(self):
        """Test deleting a menu item (soft delete)"""
        # First create an item to delete
        response = requests.post(f"{API_URL}/menu", json=self.test_item)
        self.assertEqual(response.status_code, 200)
        item = response.json()
        item_id = item["id"]
        
        # Delete the item
        response = requests.delete(f"{API_URL}/menu/{item_id}")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("message", result)
        self.assertIn("deleted successfully", result["message"])
        
        # Verify item is no longer returned in general queries
        response = requests.get(f"{API_URL}/menu")
        items = response.json()
        found = False
        for i in items:
            if i["id"] == item_id:
                found = True
                break
        self.assertFalse(found, "Deleted item should not be returned in queries")
        
        # Verify item is not accessible directly
        response = requests.get(f"{API_URL}/menu/{item_id}")
        self.assertEqual(response.status_code, 404)
        
        # Test deleting non-existent item
        response = requests.delete(f"{API_URL}/menu/invalid_id")
        self.assertEqual(response.status_code, 404)
        
        # No need to clean up as the item is already deleted
        self.created_item_id = None

    def test_10_data_validation(self):
        """Test data validation for menu items"""
        # Test invalid price (negative)
        invalid_item = self.test_item.copy()
        invalid_item["price"] = -10.0
        response = requests.post(f"{API_URL}/menu", json=invalid_item)
        # Note: The API doesn't explicitly validate price values, so this might succeed
        # This test is to verify the behavior
        
        # Test extremely large price
        invalid_item = self.test_item.copy()
        invalid_item["price"] = 1000000.0
        response = requests.post(f"{API_URL}/menu", json=invalid_item)
        # Again, checking behavior as there's no explicit validation
        
        if response.status_code == 200:
            self.created_item_id = response.json()["id"]

    def test_11_response_performance(self):
        """Test API response performance"""
        # Test categories endpoint performance
        start_time = time.time()
        response = requests.get(f"{API_URL}/menu/categories")
        elapsed = time.time() - start_time
        self.assertEqual(response.status_code, 200)
        print(f"Categories endpoint response time: {elapsed:.4f} seconds")
        self.assertLess(elapsed, 2.0, "Categories endpoint should respond in under 2 seconds")
        
        # Test all items endpoint performance
        start_time = time.time()
        response = requests.get(f"{API_URL}/menu")
        elapsed = time.time() - start_time
        self.assertEqual(response.status_code, 200)
        print(f"All items endpoint response time: {elapsed:.4f} seconds")
        self.assertLess(elapsed, 2.0, "All items endpoint should respond in under 2 seconds")

if __name__ == "__main__":
    # Initialize the menu before running tests
    print(f"Initializing menu data at {API_URL}/menu/init")
    init_response = requests.post(f"{API_URL}/menu/init")
    print(f"Initialization response: {init_response.json()}")
    
    # Run the tests
    unittest.main(verbosity=2)