import requests
import os

OUTPUT_DIR = "corpus/owasp"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def fetch_cve_data():
    """Fetches vulnerabilities from NVD API."""
    print("Fetching vulnerabilities from NVD...")

    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    params = {
        "keywordSearch": "python",
        "resultsPerPage": 8
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()
        vulnerabilities = data.get("vulnerabilities", [])

        for vuln in vulnerabilities:
            cve_id = vuln["cve"]["id"]

            descriptions = vuln["cve"].get("descriptions", [])
            description = (
                descriptions[0]["value"]
                if descriptions
                else "No description available."
            )

            file_path = os.path.join(OUTPUT_DIR, f"{cve_id}.md")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"# {cve_id}\n\n{description}")

            print(f"Saved {cve_id}")

        print(f"Finished. Saved {len(vulnerabilities)} vulnerabilities.")

    except Exception as e:
        print(f"Error fetching data: {e}")


if __name__ == "__main__":
    fetch_cve_data()