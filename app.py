"""
Research Paper Analyzer - Streamlit UI
Interactive interface for agentic research paper analysis
"""
import streamlit as st
from src.agent.orchestrator import ResearchAgent
import time


# Page config
st.set_page_config(
    page_title="Research Paper Analyzer",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = ResearchAgent()
if 'results' not in st.session_state:
    st.session_state.results = None


def main():
    """Main Streamlit app"""
    
    # Header
    st.title("📚 Research Paper Analyzer")
    st.markdown("### AI-Powered Research Assistant using NVIDIA NIM")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        max_papers = st.slider("Maximum Papers", 1, 10, 5)
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This tool uses:
        - **NVIDIA NIM** (Llama-3.1-8B)
        - **ArXiv API** for papers
        - **Agentic AI** for analysis
        
        Built for NVIDIA x AWS Hackathon
        """)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        query = st.text_input(
            "🔍 Enter your research question:",
            placeholder="e.g., What are the latest advances in transformer architectures?"
        )
    
    with col2:
        st.write("")
        st.write("")
        analyze_button = st.button("🚀 Analyze", type="primary", use_container_width=True)
    
    # Run analysis
    if analyze_button and query:
        with st.spinner("🤖 Agent is working..."):
            # Create progress indicators
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Run analysis with progress updates
            status_text.text("🧠 Decomposing query...")
            progress_bar.progress(10)
            time.sleep(0.5)
            
            status_text.text("🔍 Searching ArXiv...")
            progress_bar.progress(30)
            
            # Run full analysis
            results = st.session_state.agent.run_full_analysis(query, max_papers)
            st.session_state.results = results
            
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
            time.sleep(0.5)
            status_text.empty()
            progress_bar.empty()
    
    # Display results
    if st.session_state.results:
        results = st.session_state.results
        
        if results.get("error"):
            st.error(f"❌ Error: {results['error']}")
            return
        
        st.markdown("---")
        st.header("📊 Analysis Results")
        
        # Sub-queries
        with st.expander("🧠 Query Decomposition", expanded=True):
            st.markdown("**Sub-questions generated:**")
            for i, sq in enumerate(results.get("sub_queries", []), 1):
                st.markdown(f"{i}. {sq}")
        
        # Papers found
        with st.expander("📚 Papers Analyzed", expanded=True):
            papers = results.get("papers", [])
            st.markdown(f"**Found {len(papers)} papers:**")
            
            for i, paper in enumerate(papers, 1):
                metadata = paper.get("arxiv_metadata", {})
                st.markdown(f"""
                **[Paper {i}] {metadata.get('title', 'Unknown')}**
                - Authors: {', '.join(metadata.get('authors', ['Unknown'])[:3])}
                - Published: {metadata.get('published', 'Unknown')}
                - Length: {paper.get('text_length', 0):,} characters
                """)
        
        # Main analysis
        st.markdown("---")
        st.subheader("💡 Synthesized Answer")
        st.markdown(results.get("analysis", "No analysis generated"))
        
        # Methodology comparison
        st.markdown("---")
        st.subheader("🔬 Methodology Comparison")
        st.markdown(results.get("methodology_comparison", "No comparison generated"))
        
        # Gap analysis
        st.markdown("---")
        st.subheader("🎯 Research Gaps")
        st.markdown(results.get("gap_analysis", "No gap analysis generated"))
        
        # Download results
        st.markdown("---")
        if st.button("💾 Download Full Report"):
            report = generate_report(results)
            st.download_button(
                label="📄 Download Report",
                data=report,
                file_name=f"research_analysis_{int(time.time())}.txt",
                mime="text/plain"
            )


def generate_report(results: dict) -> str:
    """Generate downloadable text report"""
    report = f"""
RESEARCH PAPER ANALYSIS REPORT
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

QUERY: {results['query']}

{'='*80}
SUB-QUERIES
{'='*80}
{chr(10).join(f"{i}. {sq}" for i, sq in enumerate(results.get('sub_queries', []), 1))}

{'='*80}
PAPERS ANALYZED
{'='*80}
{chr(10).join(f"[{i}] {p.get('arxiv_metadata', {}).get('title', 'Unknown')}" for i, p in enumerate(results.get('papers', []), 1))}

{'='*80}
SYNTHESIZED ANSWER
{'='*80}
{results.get('analysis', '')}

{'='*80}
METHODOLOGY COMPARISON
{'='*80}
{results.get('methodology_comparison', '')}

{'='*80}
RESEARCH GAPS
{'='*80}
{results.get('gap_analysis', '')}

{'='*80}
END OF REPORT
{'='*80}
"""
    return report


if __name__ == "__main__":
    main()