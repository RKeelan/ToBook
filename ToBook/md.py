from bs4 import BeautifulSoup
import markdown
import os
from typing import List

from .input_format import InputFormat, Chapter

class Md(InputFormat):
    def get_title(self) -> str:
        return os.path.splitext(os.path.basename(self.input_path))[0]

    def get_chapters(self) -> List[Chapter]:
        with open(self.input_path, 'r', encoding='utf-8') as file:
            markdown_content = file.read()
        chapter_content = markdown.markdown(markdown_content)
        return [Chapter(title="Chapter 1", content=chapter_content)]  # No images for markdown files