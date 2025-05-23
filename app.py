import streamlit as st
import pandas as pd
import ast
import matplotlib.pyplot as plt

st.set_page_config("Tourist Experience Analysis", layout="wide")
st.title("🌏 Aesthetic Yatra Analysis Dashboard")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("tourism_dataset_5000.csv")
    df['Interests'] = df['Interests'].apply(ast.literal_eval)
    df['Sites Visited'] = df['Sites Visited'].apply(ast.literal_eval)
    return df

df = load_data()

# Show data
if st.checkbox("Show raw data"):
    st.dataframe(df)

# Sidebar filters
st.sidebar.header("🔍 Filters")
age_range = st.sidebar.slider("Select Age Range", int(df["Age"].min()), int(df["Age"].max()), (25, 50))
interest_filter = st.sidebar.multiselect("Select Interests", ['Art', 'History', 'Architecture', 'Cultural', 'Nature'])

# Filter by age and interests
filtered_df = df[df['Age'].between(age_range[0], age_range[1])]
if interest_filter:
    filtered_df = filtered_df[filtered_df['Interests'].apply(lambda x: any(i in x for i in interest_filter))]

st.subheader("📊 Filtered Tourist Data")
st.write(filtered_df[['Tourist ID', 'Age', 'Interests', 'Site Name', 'Satisfaction']])

# Plot satisfaction distribution
st.subheader("📈 Satisfaction Distribution")
fig, ax = plt.subplots()
filtered_df['Satisfaction'].value_counts().sort_index().plot(kind='bar', ax=ax)
ax.set_xlabel("Satisfaction Level")
ax.set_ylabel("Number of Tourists")
st.pyplot(fig)

# VR experience vs. satisfaction
st.subheader("🎮 VR Experience vs Satisfaction")
fig2, ax2 = plt.subplots()
ax2.scatter(filtered_df['VR Experience Quality'], filtered_df['Satisfaction'], alpha=0.7)
ax2.set_xlabel("VR Experience Quality")
ax2.set_ylabel("Satisfaction")
st.pyplot(fig2)

# Recommendation accuracy
st.subheader("📍 Recommendation Accuracy")
st.write(f"Average Accuracy: {filtered_df['Recommendation Accuracy'].mean():.2f}%")
