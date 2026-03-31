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
    # 1. Get titles and IDs 
    listings = load_listing_results(html_path)
    full_data = []
    
    # 2. Loop through and grab the deep details for each 
    for title, l_id in listings:
        details = get_listing_details(l_id)
        info = details[l_id]
        
        # 3. Combine into the specific tuple order required 
        entry = (title, l_id, info['policy_number'], info['host_type'], 
                 info['host_name'], info['room_type'], info['location_rating'])
        full_data.append(entry)
        
    return full_data
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
    # Sort by location rating descending 
    sorted_data = sorted(data, key=lambda x: x[6], reverse=True)
    
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        # Write the headers exactly as requested
        writer.writerow(["Listing Title", "Listing ID", "Policy Number", "Host Type", "Host Name", "Room Type", "Location Rating"])
        # Write the actual data rows
        writer.writerows(sorted_data)
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================

# Inside your TestCases class:
def test_create_listing_database(self):
    # Check that each tuple has 7 elements
    for row in self.detailed_data:
        self.assertEqual(len(row), 7)
    
    # Spot-check the last tuple in the list
    expected_last = ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8)
    self.assertEqual(self.detailed_data[-1], expected_last)

def test_output_csv(self):
    out_path = os.path.join(self.base_dir, "test.csv")
    output_csv(self.detailed_data, out_path)
    
    with open(out_path, 'r', encoding='utf-8-sig') as f:
        reader = list(csv.reader(f))
        # Check that the first data row (after header) matches the top-rated listing 
        first_data_row = reader[1]
        self.assertEqual(first_data_row[0], "Guesthouse in San Francisco")
        self.assertEqual(first_data_row[1], "49591060")
        self.assertEqual(first_data_row[-1], "5.0")


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
    room_totals = {}
    room_counts = {}
    
    for row in data:
        room_type = row[5]
        rating = row[6]
        
        # skip those 0.0 ratings per the instructions 
        if rating > 0:
            room_totals[room_type] = room_totals.get(room_type, 0) + rating
            room_counts[room_type] = room_counts.get(room_type, 0) + 1
            
    # calc the average for each type found
    averages = {rtype: round(room_totals[rtype] / room_counts[rtype], 1) for rtype in room_totals}
    return averages
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
    invalid_ids = []
    # official regex for 20##-00####STR or STR-000#### 
    pattern1 = r'^20\d{2}-00\d{4}STR$'
    pattern2 = r'^STR-000\d{4}$'
    
    for row in data:
        l_id = row[1]
        policy = row[2]
        
        # skip the ones that aren't numbers
        if policy in ["Pending", "Exempt"]:
            continue
            
        # if it doesn't match either valid format, flag it
        if not (re.match(pattern1, policy) or re.match(pattern2, policy)):
            invalid_ids.append(l_id)
            
    return invalid_ids
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
    url = f"https://scholar.google.com/scholar?q={query}"
    # need a user-agent so google doesn't block the request immediately
    headers = {'User-Agent': 'Mozilla/5.0'}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # article titles are usually in h3 tags with class gs_rt
    titles = [t.get_text() for t in soup.find_all('h3', class_='gs_rt')]
    return titles
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================

# Final Test Cases
def test_avg_location_rating_by_room_type(self):
    res = avg_location_rating_by_room_type(self.detailed_data)
    # verify the private room avg matches the rubric
    self.assertEqual(res.get("Private Room"), 4.9)

def test_validate_policy_numbers(self):
    invalid = validate_policy_numbers(self.detailed_data)
    # the instructions say this specific ID should be the only one 
    self.assertIn("16204265", invalid)
    self.assertEqual(len(invalid), 1)


class TestCases(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")

        self.listings = load_listing_results(self.search_results_path)
        self.detailed_data = create_listing_database(self.search_results_path)

    def test_load_listing_results(self):
        # Check that the number of listings extracted is 18 [cite: 111]
        self.assertEqual(len(self.listings), 18)
        # Check that the FIRST (title, id) tuple is correct [cite: 112]
        self.assertEqual(self.listings[0], ("Loft in Mission District", "1944564"))

    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]
        # Call get_listing_details() on each listing id [cite: 114]
        results = [get_listing_details(id) for id in html_list]

        # 1) Check that listing 467507 has the correct policy number [cite: 117]
        self.assertEqual(results[0]["467507"]["policy_number"], "STR-0005349")
        # 2) Check listing 1944564 host type and room type [cite: 118, 120]
        self.assertEqual(results[2]["1944564"]["host_type"], "Superhost")
        self.assertEqual(results[2]["1944564"]["room_type"], "Entire Room")
        # 3) Check listing 1944564 location rating [cite: 121]
        self.assertEqual(results[2]["1944564"]["location_rating"], 4.9)

    def test_create_listing_database(self):
        # Check that each tuple in detailed_data has exactly 7 elements [cite: 123]
        for row in self.detailed_data:
            self.assertEqual(len(row), 7)

        # Spot-check the last tuple in the database [cite: 124, 126, 127]
        expected_last = ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8)
        self.assertEqual(self.detailed_data[-1], expected_last)

    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")
        # Write the detailed_data to a CSV file [cite: 129]
        output_csv(self.detailed_data, out_path)
        
        # Read the CSV back in [cite: 130]
        with open(out_path, 'r', encoding='utf-8-sig') as f:
            reader = list(csv.reader(f))
            # Check the first data row matches expectations [cite: 132]
            first_data_row = reader[1]
            self.assertEqual(first_data_row[0], "Guesthouse in San Francisco")
            self.assertEqual(first_data_row[1], "49591060")
            self.assertEqual(first_data_row[2], "STR-0000253")
            self.assertEqual(first_data_row[-1], "5.0")

        if os.path.exists(out_path):
            os.remove(out_path)

    def test_avg_location_rating_by_room_type(self):
        # Call the function and save output [cite: 134]
        res = avg_location_rating_by_room_type(self.detailed_data)
        # Check that the average for "Private Room" is 4.9 [cite: 135]
        self.assertEqual(res.get("Private Room"), 4.9)

    def test_validate_policy_numbers(self):
        # Call validate_policy_numbers() [cite: 137]
        invalid = validate_policy_numbers(self.detailed_data)
        # Check that the list contains exactly "16204265" [cite: 138]
        self.assertIn("16204265", invalid)
        self.assertEqual(len(invalid), 1)


def main():
    detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
    output_csv(detailed_data, "airbnb_dataset.csv")


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)