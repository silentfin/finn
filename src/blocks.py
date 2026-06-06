def markdown_to_blocks(markdown):
    return list(data.strip() for data in markdown.split("\n\n") if data.strip())
