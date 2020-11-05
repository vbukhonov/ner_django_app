import datetime
import json
from xml.etree import ElementTree
from zipfile import ZipFile

from django.conf import settings
from spacy.lang.en import English

nlp = English()


def process_archive(path, mongodb):
    with ZipFile(path, 'r') as patents_zip:
        for name in patents_zip.namelist():
            with patents_zip.open(name) as patent_xml_file:
                application_document_id, year, title, abstract, description = (
                    process_xml_patent(patent_xml_file.read())
                )
                # Run NER over abstract and
                abstract_and_description = "{}\n{}".format(abstract,
                                                           description)
                ners_as_json = perform_ner(abstract_and_description)
                
                # Persist everything in MongoDB.
                mongodb.patents.insert_one(
                    {
                        "application_document_id": application_document_id,
                        "year": year,
                        "title": title,
                        "abstract": abstract,
                        "ners_as_json": json.dumps(ners_as_json)
                    }
                )
                if settings.DEBUG:
                    print("Processed patent {} from file {}.".format(name, path))


def process_xml_patent(patent_as_xml_string):
    root = ElementTree.fromstring(patent_as_xml_string)
    # Collect metadata from bibliographic data.
    application_document_id = ""
    title = ""
    year = datetime.datetime.now().year
    bibliographic_data = root.find("bibliographic-data")
    if bibliographic_data is not None:
        # Get the application data.
        # Save only document id which is in questel format.
        if bibliographic_data.find("application-reference") is not None:
            for item in bibliographic_data.find("application-reference").findall("document-id"):
                try:
                    if item.attrib["data-format"] == "questel":
                        application_document_id = (
                            item.find("doc-number").text if item.find("doc-number").text
                            else ""
                        )
                except Exception:
                    pass
        # Get the year when the patent was produced.
        try:
            year = int(root.attrib['date-produced'][:-4])
        except Exception:
            year = datetime.datetime.now().year
        
        # Get the title.
        if bibliographic_data.find("invention-title") is not None:
            title = bibliographic_data.find("invention-title").text
    
    # Collect abstract.
    abstract_element = root.find("abstract")
    abstract_data_list = []
    if abstract_element is not None:
        for p_item in abstract_element.findall("p"):
            abstract_data_list.append(p_item.text.replace("<br/>", "\n"))
    abstract = "\n".join(abstract_data_list)
    
    # Collect description.
    description_element = root.find("description")
    description_data_list = []
    if description_element is not None:
        for child in description_element:
            description_data_list.append(child.text)
    description = "\n".join(description_data_list)

    return application_document_id, year, title, abstract, description


def perform_ner(input_text):
    doc = nlp(input_text)
    return doc.to_json()
