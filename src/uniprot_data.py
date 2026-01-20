import requests
import os


def fetch_mouse_brain_data():
    """Returns TSV string for reviewed mouse brain proteins."""
    # 10090: Mus musculus (Mouse): https://www.uniprot.org/taxonomy/10090
    # reviewed means manually annotated
    query = "taxonomy_id:10090 AND tissue:brain AND reviewed:true"
    fields = "accession,id,protein_name,go_p,go_c,go_f"
    return get_uniprot_data(query, fields)


URL = "https://rest.uniprot.org/uniprotkb/search"


def get_uniprot_data(query, fields):
    """Fetches data from UniProt and returns raw TSV string."""
    params = {
        "query": query,
        "fields": fields,
        "format": "tsv",
        "size": 500  # Number of records per request
    }

    response = requests.get(URL, params=params)
    response.raise_for_status()

    tsv_content = response.text

    # Simple pagination loop
    while 'next' in response.links:
        response = requests.get(response.links['next']['url'])
        response.raise_for_status()
        # Skip the header row for subsequent batches
        lines = response.text.splitlines()
        if len(lines) > 1:
            tsv_content += "\n" + "\n".join(lines[1:])

    return tsv_content


if __name__ == "__main__":
    print("Fetching data from UniProt...")
    tsv_data = fetch_mouse_brain_data()

    output_path = "../data/uniprot_mouse_brain.tsv"

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(tsv_data)

    print(f"Success! Data saved.")
