"""
ArXiv Paper Fetcher
Downloads research papers from ArXiv based on search queries
"""
import arxiv
import os
from typing import List, Dict
from src.utils.helpers import ensure_dir


class ArxivFetcher:
    """Fetch papers from ArXiv"""
    
    def __init__(self, download_dir: str = "data/raw"):
        self.download_dir = download_dir
        ensure_dir(download_dir)
    
    def search_papers(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search for papers on ArXiv
        
        Args:
            query: Search query string
            max_results: Maximum number of papers to fetch
            
        Returns:
            List of paper metadata dictionaries
        """
        print(f"🔍 Searching ArXiv for: '{query}'...")
        
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        papers = []
        
        for result in search.results():
            paper_info = {
                "title": result.title,
                "authors": [author.name for author in result.authors],
                "summary": result.summary,
                "published": result.published.strftime("%Y-%m-%d"),
                "arxiv_id": result.entry_id.split('/')[-1],
                "pdf_url": result.pdf_url,
                "categories": result.categories
            }
            papers.append(paper_info)
            print(f"  ✅ Found: {paper_info['title'][:60]}...")
        
        print(f"📚 Found {len(papers)} papers")
        return papers
    
    def download_paper(self, paper: Dict) -> str:
        """
        Download a single paper PDF
        
        Args:
            paper: Paper metadata dictionary
            
        Returns:
            Path to downloaded PDF file
        """
        arxiv_id = paper['arxiv_id']
        filename = f"{arxiv_id.replace('/', '_')}.pdf"
        filepath = os.path.join(self.download_dir, filename)
        
        # Skip if already downloaded
        if os.path.exists(filepath):
            print(f"  ⏭️  Already downloaded: {filename}")
            return filepath
        
        try:
            print(f"  📥 Downloading: {paper['title'][:60]}...")
            
            # Use arxiv library to download
            paper_obj = next(arxiv.Search(id_list=[arxiv_id]).results())
            paper_obj.download_pdf(dirpath=self.download_dir, filename=filename)
            
            print(f"  ✅ Saved to: {filepath}")
            return filepath
        
        except Exception as e:
            print(f"  ❌ Error downloading {arxiv_id}: {str(e)}")
            return None
    
    def download_papers(self, papers: List[Dict]) -> List[str]:
        """
        Download multiple papers
        
        Args:
            papers: List of paper metadata dictionaries
            
        Returns:
            List of paths to downloaded PDF files
        """
        print(f"\n📥 Downloading {len(papers)} papers...")
        
        filepaths = []
        for paper in papers:
            filepath = self.download_paper(paper)
            if filepath:
                filepaths.append(filepath)
        
        print(f"\n✅ Downloaded {len(filepaths)}/{len(papers)} papers successfully")
        return filepaths
    
    def fetch_and_download(self, query: str, max_results: int = 5) -> tuple:
        """
        Search and download papers in one go
        
        Args:
            query: Search query string
            max_results: Maximum number of papers to fetch
            
        Returns:
            Tuple of (papers metadata, downloaded filepaths)
        """
        papers = self.search_papers(query, max_results)
        filepaths = self.download_papers(papers)
        return papers, filepaths