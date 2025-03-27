# app.py
import streamlit as st

# ✅ MUST be the first Streamlit command
st.set_page_config(
    page_title="Spotify Reco+ Dashboard",
    page_icon="🎧",
    layout="wide"
)

# 📦 Imports
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt


# 🎨 Dark theme and Spotify styling

custom_css = """
<style>
    body, .stApp {
        background-color: #0f1117;
        color: white;
    }

    .stMarkdown, .stText, .stDataFrame {
        color: white !important;
    }

    .stDataFrame {
        background-color: #1a1a1a;
        color: white !important;
    }

    .css-1cpxqw2, .css-1v0mbdj, .stButton>button {
        background-color: #1db954 !important;
        color: white !important;
        border-radius: 8px;
    }

    /* ✅ SLIDER STYLE – Spotify Green & Animated */
    [data-testid="stSlider"] .st-c2 {
        background: linear-gradient(to right, #1db954, #1ed760);
        height: 6px;
        border-radius: 6px;
    }

    [data-testid="stSlider"] .st-c4 {
        background-color: #1db954 !important;
        border: 3px solid white;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        box-shadow: 0 0 10px #1db954;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    [data-testid="stSlider"] .st-c4:hover {
        transform: scale(1.25);
        box-shadow: 0 0 16px #1ed760;
    }

    [data-testid="stSlider"] .css-1ptx2yq, 
    [data-testid="stSlider"] .css-1d391kg {
        color: #1db954 !important;
        font-weight: bold;
    }
</style>
"""


st.markdown(custom_css, unsafe_allow_html=True)

plt.style.use("dark_background")
sns.set_palette("summer")

# 📊 Load the data
@st.cache_data
def load_data():
    artists = pd.read_csv("datasets/artists_gp1.dat", sep="\t")
    user_artists = pd.read_csv("datasets/user_artists_gp1.dat", sep="\t")
    merged = user_artists.merge(artists, left_on="artistID", right_on="id")
    return artists, user_artists, merged

artists_df, user_artists_df, merged_df = load_data()

# ======================
# 🎧 Main Title
st.title("🎧 User Data Analysis – Spotify Reco+")

# 📋 Data Preview
st.subheader("Data Preview")
st.dataframe(merged_df.head(15))

# 🔍 Sidebar filter
st.sidebar.title("Filters")
min_listens = st.sidebar.slider("Minimum number of listens", 0, 500, 100)
filtered_df = merged_df[merged_df["weight"] >= min_listens]

# ======================
# 🎤 Top 10 Most Listened Artists
st.subheader("🎤 Top 10 Most Listened Artists")
top_artists = filtered_df.groupby("name")["weight"].sum().sort_values(ascending=False).head(10)
fig1, ax1 = plt.subplots()
top_artists.plot(kind="barh", ax=ax1, color="#1db954")
ax1.set_title("Top 10 Artists by Total Listens")
ax1.set_xlabel("Total Listens")
ax1.invert_yaxis()
st.pyplot(fig1)

# 🧠 Insight
st.markdown("### 🧠 Insights")
top_3 = top_artists.head(3)
st.markdown(f"""
- **{top_3.index[0]}** leads with **{top_3.iloc[0]:,} listens**.
- Followed by **{top_3.index[1]}** and **{top_3.index[2]}**, representing strong pop/rock influence.
- Important to balance popularity with **music discovery**.
""")

# ======================
# 👤 User Listening Diversity
st.subheader("👤 User Listening Diversity")
artist_per_user = user_artists_df.groupby("userID")["artistID"].nunique()
fig2, ax2 = plt.subplots()
sns.histplot(artist_per_user, bins=30, kde=True, ax=ax2, color="#1db954")
ax2.set_title("Number of Different Artists Listened to per User")
ax2.set_xlabel("Number of Artists")
st.pyplot(fig2)

st.markdown("### 🧠 Insights")
avg_art = artist_per_user.mean()
med_art = artist_per_user.median()
min_art = artist_per_user.min()
max_art = artist_per_user.max()
st.markdown(f"""
- Users listen to **{avg_art:.1f} artists on average** (median: {med_art}).
- Some users only listen to **{min_art}**, others up to **{max_art}** artists.
- Recommendation strategies should adapt to **explorers vs loyalists**.
""")

# ======================
# 📈 Total Listens per User
st.subheader("📈 User Activity")
total_listens = user_artists_df.groupby("userID")["weight"].sum()
fig3, ax3 = plt.subplots()
sns.histplot(total_listens, bins=30, kde=True, ax=ax3, color="#1db954")
ax3.set_title("Total Listens per User")
ax3.set_xlabel("Number of Listens")
st.pyplot(fig3)

st.markdown("### 🧠 Insights")
avg_total = total_listens.mean()
med_total = total_listens.median()
max_total = total_listens.max()
top_user = total_listens.idxmax()
st.markdown(f"""
- Average: **{avg_total:,.0f} listens**, median: **{med_total:,.0f}**.
- Top user (ID **{top_user}**) has **{max_total:,.0f} listens**.
- Indicates **a few power users dominate** listening volume.
""")

# ======================
# 🏆 Top 10 Most Active Users
st.subheader("🏆 Top 10 Most Active Users")
top_users = total_listens.sort_values(ascending=False).head(10)
fig4, ax4 = plt.subplots()
top_users.plot(kind="barh", ax=ax4, color="#1db954")
ax4.set_title("Top Users by Total Listens")
ax4.set_xlabel("Number of Listens")
ax4.invert_yaxis()
st.pyplot(fig4)

st.markdown("### 🧠 Insights")
top_ids = top_users.index.tolist()
top_vals = top_users.values.tolist()
st.markdown(f"""
- User **{top_ids[0]}** dominates with **{top_vals[0]:,} listens**.
- All top 10 users exceed **{top_vals[-1]:,} listens**.
- They are **high-value users** – ideal targets for loyalty strategies.
""")

# ======================
# ✅ Footer
st.markdown("---")
st.markdown("Project by **Jade, Daniel, Luna & Laurie** – *Spotify 💚")