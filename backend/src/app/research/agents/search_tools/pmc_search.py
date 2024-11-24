import requests
import bs4 as bs

class PubMedSearcher:
    def __init__(self, query, max_results=10):
        self.ops_pmc = []
        self.max_results = max_results
    def get_results(self, query):
      url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
      params = {
          "query": query,
          "format": "json",
          "pageSize": self.max_results
      }
      response = requests.get(url, params=params)
      data = response.json()
      return self.get_cleaned_data(data)
    def get_cleaned_data(self, data):
      for result in data["resultList"]["result"]:
        if result["isOpenAccess"] == "Y":
          doi = result["doi"]
          pmcid = result["pmcid"]
          content_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/{f}/fullTextXML".format(f=pmcid)
          url_ref = "https://www.ebi.ac.uk/europepmc/webservices/rest/{source}/{id}/references?format=json".format(source=result["source"],id=result["id"])
          references = requests.get(url_ref).json()
          references_list = []
          for elem in references["referenceList"]["reference"]:
            references_list.append({
                "title": elem["title"],
                "author": elem["authorString"],
                "year": elem["pubYear"],
                "journal":elem["journalAbbreviation"]
            })
          response = requests.get(content_url)
          content_xml = bs.BeautifulSoup(response.text, 'lxml')
          authors = result["authorString"].split(", ")
          self.ops_pmc.append({"id": doi,
                            "title":result["title"],
                            "author": authors,
                            "summary": content_xml.find('abstract').get_text(),
                            "year": result["pubYear"],
                            "url":"https://doi.org/"+doi,
                            "reference": references_list})
      return self.ops_pmc