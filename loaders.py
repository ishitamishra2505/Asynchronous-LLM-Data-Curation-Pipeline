from abc import ABC, abstractmethod
from typing import List

import pymupdf  # This is a super-fast Python library called PyMuPDF
import asyncio
from pathlib import Path

# We need to bring in the ID cards we just made in models.py!
from models import Document, DocumentType

class BaseLoader(ABC):
    def __init__(self):
        # A blank list for now. Later, our specialists will fill this with "pdf" or "txt".
        self.supported_formats: List[DocumentType] = []

    @abstractmethod
    async def load_single(self, source: str, **kwargs) -> Document:
        # The 'pass' means "I don't do the work here, the specialists will do it later."
        pass


class PDFLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        # This specialist holds up a sign saying: "I only handle PDFs!"
        self.supported_formats = [DocumentType.PDF]

    async def load_single(self, source: str, **kwargs) -> Document:
        file_path = Path(source)
        
        # Step 1: Check if the file actually exists on your laptop
        if not file_path.exists():
            raise FileNotFoundError(f"Oops! Could not find {source}")
            
        # Step 2: Extract the text 
        content = await self._extract_pdf_text(file_path)
        
        # Step 3: Pack it perfectly into the Document box we made earlier!
        return Document(
            title=file_path.stem,  # Grabs the file name without the .pdf extension
            content=content,
            source=str(file_path),
            doc_type=DocumentType.PDF,
            word_count=len(content.split()),
            char_count=len(content)
        )


async def _extract_pdf_text(self, path: Path) -> str:
        # We put the heavy reading in a background task so it doesn't block our fast highway
        def _read_pages():
            doc = pymupdf.open(path)  # Open the PDF book
            text_parts = []
            
            # Loop through it page by page.
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text = page.get_text()
                
                # Only save the page if it actually has text on it
                if text.strip():
                    text_parts.append(f"Page {page_num + 1}:\n{text}")
                    
            doc.close()
            return "\n\n".join(text_parts) # Glue all the pages together with spacing
            
        # This tells Python: "Go run this heavy reading in the background"
        return await asyncio.to_thread(_read_pages)


class DocumentLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        # This worker holds a sign with a bunch of different text formats!
        self.supported_formats = [
            DocumentType.TXT, 
            DocumentType.MD,
            DocumentType.CSV
        ]

    async def load_single(self, source: str, **kwargs) -> Document:
        file_path = Path(source)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Oops! Could not find {source}")
            
        # For plain text files, reading is super easy and fast
        # We still push it to a background thread just in case it's a massive file
        content = await asyncio.to_thread(file_path.read_text, encoding="utf-8")
        
        # Grab the extension so we know what type to put on the ID card
        extension = file_path.suffix.lower().strip('.')
        doc_type = DocumentType(extension)
        
        return Document(
            title=file_path.stem,
            content=content,
            source=str(file_path),
            doc_type=doc_type,
            word_count=len(content.split()),
            char_count=len(content)
        )


class UnifiedLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        # The boss hires our specialists!
        self.pdf_loader = PDFLoader()

        self.doc_loader = DocumentLoader()
        # (We will add the text and web loaders here later!)
        
        # The boss holds a sign saying: "I accept ALL formats!"
        self.supported_formats = list(DocumentType)

    async def load_single(self, source: str, **kwargs) -> Document:
        file_path = Path(source)
        
        # Step 1: The Detective Work (grab the extension)
        extension = file_path.suffix.lower().strip('.')
        
        # Step 2: Route traffic to the correct specialist
        if extension == "pdf":
            return await self.pdf_loader.load_single(source)

        elif extension in ["txt", "md", "csv"]:
            return await self.doc_loader.load_single(source)
        
        else:
            # If it's a file type we haven't built a loader for yet:
            raise ValueError(f"Sorry, we don't have a specialist for .{extension} files yet!")

    async def load_directory(self, folder_path: str, max_workers: int = 3) -> list[Document]:
        # Step 1: Set up the bouncer! Only 3 files allowed at once.
        semaphore = asyncio.Semaphore(max_workers)
        
        # This is a mini-function that forces a file to wait for the bouncer's permission
        async def load_with_semaphore(file_path):
            async with semaphore:  # "Excuse me, can I come in?"
                return await self.load_single(str(file_path))
                
        # Step 2: Find all the files in the folder (let's pretend we have a list of them)
        folder = Path(folder_path)
        all_files = [f for f in folder.glob("*.*") if f.is_file()]
        
        # Step 3: Tell all the files to go line up at the bouncer's door
        tasks = [load_with_semaphore(f) for f in all_files]
        
        # Step 4: Fire them all off at once! (This is Python's version of Promise.all)
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Step 5: Only keep the successful Documents and ignore the ones that failed
        documents = []
        for result in results:
            if isinstance(result, Document):
                documents.append(result)
            else:
                # Add this to reveal the silent failure!
                print(f"Worker Error on a file: {repr(result)}")

        return documents

