def web_search(query: str, max_results: int = 5) -> str:
    try:
        from ddgs import DDGS
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append(
                    f"- {r.get('title', '')}\n  {r.get('href', '')}\n  {r.get('body', '')}"
                )
        return "\n\n".join(results) if results else "No results found."
    except Exception as e:
        return f"Error performing web search: {e}"
