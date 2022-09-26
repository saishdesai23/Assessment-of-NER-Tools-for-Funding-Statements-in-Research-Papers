import entrezpy.esearch.esearcher
import entrezpy.efetch.efetcher
import math, json, os, sys

# search articles based on terms and filters
search = entrezpy.esearch.esearcher.Esearcher("entrezpy",
                                         "your_email_here",
                                         apikey="your_api_key_here")
search_analyzer = search.inquire({'db' : 'pmc',
                      'term' : 'open access[filter]',
                      'rettype' : 'count',
                      'datetype' : 'pdat',
                      'mindate' : '2022/01/01',
                      'maxdate' : '2022/01/01'})

print(f'Search resulted in {search_analyzer.result.count} PMIDs')

# retrieve article information
pmids = search_analyzer.result.uids
retmax = 1000 # maximum PMIDs per request 

output_folder = 'pmc_oa'
if not os.path.exists(output_folder):
  os.mkdir(output_folder)

for i in range(math.ceil(len(pmids) / retmax)):
  with open(f'{output_folder}/{(i + 1) * retmax}.xml', 'w') as sys.stdout:
    fetcher = entrezpy.efetch.efetcher.Efetcher("entrezpy",
                                           "your_email_here",
                                         apikey="your_api_key_here")
    fetcher_analyzer = fetcher.inquire({'db' : 'pmc', 'retmode' : 'xml',
                          'id' : pmids[i * retmax : i * retmax + retmax],
                          'usehistory' : False})