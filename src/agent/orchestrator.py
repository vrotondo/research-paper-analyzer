"""
Research Paper Analyzer Agent Orchestrator
Coordinates the entire agentic workflow:
1. Query decomposition
2. Paper search & retrieval
3. Multi-step reasoning
4. Synthesis with citations
"""
from typing import List, Dict, Tuple
from src.agent.llm_client import NvidiaLLMClient
from src.retrieval.arxiv_fetcher import ArxivFetcher
from src.retrieval.pdf_processor import PDFProcessor


class ResearchAgent:
    """Autonomous research paper analysis agent"""
    
    def __init__(self):
        self.llm = NvidiaLLMClient()
        self.fetcher = ArxivFetcher()
        self.processor = PDFProcessor()
        
        # Agent prompts
        self.system_prompt = """You are an expert research assistant that helps analyze and synthesize information from academic papers. 
You provide accurate, well-cited answers based on the papers provided."""
    
    def decompose_query(self, query: str) -> List[str]:
        """
        Break down complex research question into sub-queries
        
        Args:
            query: Original research question
            
        Returns:
            List of sub-queries
        """
        prompt = f"""Break down this research question into 2-3 specific sub-questions that would help answer it comprehensively.
Return only the sub-questions, one per line, numbered.

Research Question: {query}

Sub-questions:"""
        
        response = self.llm.generate_response(
            prompt=prompt,
            system_message="You are a research methodology expert."
        )
        
        # Parse sub-queries
        sub_queries = [line.strip() for line in response.split('\n') if line.strip() and any(char.isdigit() for char in line[:3])]
        
        # Fallback to original query if parsing fails
        if not sub_queries:
            sub_queries = [query]
        
        return sub_queries
    
    def search_papers(self, query: str, max_results: int = 5) -> Tuple[List[Dict], List[str]]:
        """
        Search and download papers for a query
        
        Args:
            query: Search query
            max_results: Maximum papers to fetch
            
        Returns:
            Tuple of (paper metadata, file paths)
        """
        papers, filepaths = self.fetcher.fetch_and_download(query, max_results)
        return papers, filepaths
    
    def process_papers(self, filepaths: List[str], papers_metadata: List[Dict]) -> List[Dict]:
        """
        Extract text from downloaded papers
        
        Args:
            filepaths: List of PDF paths
            papers_metadata: List of paper metadata
            
        Returns:
            List of processed paper data
        """
        return self.processor.process_papers(filepaths, papers_metadata)
    
    def analyze_papers(self, query: str, papers: List[Dict]) -> str:
        """
        Analyze papers and generate answer to query
        
        Args:
            query: Research question
            papers: List of processed papers with text
            
        Returns:
            Analysis response
        """
        # Prepare context from papers
        context = self._build_context(papers)
        
        prompt = f"""Based on the research papers provided below, answer this question comprehensively:

Question: {query}

Research Papers:
{context}

Provide a detailed answer that:
1. Synthesizes information from multiple papers
2. Identifies key findings and methodologies
3. Notes any contradictions or gaps
4. Cites specific papers using [Paper N] format

Answer:"""
        
        response = self.llm.generate_response(
            prompt=prompt,
            system_message=self.system_prompt,
            max_tokens=1500
        )
        
        return response
    
    def _build_context(self, papers: List[Dict], max_chars: int = 8000) -> str:
        """
        Build context string from papers for LLM
        
        Args:
            papers: List of processed papers
            max_chars: Maximum characters to include
            
        Returns:
            Formatted context string
        """
        context_parts = []
        current_length = 0
        
        for i, paper in enumerate(papers, 1):
            # Get paper info
            title = paper.get('arxiv_metadata', {}).get('title', 'Unknown Title')
            authors = paper.get('arxiv_metadata', {}).get('authors', ['Unknown'])
            summary = paper.get('arxiv_metadata', {}).get('summary', '')
            
            # Extract relevant text (first 2000 chars of paper)
            text_excerpt = paper.get('text', '')[:2000]
            
            paper_context = f"""
[Paper {i}]
Title: {title}
Authors: {', '.join(authors[:3])}
Summary: {summary}
Excerpt: {text_excerpt}...
---"""
            
            # Check if adding this would exceed limit
            if current_length + len(paper_context) > max_chars:
                break
            
            context_parts.append(paper_context)
            current_length += len(paper_context)
        
        return "\n".join(context_parts)
    
    def compare_methodologies(self, papers: List[Dict]) -> str:
        """
        Compare research methodologies across papers
        
        Args:
            papers: List of processed papers
            
        Returns:
            Comparison analysis
        """
        context = self._build_context(papers)
        
        prompt = f"""Compare and contrast the research methodologies used in these papers:

{context}

Provide an analysis that:
1. Identifies different methodological approaches
2. Compares their strengths and weaknesses
3. Notes which methods are most common
4. Cites specific papers using [Paper N] format

Analysis:"""
        
        response = self.llm.generate_response(
            prompt=prompt,
            system_message=self.system_prompt,
            max_tokens=1500
        )
        
        return response
    
    def identify_gaps(self, query: str, papers: List[Dict]) -> str:
        """
        Identify research gaps based on current literature
        
        Args:
            query: Research area
            papers: List of processed papers
            
        Returns:
            Gap analysis
        """
        context = self._build_context(papers)
        
        prompt = f"""Based on these research papers about "{query}", identify gaps in the current literature:

{context}

Provide an analysis that:
1. Lists what topics are well-covered
2. Identifies missing perspectives or approaches
3. Suggests potential research directions
4. Cites specific papers using [Paper N] format

Gap Analysis:"""
        
        response = self.llm.generate_response(
            prompt=prompt,
            system_message=self.system_prompt,
            max_tokens=1500
        )
        
        return response
    
    def run_full_analysis(self, query: str, max_papers: int = 5) -> Dict:
        """
        Run complete research analysis workflow
        
        Args:
            query: Research question
            max_papers: Maximum papers to analyze
            
        Returns:
            Dictionary with analysis results and metadata
        """
        results = {
            "query": query,
            "sub_queries": [],
            "papers": [],
            "analysis": "",
            "methodology_comparison": "",
            "gap_analysis": "",
            "error": None
        }
        
        try:
            # Step 1: Decompose query
            print("\n🧠 Decomposing research question...")
            sub_queries = self.decompose_query(query)
            results["sub_queries"] = sub_queries
            print(f"   Generated {len(sub_queries)} sub-questions")
            
            # Step 2: Search papers
            print("\n🔍 Searching for papers...")
            papers, filepaths = self.search_papers(query, max_papers)
            
            if not papers:
                results["error"] = "No papers found for query"
                return results
            
            # Step 3: Process papers
            print("\n📄 Processing papers...")
            processed_papers = self.process_papers(filepaths, papers)
            results["papers"] = processed_papers
            
            if not processed_papers:
                results["error"] = "Failed to process papers"
                return results
            
            # Step 4: Analyze papers
            print("\n🤔 Analyzing papers...")
            results["analysis"] = self.analyze_papers(query, processed_papers)
            
            # Step 5: Compare methodologies
            print("\n📊 Comparing methodologies...")
            results["methodology_comparison"] = self.compare_methodologies(processed_papers)
            
            # Step 6: Identify gaps
            print("\n🔬 Identifying research gaps...")
            results["gap_analysis"] = self.identify_gaps(query, processed_papers)
            
            print("\n✅ Analysis complete!")
            
        except Exception as e:
            results["error"] = str(e)
            print(f"\n❌ Error during analysis: {str(e)}")
        
        return results