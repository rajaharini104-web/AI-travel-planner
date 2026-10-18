import streamlit as st
import ollama
from datetime import date

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)

MODEL_NAME = "qwen2.5:1.5b"

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

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
        font-weight: bold;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #52677d;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .stButton > button {
        border-radius: 10px;
        min-height: 45px;
        font-weight: bold;
    }

    .stDownloadButton > button {
        border-radius: 10px;
        min-height: 45px;
        font-weight: bold;
    }

    div[data-testid="stForm"] {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #dce8f5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# APPLICATION HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">✈️ AI Travel Planner</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Plan your perfect 3-day trip with AI!</div>',
    unsafe_allow_html=True
)

st.write(
    "Discover amazing places, organize your activities, "
    "and plan your trip according to your budget."
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.header("🌍 About the Planner")

    st.write(
        "AI Travel Planner creates personalized three-day "
        "travel itineraries based on your destination, "
        "budget, interests, and preferences."
    )

    st.divider()

    st.subheader("✨ Features")

    st.write("🗺️ Personalized travel itinerary")
    st.write("📅 Three-day trip planning")
    st.write("💰 Budget estimation")
    st.write("📍 Places to visit")
    st.write("🍽️ Local food recommendations")
    st.write("🚗 Transportation suggestions")
    st.write("📥 Downloadable travel plan")

    st.divider()

    st.caption("Built with Python, Streamlit, and Ollama AI.")

# --------------------------------------------------
# TRAVEL INPUT FORM
# --------------------------------------------------

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
            "places suitable for families."
        )
    )

    submitted = st.form_submit_button(
        "✨ Generate My Travel Plan",
        use_container_width=True
    )

# --------------------------------------------------
# GENERATE TRAVEL PLAN
# --------------------------------------------------

if submitted:

    if not destination.strip():

        st.error("Please enter your destination city.")

    elif not interests:

        st.error("Please select at least one interest.")

    else:

        prompt = f"""
You are a helpful, practical, and knowledgeable AI travel planner.

Create a personalized itinerary for a three-day trip.

TRAVEL DETAILS:

Destination: {destination}
Total budget: ₹{budget}
Number of travelers: {travelers}
Interests: {", ".join(interests)}
Travel style: {travel_style}
Trip start date: {start_date.strftime("%d %B %Y")}
Include transportation costs: {"Yes" if include_transport else "No"}
Additional preferences: {special_requests if special_requests.strip() else "None"}

YOUR TASK:

Create exactly three days of travel planning.

For EACH DAY, include:

1. Morning activities.
2. Afternoon activities.
3. Evening activities.
4. Places to visit.
5. Suggested food or restaurants.
6. Estimated expenses where relevant.

BUDGET REQUIREMENTS:

1. Respect the total budget of ₹{budget} for {travelers} traveler(s).
2. Give a realistic estimated expense breakdown.
3. Include accommodation, food, local transportation, entry tickets,
   and other expenses where applicable.
4. Include transportation costs in the budget only if requested.
5. Clearly state whether the estimated total fits the budget.
6. If the budget is insufficient, suggest practical adjustments.
7. Explain that all costs are estimates and may change.

TRAVEL REQUIREMENTS:

1. Recommend places relevant to the destination and selected interests.
2. Organize nearby attractions together where practical.
3. Avoid creating an unnecessarily rushed schedule.
4. Include useful local travel tips.
5. Suggest local dishes or food options.
6. Consider the selected travel style.
7. Respect any additional preferences.
8. Do not invent exact opening hours, ticket prices, hotel availability,
   or transportation schedules.
9. If information is uncertain, clearly label it as an estimate.
10. Remind the traveler to verify current details before booking.

USE THIS OUTPUT FORMAT:

# ✈️ Three-Day Travel Itinerary: {destination}

## 1. Trip Overview
Destination, dates, number of travelers, travel style, and total budget.

## 2. Day 1: Explore the Destination
Morning:
Afternoon:
Evening:

Places to visit:
Food recommendations:
Estimated daily expenses:

## 3. Day 2: Discover More
Morning:
Afternoon:
Evening:

Places to visit:
Food recommendations:
Estimated daily expenses:

## 4. Day 3: Final Day
Morning:
Afternoon:
Evening:

Places to visit:
Food recommendations:
Estimated daily expenses:

## 5. Estimated Budget Breakdown
Provide a table showing each expense category and estimated cost in INR.

## 6. Local Food Recommendations
Suggest local dishes and suitable food options.

## 7. Transportation Suggestions
Explain practical ways to travel around the destination.

## 8. Important Travel Tips
Provide useful safety, weather, packing, and planning tips.

## 9. Budget Summary
Show the estimated total cost and compare it with the available budget.

## 10. Final Recommendation
Give a short conclusion about how to make the trip enjoyable and affordable.

Make the response well-organized, readable, practical, and detailed.
Use headings, bullet points, and tables where useful.
"""

        # --------------------------------------------------
        # DISPLAY RESULTS
        # --------------------------------------------------

        st.divider()

        st.subheader(f"🗺️ Your Trip to {destination}")

        try:

            with st.spinner(
                "✈️ Planning your trip... The AI is preparing your itinerary."
            ):

                response_area = st.empty()

                generated_text = ""

                stream = ollama.chat(
                    model=MODEL_NAME,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a reliable travel-planning assistant. "
                                "Create practical, organized, budget-conscious "
                                "travel recommendations. Clearly identify "
                                "estimates and never pretend uncertain details "
                                "are verified facts."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    stream=True,
                    options={
                        "temperature": 0.3,
                        "num_predict": 1800
                    }
                )

                for chunk in stream:

                    message = chunk.get("message", {})

                    content = message.get("content", "")

                    generated_text += content

                    response_area.markdown(
                        generated_text + " ▌"
                    )

                response_area.markdown(generated_text)

            # --------------------------------------------------
            # DOWNLOAD ITINERARY
            # --------------------------------------------------

            if generated_text.strip():

                st.success(
                    "🎉 Your travel itinerary has been generated successfully!"
                )

                safe_destination = (
                    destination.strip()
                    .replace(" ", "_")
                    .replace("/", "_")
                    .replace("\\", "_")
                )

                st.download_button(
                    label="📥 Download Your Travel Plan",
                    data=generated_text,
                    file_name=f"{safe_destination}_travel_plan.txt",
                    mime="text/plain",
                    use_container_width=True
                )

                st.info(
                    "Travel reminder: The itinerary is AI-generated. "
                    "Verify current prices, opening hours, weather, "
                    "transportation, and booking availability before travelling."
                )

            else:

                st.warning(
                    "The AI returned an empty response. Please try again."
                )

        except Exception as error:

            st.error(
                "Unable to generate the travel plan."
            )

            st.write("Please check the following:")

            st.write(
                "1. Make sure Ollama is installed on your computer."
            )

            st.write(
                "2. Make sure Ollama is running."
            )

            st.write(
                "3. Make sure the required AI model is downloaded."
            )

            st.write(
                "4. Check that your model name matches MODEL_NAME in app.py."
            )

            st.write("Error details:")

            st.code(str(error))

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown(
    """
    <div style="text-align: center; color: #52677d;">
        ✈️ <b>AI Travel Planner</b><br>
        Built with Python, Streamlit, and Ollama AI<br>
        Plan smarter. Travel better. Explore more! 🌍
    </div>
    """,
    unsafe_allow_html=True
)