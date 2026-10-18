import os
from datetime import date

import streamlit as st
from groq import Groq


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# API CONFIGURATION
# ==================================================

MODEL_NAME = "llama-3.1-8b-instant"


def get_api_key():
    """Read the Groq API key from Streamlit secrets or environment."""

    try:
        api_key = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        api_key = ""

    if not api_key:
        api_key = os.getenv("GROQ_API_KEY", "")

    return api_key


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #eef7ff, #f8f4ff);
    }

    .main-title {
        text-align: center;
        color: #244a73;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #52677d;
        font-size: 17px;
        margin-bottom: 25px;
    }

    .stButton > button,
    .stDownloadButton > button {
        border-radius: 10px;
        min-height: 45px;
        font-weight: bold;
    }

    div[data-testid="stForm"] {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 22px;
        border-radius: 15px;
        border: 1px solid #dce8f5;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #dce8f5;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# HEADER
# ==================================================

st.markdown(
    '<div class="main-title">✈️ AI Travel Planner</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Plan your perfect three-day trip with AI!'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "Discover amazing places, organize your activities, "
    "and plan your trip according to your budget and interests."
)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:
    st.header("🌍 About the Planner")

    st.write(
        "Your personal AI travel assistant creates a three-day "
        "itinerary based on your destination, budget, interests, "
        "and travel preferences."
    )

    st.divider()

    st.subheader("✨ Features")

    st.write("🗺️ Personalized itinerary")
    st.write("📅 Three-day trip planning")
    st.write("💰 Estimated budget breakdown")
    st.write("📍 Places to visit")
    st.write("🍽️ Local food suggestions")
    st.write("🚗 Transportation recommendations")
    st.write("📥 Downloadable travel plan")

    st.divider()

    st.caption("Built with Python, Streamlit, and Groq AI.")


# ==================================================
# TRAVEL INPUT FORM
# ==================================================

with st.form("travel_planner_form"):

    st.subheader("🧳 Enter Your Travel Details")

    col1, col2 = st.columns(2)

    with col1:
        destination = st.text_input(
            "📍 Destination City",
            placeholder="Example: Ooty, Chennai, Goa"
        )

        budget = st.number_input(
            "💰 Total Budget (₹)",
            min_value=1000,
            max_value=1000000,
            value=10000,
            step=1000
        )

        travelers = st.number_input(
            "👥 Number of Travelers",
            min_value=1,
            max_value=50,
            value=2,
            step=1
        )

    with col2:
        interests = st.multiselect(
            "🎯 Your Interests",
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
            "🧳 Travel Style",
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
            "📅 Trip Start Date",
            value=date.today()
        )

    include_transport = st.checkbox(
        "Include transportation costs in the budget",
        value=True
    )

    special_requests = st.text_area(
        "💬 Additional Preferences (Optional)",
        placeholder=(
            "Example: Vegetarian food, avoid crowded places, "
            "suggest famous restaurants, or recommend "
            "family-friendly attractions."
        )
    )

    submitted = st.form_submit_button(
        "✨ Generate My Travel Plan",
        use_container_width=True
    )


# ==================================================
# GENERATE THE TRAVEL ITINERARY
# ==================================================

if submitted:

    if not destination.strip():
        st.error("Please enter your destination city.")

    elif not interests:
        st.error("Please select at least one interest.")

    else:

        api_key = get_api_key()

        if not api_key:
            st.error(
                "Groq API key not found. Configure GROQ_API_KEY "
                "in your local .streamlit/secrets.toml file or "
                "in Streamlit Community Cloud secrets."
            )

            st.info(
                "Do not place your API key directly in app.py "
                "or upload it to a public GitHub repository."
            )

        else:

            client = Groq(api_key=api_key)

            transport_instruction = (
                "Include transportation costs in the budget."
                if include_transport
                else
                "Exclude transportation costs from the budget "
                "and state that they are not included."
            )

            prompt = f"""
You are a practical and knowledgeable AI travel planner.

Create a personalized itinerary for exactly three days.

TRAVEL DETAILS

Destination: {destination}
Total budget: ₹{budget}
Number of travelers: {travelers}
Interests: {", ".join(interests)}
Travel style: {travel_style}
Trip start date: {start_date.strftime("%d %B %Y")}
Transportation: {transport_instruction}
Additional preferences: {special_requests.strip() or "None"}

REQUIREMENTS

1. Create exactly three days of itinerary.
2. Divide every day into morning, afternoon, and evening.
3. Suggest attractions appropriate for the destination and interests.
4. Group nearby attractions together where practical.
5. Recommend local dishes and food options.
6. Suggest suitable transportation options.
7. Give an estimated budget breakdown in Indian Rupees.
8. Consider accommodation, food, local transport, tickets, and other
   relevant expenses.
9. Respect the budget of ₹{budget} for {travelers} traveler(s).
10. If the budget is insufficient, explain why and suggest adjustments.
11. Do not claim to have checked live prices or availability.
12. Clearly label costs as estimates.
13. Do not invent exact opening hours, ticket prices, or schedules.
14. Include useful safety, weather, and packing tips.
15. Make the itinerary easy to read with headings and bullet points.

OUTPUT FORMAT

# Three-Day Travel Itinerary: {destination}

## Trip Overview

## Day 1: Explore the Destination
Morning:
Afternoon:
Evening:
Food suggestions:
Estimated expenses:

## Day 2: Discover More
Morning:
Afternoon:
Evening:
Food suggestions:
Estimated expenses:

## Day 3: Final Day
Morning:
Afternoon:
Evening:
Food suggestions:
Estimated expenses:

## Estimated Budget Breakdown

Show expense categories and estimated costs in INR.

## Local Food Recommendations

## Transportation Suggestions

## Important Travel Tips

## Budget Summary

Compare the estimated total with the available budget.
Clarify what is included and excluded.

## Final Recommendation

Remind the traveler to verify current prices, opening hours,
weather, and availability before making bookings.
"""

            st.divider()

            st.subheader(f"🗺️ Your Trip to {destination}")

            try:
                with st.spinner(
                    "✈️ Your AI travel assistant is preparing your itinerary..."
                ):

                    response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are a reliable AI travel planner. "
                                    "Create practical, organized, budget-aware "
                                    "travel plans. Clearly label estimates and "
                                    "never pretend uncertain information "
                                    "has been verified."
                                )
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0.4,
                        max_tokens=3500
                    )

                    generated_text = (
                        response.choices[0].message.content or ""
                    ).strip()

                if generated_text:

                    st.success(
                        "🎉 Your travel itinerary is ready!"
                    )

                    st.markdown(generated_text)

                    st.download_button(
                        label="📥 Download Your Travel Plan",
                        data=generated_text,
                        file_name=(
                            destination.strip().replace(" ", "_")
                            + "_travel_plan.txt"
                        ),
                        mime="text/plain",
                        use_container_width=True
                    )

                    st.info(
                        "Travel reminder: This itinerary is AI-generated. "
                        "Verify current prices, opening hours, weather, "
                        "transport options, and availability before booking."
                    )

                else:
                    st.warning(
                        "The AI returned an empty response. Please try again."
                    )

            except Exception as error:
                st.error(
                    "We couldn't generate your travel itinerary."
                )

                st.write(
                    "Check your internet connection, Groq API key, "
                    "account usage limits, and model availability."
                )

                with st.expander("View technical error"):
                    st.code(str(error))


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.markdown(
    """
    <div style="text-align: center; color: #52677d;">
        ✈️ <b>AI Travel Planner</b><br>
        Built with Python, Streamlit, and Groq AI<br>
        Plan smarter. Travel better. Explore more! 🌍
    </div>
    """,
    unsafe_allow_html=True
)