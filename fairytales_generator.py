import streamlit as st
import pandas as pd
import csv
from datetime import datetime
from keboola_streamlit import KeboolaStreamlit

# Initialize Keboola connection
try:
    # Retrieve credentials from Streamlit secrets
    KEBOOLA_URL = st.secrets["kbc_url"]
    STORAGE_API_TOKEN = st.secrets["kbc_token"]
    
    # Initialize the KeboolaStreamlit instance
    keboola = KeboolaStreamlit(root_url=KEBOOLA_URL, token=STORAGE_API_TOKEN)
except Exception as e:
    st.error(f"❌ Failed to initialize Keboola connection: {str(e)}")
    st.info("💡 Make sure KEBOOLA_URL and STORAGE_API_TOKEN are set in Streamlit secrets.")
    keboola = None

# Page configuration
st.set_page_config(
    page_title="🏰 Fairytales Generator",
    page_icon="🧚‍♀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load books data
books = pd.read_csv('in/tables/books.csv')

# Function to create selectbox data for books
def create_book_selectbox_data(books_df):
    """Create selectbox data with book titles and IDs."""
    book_options = []
    for _, book in books_df.iterrows():
        title = book['title']
        book_id = book['book_id']
        display_text = f"{title} ({book_id})"
        book_options.append((display_text, book_id))
    
    book_options.sort(key=lambda x: x[0])
    options = [option[0] for option in book_options]
    
    def get_book_id(selected_display):
        for display, book_id in book_options:
            if display == selected_display:
                return book_id
        return None
    
    return options, get_book_id



# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #8B4513;
        font-size: 3rem;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .section-header {
        color: #4B0082;
        font-size: 1.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #DDA0DD;
        padding-bottom: 0.5rem;
    }
    .stButton > button {
        background-color: #FF69B4;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-size: 1.1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #FF1493;
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">🏰 Fairytales Generator 🏰</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Create Your Perfect Story - Simple & Easy</p>', unsafe_allow_html=True)

# Create tabs for different functionalities
tab1, tab2 = st.tabs(["📝 Create Story", "📖 Read Stories"])

with tab1:
    # Single column layout from top to bottom

    # 🧚‍♀️ MAIN CHARACTER SECTION
    st.markdown('<h2 class="section-header">🧚‍♀️ Main Character</h2>', unsafe_allow_html=True)

    main_character = st.text_input("Main Character", placeholder="Enter your hero's name and description...")

    # 🏰 LOCATION SECTION
    st.markdown('<h2 class="section-header">🏰 Location</h2>', unsafe_allow_html=True)

    location = st.selectbox(
        "Location",
        ["Enchanted Forest", "Royal Castle", "Small Village", "Magical Realm", "Mountain Peak", "Underwater Kingdom", "Cloud City", "Dark Woods"],
        index=None,
        placeholder="Select or type a custom location...",
        accept_new_options=True
    )

    # ⚔️ MAIN PROBLEM SECTION
    st.markdown('<h2 class="section-header">⚔️ Main Problem</h2>', unsafe_allow_html=True)

    main_problem = st.text_area(
        "Main Problem/Challenge",
        placeholder="What challenge must your character overcome? What adventure awaits?",
        height=100
    )

    # 📖 INSPIRATION SECTION
    st.markdown('<h2 class="section-header">📖 Inspiration from Existing Book</h2>', unsafe_allow_html=True)
    
    inspiration_options, get_inspiration_book_id = create_book_selectbox_data(books)
    
    selected_inspiration_display = st.selectbox(
        "Choose a book for inspiration",
        options=inspiration_options,
        index=None,
        placeholder="Select a book for inspiration..."
    )
    
    selected_inspiration_id = get_inspiration_book_id(selected_inspiration_display) if selected_inspiration_display else None

    # 🌍 TARGET LANGUAGE SECTION
    st.markdown('<h2 class="section-header">🌍 Target Language</h2>', unsafe_allow_html=True)

    target_language = st.selectbox(
        "Target Language",
        ["English", "Spanish", "French", "German", "Italian", "Portuguese", "Dutch", "Russian", "Polish", "Czech", "Slovak", "Hungarian", "Romanian", "Bulgarian", "Croatian", "Serbian", "Slovenian", "Greek", "Turkish", "Finnish", "Swedish", "Norwegian", "Danish", "Icelandic", "Irish", "Welsh", "Scottish Gaelic", "Catalan", "Basque", "Galician", "Ukrainian", "Belarusian", "Lithuanian", "Latvian", "Estonian", "Maltese", "Luxembourgish", "Albanian", "Macedonian", "Bosnian", "Montenegrin", "Chinese", "Japanese", "Korean", "Arabic", "Hindi"],
        index=None,
        placeholder="Select or type a custom language...",
        accept_new_options=True
    )

    # Action buttons at the bottom
    st.markdown("---")


    if st.button("💾 Generate Fairytale", use_container_width=True):
        # Prepare data for upload
        story_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'inspiration_book_id': selected_inspiration_id,
            'inspiration_book_title': selected_inspiration_display,
            'main_character': main_character,
            'location': location,
            'main_problem': main_problem,
            'target_language': target_language
        }

        try:
            # Check if Keboola connection is available
            if keboola is None:
                st.error("❌ Keboola connection not available. Please check your configuration.")

            # Create DataFrame from the story data
            df = pd.DataFrame([story_data])

            # Upload to Keboola storage using write_table method
            keboola.write_table(
                table_id="in.c-generator-data.story",
                df=df,
                is_incremental=False  # Append mode to add new rows
            )

            st.success("✨ Story configuration uploaded to Keboola storage!")
            st.balloons()

        except Exception as e:
            st.error(f"❌ Error uploading to Keboola: {str(e)}")
            st.info("💡 Make sure you're running this app in a Keboola environment with proper authentication.")

with tab2:
    # 📖 READ STORIES TAB
    st.markdown('<h2 class="section-header">📖 Generated Fairytales</h2>', unsafe_allow_html=True)
    
    # Button to refresh and load the latest fairytale
    if st.button("🔄 Load Latest Fairytale", use_container_width=True):
        try:
            # Check if Keboola connection is available
            if keboola is None:
                st.error("❌ Keboola connection not available. Please check your configuration.")
            else:
                # Read the latest fairytale from the specified table
                df = keboola.read_table("out.c-fairytale-ai-pipeline.story")
                
                if df is not None and not df.empty:
                    # Get the latest fairytale (assuming there's a timestamp or we take the last row)
                    latest_fairytale = df.iloc[-1]  # Get the last row
                    
                    # Display the fairytale
                    st.markdown("### 🏰 Latest Generated Fairytale")
                    st.markdown("---")
                    
                    # Check if 'fairytale' column exists
                    if 'fairytale' in latest_fairytale:
                        fairytale_text = latest_fairytale['fairytale']
                        
                        # Display the fairytale in a nice format
                        st.markdown(f"""
                        <div style="
                            background-color: #f8f9fa;
                            padding: 2rem;
                            border-radius: 10px;
                            border-left: 5px solid #8B4513;
                            font-family: 'Georgia', serif;
                            font-size: 1.1rem;
                            line-height: 1.6;
                            color: #333;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        ">
                            {fairytale_text}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display additional metadata if available
                        st.markdown("### 📊 Story Details")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            if 'timestamp' in latest_fairytale:
                                st.info(f"📅 Generated: {latest_fairytale['timestamp']}")
                            if 'main_character' in latest_fairytale:
                                st.info(f"👤 Main Character: {latest_fairytale['main_character']}")
                        
                        with col2:
                            if 'location' in latest_fairytale:
                                st.info(f"🏰 Location: {latest_fairytale['location']}")
                            if 'target_language' in latest_fairytale:
                                st.info(f"🌍 Language: {latest_fairytale['target_language']}")
                        
                        st.success("✨ Fairytale loaded successfully!")
                        st.balloons()
                        
                    else:
                        st.warning("⚠️ No 'fairytale' column found in the data. Available columns:")
                        st.write(df.columns.tolist())
                        
                        # Show the raw data for debugging
                        st.markdown("### 📋 Raw Data")
                        st.dataframe(df)
                        
                else:
                    st.warning("📭 No fairytales found in the storage. Generate some stories first!")
                    
        except Exception as e:
            st.error(f"❌ Error reading from Keboola: {str(e)}")
            st.info("💡 Make sure the table 'out.c-fairytale-ai-pipeline.story' exists and contains fairytale data.")
    
    # Display instructions
    st.markdown("---")
    st.markdown("""
    ### 💡 How to use this tab:
    1. Click **"🔄 Load Latest Fairytale"** to fetch the most recent story from Keboola storage
    2. The fairytale will be displayed in a beautiful, readable format
    3. Additional story details will be shown below the main text
    4. If no stories are found, make sure to generate some stories first using the "Create Story" tab
    """)

# Display current configuration in sidebar (only show when in Create Story tab)
if 'main_character' in locals():
    with st.sidebar:
        st.markdown("## 📋 Current Configuration")
        st.markdown("---")
        
        if selected_inspiration_id:
            st.write(f"**Inspiration:** {selected_inspiration_display}")
        if main_character:
            st.write(f"**Main Character:** {main_character}")
        if location:
            st.write(f"**Location:** {location}")
        if main_problem:
            st.write(f"**Main Problem:** {main_problem[:50]}...")
        if target_language:
            st.write(f"**Target Language:** {target_language}")
        
        st.markdown("---")
        st.markdown("### 🎯 Story Summary")
        filled_fields = sum([bool(selected_inspiration_id), bool(main_character), bool(location), bool(main_problem), bool(target_language)])
        st.metric("Fields Completed", f"{filled_fields}/5")

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #666; font-style: italic;">🧚‍♀️ Created with magic and Streamlit 🧚‍♀️</p>',
    unsafe_allow_html=True
)
