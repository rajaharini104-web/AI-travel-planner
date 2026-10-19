import os
from datetime import date, timedelta

import streamlit as st
from groq import Groq


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)


# =====================================================
# CONFIGURATION
# =====================================================

MODEL_NAME = "llama-3.1-8b-instant"


# =====================================================
# API KEY
# =====================================================

def get_api_key():
    try:
        key = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        key = ""

    if not key:
        key = os.environ.get("GROQ_API_KEY", "")

    return key


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #eef7ff, #f8f4ff);
    }

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: #244a73;
        padding-top: 10px;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        color: #52677d;
        margin-bottom: 25px;
    }

    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.85);
        padding: 22px;
        border-radius: 15px;
        border: 1px solid #dce8f5;
    }

    .stButton button,
    .stDownloadButton button {
        border-radius: 10px;
        font-weight: bold;
        min-height: 45px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# HEADER
# =====================================================

st.markdown(
    '<div class="title">✈️ AI Travel Planner</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your personal AI assistant for planning unforgettable trips'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "Plan a three-day trip based on your destination, "
    "budget, interests, and travel preferences."
)


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.header("🌍 About the App")

    st.write(
        "AI Travel Planner generates personalized travel "
        "itineraries using artificial intelligence."
    )

    st.divider()

    st.subheader("Features")

    st.write("📍 Destination-based planning")
    st.write("📅 Three-day itinerary")
    st.write("💰 Budget estimation")
    st.write("🍽️ Food recommendations")
    st.write("🚗 Transport suggestions")
    st.write("📥 Downloadable itinerary")

    st.divider()

    st.caption("Python + Streamlit + Groq AI")


# =====================================================
# USER INPUT FORM
# =====================================================

with st.form("travel_form"):

    st.subheader("🧳 Enter Your Travel Details")

    col1, col2 = st.columns(2)

    with col1:

        destination = st.text_input(
            "Destination City",
            placeholder="Example: Ooty, Goa, Mysuru"
        )

        budget = st.number_input(
            "Total Budget (₹)",
            min_value=1000,
            max_value=1000000,
            value=10000,
            step=1000
        )

        travelers = st.number_input(
            "Number of Travelers",
            min_value=1,
            max_value=50,
            value=2
        )

    with col2:

        interests = st.multiselect(
            "Select Your Interests",
            [
                "Nature",
                "Adventure",
                "Beaches",
                "Historical Places",
                "Temples",
                "Shopping",
                "Food",
                "Photography",
                "Museums",
                "Relaxation"
            ],
            default=["Nature", "Food"]
        )

        travel_style = st.selectbox(
            "Travel Style",
            [
                "Budget-Friendly",
                "Comfortable",
                "Luxury",
                "Adventure",
                "Family Trip",
                "Solo Travel",
                "Friends Trip"
            ]
        )

        start_date = st.date_input(
            "Trip Start Date",
            value=date.today(),
            min_value=date.today(),
            max_value=date.today() + timedelta(days=730)
        )

    include_transport = st.checkbox(
        "Include transportation in the budget",
        value=True
    )

    additional_preferences = st.text_area(
        "Additional Preferences (Optional)",
        placeholder=(
            "Example: Vegetarian food, family-friendly places, "
            "avoid crowded locations..."
        )
    )

    submitted = st.form_submit_button(
        "✨ Generate My Travel Plan",
        use_container_width=True
    )


# =====================================================
# GENERATE ITINERARY
# =====================================================

if submitted:

    if not destination.strip():

        st.error("Please enter a destination.")

    elif not interests:

        st.error("Please select at least one interest.")

    elif MODEL_NAME == "PASTE_YOUR_AVAILABLE_MODEL_ID_HERE":

        st.error(
            "Please replace MODEL_NAME in app.py with a valid "
            "model ID from the Groq Models page."
        )

    else:

        api_key = get_api_key()

        if not api_key:

            st.error(
                "Groq API key not found. Configure GROQ_API_KEY "
                "in Streamlit Cloud Secrets."
            )

        else:

            prompt = f"""
You are an experienced and practical AI travel planner.

Create a detailed three-day itinerary for the user.

TRAVEL DETAILS

Destination: {destination}
Budget: INR {budget}
Travelers: {travelers}
Interests: {", ".join(interests)}
Travel style: {travel_style}
Start date: {start_date.strftime("%d %B %Y")}
Include transportation costs: {include_transport}
Additional preferences: {additional_preferences or "None"}

INSTRUCTIONS

1. Create exactly three days.
2. Divide each day into morning, afternoon, and evening.
3. Recommend relevant places and activities.
4. Suggest local food and transportation options.
5. Provide estimated costs in Indian Rupees.
6. Respect the total budget for all travelers.
7. Include accommodation and food costs where relevant.
8. Clearly state whether transportation is included.
9. Explain if the budget is insufficient.
10. Do not invent verified ticket prices, opening hours,
    hotel availability, or transport schedules.
11. Clearly label all cost estimates.
12. Include practical travel and safety tips.
13. Use clear headings, bullet points, and tables.

OUTPUT FORMAT

# Three-Day Travel Plan: {destination}

## Trip Overview

## Day 1
Morning:
Afternoon:
Evening:
Food suggestions:
Estimated expenses:

## Day 2
Morning:
Afternoon:
Evening:
Food suggestions:
Estimated expenses:

## Day 3
Morning:
Afternoon:
Evening:
Food suggestions:
Estimated expenses:

## Estimated Budget Breakdown

## Local Food Recommendations

## Transportation Suggestions

## Travel Tips

## Final Budget Summary

Compare estimated expenses with the user's budget.

Remind the user to verify current prices, opening hours,
weather, and availability before making reservations.
"""

            st.divider()

            st.subheader(f"🗺️ Your Trip to {destination}")

            try:

                client = Groq(api_key=api_key)

                with st.spinner(
                    "Planning your trip with AI... Please wait."
                ):

                    response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are a practical and reliable "
                                    "travel planning assistant. "
                                    "Clearly label estimates and "
                                    "never claim unverified information "
                                    "is current."
                                )
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0.3,
                        max_tokens=3000
                    )

                    itinerary = (
                        response.choices[0].message.content or ""
                    ).strip()

                if itinerary:

                    st.success("Your travel plan is ready!")

                    st.markdown(itinerary)

                    safe_name = (
                        destination.strip()
                        .replace(" ", "_")
                        .replace("/", "_")
                        .replace("\\", "_")
                    )

                    st.download_button(
                        label="📥 Download Travel Plan",
                        data=itinerary,
                        file_name=f"{safe_name}_travel_plan.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                    st.info(
                        "This plan is AI-generated. Verify prices, "
                        "opening hours, transport, weather, and "
                        "availability before booking."
                    )

                else:

                    st.warning(
                        "The AI returned an empty response. "
                        "Please try again."
                    )

            except Exception as error:

                st.error("Unable to generate the travel plan.")

                error_text = str(error)

                if "model_not_found" in error_text.lower():
                    st.warning(
                        "The model ID is invalid or unavailable "
                        "to your account. Check Groq's current model "
                        "list and update MODEL_NAME in app.py."
                    )

                elif "authentication" in error_text.lower() or "401" in error_text:
                    st.warning(
                        "Check that your Groq API key is correct "
                        "and has not been revoked."
                    )

                elif "429" in error_text or "rate_limit" in error_text.lower():
                    st.warning(
                        "The API usage limit may have been reached. "
                        "Check your Groq account's usage and limits."
                    )

                with st.expander("Technical error details"):
                    st.code(error_text)


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#52677d;">
        ✈️ <b>AI Travel Planner</b><br>
        Built with Python, Streamlit, and Groq AI<br>
        Plan smarter. Travel better. Explore more! 🌍
    </div>
    """,
    unsafe_allow_html=True
)