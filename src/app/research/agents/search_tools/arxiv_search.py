import arxiv

class ArxivSearcher:
    def __init__(self, query, max_results=10, criterion = arxiv.SortCriterion.Relevance):
        self.client = arxiv.Client()
        self.criterion = criterion
        self.ops = []
        self.max_results = max_results
    def get_results(self, query):
      self.search = arxiv.Search(
            query=query,
            max_results = self.max_results,
            sort_by = self.criterion
        )
      results = list(self.client.results(self.search))
      results_values = []
      seen_ids = set()  
      for elem in results:
        content = {}
        content["title"] = elem.title
        content["author"] = list(map(lambda x: x.name,elem.authors))
        content["summary"] = elem.summary
        content["year"] = elem.updated.year
        content["url"] = elem.entry_id
        content["reference"] = []
        if content["url"] in seen_ids:
          continue  # Saltar si ya hemos visto este ID
        else:
          seen_ids.add(content["url"])  # Agregar el ID al conjunto si es nuevo
          results_values.append(content)
      return results_values