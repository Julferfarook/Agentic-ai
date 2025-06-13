import streamlit as st
import google.generativeai as genai
from datetime import datetime
from fpdf import FPDF

# ---- Gemini API Setup ----
genai.configure(api_key="AIzaSyCRH7VbZYOGX4YV_7PNhv0TUVTQvcchhno")
model = genai.GenerativeModel("gemini-2.0-flash")

# ---- App Theme & Branding ----
st.set_page_config(page_title="🧬 Gym Fuel: AI Diet Planner", layout="centered")
st.markdown("""
<style>
    html, body {
        background: linear-gradient(to bottom right, #2c3e50, #4ca1af);
        color: #fff;
    }
    .stTextInput, .stNumberInput, .stSelectbox, .stRadio, .stMultiselect {
        color: black !important;
    }
    .stDownloadButton > button {
        background-color: #f39c12;
        color: white;
        font-weight: bold;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---- Title ----
st.title("🏋️‍♂️ Gym Fuel: AI Diet Planner")
st.caption("Eat Clean. Lift Heavy. Powered by Gemini AI ⚡")

# ---- Input Form ----
with st.form("input_form"):
    st.subheader("🎯 Personalization")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Name")
        weight = st.number_input("Current Weight (kg)", 40.0, 200.0)
        height = st.number_input("Height (cm)", 130.0, 220.0)
    with col2:
        goal = st.selectbox("Fitness Goal", ["Lose Fat", "Build Muscle", "Stay Fit"])
        body_type = st.selectbox("Body Type", ["Ectomorph", "Mesomorph", "Endomorph"])
        diet_type = st.radio("Diet Preference", ["Vegan", "Non-Vegan"])

    cuisine = st.multiselect("🍽️ Preferred Cuisines", ["Indian", "Italian", "Mexican", "American", "Chinese"])
    submitted = st.form_submit_button("Generate AI Meal Plan")

# ---- Meal Plan Generation ----
if submitted:
    with st.spinner("🧠 Gemini is cooking your personalized meal plan..."):
        prompt = f"""
        You're a certified fitness coach and expert nutritionist.
        Design a professional, highly motivating weekly meal plan based on:

        Name: {name}
        Weight: {weight} kg
        Height: {height} cm
        Goal: {goal}
        Body Type: {body_type}
        Diet Type: {diet_type}
        Cuisine Preferences: {', '.join(cuisine)}

        Include:
        - A 7-day meal plan with breakfast, lunch, dinner and snacks.
        - Time-wise structured flow (e.g., 7AM - Breakfast: ...).
        - Nutrition tips for gym goers.
        - Daily motivational quotes.
        Return it in a friendly, structured format.
        """

        try:
            response = model.generate_content(prompt)
            plan_text = response.text

            # ---- Display Output ----
            st.success("✅ Meal Plan Ready!")
            st.markdown("### 🥗 Your Gemini-Crafted Diet Plan")
            st.markdown(plan_text)

            # ---- Generate PDF for Download ----
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for line in plan_text.split("\n"):
                pdf.multi_cell(0, 10, txt=line)

            file_path = f"/mnt/data/{name.replace(' ', '_')}_diet_plan.pdf"
            pdf.output(file_path)
            with open(file_path, "rb") as f:
                st.download_button("📄 Download Meal Plan PDF", f, file_name=f"{name}_diet_plan.pdf", mime="application/pdf")

        except Exception as e:
            st.error("⚠️ Error generating plan.")
            st.exception(e)

# ---- Progress Tracker ----
st.markdown("---")
st.subheader("📆 Daily Progress Journal")

with st.form("progress_log"):
    log_date = st.date_input("Log Date", datetime.today())
    logged_weight = st.number_input("Today's Weight (kg)", 40.0, 200.0)
    notes = st.text_area("📒 Notes (workouts, meals followed, etc.)")
    log_submit = st.form_submit_button("Save Entry")

if log_submit:
    st.success(f"Progress logged for {log_date.strftime('%Y-%m-%d')} 💪")
    st.balloons()

# ---- Footer ----
st.markdown("---")
st.caption("Made with 💚 for gym warriors. | Powered by Gemini Flash 2.0")
