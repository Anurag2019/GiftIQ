import streamlit as st
import requests


# ----------------------------
# App Config
# ----------------------------
st.set_page_config(
    page_title="GiftIQ",
    page_icon="🎁",
    layout="wide"
)

# def apply_sidebar_hover_style():
st.markdown(
        """
        <style>
          .stApp {
    background-image: 
        linear-gradient(
            rgba(255, 255, 255, 0.75),
            rgba(255, 255, 255, 0.75)
        ),
        url("https://images.unsplash.com/photo-1513885535751-8b9238bd345a");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* Main content transparency */
.block-container {
    background: rgba(255, 255, 255, 0.65);
    padding: 2rem;
    border-radius: 18px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.15);
}
        /* Sidebar background */
        section[data-testid="stSidebar"] {
            background-color: #0F172A;
        }

        /* Sidebar text */
        section[data-testid="stSidebar"] * {
            color: white;
        }

        /* Radio item container */
        div[role="radiogroup"] > label {
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 6px;
            transition: all 0.3s ease;
        }

        /* Hover effect */
        div[role="radiogroup"] > label:hover {
            background-color: #22C55E; /* GiftIQ green */
            color: black;
            cursor: pointer;
        }

        /* Selected item */
        div[role="radiogroup"] > label[data-checked="true"] {
            background-color: #16A34A;
            color: black;
            font-weight: bold;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
#----------------------------
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
    " ",
    ["Home", "Analyze Profile",  "Gift Recommendations", "About"],
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
        user_input = st.text_input("𝕏 Enter Twitter/X Handle", placeholder="@twitter_username")
    elif input_type == "Public Instagram Handle":
        user_input = st.text_input("📷 Enter Instagram Handle", placeholder="@intagram_username")
    elif input_type == "Manual Bio Text":
        user_input = st.text_input("✍️ Enter Bio Text", placeholder="Paste your bio text here")

    st.markdown("[**Bio unavailable or missing?**](https://www.example.com) - Get help finding profile information")

    st.info(
        "🔒 Privacy First: We only analyze **public information** or text you provide. "
        "No login, no private data, no scraping behind authentication."
    )

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🧠 Analyze Personality"):
            if input_type == "Select Input Type":
                st.warning("Please select an input type.")
            elif not user_input.strip():
                st.warning("Please enter a valid input.")
            else:
                error_msg = None
                try:
                    with st.spinner("Analyzing personality & interests..."):
                        # Map input type to API source parameter
                        source_map = {
                            "Public Twitter/X Handle": "twitter",
                            "Public Instagram Handle": "instagram",
                            "Manual Bio Text": "manual"
                        }
                        source = source_map.get(input_type)
                        
                        # Call the backend API with source and value
                        response = requests.post(
                            "http://localhost:5000/recommend_gifts",
                            json={"source": source, "value": user_input},
                            
                        )
                        
                        data = response.json()
                        
                        # Check if the API returned a failure
                        if not data.get("success", True):
                            # Store error message to display after spinner stops
                            if data.get("error_type") == "private_account":
                                error_msg = f"❌ {data.get('error')}"
                            else:
                                # For other errors, show generic message
                                error_msg = "❌ **Analysis Failed**\n\nPlease check your input and try again."
                        elif response.status_code == 200:
                            st.session_state.analysis_result = {
                                "traits": data.get("traits", []),
                                "interests": data.get("interests", []),
                                "gifts": data.get("gifts", [])
                            }
                            st.success("✅ Analysis complete!")
                            st.session_state.page = "Gift Recommendations"
                            st.rerun()
                        else:
                            error_msg = "❌ Something went wrong. Please try again."
                except requests.exceptions.ConnectionError:
                    error_msg = "❌ Cannot connect to API server. Make sure it's running on http://localhost:5000"
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                
                # Display error message after spinner stops
                if error_msg:
                    st.error(error_msg)
    
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

        # Display Personality Traits
        st.subheader("🧠 Personality Traits")
        if result.get("traits"):
            trait_badges = " | ".join([f"✨ {trait.replace('_', ' ').title()}" for trait in result["traits"]])
            st.markdown(f"**{trait_badges}**")
        else:
            st.write("No traits detected")

        # Display Interests
        st.subheader("🎯 Interests")
        if result.get("interests"):
            interest_badges = " • ".join([f"🎪 {interest.title()}" for interest in result["interests"]])
            st.markdown(f"**{interest_badges}**")
        else:
            st.write("No interests detected")

        # Display Top 5 Gift Recommendations
        st.subheader("🛍️ Top 5 Gift Recommendations")

        gifts = result.get("gifts", [])
        
        if gifts:
            # Get top 5 gifts
            top_gifts = gifts[:5]
            
            # Create responsive grid layout (1-2 columns based on screen size)
            cols = st.columns(2, gap="medium")
            
            for idx, gift in enumerate(top_gifts):
                col_idx = idx % 2
                with cols[col_idx]:
                    # Create attractive card with border styling
                    st.markdown(f"""
                    <div style="
                        border: 2px solid #22C55E;
                        border-radius: 15px;
                        padding: 20px;
                        margin-bottom: 15px;
                        background: linear-gradient(135deg, rgba(34, 197, 94, 0.05) 0%, rgba(34, 197, 94, 0.02) 100%);
                        box-shadow: 0 4px 15px rgba(34, 197, 94, 0.1);
                    ">
                        <h3 style="color: #16A34A; margin-top: 0;">#{idx+1} {gift.get('title', 'Gift')}</h3>
                        <hr style="border: 1px solid #22C55E;">
                        <p style="color: #666; font-size: 14px; margin: 8px 0;">
                            <strong>Category:</strong> {gift.get('category', 'General').title()}
                        </p>
                        <p style="color: #16A34A; font-size: 20px; font-weight: bold; margin: 12px 0;">
                            ₹{gift.get('price', 'N/A')} {gift.get('currency', 'INR')}
                        </p>
                        <div style="margin: 12px 0;">
                    """, unsafe_allow_html=True)
                    
                    # Display gift image with optimized styling
                    try:
                        st.image(
                            gift.get("image", "https://via.placeholder.com/200"),
                            use_container_width=True,
                            caption=None
                        )
                    except Exception:
                        st.image("https://via.placeholder.com/200", use_container_width=True)
                    
                    # Display tags
                    if gift.get("tags"):
                        tags_html = " ".join([f"<span style='background: #E8F5E9; color: #16A34A; padding: 4px 8px; border-radius: 20px; font-size: 12px; margin-right: 5px; display: inline-block;'>{tag}</span>" for tag in gift.get("tags", [])])
                        st.markdown(f"<div style='margin: 10px 0;'>{tags_html}</div>", unsafe_allow_html=True)
                    
                    # Buy Now button with marketplace link
                    marketplace_link = gift.get('link', 'https://amazon.in')
                    st.markdown(f"""
                        <a href="{marketplace_link}" target="_blank" rel="noopener noreferrer">
                            <button style="
                                width: 100%;
                                padding: 10px;
                                background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%);
                                color: white;
                                border: none;
                                border-radius: 8px;
                                font-weight: bold;
                                cursor: pointer;
                                font-size: 14px;
                                transition: all 0.3s ease;
                                margin-top: 10px;
                            " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 20px rgba(34, 197, 94, 0.3)';" 
                               onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
                                🛒 Buy Now on Amazon
                            </button>
                        </a>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
            
            st.balloons()
        else:
            st.info("No gift recommendations available for detected interests.")
        
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
    **GiftIQ** is an AI-powered gift recommendation system that understands peoples' personality traits and interests
    before suggesting products.

    
    ### 🛡️ Ethics & Privacy
    - No login required
    - No private data access
    - Manual bio supported
    - Public info only
    """)

    st.success("Product-Ready for startups 🚀")
