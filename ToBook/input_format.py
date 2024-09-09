from abc import ABC, abstractmethod
from ebooklib import epub
import hashlib
from pathlib import Path
from typing import List, Tuple

class Chapter:
    def __init__(self, title: str, content: str, images: List[Tuple[str, bytes]] = None):
        self.title = title
        self.content = content
        self.images = images or []

class InputFormat(ABC):
    def __init__(self, input_path: str):
        self.input_path = input_path

    def to_epub(self, output_file):
        book = epub.EpubBook()
        book.set_language('en')

        title = self.get_title()
        book.set_title(title)

        chapters = self.get_chapters()
        all_content = "\n".join([chapter.content for chapter in chapters])
        identifier = self.generate_identifier(all_content)
        book.set_identifier(identifier)

        epub_chapters = []
        for i, chapter in enumerate(chapters, start=1):
            chapter_file = f'{chapter.title}.xhtml'
            epub_chapter = epub.EpubHtml(title=chapter.title, file_name=chapter_file, lang='en')
            epub_chapter.content = chapter.content
            book.add_item(epub_chapter)
            epub_chapters.append(epub_chapter)

            for img_filename, img_content in chapter.images:
                img_item = epub.EpubItem(file_name=f"images/{img_filename}", content=img_content, media_type="image/jpeg")
                book.add_item(img_item)

        # Table Of Contents
        book.toc = epub_chapters

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
        book.spine = ["nav"] + epub_chapters

        epub.write_epub(output_file, book, {})
        return identifier

    @staticmethod
    def generate_identifier(content: str) -> str:
        hasher = hashlib.sha256()
        hasher.update(content.encode('utf-8'))
        return 'urn:uuid:' + hasher.hexdigest()

    @abstractmethod
    def get_title(self) -> str:
        pass

    @abstractmethod
    def get_chapters(self) -> List[Chapter]:
        pass