import arxiv

class ArxivSearcher:
    def __init__(self):
        self.client = arxiv.Client()

    def search(self, query, max_results=1, sort_by="Relevance"):
        # Create search parameters
        search = arxiv.Search(query=query,
                              max_results=max_results,
                              sort_by=arxiv.SortCriterion[sort_by])

        # Execute search and format results
        results = []
        for result in self.client.results(search):
            paper = {
                'title': result.title,
                'authors': [author.name for author in result.authors],
                'abstract': result.summary,
                'published': result.published.strftime("%Y-%m-%d"),
                'updated': result.updated.strftime("%Y-%m-%d"),
                'pdf_url': result.pdf_url,
                'entry_id': result.entry_id,
                'categories': result.primary_category
            }
            results.append(paper)

        return results

    def get_paper_by_id(self, paper_id):
        search = arxiv.Search(id_list=[paper_id])
        try:
            paper = next(self.client.results(search))
            return {
                'title': paper.title,
                'authors': [author.name for author in paper.authors],
                'abstract': paper.summary,
                'pdf_url': paper.pdf_url,
                'entry_id': paper.entry_id
            }
        except StopIteration:
            raise ValueError(f"Paper with ID {paper_id} not found")
