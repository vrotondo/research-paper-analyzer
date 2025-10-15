"""
Test ArXiv Fetcher and PDF Processor
Run this to test paper downloading and processing
"""
from src.retrieval.arxiv_fetcher import ArxivFetcher
from src.retrieval.pdf_processor import PDFProcessor


def test_search():
    """Test searching ArXiv"""
    print("="*60)
    print("TEST 1: Search ArXiv")
    print("="*60)
    
    fetcher = ArxivFetcher()
    
    # Search for papers
    query = "large language models"
    papers = fetcher.search_papers(query, max_results=3)
    
    print("\n📋 Found papers:")
    for i, paper in enumerate(papers, 1):
        print(f"\n{i}. {paper['title']}")
        print(f"   Authors: {', '.join(paper['authors'][:3])}")
        print(f"   Published: {paper['published']}")
        print(f"   ArXiv ID: {paper['arxiv_id']}")
    
    return papers


def test_download(papers):
    """Test downloading papers"""
    print("\n" + "="*60)
    print("TEST 2: Download Papers")
    print("="*60)
    
    fetcher = ArxivFetcher()
    
    # Download first paper only for testing
    test_paper = papers[0]
    filepath = fetcher.download_paper(test_paper)
    
    return [filepath] if filepath else []


def test_processing(filepaths, papers):
    """Test PDF processing"""
    print("\n" + "="*60)
    print("TEST 3: Process PDFs")
    print("="*60)
    
    processor = PDFProcessor()
    
    # Process the downloaded paper
    processed = processor.process_papers(filepaths, [papers[0]])
    
    if processed:
        paper = processed[0]
        print(f"\n📊 Paper Statistics:")
        print(f"   Filename: {paper['filename']}")
        print(f"   Pages: {paper['pdf_metadata']['num_pages']}")
        print(f"   Text length: {paper['text_length']:,} characters")
        
        # Show first 500 characters
        print(f"\n📄 Text Preview:")
        print(paper['text'][:500] + "...")
        
        # Test chunking
        chunks = processor.chunk_text(paper['text'], chunk_size=500, overlap=100)
        print(f"\n✂️  Text chunked into {len(chunks)} pieces for retrieval")
    
    return processed


def main():
    """Run all tests"""
    print("="*60)
    print("ArXiv Fetcher & PDF Processor Test")
    print("="*60)
    
    try:
        # Test 1: Search
        papers = test_search()
        
        if not papers:
            print("\n❌ No papers found. Exiting.")
            return
        
        # Test 2: Download
        filepaths = test_download(papers)
        
        if not filepaths:
            print("\n❌ No papers downloaded. Exiting.")
            return
        
        # Test 3: Process
        processed = test_processing(filepaths, papers)
        
        print("\n" + "="*60)
        print("✅ All tests completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()