from bs4 import BeautifulSoup
import re

def normalize(data:str) -> str:
    """
    Clean and normalize scraped HTML/text:
    - Remove scripts, styles, and hidden tags
    - Collapse whitespace
    - Strip non-textual elements
    - Return a clean readable string
    """

    if not data:
        return ""

    # Parse HTML safely
    soup = BeautifulSoup(data, "html.parser")

    # Remove irrelevant tags
    for tag in soup(["script", "style", "noscript", "iframe", "svg", "meta", "link"]):
        tag.decompose()

    # Remove comments
    for comment in soup.find_all(string=lambda txt: isinstance(txt, (type(soup.comment),))):
        comment.extract()

    # Get visible text
    text = soup.get_text(separator=" ", strip=True)

    # Collapse multiple spaces/newlines into one space
    text = re.sub(r"\s+", " ", text)

    # Remove very short or meaningless lines
    text = re.sub(r"(Accept|cookies|privacy policy|terms of use)[^.]*", "", text, flags=re.I)

    return text.strip()
