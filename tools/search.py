from ddgs import DDGS


class SearchTool:

    def search(self, query, max_results=5):

        try:

            with DDGS() as ddgs:

                results = list(
                    ddgs.text(
                        query,
                        max_results=max_results
                    )
                )

            return results

        except Exception as e:

            print("Search Error:", e)

            return []


search_tool = SearchTool()