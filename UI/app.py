import streamlit as st


# ----------------------------
# App Config
# ----------------------------
st.set_page_config(
    page_title="GiftIQ",
    page_icon="🎁",
    layout="wide"
)

# ----------------------------
# Session State Init
# ----------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# ----------------------------
# Sidebar Navigation
# ----------------------------
st.sidebar.title("🎁 GiftIQ")
st.sidebar.caption("*Smarter Gifts, Powered By Insight*")

menu = st.sidebar.radio(
    "Navigate",
    ["Home", "Analyze Profile", "Gift Recommendations", "About"],
    index=["Home", "Analyze Profile", "Gift Recommendations", "About"].index(st.session_state.page)
)

if menu != st.session_state.page:
    st.session_state.page = menu

# ----------------------------
# Screen 1: Home
# ----------------------------
if st.session_state.page == "Home":
    st.title("🎁 GiftIQ")
    st.subheader("*Smarter Gifts, Powered By Insight*")

    st.markdown("""
    ### 🎯 The Problem
    Buying gifts is hard because we rarely know what someone truly wants. 
    Most gift choices are based on assumptions, trends, or last-minute guessesleading to generic or unused items. 
    Even though people share their interests online, turning that information into meaningful gift ideas is challenging. 
    This makes gifting stressful instead of thoughtful leading to missed emotional connection and lacking personal touch.

    ### 💡 Our Solution
    GiftIQ uses AI to analyze public bios or user-provided texts to understand a person’s personality, interests, and preferences. 
    Based on these insights, it intelligently recommends personalized gift ideas that genuinely match what the person would enjoy. 
    This turns guesswork into confident, thoughtful gifting.
    Every recommendation is driven by insight, not assumptions, resulting in smarter gifting with less effort and time.
    """)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Gift Discovery", use_container_width=True):
            st.session_state.page = "Analyze Profile"
            st.rerun()

# ----------------------------
# Screen 2: Analyze Profile
# ----------------------------
elif st.session_state.page == "Analyze Profile":
    st.title("🔍 Analyze Profile")

    input_type = st.selectbox(
        "Choose input type",
        [   "Select Input Type",
            "Public Twitter/X Handle",
            "Public Instagram Handle",
            "Manual Bio Text"
        ],
        index=0
    )

    # Customize label based on selected input type
    if input_type == "Select Input Type":
        user_input = st.text_input("Enter handle or bio text", disabled=True)
    elif input_type == "Public Twitter/X Handle":
        user_input = st.text_input("𝕏 Enter Twitter/X Handle", placeholder="@username")
    elif input_type == "Public Instagram Handle":
        user_input = st.text_input("📷 Enter Instagram Handle", placeholder="@username")
    elif input_type == "Manual Bio Text":
        user_input = st.text_input("✍️ Enter Bio Text", placeholder="Paste your bio text here")

    st.info(
        "🔒 Privacy First: We only analyze **public information** or text you provide. "
        "No login, no private data, no scraping behind authentication."
    )

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🧠 Analyze Personality"):
            if not user_input.strip():
                st.warning("Please enter a valid input.")
            else:
                with st.spinner("Analyzing personality & interests..."):
                    # Mock result (replace with backend API call)
                    st.session_state.analysis_result = {
                        "traits": ["Creative", "Tech-Savvy", "Minimalist"],
                        "interests": ["AI", "Gadgets", "Productivity"],
                        "summary": "Enjoys technology, innovation, and practical tools."
                    }

                st.success("Analysis complete!")
                st.session_state.page = "Gift Recommendations"
                st.rerun()
    
    with col2:
        if st.button("← Back"):
            st.session_state.page = "Home"
            st.rerun()

# ----------------------------
# Screen 3: Gift Recommendations
# ----------------------------
elif st.session_state.page == "Gift Recommendations":
    st.title("🎁 Gift Recommendations")

    if not st.session_state.analysis_result:
        st.warning("Please analyze a profile first.")
    else:
        result = st.session_state.analysis_result

        st.subheader("🧠 Personality Traits")
        st.write(", ".join(result["traits"]))

        st.subheader("🎯 Interests")
        st.write(", ".join(result["interests"]))

        st.subheader("📝 Insight Summary")
        st.info(result["summary"])

        st.subheader("🛍️ Recommended Gifts")

        col1, col2, col3 = st.columns(3)

        gifts = [
            ("Smart Desk Organizer", "https://amazon.com", "₹2,499"),
            ("AI-Powered Notebook", "https://etsy.com", "₹1,999"),
            ("Minimalist Tech Backpack", "https://amazon.com", "₹3,999"),
        ]

        for col, gift in zip([col1, col2, col3], gifts):
            with col:
                st.image("https://via.placeholder.com/200", use_container_width=True)
                st.markdown(f"**{gift[0]}**")
                st.caption(gift[2])
                st.markdown(f"[Buy Now]({gift[1]})")

        st.divider()
        
        nav_col1, nav_col2 = st.columns(2)
        with nav_col1:
            if st.button("← Back"):
                st.session_state.page = "Analyze Profile"
                st.rerun()
        
        with nav_col2:
            if st.button("Home 🏠"):
                st.session_state.page = "Home"
                st.rerun()

# ----------------------------
# Screen 4: About
# ----------------------------
elif st.session_state.page == "About":
    st.title("ℹ️ About GiftIQ")

    st.markdown("""
    **GiftIQ** is an AI-powered gift recommendation system that understands people
    before suggesting products.

    ### ⚙️ Tech Stack
    - Streamlit (Frontend)
    - Flask (Backend APIs)
    - NLP + Semantic Matching
    - Public Profile Parsing (Ethical)

    ### 🛡️ Ethics & Privacy
    - No login required
    - No private data access
    - Manual bio supported
    - Public info only
    """)

    st.success("Product-Ready for startups 🚀")
