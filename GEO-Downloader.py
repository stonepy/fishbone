""" Download GEO Data Set Accroding to GSE ID(s) | GEO Dowloader | 2018-10-24 Hwx """


import os
import sys
import time
import argparse
import importlib

import subprocess as sp
import multiprocessing as mp


# Default Configures
config = {
    "core" : 4,
    "base_url" : "https://www.ncbi.nlm.nih.gov/geo/download/?acc="
}

# Module List
module_list = [
    "urllib",
    "bs4",
    "wget"
]

# Check Modules That Will Be Used, Install Them When Necessary
for mdl in module_list:

    try:
        importlib.import_module(mdl)

    except ModuleNotFoundError as e:
        print("\n**** Warning: %s \n Try to Install This Package ...\n" % e)

        try:
            cmd = ["pip","install", mdl]
            print(" Use Command To Install: %s\n" % " ".join(cmd))
            sp.run(cmd)
            importlib.import_module(mdl)

        except Exception as e:
            sys.exit("\n**** Error: %s \n> Please Install This Package Manually.\n" % e)

# For the Temporary
import urllib
import bs4
import wget



def html_analyzer(url, id):
    """ Get Downlaod Address """

    print("\nStart Analysing %s\n" % url)

    # Retrive Request of HTML
    html_handler = urllib.request.urlopen(url)
    html_text = ""
    for l in html_handler:
        l = l.decode("utf-8")
        html_text += l

    # Convert into BeautifulSoup Object
    soup = bs4.BeautifulSoup(html_text, "lxml")

    # Parse File Download Address
    download_addr_list = []
    for a in soup.find_all("a"):
        href = a.get("href")
        if id in href and href.endswith("soft.gz"):
            download_addr_list.append(href)
        elif id in href and href.endswith("xml.tgz"):
            download_addr_list.append(href)
        elif id in href and href.endswith("series_matrix.txt.gz"):
            download_addr_list.append(href)
        elif id in href and href.endswith("RAW.tar"):
            download_addr_list.append(href)

    return download_addr_list


def downloader(file_url):
    """ Download Data """

    print("\nStart Downloading")
    try:
        file_name = file_url.split("/")[-1]
        file_path = os.path.join(file_name)
        print("\n>>>> Downloading: %s\n  From: %s\n" % (file_name, file_url))
        cmd = ["wget", "-c", file_url]
        sp.call(cmd)

        print("\n<<<< Finished Downlaod: %s\n" % file_name)
    except Exception as e:
        print("\n**** Warning: %s\n" % e)


def arg_parse(config):
    """ Prepare For Core Function """

    description = "Description:\n    This program is used to download GEO data from NCBI. Default mode will download '*.soft.gz', '*.xml.tgz', '*_series_matrix.txt.gz' and '*_RAW.tar' files. NOTE: It was only tested in 'Python3.6/Ubuntu 18.04.1 LTS' environment."

    # Get GSE ID From Command Line
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("GSE_ID", help="One or more GSE ID, seperated by comma.")

    # **** These Arguments Are Not Available Now {{{ ****
    parser.add_argument("--output", help="The path to the folder you want to store download files.")

    parser.add_argument("--config", help="Use config file instead of command line arguments input.")

    parser.add_argument("--matrix", help="GSExxx_series_matrix.txt.gz or GSExxx-GPLxxx_series_matrix.txt.gz gzipped Series-matrix files Series_matrix files are summary text files that include a tab-delimited value-matrix table generated from the 'VALUE' column of each Sample record, headed by Sample and Series metadata. These files include SOFT attribute labels. Data generated from multiple Platforms are contained in separate files. It is recommended to view Series_matrix files in a spreadsheet application like Excel. CAUTION: value data are extracted directly from the original records with no consideration as to whether the values are directly comparable.")

    parser.add_argument("--miniml", help="GSExxx_family.xml.tgz tarred gzipped MINiML files by Series (GSE) GSExxx_family files contain MINiML-formatted data for all Platforms (GPL) and Samples (GSM) associated with one Series (GSE).")

    parser.add_argument("--soft", help="GSExxx_family.soft.gz gzipped SOFT files by Series (GSE) GSExxx_family files contain SOFT-formatted data for all Platforms (GPL) and Samples (GSM) associated with one Series (GSE).")

    parser.add_argument("--suppl", help="GSExxx_RAW.tar tarred files for all Sample supplementary files corresponding to a Series, as well as any additional files the submitter wants make available. All submitters have been asked to provide supplementary data (for example, Affymetrix .CEL files or cDNA array .GPR files) to accompany their GEO records.  If you are unable to locate supplementary data for your experiment of interest, we suggest that you contact the submitter directly to encourage that they supply raw data files to GEO so that we may make them available to the scientific community. If you are interested in locating all instances of a particular file type, we suggest that you use Entrez GEO DataSets at http://www.ncbi.nlm.nih.gov/gds/.  For example, to locate all .cel files corresponding to Affymetrix HG-U133A array that has GEO accession GPL96, search with: GPL96 AND 'cel'[Supplementary Files]")

    # **** These Arguments Are Not Available Now }}} ****

    parser.add_argument("--core", help="The number of core will be used.")
    print("\n    Example:\n        python geo_downloader.py GSE21653,GSE21652\n")
    args = parser.parse_args()

    # Get ID(s)
    id = args.GSE_ID
    try:
        id_list = id.split(",")
        for id in id_list:
            if "gse" not in id.lower():
                sys.exit("\n**** Please Check Your IDs.  ==> '%s' Is Not A Valid ID \n" % id)
    except:
        sys.exit("\n**** Please Check Your IDs.  ==>  Must Seperate With Comma\n")

    # Get Output Folder
    try:
        output_dir = args.output
    except:
        output_dir = "."

    # Add Arguments to Variable Conifg
    config["id_list"]    = id_list
    config["output_dir"] = output_dir

    return config


def main(config):
    """ Main Workflow """

    arg_parse(config)

    # Manage Parse Download URL From HTML and Download Data
    # Get Download URL
    data_url_list = []
    for id in config["id_list"]:
        url = config["base_url"] + id
        for data_url in html_analyzer(url, id):
            data_url_list.append(data_url)
        time.sleep(0.5)

    # Start Downloading
    p =  mp.Pool(config["core"])
    try:
        p.map(downloader, data_url_list)

    except Exception as e:
        sys.exit("\n**** %s\n" % e)

    print("\n==== Finished Downloading Completely! ====\n")


main(config)
