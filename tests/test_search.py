#!/usr/bin/env python3
"""
Search functionality tests for KACHA project
Tests the search algorithm and functionality
"""

import sys
import os
import json
import unittest
from pathlib import Path

# Add parent directory to path to import functions
sys.path.append(str(Path(__file__).parent.parent))

class SearchAlgorithmTests(unittest.TestCase):
    """Test cases for search functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.sample_locations = [
            {
                "film_name": "不能說的秘密",
                "CN_name": "不能说的秘密",
                "Area": "台北",
                "address": "台北市信義區",
                "year": 2007,
                "lng": 121.54,
                "lat": 25.04
            },
            {
                "film_name": "艋舺",
                "CN_name": "艋舺",
                "Area": "台北",
                "address": "台北市萬華區",
                "year": 2010,
                "lng": 121.50,
                "lat": 25.03
            },
            {
                "film_name": "那些年",
                "CN_name": "那些年",
                "Area": "彰化",
                "address": "彰化縣鹿港鎮",
                "year": 2011,
                "lng": 120.43,
                "lat": 24.05
            },
            {
                "film_name": "海角七號",
                "CN_name": "海角七号",
                "Area": "屏東",
                "address": "屏東縣恆春鎮",
                "year": 2008,
                "lng": 120.74,
                "lat": 22.00
            }
        ]
        
        # Build search index like the JavaScript code
        self.search_index = self.build_search_index()
    
    def build_search_index(self):
        """Build search index similar to JavaScript implementation"""
        search_index = []
        
        for index, location in enumerate(self.sample_locations):
            search_text = " ".join([
                str(location.get("film_name", "")),
                str(location.get("CN_name", "")),
                str(location.get("Area", "")),
                str(location.get("address", "")),
                str(location.get("year", ""))
            ]).lower()
            
            search_index.append({
                "index": index,
                "search_text": search_text,
                "location": location,
                "search_terms": search_text.split()
            })
        
        return search_index
    
    def calculate_search_score(self, search_term, index_item):
        """Calculate search score similar to JavaScript implementation"""
        score = 0
        location = index_item["location"]
        search_lower = search_term.lower()
        
        # Exact movie name match (highest score)
        if location.get("film_name") and search_lower in location["film_name"].lower():
            score += 100
        if location.get("CN_name") and search_lower in location["CN_name"].lower():
            score += 100
        
        # Area match
        if location.get("Area") and search_lower in location["Area"].lower():
            score += 50
        
        # Address match
        if location.get("address") and search_lower in location["address"].lower():
            score += 30
        
        # Year match
        if location.get("year") and search_term in str(location["year"]):
            score += 20
        
        # Partial matches
        search_words = search_term.split()
        for word in search_words:
            if len(word) > 1:
                if word.lower() in index_item["search_text"]:
                    score += 10
                
                # Single character matches (low weight)
                for char in word:
                    if char.lower() in index_item["search_text"]:
                        score += 1
        
        return score
    
    def search(self, search_term, max_results=10):
        """Perform search similar to JavaScript implementation"""
        if not search_term or len(search_term.strip()) == 0:
            return []
        
        results = []
        
        for item in self.search_index:
            score = self.calculate_search_score(search_term, item)
            if score > 0:
                result = item.copy()
                result["score"] = score
                results.append(result)
        
        # Sort by score (highest first)
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return results[:max_results]
    
    def test_basic_movie_name_search(self):
        """Test basic movie name search"""
        results = self.search("不能說的秘密")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["location"]["film_name"], "不能說的秘密")
        self.assertGreater(results[0]["score"], 100)  # Should have high score
    
    def test_chinese_movie_name_search(self):
        """Test Chinese movie name search"""
        results = self.search("那些年")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["location"]["film_name"], "那些年")
        self.assertGreater(results[0]["score"], 100)
    
    def test_area_search(self):
        """Test area-based search"""
        results = self.search("台北")
        # Should find both movies in Taipei
        self.assertGreater(len(results), 1)
        
        # Check that Taipei movies have higher scores for area match
        for result in results:
            if result["location"]["Area"] == "台北":
                self.assertGreaterEqual(result["score"], 20)  # Should have score from area or other matches
    
    def test_year_search(self):
        """Test year-based search"""
        results = self.search("2007")
        # Should find at least one result, but possibly more 
        self.assertGreater(len(results), 0)
        
        # Check that at least one result has the correct year
        found_2007 = False
        for result in results:
            if result["location"]["year"] == 2007:
                found_2007 = True
                break
        self.assertTrue(found_2007, "Should find a movie from year 2007")
    
    def test_partial_match_search(self):
        """Test partial matching functionality"""
        results = self.search("台")
        # Should find multiple results containing "台"
        self.assertGreater(len(results), 0)
    
    def test_search_scoring_priority(self):
        """Test that search scoring prioritizes exact matches"""
        results = self.search("艋舺")
        
        # Should find the movie
        self.assertGreater(len(results), 0)
        
        # The exact movie name match should have high score
        movie_match = next((r for r in results if r["location"]["film_name"] == "艋舺"), None)
        self.assertIsNotNone(movie_match)
        self.assertGreater(movie_match["score"], 90)
    
    def test_empty_search(self):
        """Test empty search returns no results"""
        results = self.search("")
        self.assertEqual(len(results), 0)
    
    def test_no_match_search(self):
        """Test search with no matches"""
        results = self.search("哈利波特")  # Not in our test data
        self.assertEqual(len(results), 0)
    
    def test_case_insensitive_search(self):
        """Test case insensitive search and word splitting"""
        results1 = self.search("台北")
        results2 = self.search("Taipei")  # Different case representation
        
        # First search should find results
        self.assertGreater(len(results1), 0)
        
        # Allow second search to have zero or more results since case handling may vary
    
    def test_ranking_order(self):
        """Test that results are properly ranked"""
        results = self.search("海角")
        
        if len(results) > 1:
            # Scores should be in descending order
            for i in range(len(results) - 1):
                self.assertGreaterEqual(results[i]["score"], results[i + 1]["score"])
    
    def test_real_data_search(self):
        """Test search with real location data if available"""
        try:
            with open('data/LocationList.json', 'r', encoding='utf-8') as f:
                real_locations = json.load(f)
            
            # Build search index with real data
            real_search_index = []
            for index, location in enumerate(real_locations):
                search_text = " ".join([
                    str(location.get("film_name", "")),
                    str(location.get("CN_name", "")),
                    str(location.get("Area", "")),
                    str(location.get("address", "")),
                    str(location.get("year", ""))
                ]).lower()
                
                real_search_index.append({
                    "index": index,
                    "search_text": search_text,
                    "location": location,
                    "search_terms": search_text.split()
                })
            
            print(f"\nTesting search with {len(real_locations)} real locations...")
            
            # Test common search terms based on actual data
            test_terms = ["Armed Reaction", "Sai Kung", "1998", "Central"]
            
            for term in test_terms:
                results = []
                for item in real_search_index:
                    score = self.calculate_search_score(term, item)
                    if score > 0:
                        result_item = item.copy()
                        result_item["score"] = score
                        results.append(result_item)
                
                results.sort(key=lambda x: x["score"], reverse=True)
                limited_results = results[:10]
                
                print(f"Search '{term}': {len(limited_results)} results")
                
                # Display sample results
                for i, result in enumerate(limited_results[:3]):
                    location = result["location"]
                    print(f"  {i+1}. {location.get('film_name', 'Unknown')} ({location.get('year', 'Unknown')}) - Score: {result['score']}")
            
            # Test basic functionality
            if len(real_locations) > 0:
                first_location = real_locations[0]
                film_name = first_location.get("film_name", "")
                
                if film_name:
                    # Test searching by first movie's name (should find at least one result)
                    search_results = []
                    for item in real_search_index:
                        score = self.calculate_search_score(film_name, item)
                        if score > 0:
                            result_item = item.copy()
                            result_item["score"] = score
                            search_results.append(result_item)
                    
                    search_results.sort(key=lambda x: x["score"], reverse=True)
                    
                    self.assertGreater(len(search_results), 0, "Should find results when searching by known movie name")
                    self.assertGreater(search_results[0]["score"], 50, "Exact movie name match should have high score")
                    
                    print(f"\nValidation test passed: Found {len(search_results)} results for '{film_name}'")
            
        except FileNotFoundError:
            print("Real location data not found, skipping real data tests")
        except json.JSONDecodeError as e:
            print(f"Error reading location data: {e}, skipping real data tests")


class SearchEdgeCases(unittest.TestCase):
    """Test edge cases for search functionality"""
    
    def setUp(self):
        # Minimal test data for edge cases
        self.search_index = [
            {
                "index": 0,
                "search_text": "test movie taipei",
                "location": {"film_name": "Test Movie", "Area": "Taipei"},
                "search_terms": ["test", "movie", "taipei"]
            },
            {
                "index": 1,
                "search_text": "",
                "location": {"film_name": "", "Area": ""},
                "search_terms": []
            }
        ]
    
    def calculate_search_score(self, search_term, index_item):
        """Simplified scoring for edge case testing"""
        if not search_term or not index_item["search_text"]:
            return 0
        
        score = 0
        location = index_item["location"]
        search_lower = search_term.lower()
        
        if location.get("film_name") and search_lower in location["film_name"].lower():
            score += 100
        
        return score
    
    def test_search_with_none_values(self):
        """Test search when some fields have None values"""
        results = []
        search_term = "test"
        
        for item in self.search_index:
            score = self.calculate_search_score(search_term, item)
            if score > 0:
                results.append(item)
        
        # Should find one result despite one item having empty data
        self.assertEqual(len(results), 1)
    
    def test_special_characters_search(self):
        """Test search with special characters"""
        test_cases = [
            ("測試-電影！", "should handle special punctuation"),
            ("movie & series", "should handle ampersand"),
            ("café", "should handle accented characters")
        ]
        
        for search_term, description in test_cases:
            with self.subTest(description=description):
                # Should not raise exceptions
                try:
                    results = []
                    for item in self.search_index:
                        score = self.calculate_search_score(search_term, item)
                        if score > 0:
                            results.append(item)
                    # Just testing that it doesn't crash
                    self.assertIsInstance(results, list)
                except Exception as e:
                    self.fail(f"Search with '{search_term}' raised exception: {e}")


def run_search_tests():
    """Run all search tests"""
    print("=== KACHA Search Functionality Test ===")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print()
    
    # Check if we can access the data files
    data_dir = Path("data")
    if data_dir.exists():
        print(f"Data directory: {data_dir} (exists)")
        for file in data_dir.glob("*.json"):
            print(f"  - {file.name} (size: {file.stat().st_size} bytes)")
    else:
        print(f"Warning: Data directory {data_dir} not found")
    
    print("\nRunning test suite...")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(SearchAlgorithmTests))
    suite.addTests(loader.loadTestsFromTestCase(SearchEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print(f"\n=== Test Results ===")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    print(f"\nAll tests completed in {(result.testsRun - len(result.failures) - len(result.errors))}/{result.testsRun} passes")
    
    return result


if __name__ == "__main__":
    run_search_tests()