import pandas as pd
import numpy as np
import os
import lxml
import csv
from bs4 import BeautifulSoup as bs


def extract_tags(xml_papers) -> list:
    result = []
    art_title, pmc_id, doi, acklge = "", "", "", ""
    ack_count = 0
    for paper in xml_papers:
        art_title = paper.find_all('article-title')[0].text
        # print(art_title)

        # getting pmc & doi
        meta = paper.find_all("article-meta")
        art_ids = meta[0].find_all("article-id")

        for ids in art_ids:
            id = ids.attrs

            if id['pub-id-type'] == 'pmc':
                pmc_id = ids.text
                # print(ids.text)

            if id['pub-id-type'] == 'doi':
                doi = ids.text
                # print(doi)
            else:
                doi = 'na'

        print(pmc_id)
        # Funding Information from acknowledgement <ack> tag
        ack_tag = paper.find_all("ack")  # attrs
        print(ack_tag)
        if len(ack_tag) == 0:
            acklge = 'NA'
        else:
            ack_count += 1
            for tag in ack_tag:
                print(tag)
                if tag.find_next().name == 'p':
                    acklge = tag.find_next("p").text
                    break
                else:
                    acklge = 'NA'
        print(acklge)
        # Funding Information from <title> tag
        title = paper.find_all("title")
        for t in title:
            if t.text == 'Funding':
                funding = t.find_next("p").text
                break
            else:
                funding = 'NA'

        # Acknowledgement Information from <title> tag
        title = paper.find_all("title")
        for t in title:
            if t.text.lower() == 'acknowledgments':
                acknowledgement = t.find_next("p").text
                break
            else:
                acknowledgement = 'NA'

        # Funding Information from the footnotes section
        fn = paper.find("fn-group")  # attrs
        if fn is None:
            fn_statement = "NA"
        else:
            temp = fn.find("fn", {"fn-type": "supported-by"})
            if temp is None:
                fn_statement = "NA"
            else:
                fn_statement = temp.text

        result.append([art_title, pmc_id, doi, acklge, acknowledgement, funding, fn_statement])
    print(result)
    funding_dataframe = pd.DataFrame(result)
    funding_dataframe.columns = ['Article_Title', 'PMC_ID', 'DOI', 'ACK', 'ACKNOWLEDGEMENT', 'FUNDING', 'FOOTNOTES']
    funding_dataframe = funding_dataframe.set_index(['Article_Title'])

    print(ack_count)
    print(funding_dataframe)
    return funding_dataframe
def save_file(out_filename: str, dataframe) -> csv:
    """
    It writes list output as 'csv' file in the current directory

    :out_filename:   the name that will be give of the output file
    :input_item:   processed data in list.
    """
    dataframe.to_csv(out_filename)

if __name__ == '__main__':
    xml_path = "../data/xml"
    xml_files = os.listdir(xml_path)
    xml_files = [ele for ele in xml_files if ele.split("_")[0] == "pmc"]

    for ele in xml_files:
        print(os.path.join(xml_path, ele))
        print(ele.split("_")[-1])
        input_file = open(os.path.join(xml_path, ele), 'r')
        contents = input_file.read()

        # embedding the XML with beautiful soup module

        soup = bs(contents, 'xml')

        # extracts of the article units
        xml_papers = soup.find_all("article")
        annotated_dataframe = extract_tags(xml_papers)

        # name the processed output file
        out_filename = "../data/ack_data" + ele.split("_")[-1] + ".csv"

        # save the processed file into csv
        save_file(out_filename, annotated_dataframe)