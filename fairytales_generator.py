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
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Create Your Perfect Story</p>', unsafe_allow_html=True)

# Create tabs for different functionalities
tab1, tab2 = st.tabs(["📝 Create Story", "📖 Read Stories"])

with tab1:
    # Single column layout from top to bottom

    # 🧚‍♀️ MAIN CHARACTER SECTION
    st.markdown('<h2 class="section-header">🧚‍♀️ Main Character</h2>', unsafe_allow_html=True)

    char_name = st.text_input("Character Name", placeholder="Enter your hero's name...")

    char_type = st.selectbox(
        "Character Type",
        ["Child", "Adult", "Animal", "Magical Creature", "Princess", "Prince", "Witch", "Wizard"],
        index=None,
        placeholder="Select or type a custom character type...",
        accept_new_options=True
    )

    personality = st.multiselect(
        "Personality Traits",
        ["Brave", "Shy", "Clever", "Funny", "Kind", "Curious", "Loyal", "Adventurous", "Wise", "Playful"],
        default=["Brave", "Kind"],
        accept_new_options=True
    )

    # 🏰 SETTING & WORLD SECTION
    st.markdown('<h2 class="section-header">🏰 Setting & World</h2>', unsafe_allow_html=True)

    location = st.selectbox(
        "Location",
        ["Enchanted Forest", "Royal Castle", "Small Village", "Magical Realm", "Mountain Peak", "Underwater Kingdom", "Cloud City", "Dark Woods"],
        index=None,
        placeholder="Select or type a custom location...",
        accept_new_options=True
    )

    atmosphere = st.selectbox(
        "Atmosphere",
        ["Dark & Mysterious", "Bright & Cheerful", "Magical & Whimsical", "Serious & Dramatic", "Fun & Playful"],
        index=None,
        placeholder="Select or type a custom atmosphere...",
        accept_new_options=True
    )

    # ⚔️ CONFLICT & ADVENTURE SECTION
    st.markdown('<h2 class="section-header">⚔️ Conflict & Adventure</h2>', unsafe_allow_html=True)

    main_problem = st.text_area(
        "Main Problem/Challenge",
        placeholder="What challenge must your character overcome? What adventure awaits?",
        height=100
    )

    antagonist = st.text_input(
        "Antagonist/Villain",
        placeholder="Who or what is the main obstacle? (dragon, evil witch, curse, etc.)"
    )

    # 👥 SUPPORTING CAST SECTION
    st.markdown('<h2 class="section-header">👥 Supporting Cast</h2>', unsafe_allow_html=True)

    helper_mentor = st.text_input(
        "Helper/Mentor",
        placeholder="Wise character who helps (fairy godmother, old wizard, etc.)"
    )

    # 📖 STORY PREFERENCES SECTION
    st.markdown('<h2 class="section-header">📖 Story Preferences</h2>', unsafe_allow_html=True)

    story_length = st.radio(
        "Story Length",
        ["Short (1-2 pages)", "Medium (3-5 pages)", "Long (6+ pages)"]
    )

    tone = st.selectbox(
        "Tone",
        ["Funny & Humorous", "Serious & Dramatic", "Adventurous & Exciting", "Educational & Teaching", "Romantic & Sweet", "Mysterious & Suspenseful"],
        index=None,
        placeholder="Select or type a custom tone...",
        accept_new_options=True
    )

    target_language = st.selectbox(
        "Target Language",
        ["English", "Spanish", "French", "German", "Italian", "Portuguese", "Dutch", "Russian", "Polish", "Czech", "Slovak", "Hungarian", "Romanian", "Bulgarian", "Croatian", "Serbian", "Slovenian", "Greek", "Turkish", "Finnish", "Swedish", "Norwegian", "Danish", "Icelandic", "Irish", "Welsh", "Scottish Gaelic", "Catalan", "Basque", "Galician", "Ukrainian", "Belarusian", "Lithuanian", "Latvian", "Estonian", "Maltese", "Luxembourgish", "Albanian", "Macedonian", "Bosnian", "Montenegrin", "Chinese", "Japanese", "Korean", "Arabic", "Hindi"],
        index=None,
        placeholder="Select or type a custom language...",
        accept_new_options=True
    )

    # 🎨 VISUAL STYLE SECTION
    st.markdown('<h2 class="section-header">🎨 Visual Style</h2>', unsafe_allow_html=True)

    art_style = st.radio(
        "Art Style",
        ["Cartoon & Colorful", "Realistic & Detailed", "Watercolor & Soft", "Abstract & Artistic"]
    )

    # Action buttons at the bottom
    st.markdown("---")


    if st.button("💾 Generate Fairytale", use_container_width=True):
        # Prepare data for upload
        story_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'character_name': char_name,
            'character_type': char_type,
            'personality_traits': ', '.join(personality) if personality else '',
            'location': location,
            'atmosphere': atmosphere,
            'main_problem': main_problem,
            'antagonist': antagonist,
            'helper_mentor': helper_mentor,
            'story_length': story_length,
            'tone': tone,
            'target_language': target_language,
            'art_style': art_style
        }

        try:
            # Check if Keboola connection is available
            if keboola is None:
                st.error("❌ Keboola connection not available. Please check your configuration.")

            # Create DataFrame from the story data
            df = pd.DataFrame([story_data])

            # Upload to Keboola storage using write_table method
            keboola.write_table(
                table_id="in.c-generator-data.story-config",
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
                            if 'character_name' in latest_fairytale:
                                st.info(f"👤 Character: {latest_fairytale['character_name']}")
                        
                        with col2:
                            if 'location' in latest_fairytale:
                                st.info(f"🏰 Setting: {latest_fairytale['location']}")
                            if 'tone' in latest_fairytale:
                                st.info(f"🎭 Tone: {latest_fairytale['tone']}")
                        
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
if 'char_name' in locals():
    with st.sidebar:
        st.markdown("## 📋 Current Configuration")
        st.markdown("---")
        
        if char_name:
            st.write(f"**Hero:** {char_name}")
        if char_type:
            st.write(f"**Type:** {char_type}")
        if location:
            st.write(f"**Setting:** {location}")
        if main_problem:
            st.write(f"**Challenge:** {main_problem[:50]}...")
        if story_length:
            st.write(f"**Length:** {story_length}")
        if tone:
            st.write(f"**Tone:** {tone}")
        
        st.markdown("---")
        st.markdown("### 🎯 Quick Stats")
        st.metric("Personality Traits", len(personality))

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #666; font-style: italic;">🧚‍♀️ Created with magic and Streamlit 🧚‍♀️</p>',
    unsafe_allow_html=True
)
