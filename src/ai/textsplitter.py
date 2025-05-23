from abc import ABC, abstractmethod
from typing import List, Optional


class TextSplitter(ABC):
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("Cannot have chunk_overlap >= chunk_size")

    @abstractmethod
    def split_text(self, text: str) -> List[str]:
        """Split a single piece of text into chunks"""
        pass

    def create_documents(self, texts: List[str]) -> List[str]:
        documents = []
        for text in texts:
            chunks = self.split_text(text)
            documents.extend(chunks)
        return documents

    def split_documents(self, documents: List[str]) -> List[str]:
        return self.create_documents(documents)

    def _join_docs(self, docs: List[str], separator: str) -> Optional[str]:
        text = separator.join(docs).strip()
        return text if text else None

    def merge_splits(self, splits: List[str], separator: str) -> List[str]:
        docs = []
        current_doc = []
        total = 0

        for d in splits:
            length = len(d)
            if total + length >= self.chunk_size:
                if total > self.chunk_size:
                    print(f"Warning: Created a chunk of size {total}, which is longer than {self.chunk_size}")
                if current_doc:
                    doc = self._join_docs(current_doc, separator)
                    if doc is not None:
                        docs.append(doc)
                    # Reduce overlap
                    while (
                        total > self.chunk_overlap or
                        (total + length > self.chunk_size and total > 0)
                    ):
                        total -= len(current_doc[0])
                        current_doc.pop(0)
            current_doc.append(d)
            total += length

        final_doc = self._join_docs(current_doc, separator)
        if final_doc is not None:
            docs.append(final_doc)

        return docs


class RecursiveCharacterTextSplitter(TextSplitter):
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separators: Optional[List[str]] = None
    ):
        super().__init__(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.separators = separators or ['\n\n', '\n', '.', ',', '>', '<', ' ', '']

    def split_text(self, text: str) -> List[str]:
        final_chunks = []

        # Choose best separator
        separator = self.separators[-1]
        for s in self.separators:
            if s == '' or s in text:
                separator = s
                break

        splits = text.split(separator) if separator else list(text)

        good_splits = []
        for part in splits:
            if len(part) < self.chunk_size:
                good_splits.append(part)
            else:
                if good_splits:
                    merged = self.merge_splits(good_splits, separator)
                    final_chunks.extend(merged)
                    good_splits = []
                deeper_chunks = self.split_text(part)
                final_chunks.extend(deeper_chunks)

        if good_splits:
            merged = self.merge_splits(good_splits, separator)
            final_chunks.extend(merged)

        return final_chunks
