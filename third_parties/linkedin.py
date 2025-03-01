import os
import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """
    Scrape information from LinkedIn profiles,
    manually scrape the information from the LinkedIn profile"""
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/yauritux/32b949109b6bff3f174e1330d529130c/raw/377b1fa8d85d82e581e29b24ac542c9e6b7c88dd/allard_buijze_scrapin.json"
        githubAccessToken = os.environ["GH_ACCESS_TOKEN"]
        headers = {
            "Authorization": f"token {githubAccessToken}",
            "Accept": "application/vnd.github.v3+json",
        }
        response = requests.get(linkedin_profile_url, headers=headers, timeout=10)
    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey": os.environ["SCRAPIN_API_KEY"],
            "linkedInUrl": linkedin_profile_url,
        }
        response = requests.get(
            api_endpoint,
            params=params,
            timeout=10,
        )

    data = response.json().get("person")
    data = {}
    if hasattr(data, "items"):
        for k, v in data.items():
            if v not in ([], "", "", None) and k not in ["certifications"]:
                data[k] = v

    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/abuijze/", mock=True
        )
    )
