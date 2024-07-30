import base64
import os
import requests

from openai import OpenAI
from pdf2image import convert_from_path
from langchain.schema import Document


class GPTParser:
    """
    This class uses OpenAI's GPT-4o mini model to parse PDFs and extract text, images and equations.
    It is the most advanced parser in the system and is able to handle complex formats and layouts
    """

    def __init__(self):
        self.client = OpenAI()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.prompt = """
         The provided documents are images of PDFs of lecture slides of deep learning material.
         They contain LaTeX equations, images, and text. 
         The goal is to extract the text, images and equations from the slides and convert everything to markdown format. Some of the equations may be complicated.
         The markdown should be clean and easy to read, and any math equation should be converted to LaTeX, between $$. 
         For images, give a description and if you can, a source. Separate each page with '---'.
         Just respond with the markdown.
         """

    def parse(self, pdf_path):
        images = convert_from_path(pdf_path)
        for i, image in enumerate(images):
            image.save(f'output/images/page{i}.jpg', 'JPEG')

        encoded_images = [self.encode_image(
            f'output/images/page{im}.jpg') for im in range(len(images))]

        chunks = [encoded_images[i:i + 5] for i in range(0, len(encoded_images), 5)]

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        output = ""
        for chunk_num, chunk in enumerate(chunks):
            print(f"Processing chunk {chunk_num + 1}/{len(chunks)})")

            content = [{"type": "image_url", "image_url": {
                "url": f"data:image/jpeg;base64,{image}"}} for image in chunk]

            content.insert(0, {"type": "text", "text": self.prompt})

            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "user",
                        "content": content
                    }
                ],
            }

            response = requests.post(
                "https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

            resp = response.json()
            print("Response", resp)

            chunk_output = resp['choices'][0]['message']['content']

            output += chunk_output + "\n---\n"

        output = output.split("\n---\n")

        documents = [
            Document(
                page_content=page,
                metadata={"source": pdf_path, "page": i}
            ) for i, page in enumerate(output)
        ]
        return documents

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
