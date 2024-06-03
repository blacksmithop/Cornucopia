from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders.parsers.pdf import (
    PyMuPDFParser,
)
from typing import Iterator
from langchain_core.document_loaders import Blob
from io import BytesIO
from typing import Any, List
from langchain_core.documents import Document
import logging


class BytesIOPyMuPDFLoader(PyMuPDFLoader):
    """Load `PDF` files using `PyMuPDF` from a BytesIO stream."""

    def __init__(
        self,
        pdf_stream: BytesIO,
        *,
        extract_images: bool = False,
        **kwargs: Any,
    ) -> None:
        """Initialize with a BytesIO stream."""
        try:
            import fitz  # noqa:F401
        except ImportError:
            raise ImportError(
                "`PyMuPDF` package not found, please install it with "
                "`pip install pymupdf`"
            )
        # We don't call the super().__init__ here because we don't have a file_path.
        self.pdf_stream = pdf_stream
        self.extract_images = extract_images
        self.text_kwargs = kwargs

    def load(self, **kwargs: Any) -> List[Document]:
        """Load file."""
        if kwargs:
            logging.warning(
                f"Received runtime arguments {kwargs}. Passing runtime args to `load`"
                f" is deprecated. Please pass arguments during initialization instead."
            )

        text_kwargs = {**self.text_kwargs, **kwargs}

        # Use 'stream' as a placeholder for file_path since we're working with a stream.
        blob = Blob.from_data(self.pdf_stream.getvalue(), path="stream")

        parser = PyMuPDFParser(
            text_kwargs=text_kwargs, extract_images=self.extract_images
        )

        return parser.parse(blob)
    
    
from langchain_core.document_loaders import BaseBlobParser, Blob


class BytesIOTextLoader(BaseBlobParser):
    """A simple parser that creates a document from each line."""

    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        """Parse a blob into a document line by line."""
        line_number = 0
        with blob.as_bytes_io() as f:
            for line in f:
                line_number += 1
                yield Document(
                    page_content=line,
                    metadata={"line_number": line_number, "source": blob.source},
                )