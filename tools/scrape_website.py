import re
import requests
from bs4 import BeautifulSoup

def get_social_media_links(url: str) -> dict:
    """
    Scrapes a website to find links to social media sites.

    Args:
        url: The URL of the website to scrape.

    Returns:
        A dictionary containing the found social media links.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        page_source = response.text
    except requests.exceptions.RequestException as e:
        return {"error": f"Could not retrieve the website: {e}"}

    soup = BeautifulSoup(page_source, 'html.parser')
    
    links = {
        "instagram": None, 
        "linkedin": None,
        "facebook": None,
        "twitter": None,
        "youtube": None,
        "github": None,
        "tiktok": None
    }
    
    social_patterns = {
        "instagram": r'instagram\.com',
        "linkedin": r'linkedin\.com',
        "facebook": r'facebook\.com',
        "twitter": r'twitter\.com|x\.com',
        "youtube": r'youtube\.com',
        "github": r'github\.com',
        "tiktok": r'tiktok\.com'
    }

    # Find all links on the page
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        for social, pattern in social_patterns.items():
            if links[social] is None and re.search(pattern, href):
                links[social] = href

    # Filter out empty links
    found_links = {key: value for key, value in links.items() if value}

    if not found_links:
        return {"message": "No social media links found on the page."}

    return found_links

if __name__ == '__main__':
    # Example usage
    test_url = "https://www.example.com"  # Replace with a URL for testing
    social_links = get_social_media_links(test_url)
    print(f"Found social media links on {test_url}:")
    print(social_links)