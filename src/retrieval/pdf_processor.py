"""
PDF Text Processor
Extracts and processes text from research paper PDFs
"""
import os
from pypdf import PdfReader
from typing import Dict, List
from src.utils.helpers import ensure_dir


class PDFProcessor:
    """Extract and process text from PDFs"""
    
    def __init__(self, output_dir: str = "data/processed"):
        self.output_dir = output_dir
        ensure_dir(output_dir)
    
    def extract_text(self, pdf_path: str) -> str:
        """
        Extract text from a PDF file
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text as string
        """
        try:
            reader = PdfReader(pdf_path)
            
            text = ""
            for page_num, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
            
            return text.strip()
        
        except Exception as e:
            print(f"❌ Error extracting text from {pdf_path}: {str(e)}")
            return ""
    
    def extract_metadata(self, pdf_path: str) -> Dict:
        """
        Extract metadata from PDF
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary of metadata
        """
        try:
            reader = PdfReader(pdf_path)
            metadata = reader.metadata
            
            return {
                "title": metadata.get("/Title", "Unknown"),
                "author": metadata.get("/Author", "Unknown"),
                "subject": metadata.get("/Subject", ""),
                "creator": metadata.get("/Creator", ""),
                "producer": metadata.get("/Producer", ""),
                "num_pages": len(reader.pages)
            }
        
        except Exception as e:
            print(f"❌ Error extracting metadata from {pdf_path}: {str(e)}")
            return {}
    
    def process_paper(self, pdf_path: str, paper_metadata: Dict = None) -> Dict:
        """
        Process a single paper: extract text and metadata
        
        Args:
            pdf_path: Path to PDF file
            paper_metadata: Optional ArXiv metadata
            
        Returns:
            Dictionary with paper data
        """
        filename = os.path.basename(pdf_path)
        print(f"📄 Processing: {filename}")
        
        # Extract text
        text = self.extract_text(pdf_path)
        if not text:
            print(f"  ⚠️  No text extracted from {filename}")
            return None
        
        # Extract PDF metadata
        pdf_metadata = self.extract_metadata(pdf_path)
        
        # Combine all data
        paper_data = {
            "filename": filename,
            "filepath": pdf_path,
            "text": text,
            "text_length": len(text),
            "pdf_metadata": pdf_metadata
        }
        
        # Add ArXiv metadata if provided
        if paper_metadata:
            paper_data["arxiv_metadata"] = paper_metadata
        
        print(f"  ✅ Extracted {len(text)} characters from {pdf_metadata['num_pages']} pages")
        
        return paper_data
    
    def process_papers(self, pdf_paths: List[str], papers_metadata: List[Dict] = None) -> List[Dict]:
        """
        Process multiple papers
        
        Args:
            pdf_paths: List of PDF file paths
            papers_metadata: Optional list of ArXiv metadata
            
        Returns:
            List of processed paper data
        """
        print(f"\n📚 Processing {len(pdf_paths)} papers...")
        
        processed_papers = []
        
        for i, pdf_path in enumerate(pdf_paths):
            metadata = papers_metadata[i] if papers_metadata and i < len(papers_metadata) else None
            paper_data = self.process_paper(pdf_path, metadata)
            
            if paper_data:
                processed_papers.append(paper_data)
        
        print(f"\n✅ Successfully processed {len(processed_papers)}/{len(pdf_paths)} papers")
        return processed_papers
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        Split text into overlapping chunks for better retrieval
        
        Args:
            text: Text to chunk
            chunk_size: Size of each chunk in characters
            overlap: Number of overlapping characters between chunks
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += (chunk_size - overlap)
        
        return chunks