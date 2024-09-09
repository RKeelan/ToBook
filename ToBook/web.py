from bs4 import BeautifulSoup
import click
import json
import os
import requests
from typing import List
import uuid

from .input_format import InputFormat, Chapter

class Web(InputFormat):
    def get_title(self) -> str:
        return os.path.splitext(os.path.basename(self.input_path))[0]

    def get_chapters(self) -> List[Chapter]:
        with open(self.input_path, 'r') as file:
            urls = json.load(file)

        if not isinstance(urls, list):
            raise ValueError("The JSON file should contain a list of URLs")

        chapters = []
        for i, url in enumerate(urls, start=1):  # Consider removing the slice in production
            content, images = self.fetch_content_and_images(url)
            chapters.append(Chapter(title=f"Chapter {i}", content=content, images=images))
        return chapters

    def fetch_content_and_images(self, url: str) -> tuple[str, List[tuple[str, bytes]]]:
        response = requests.get(url)
        if response.status_code != 200:
            raise click.ClickException(f"Failed to retrieve content from {url}")

        soup = BeautifulSoup(response.text, 'html.parser')
        article = soup.find('article')
        if not article:
            raise click.ClickException(f"No <article> tag found in {url}")

        images = []
        for img in article.find_all('img'):
            img_url = img.get('src')
            img_content = self.fetch_image(img_url)
            img_filename = f"image_{uuid.uuid4().hex}.jpg"
            images.append((img_filename, img_content))
            img['src'] = f"images/{img_filename}"

        return str(article), images

    def fetch_image(self, img_url: str) -> bytes:
        try:
            response = requests.get(img_url)
            if response.status_code == 200:
                return response.content
        except Exception as e:
            print(f"Failed to fetch image from {img_url}: {str(e)}")
        return b''
