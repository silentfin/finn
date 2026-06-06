import sys

from website import copy_files, generate_pages_recursive


def main():
    if len(sys.argv) > 1:
        print(sys.argv)
        basepath = sys.argv[1]
    else:
        basepath = "/"
    copy_files("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
