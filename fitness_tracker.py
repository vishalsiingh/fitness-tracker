import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load Datasets
calories_df = pd.read_csv("calories(in).csv")
exercise_df = pd.read_csv("exercise(in).csv")

# Merge Data
fitness_df = pd.merge(exercise_df, calories_df, on="User_ID")

# Function to Calculate Calories Burned
def calculate_calories_burned(duration, weight, heart_rate):
    return (duration * weight * heart_rate) / 100

# Apply the function
fitness_df["Calories_Burned"] = fitness_df.apply(
    lambda row: calculate_calories_burned(row["Duration"], row["Weight"], row["Heart_Rate"]), axis=1
)

# Calculate Net Calories (Intake - Burned)
fitness_df["Net_Calories"] = fitness_df["Calories"] - fitness_df["Calories_Burned"]

# Compute BMI
fitness_df["BMI"] = fitness_df["Weight"] / ((fitness_df["Height"] / 100) ** 2)

# Streamlit UI
st.title("🏋️‍♂️ Personal Fitness Tracker")
st.sidebar.header("📊 User Filters")

# User selection
user_ids = fitness_df["User_ID"].unique()
selected_user = st.sidebar.selectbox("Select a User", user_ids)

# Display user-specific data
user_data = fitness_df[fitness_df["User_ID"] == selected_user]
st.subheader(f"📌 Fitness Summary for User {selected_user}")
st.write(user_data[["Gender", "Age", "Height", "Weight", "Duration", "Calories", "Calories_Burned", "Net_Calories", "BMI"]])

# Plot Calories Burned vs. Duration
st.subheader("🔥 Calories Burned vs. Exercise Duration")
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(x=user_data["Duration"], y=user_data["Calories_Burned"], hue=user_data["Gender"], ax=ax)
plt.xlabel("Exercise Duration (mins)")
plt.ylabel("Calories Burned")
st.pyplot(fig)

# Progress Indicator
st.subheader("📈 Progress Insights")
if user_data["Net_Calories"].values[0] < 0:
    st.success("Great job! You are burning more calories than consuming. Keep it up! 💪")
else:
    st.warning("Try to increase activity or adjust diet for better results. ⚡")

# BMI Analysis
bmi = user_data["BMI"].values[0]
if bmi < 18.5:
    st.info("Your BMI indicates you are underweight. Consider a balanced diet. 🍎")
elif 18.5 <= bmi < 24.9:
    st.success("Your BMI is in the healthy range! Keep maintaining it. ✅")
elif 25 <= bmi < 29.9:
    st.warning("You are overweight. Focus on regular exercise. 🏃‍♂️")
else:
    st.error("You are in the obese range. Consider consulting a nutritionist. 🏥")

st.sidebar.markdown("---")
st.sidebar.write("Made with ❤️ by Vishal")

