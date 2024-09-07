from abc import ABC, abstractmethod
from ebooklib import epub
import hashlib
from typing import List

class InputFormat(ABC):
    def __init__(self, input_path: str):
        self.input_path = input_path

    def make_epub(self, title: str, chapter_content: List[str]) -> epub.EpubBook:
        all_content = "\n".join(chapter_content)
        identifier = InputFormat.generate_identifier(all_content)
        book = epub.EpubBook()
        book.set_identifier(title)
        book.set_title(title)
        book.set_language('en')

        chapters = []
        for i, content in enumerate(chapter_content, start=1):
            chapter_title = f"Chapter {i}"
            chapter_file = f'{chapter_title}.xhtml'
            chapter = epub.EpubHtml(title=chapter_title, file_name=chapter_file, lang='en')
            chapter.content = content
            book.add_item(chapter)
            chapters.append(chapter)

        # Table Of Contents
        book.toc = chapters

        # Add default NCX and Nav file
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # Define CSS style
        style = '''
        body { font-family: Arial, sans-serif; }
        h1 { color: #333; font-size: 2em; }
        p { line-height: 1.6; }
        '''
        nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
        book.add_item(nav_css)

        # Basic spine
        book.spine = ["nav"] + chapters

        return (book, identifier)

    @staticmethod
    def generate_identifier(content: str) -> str:
        hasher = hashlib.sha256()
        hasher.update(content.encode('utf-8'))
        return 'urn:uuid:' + hasher.hexdigest()

    @abstractmethod
    def to_epub(self, output_file):
        pass
    
