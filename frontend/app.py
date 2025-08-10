import streamlit as st
import requests
import time
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Sentiment Analyzer",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sentiment-positive {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .sentiment-negative {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .sentiment-neutral {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .stButton > button {
        width: 100%;
        background-color: #2E86AB;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 0.75rem;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">🎭 Sentiment Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; font-size: 1.2rem;">Powered by Mistral AI via Ollama</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.write("This application uses the Mistral language model to analyze the sentiment of text input.")
    
    st.header("🚀 How it works")
    st.write("1. Enter your text in the main area")
    st.write("2. Click 'Analyze Sentiment'")
    st.write("3. Get instant sentiment classification")
    
    st.header("📊 Sentiment Types")
    st.write("• **Positive**: Happy, joyful, satisfied")
    st.write("• **Negative**: Sad, angry, frustrated")
    st.write("• **Neutral**: Factual, balanced, objective")
    
    # Health check
    st.header("🔍 System Status")
    if st.button("Check System Health"):
        try:
            health_response = requests.get("http://localhost:8000/health/", timeout=5)
            if health_response.status_code == 200:
                health_data = health_response.json()
                st.success("✅ API is running")
                if health_data.get("ollama_status") == "connected":
                    st.success("✅ Ollama is connected")
                    if health_data.get("mistral_available"):
                        st.success("✅ Mistral model is available")
                    else:
                        st.warning("⚠️ Mistral model not found")
                else:
                    st.error("❌ Ollama is not connected")
            else:
                st.error("❌ API is not responding")
        except Exception as e:
            st.error(f"❌ Cannot connect to API: {str(e)}")

# Main content area
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Text input
    st.subheader("📝 Enter your text:")
    text_input = st.text_area(
        label="Text to analyze",
        height=150,
        placeholder="Type or paste your text here...\n\nExample: 'I love this new product! It works perfectly and exceeded my expectations.'",
        label_visibility="collapsed",
        key="text_input_area",
        value=st.session_state.get("text_input", "")
    )
    
    # Character count
    char_count = len(text_input)
    st.caption(f"Characters: {char_count}")
    
    # Analyze button
    analyze_button = st.button("🔍 Analyze Sentiment", type="primary")
    
    # Analysis section
    if analyze_button:
        if not text_input.strip():
            st.error("⚠️ Please enter some text to analyze!")
        else:
            with st.spinner("Analyzing sentiment... This may take a few seconds."):
                try:
                    # Make request to backend
                    start_time = time.time()
                    response = requests.post(
                        "http://localhost:8000/analyze/", 
                        data={"text": text_input},
                        timeout=45
                    )
                    end_time = time.time()
                    
                    if response.status_code == 200:
                        result = response.json()
                        sentiment = result.get("sentiment", "Unknown")
                        processing_time = round(end_time - start_time, 2)
                        
                        st.success("✅ Analysis complete!")
                        
                        # Display result with styling
                        sentiment_lower = sentiment.lower()
                        if sentiment_lower == "positive":
                            st.markdown(f"""
                            <div class="sentiment-positive">
                                <h3>😊 Sentiment: {sentiment}</h3>
                                <p>The text expresses a positive sentiment.</p>
                            </div>
                            """, unsafe_allow_html=True)
                        elif sentiment_lower == "negative":
                            st.markdown(f"""
                            <div class="sentiment-negative">
                                <h3>😞 Sentiment: {sentiment}</h3>
                                <p>The text expresses a negative sentiment.</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="sentiment-neutral">
                                <h3>😐 Sentiment: {sentiment}</h3>
                                <p>The text expresses a neutral sentiment.</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Additional info
                        with st.expander("📊 Analysis Details"):
                            st.write(f"**Processing time:** {processing_time} seconds")
                            st.write(f"**Text length:** {len(text_input)} characters")
                            st.write(f"**Analyzed at:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                            if "raw_response" in result:
                                st.write(f"**Raw model response:** {result['raw_response']}")
                    else:
                        error_detail = response.json().get("detail", "Unknown error")
                        st.error(f"❌ Error: {error_detail}")
                        
                except requests.exceptions.Timeout:
                    st.error("⏰ Request timed out. The model might be taking longer than expected.")
                except requests.exceptions.ConnectionError:
                    st.error("🔌 Cannot connect to the backend API. Make sure the FastAPI server is running on localhost:8000")
                except Exception as e:
                    st.error(f"❌ An unexpected error occurred: {str(e)}")

# Sample texts for testing
st.subheader("💡 Try these sample texts:")
sample_texts = {
    "Positive": "I absolutely love this new restaurant! The food was delicious and the service was exceptional.",
    "Negative": "This movie was terrible. I wasted my money and fell asleep halfway through.",
    "Neutral": "The meeting is scheduled for 2 PM tomorrow in conference room B. Please bring your laptops."
}

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("😊 Positive Example"):
        st.session_state.sample_text = sample_texts["Positive"]

with col2:
    if st.button("😞 Negative Example"):
        st.session_state.sample_text = sample_texts["Negative"]

with col3:
    if st.button("😐 Neutral Example"):
        st.session_state.sample_text = sample_texts["Neutral"]

# Display sample text if selected
if "sample_text" in st.session_state:
    st.info(f"**Sample text:** {st.session_state.sample_text}")
    if st.button("📋 Use This Sample"):
        # Clear the session state to avoid infinite loops
        sample_text = st.session_state.sample_text
        del st.session_state.sample_text
        # Use the sample text by setting it in text_input
        st.session_state.text_input = sample_text
        st.rerun()

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #999;">Built with Streamlit, FastAPI, and Mistral AI • '
    '<a href="https://github.com/yourusername/sentiment-analyzer-mistral" target="_blank">View on GitHub</a></p>', 
    unsafe_allow_html=True
)