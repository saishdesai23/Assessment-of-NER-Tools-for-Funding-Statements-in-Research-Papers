import pandas as pd
import numpy as np
import os
import lxml
import csv
from bs4 import BeautifulSoup as bs


def extract_tags(xml_papers) -> list:
    result = []
    art_title, pmc_id, doi, acklge = "", "", "", ""
    fn_count = 0
    count = 0
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
        # Funding Information from acknowledgement <ack> tag
        acklge_ = paper.find("ack")  # attrs
        if acklge_ is None:
            acklge = 'NA'
        else:
            acklge = acklge_.find_all("p").text

        # Funding Information from <title> tag
        title = paper.find_all("title")
        for t in title:
            if t.text == 'Funding':
                funding = t.find_next("p").text
                break
            else:
                funding = 'NA'

        # section = paper.find_all("sec")
        # for sec in section:
        #     print(sec)
        #     if sec.title.text == "Funding":
        #         funding = sec.find("p").text
        #         print(funding)
        #         break
        #     else:
        #         funding = "NA"
                # print(funding)

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
        # acklge = acklge_.text
        # print(len(acklge_))
        # if len(acklge_) == 0:
        #     acklge = "na"
        # else:
        #     acklge = acklge_[0].p.text
        # #     # print(acklge_[0].p.text,'\n')
        result.append([art_title, pmc_id, doi, acklge, funding, fn_statement])
    print(count)
    return result

def save_file(out_filename: str, input_item: list) -> csv:
    """
    It write list output as 'csv' file in the current directory

    :out_filename:   the name that will be give of the output file
    :input_item:   processed data in list.
    """
    with open(out_filename, "w") as s:
        w = csv.writer(s)
        for row in input_item:
            w.writerow(row)

if __name__ == '__main__':
    xml_path = "../data/xml/pmc_result_20210101_20210105.xml"
    input_file = open(xml_path, 'r')
    contents = input_file.read()
    # embedding the XML with beautiful soup module

    soup = bs(contents, 'xml')

    # extracts of the article units
    xml_papers = soup.find_all("article")
    annotated_data = extract_tags(xml_papers)

    # name the processed output file
    out_filename = "../data/ack_data.csv"

    # save the processed file into csv
    save_file(out_filename, annotated_data)