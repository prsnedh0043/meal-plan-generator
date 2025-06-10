import streamlit as st
import google.generativeai as genai
from datetime import datetime
import io

# --- CONFIGURE GEMINI API ---
genai.configure(api_key="AIzaSyDtAUIRtLS1T1H5jQ2ZmcafeCenOB3vQAA")

# --- PAGE CONFIG ---
st.set_page_config(page_title="Gym Meal Planner", layout="centered")
st.markdown("""
    <style>
        body {
            background: linear-gradient(to bottom right, #1f4037, #99f2c8);
            color: white;
        }
        .stTextInput > div > div > input {
            color: black;
        }
        .stDownloadButton > button {
            background-color: #00c6ff;
            color: white;
            border-radius: 12px;
        }
    </style>
""", unsafe_allow_html=True)

# --- MAIN TITLE ---
st.title("🏋️ Gym Member Meal Planner")
st.subheader("Your Personalized Diet & Progress Tracker")

# --- USER INPUT FORM ---
with st.form("meal_form"):
    name = st.text_input("Name")
    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0)
    height = st.number_input("Height (cm)", min_value=120.0, max_value=250.0)
    goal = st.selectbox("Your Goal", ["Lose Fat", "Build Muscle", "Maintain Weight"])
    body_type = st.selectbox("Body Type", ["Ectomorph", "Mesomorph", "Endomorph"])
    diet_type = st.radio("Diet Preference", ["Vegan", "Non-Vegan"])
    cuisine = st.multiselect("Preferred Cuisine Style", ["Indian", "American", "Chinese", "Mexican", "Italian"])
    submitted = st.form_submit_button("Generate Meal Plan")

# --- GENERATE MEAL PLAN ---
if submitted:
    with st.spinner("Generating your personalized plan..."):
        prompt = f"""
        Create a professional meal plan for a gym member with the following info:
        Name: {name}
        Weight: {weight} kg
        Height: {height} cm
        Goal: {goal}
        Body Type: {body_type}
        Diet Type: {diet_type}
        Preferred Cuisine: {', '.join(cuisine)}
        Include:
        1. Detailed daily meal plan.
        2. Time-wise flowchart (e.g., 8AM - Breakfast: Oats...).
        3. Healthy gym-oriented suggestions.
        Use a formal and motivating tone.
        """

        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        plan_text = response.text

        st.success("Meal Plan Generated!")
        st.markdown("### 🥗 Your Diet Plan")
        st.markdown(plan_text)

        # --- DOWNLOAD BUTTONS ---
        diet_bytes = plan_text.encode("utf-8")
        st.download_button("📥 Download Meal Plan", data=diet_bytes, file_name=f"{name}_meal_plan.txt", mime="text/plain")

# --- PROGRESS TRACKING SECTION ---
st.markdown("---")
st.subheader("📈 Track Your Progress")
with st.form("progress_form"):
    progress_date = st.date_input("Date", value=datetime.today())
    current_weight = st.number_input("Current Weight (kg)", min_value=30.0, max_value=200.0)
    notes = st.text_area("Notes / Meals Followed Today")
    save = st.form_submit_button("Save Progress")

if save:
    st.success(f"Progress saved for {progress_date.strftime('%Y-%m-%d')}! Keep going strong 💪")

# --- FOOTER ---
st.markdown("---")
st.caption("Crafted with 💚 for fitness lovers. Powered by Gemini AI.")
