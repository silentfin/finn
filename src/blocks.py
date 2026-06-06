import re
from enum import Enum
from logging import makeLogRecord
from sys import flags


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    return list(data.strip() for data in markdown.split("\n\n") if data.strip())


def block_to_block_type(markdown_block) -> BlockType:
    if re.findall(r"^(#{1,6} )", markdown_block):
        return BlockType.HEADING
    elif re.findall(r"^```\n[\s\S]*\n```$", markdown_block, flags=re.DOTALL):
        return BlockType.CODE
    elif all(re.findall(r"^> ?", block) for block in markdown_block.split("\n")):
        return BlockType.QUOTE
    elif all(re.findall(r"^- ", block) for block in markdown_block.split("\n")):
        return BlockType.UNORDERED_LIST
    elif all(
        block.startswith(f"{index + 1}. ")
        for index, block in enumerate(markdown_block.split("\n"))
    ):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
