
import requests
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

# Official NSP website
url = "https://scholarships.gov.in/All-Scholarships"

# Create raw data folder
output_folder = Path("data/raw")
output_folder.mkdir(parents=True, exist_ok=True)

try:
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30
    )

    response.raise_for_status()

    html_content = response.text

    if not html_content.strip():
        raise ValueError("Website returned empty content")

    # Save original website content
    filename = datetime.now().strftime("nsp_raw_%Y%m%d_%H%M%S.html")
    file_path = output_folder / filename
    file_path.write_text(html_content, encoding="utf-8")

    # Generate SHA256 hash
    file_hash = hashlib.sha256(
        html_content.encode("utf-8")
    ).hexdigest()

    # Save extraction metadata
    metadata = {
        "source_url": url,
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "status_code": response.status_code,
        "file_name": filename,
        "sha256": file_hash
    }

    metadata_path = output_folder / "metadata.json"
    metadata_path.write_text(
        json.dumps(metadata, indent=4),
        encoding="utf-8"
    )

    print("NSP data downloaded successfully!")
    print("Saved file:", file_path)

except requests.RequestException as error:
    print("Website request failed:", error)

except Exception as error:
    print("Error:", error)
