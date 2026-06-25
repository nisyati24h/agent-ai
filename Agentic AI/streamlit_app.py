import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="Smart Healthy Food Agent",
    page_icon="🥗",
    layout="wide"
)

foods = [
    {"name": "Oatmeal Buah", "calories": 300, "price": 18000, "type": "diet"},
    {"name": "Salad Sayur", "calories": 250, "price": 15000, "type": "diet"},
    {"name": "Smoothie Bowl", "calories": 350, "price": 22000, "type": "diet"},
    {"name": "Greek Yogurt", "calories": 200, "price": 17000, "type": "diet"},
    {"name": "Roti Gandum Telur", "calories": 320, "price": 15000, "type": "diet"},

    {"name": "Nasi Ayam Panggang", "calories": 500, "price": 25000, "type": "maintain"},
    {"name": "Nasi Ikan Bakar", "calories": 450, "price": 23000, "type": "maintain"},
    {"name": "Sandwich Tuna", "calories": 400, "price": 20000, "type": "maintain"},
    {"name": "Nasi Telur Dadar", "calories": 420, "price": 18000, "type": "maintain"},
    {"name": "Gado-Gado", "calories": 380, "price": 17000, "type": "maintain"},

    {"name": "Chicken Steak", "calories": 650, "price": 35000, "type": "bulking"},
    {"name": "Nasi Rendang", "calories": 700, "price": 32000, "type": "bulking"},
    {"name": "Beef Teriyaki", "calories": 680, "price": 34000, "type": "bulking"},
    {"name": "Nasi Ayam Crispy", "calories": 720, "price": 30000, "type": "bulking"},
    {"name": "Spaghetti Bolognese", "calories": 620, "price": 33000, "type": "bulking"}
]

HISTORY_FILE = "history.json"

def save_history(data):
    history = []

    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except:
            history = []

    history.append(data)

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)

st.title("🥗 Smart Healthy Food Agent")
st.markdown("### AI Nutrition Planner")

col1, col2 = st.columns(2)

with col1:
    calories = st.number_input(
        "🔥 Target Kalori Harian",
        min_value=500,
        max_value=5000,
        value=1800
    )

with col2:
    budget = st.number_input(
        "💰 Budget Harian",
        min_value=10000,
        max_value=500000,
        value=60000
    )

goal = st.selectbox(
    "🎯 Tujuan Diet",
    ["diet", "maintain", "bulking"]
)

activity = st.selectbox(
    "🏃 Aktivitas Harian",
    ["Ringan", "Sedang", "Berat"]
)

if st.button("🚀 Generate Smart Meal Plan"):

    selected_foods = [f for f in foods if f["type"] == goal]

    meal_plan = selected_foods[:3]

    total_calories = sum(item["calories"] for item in meal_plan)
    total_price = sum(item["price"] for item in meal_plan)

    st.success("Rekomendasi berhasil dibuat!")

    st.subheader("🧠 Analisis AI")

    st.write(
        f"Berdasarkan target {calories} kcal, "
        f"budget Rp{budget:,}, tujuan diet '{goal}', "
        f"dan aktivitas '{activity}', AI memilih "
        f"kombinasi menu yang paling sesuai."
    )

    st.subheader("🍽️ Meal Plan")

    for item in meal_plan:
        st.info(
            f"{item['name']} | "
            f"{item['calories']} kcal | "
            f"Rp {item['price']:,}"
        )

    st.subheader("📊 Ringkasan Nutrisi")

    st.metric(
        "Total Kalori",
        f"{total_calories} kcal"
    )

    st.metric(
        "Total Biaya",
        f"Rp {total_price:,}"
    )

    history_data = {
        "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "goal": goal,
        "calories": calories,
        "budget": budget,
        "total_calories": total_calories,
        "total_price": total_price
    }

    save_history(history_data)

st.divider()

st.subheader("📜 Riwayat Rekomendasi")

if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)

    if history:
        st.dataframe(history)
    else:
        st.write("Belum ada riwayat.")