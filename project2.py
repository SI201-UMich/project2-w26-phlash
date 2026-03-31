# Name: Jaden Simmons
# Student ID: 38934105
# Email: pjaes@umich.edu
# Who or what you worked with: Gemini (AI)
# How used: Structural planning to ensure rubric requirements were met.
# Contract Alignment: Yes. I am using AI for structural guidance to 
# focus on writing the actual Python logic myself.
# --- ARGUMENTS & EXPECTED RETURN VALUES PROVIDED --- #
# --- SEE INSTRUCTIONS FOR FULL DETAILS ON METHOD IMPLEMENTATION --- #

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests  # kept for extra credit parity


# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"
"""


def load_listing_results(html_path) -> list[tuple]:
    """
    Load file data from html_path and parse through it to find listing titles and listing ids.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples containing (listing_title, listing_id)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    with open(html_path, 'r', encoding='utf-8-sig') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    listings = []
    # find all the links that look like airbnb room urls
    links = soup.find_all('a', href=re.compile(r'/rooms/\d+'))
    
    for link in links:
        url = link.get('href')
        # get the numeric id from the end of the link
        listing_id = url.split('/')[-1].split('?')[0]
        
        # use the aria-label for the title since it's usually the cleanest
        title = link.get('aria-label', '').strip()
        
        if title and (title, listing_id) not in listings:
            listings.append((title, listing_id))
            
    return listings
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================

# Inside your TestCases class:
def test_load_listing_results(self):
    # should be 18 total listings in this file
    self.assertEqual(len(self.listings), 18)
    # check the first one matches the project specs
    self.assertEqual(self.listings[0], ("Loft in Mission District", "1944564"))


def get_listing_details(listing_id) -> dict:
    """
    Parse through listing_<id>.html to extract listing details.

    Args:
        listing_id (str): The listing id of the Airbnb listing

    Returns:
        dict: Nested dictionary in the format:
        {
            "<listing_id>": {
                "policy_number": str,
                "host_type": str,
                "host_name": str,
                "room_type": str,
                "location_rating": float
            }
        }
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    file_path = os.path.join("html_files", f"listing_{listing_id}.html")
    
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # 1. Policy Number logic
    policy_tag = soup.find('li', class_='f19sbt9a')
    policy_text = policy_tag.get_text().strip() if policy_tag else ""
    
    if "pending" in policy_text.lower():
        policy = "Pending"
    elif "exempt" in policy_text.lower() or "not needed" in policy_text.lower():
        policy = "Exempt"
    else:
        # Clean up "License number: " if it exists
        policy = policy_text.replace("License number:", "").strip()

    # 2. Host info
    host_tag = soup.find('h2', class_='hpipapi')
    host_name = host_tag.get_text().replace("Hosted by ", "").strip() if host_tag else ""
    
    # Check for Superhost badge text
    host_type = "Superhost" if soup.find(string=re.compile("Superhost")) else "regular"

    # 3. Room Type logic based on subtitle
    sub_tag = soup.find('h2', class_='_147n9p1')
    subtitle = sub_tag.get_text() if sub_tag else ""
    
    if "private" in subtitle.lower():
        room_type = "Private Room"
    elif "shared" in subtitle.lower():
        room_type = "Shared Room"
    else:
        room_type = "Entire Room"

    # 4. Location Rating (pulling from the ratings section)
    location_rating = 0.0
    loc_span = soup.find('span', string="Location")
    if loc_span:
        try:
            # Finding the sibling div that holds the actual number
            score_container = loc_span.find_parent('div').find_next_sibling('div')
            location_rating = float(score_container.get_text())
        except:
            location_rating = 0.0

    return {
        listing_id: {
            "policy_number": policy,
            "host_type": host_type,
            "host_name": host_name,
            "room_type": room_type,
            "location_rating": location_rating
        }
    }
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================

# Inside your TestCases class:
def test_get_listing_details(self):
    html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]
    results = [get_listing_details(id) for id in html_list]
    
    # 1) Check policy number for 467507
    self.assertEqual(results[0]["467507"]["policy_number"], "STR-0005349")
    # 2) Check host/room type for 1944564
    self.assertEqual(results[2]["1944564"]["host_type"], "Superhost")
    self.assertEqual(results[2]["1944564"]["room_type"], "Entire Room")
    # 3) Check rating for 1944564
    self.assertEqual(results[2]["1944564"]["location_rating"], 4.9)


def create_listing_database(html_path) -> list[tuple]:
    """
    Use prior functions to gather all necessary information and create a database of listings.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples. Each tuple contains:
        (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def output_csv(data, filename) -> None:
    """
    Write data to a CSV file with the provided filename.

    Sort by Location Rating (descending).

    Args:
        data (list[tuple]): A list of tuples containing listing information
        filename (str): The name of the CSV file to be created and saved to

    Returns:
        None
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def avg_location_rating_by_room_type(data) -> dict:
    """
    Calculate the average location_rating for each room_type.

    Excludes rows where location_rating == 0.0 (meaning the rating
    could not be found in the HTML).

    Args:
        data (list[tuple]): The list returned by create_listing_database()

    Returns:
        dict: {room_type: average_location_rating}
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def validate_policy_numbers(data) -> list[str]:
    """
    Validate policy_number format for each listing in data.
    Ignore "Pending" and "Exempt" listings.

    Args:
        data (list[tuple]): A list of tuples returned by create_listing_database()

    Returns:
        list[str]: A list of listing_id values whose policy numbers do NOT match the valid format
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


# EXTRA CREDIT
def google_scholar_searcher(query):
    """
    EXTRA CREDIT

    Args:
        query (str): The search query to be used on Google Scholar
    Returns:
        List of titles on the first page (list)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


class TestCases(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")

        self.listings = load_listing_results(self.search_results_path)
        self.detailed_data = create_listing_database(self.search_results_path)

    def test_load_listing_results(self):
        # TODO: Check that the number of listings extracted is 18.
        # TODO: Check that the FIRST (title, id) tuple is  ("Loft in Mission District", "1944564").
        pass

    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        # TODO: Call get_listing_details() on each listing id above and save results in a list.

        # TODO: Spot-check a few known values by opening the corresponding listing_<id>.html files.
        # 1) Check that listing 467507 has the correct policy number "STR-0005349".
        # 2) Check that listing 1944564 has the correct host type "Superhost" and room type "Entire Room".
        # 3) Check that listing 1944564 has the correct location rating 4.9.
        pass

    def test_create_listing_database(self):
        # TODO: Check that each tuple in detailed_data has exactly 7 elements:
        # (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)

        # TODO: Spot-check the LAST tuple is ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8).
        pass

    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")

        # TODO: Call output_csv() to write the detailed_data to a CSV file.
        # TODO: Read the CSV back in and store rows in a list.
        # TODO: Check that the first data row matches ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"].

        os.remove(out_path)

    def test_avg_location_rating_by_room_type(self):
        # TODO: Call avg_location_rating_by_room_type() and save the output.
        # TODO: Check that the average for "Private Room" is 4.9.
        pass

    def test_validate_policy_numbers(self):
        # TODO: Call validate_policy_numbers() on detailed_data and save the result into a variable invalid_listings.
        # TODO: Check that the list contains exactly "16204265" for this dataset.
        pass


def main():
    detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
    output_csv(detailed_data, "airbnb_dataset.csv")


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)