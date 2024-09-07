from bs4 import BeautifulSoup
from ebooklib import epub
import markdown
import os

from .input_format import InputFormat

class Md(InputFormat):
    def to_epub(self, output_file):
        title = os.path.splitext(os.path.basename(self.input_path))[0]
        with open(self.input_path, 'r', encoding='utf-8') as file:
            markdown_content = file.read()
        chapter_content = markdown.markdown(markdown_content)
        (book, identifier) = self.make_epub(title, [chapter_content])
        epub.write_epub(output_file, book, {})
        return identifier