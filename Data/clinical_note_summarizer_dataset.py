# -*- coding: utf-8 -*-
"""Clinical note summarizer dataset.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VgySdhJD-LR0h1BEpA1WHZffaJg5WPZL
"""

# Commented out IPython magic to ensure Python compatibility.
# %cd data-for-clinical-note-summarizer

!wget ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/oa_noncomm/xml/oa_noncomm_xml.PMC001xxxxxx.baseline.2024-06-18.tar.gz
!wget ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/oa_noncomm/xml/oa_noncomm_xml.PMC002xxxxxx.baseline.2024-06-18.tar.gz
!wget ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/oa_noncomm/xml/oa_noncomm_xml.PMC003xxxxxx.baseline.2024-06-18.tar.gz

from google.colab import drive
drive.mount('/content/drive')

!cp -r /content/data-for-clinical-note-summarizer /content/drive/MyDrive/data-for-clinical-note-summarizer/

!mkdir /content/drive/MyDrive/data-for-clinical-note-summarizer

!mkdir extracted_xml_files
!tar -xzvf /content/data-for-clinical-note-summarizer/oa_noncomm_xml.PMC001xxxxxx.baseline.2024-06-18.tar.gz -C extracted_xml_files
!tar -xzvf /content/data-for-clinical-note-summarizer/oa_noncomm_xml.PMC002xxxxxx.baseline.2024-06-18.tar.gz -C extracted_xml_files
!tar -xzvf /content/data-for-clinical-note-summarizer/oa_noncomm_xml.PMC003xxxxxx.baseline.2024-06-18.tar.gz -C extracted_xml_files

!sudo apt-get install -y libxml2-utils

!xmllint --format /content/data-for-clinical-note-summarizer/extracted_xml_files/PMC001xxxxxx/PMC1193645.xml

import xml.etree.ElementTree as ET

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root

root = parse_xml('/content/data-for-clinical-note-summarizer/extracted_xml_files/PMC001xxxxxx/PMC1193645.xml')

def collect_tags(element, tags_set):
    tags_set.add(element.tag)
    for child in element:
        collect_tags(child, tags_set)

tags_set = set()
collect_tags(root, tags_set)

unique_tags = list(tags_set)

print("Unique Tags in the XML File:")
for tag in unique_tags:
    print(tag)

import xml.etree.ElementTree as ET
import json

def parse_xml(file_path):
    """
    Parse the XML file and return its root element.
    """
    tree = ET.parse(file_path)
    return tree.getroot()

def extract_metadata(root):
    """
    Extract metadata such as journal information, article title, subtitle, authors, correspondence,
    publication date, volume, issue, pages, DOI, keywords, and abbreviations.
    """
    metadata = {
        "journal_title": root.findtext(".//journal-title", default="").strip(),
        "issns": {
            "print": root.findtext(".//issn[@pub-type='ppub']", default="").strip(),
            "online": root.findtext(".//issn[@pub-type='epub']", default="").strip()
        },
        "publisher": root.findtext(".//publisher-name", default="").strip(),
        "article_title": root.findtext(".//article-title", default="").strip(),
        "subtitle": root.findtext(".//subtitle", default="").strip(),
        "authors": [],
        "correspondence": [],
        "publication_date": root.findtext(".//pub-date/year", default="").strip(),
        "volume": root.findtext(".//volume", default="").strip(),
        "issue": root.findtext(".//issue", default="").strip(),
        "pages": root.findtext(".//fpage", default="").strip() + "-" + root.findtext(".//lpage", default="").strip(),
        "doi": root.findtext(".//article-id[@pub-id-type='doi']", default="").strip(),
        "abstract": [],
        "keywords": [],
        "abbreviations": []
    }

    # Extract authors
    for contrib in root.findall(".//contrib[@contrib-type='author']"):
        surname = contrib.findtext(".//surname", default="").strip()
        given_names = contrib.findtext(".//given-names", default="").strip()
        if surname or given_names:
            metadata["authors"].append(f"{given_names} {surname}".strip())

    # Extract correspondence
    for corr in root.findall(".//address/email"):
        metadata["correspondence"].append(corr.text.strip())

    # Extract abstract
    for abstract in root.findall(".//abstract"):
        metadata["abstract"].append(" ".join(abstract.itertext()).strip())

    # Extract keywords
    for kwd in root.findall(".//kwd"):
        metadata["keywords"].append(kwd.text.strip())

    # Extract abbreviations
    for abbrev in root.findall(".//abbrev"):
        metadata["abbreviations"].append(abbrev.text.strip())

    return metadata

def extract_sections(root):
    """
    Recursively extract sections, including titles, paragraphs, figures, tables, lists, and subsections.
    """
    def parse_section(section):
        section_data = {
            "title": section.findtext("title", default="").strip(),
            "paragraphs": [" ".join(p.itertext()).strip() for p in section.findall("p")],
            "figures": [],
            "tables": [],
            "lists": [],
            "subsections": []
        }

        # Extract figures
        for fig in section.findall("fig"):
            caption = " ".join(fig.find("caption").itertext()).strip() if fig.find("caption") else ""
            section_data["figures"].append({"caption": caption})

        # Extract tables
        for table in section.findall("table-wrap"):
            caption = " ".join(table.find("caption").itertext()).strip() if table.find("caption") else ""
            section_data["tables"].append({"caption": caption})

        # Extract lists
        for list_element in section.findall("list"):
            list_items = [item.text.strip() for item in list_element.findall("list-item") if item.text]
            section_data["lists"].append(list_items)

        # Recursively extract subsections
        for subsection in section.findall("sec"):
            section_data["subsections"].append(parse_section(subsection))

        return section_data

    sections = []
    for top_section in root.findall(".//sec"):
        sections.append(parse_section(top_section))
    return sections

def extract_references(root):
    """
    Extract references from the article, including titles and other metadata.
    """
    references = []
    for ref in root.findall(".//ref"):
        ref_data = {
            "title": ref.findtext(".//article-title", default="").strip(),
            "authors": [],
            "journal": ref.findtext(".//source", default="").strip(),
            "year": ref.findtext(".//year", default="").strip()
        }

        # Extract authors in reference
        for person in ref.findall(".//name"):
            surname = person.findtext("surname", default="").strip()
            given_names = person.findtext("given-names", default="").strip()
            if surname or given_names:
                ref_data["authors"].append(f"{given_names} {surname}".strip())

        references.append(ref_data)

    return references

def extract_full_article(file_path):
    """
    Extract the complete article data, including metadata, sections, and references.
    """
    root = parse_xml(file_path)
    data = extract_metadata(root)
    data["sections"] = extract_sections(root)
    data["references"] = extract_references(root)
    return data

def save_to_json(data, output_file):
    """
    Save extracted data to a JSON file.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # Input XML file path
    xml_file = "/content/data-for-clinical-note-summarizer/extracted_xml_files/PMC001xxxxxx/PMC1474074.xml"  # Replace with your XML file path
    output_file = "output.json"        # Output JSON file

    # Extract data and save to JSON
    article_data = extract_full_article(xml_file)
    save_to_json(article_data, output_file)

    print(f"Extraction complete. Data saved to {output_file}.")

import os
import csv
import xml.etree.ElementTree as ET

def parse_xml(file_path):
    """
    Parse the XML file and return its root element.
    """
    tree = ET.parse(file_path)
    return tree.getroot()

def extract_metadata(root):
    """
    Extract metadata such as journal information, article title, abstract, keywords, and publication details.
    """
    metadata = {
        "journal_title": root.findtext(".//journal-title", default="").strip(),
        "article_title": root.findtext(".//article-title", default="").strip(),
        "authors": "; ".join(
            f"{author.findtext('.//given-names', default='').strip()} {author.findtext('.//surname', default='').strip()}"
            for author in root.findall(".//contrib[@contrib-type='author']")
        ),
        "publication_date": root.findtext(".//pub-date/year", default="").strip(),
        "doi": root.findtext(".//article-id[@pub-id-type='doi']", default="").strip(),
    }

    # Extract abstract - fix for joining all text
    abstract = root.find(".//abstract")
    if abstract is not None:
        metadata["abstract"] = " ".join(abstract.itertext()).strip()
    else:
        metadata["abstract"] = ""

    # Extract keywords
    metadata["keywords"] = "; ".join([kwd.text.strip() for kwd in root.findall(".//kwd")])

    return metadata

def extract_sections(root):
    """
    Extract content (paragraphs, figures, tables) for each section and return as strings.
    """
    sections_content = {
        "paragraphs": "",
        "figures": "",
        "tables": "",
        "lists": "",
    }

    def parse_section(section, parent_title=""):
        section_title = section.findtext("title", default="").strip()
        full_title = f"{parent_title} > {section_title}" if parent_title else section_title

        # Append paragraphs
        for paragraph in section.findall("p"):
            sections_content["paragraphs"] += " ".join(paragraph.itertext()).strip() + " "

        # Append figures
        for figure in section.findall("fig"):
            caption = figure.find("caption")
            if caption is not None:
                sections_content["figures"] += " ".join(caption.itertext()).strip() + " "

        # Append tables
        for table in section.findall("table-wrap"):
            caption = table.find("caption")
            if caption is not None:
                sections_content["tables"] += " ".join(caption.itertext()).strip() + " "

        # Recursively process subsections
        for subsection in section.findall("sec"):
            parse_section(subsection, parent_title=full_title)

    # Start processing top-level sections
    for top_section in root.findall(".//sec"):
        parse_section(top_section)

    return sections_content

def process_folder(input_folder, output_csv):
    """
    Process all XML files in a folder and save the extracted data to a CSV file.
    """
    # CSV header: Metadata fields + content fields for sections
    csv_header = [
        "journal_title", "article_title", "authors", "publication_date", "doi",
        "abstract", "keywords", "paragraphs", "figures", "tables", "lists"
    ]

    rows = []

    # Process each XML file in the folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".xml"):
            file_path = os.path.join(input_folder, file_name)
            try:
                root = parse_xml(file_path)
                article_metadata = extract_metadata(root)
                sections_content = extract_sections(root)

                # Combine metadata with sections content
                row = {**article_metadata, **sections_content}
                rows.append(row)

            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    # Write all data to CSV
    with open(output_csv, mode="w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_header)
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    # Folder containing XML files
    input_folder = "/content/extracted_xml_files/PMC002xxxxxx"  # Replace with your folder path
    output_csv = "final_output.csv"  # Output CSV file

    # Process all files and save to CSV
    process_folder(input_folder, output_csv)
    print(f"Extraction complete. Data saved to {output_csv}.")

import pandas as pd
csv2 = pd.read_csv("/content/data-for-clinical-note-summarizer/detailed_output.csv")

csv2.head(10)

import pandas as pd
csv = pd.read_csv("/content/data-for-clinical-note-summarizer/final_output.csv")

csv.head(10)

import pandas as pd

# Select only the 'abstract' and 'paragraphs' columns
df_filtered = csv[['abstract', 'paragraphs']]

# Save the filtered dataframe to a new CSV or any other format
df_filtered.to_csv('filtered_data1.csv', index=False)

# Display the first few rows of the filtered data to verify

df_filtered.head()

import csv


def append_csv_files(file1, file2, output_file):
    # Increase the field size limit
    csv.field_size_limit(100000000)  # Set to a large value, e.g., 100 MB

    # Open the first file and read its contents
    with open(file1, mode='r', newline='') as f1:
        reader1 = csv.reader(f1)
        data1 = list(reader1)

    # Open the second file and read its contents
    with open(file2, mode='r', newline='') as f2:
        reader2 = csv.reader(f2)
        data2 = list(reader2)

    # Open the output file and write the combined contents
    with open(output_file, mode='w', newline='') as f_out:
        writer = csv.writer(f_out)
        # Write the header from the first file
        writer.writerow(data1[0])
        # Write the data from the first file (excluding the header)
        writer.writerows(data1[1:])
        # Write the data from the second file (excluding the header)
        writer.writerows(data2[1:])
# Example usage
file1 = '/content/data-for-clinical-note-summarizer/filtered_data.csv'
file2 = '/content/data-for-clinical-note-summarizer/filtered_data1.csv'
output_file = 'combined_output.csv'
append_csv_files(file1, file2, output_file)

x = pd.read_csv('/content/data-for-clinical-note-summarizer/combined_output.csv')

x.head()