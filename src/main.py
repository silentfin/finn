from textnode import TextNode, TextType


def main():
    md = TextNode("Cool search engine", TextType.LINK, "https://noai.duckduckgo.com/")
    print(md)


if __name__ == "__main__":
    main()
