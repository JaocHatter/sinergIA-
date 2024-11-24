import requests

class PlosSearcher:
  def __init__(self, max_results=10):
    self.ops_plos = []
  def get_results(self, query):
    # The query is the URL
    plos_response = requests.get(query, headers = {"User-Agent":"Research Budy"})
    docs_ = plos_response.json()['response']['docs']
    return self.get_cleaned_data(docs_)
  def get_cleaned_data(self, docs_):
    for elem in docs_:
      content = {}
      content["id"] = elem["id"] # doi
      content["title"] = elem["title"]
      content["author"] = elem["author"]
      content["summary"] = elem["abstract"][0]
      content["year"] = elem["publication_date"][:4]
      content["url"] = "https://doi.org/"+elem["id"]
      cleaned_data = [item for item in elem["reference"] if item.strip() != '|  |  |']
      #references
      for idx,paper in enumerate(cleaned_data):
        parts = paper.split('|')
        authors = [author.strip() for author in parts[0].replace("\n", "").split(",") if author.strip()]
        year = parts[1].strip() if len(parts) > 1 else None
        title = parts[2].strip() if len(parts) > 2 else None
        topic = parts[3].strip() if len(parts) > 3 else None
        if title == "":
          title = topic
        paper_dict = {
            'title': title,
            'author': authors,
            'year': year,
            'journal': topic
        }
        cleaned_data[idx] = paper_dict
      content["reference"] = cleaned_data
      self.ops_plos.append(content)
    return self.ops_plos
