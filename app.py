import streamlit as st
import pandas as pd
from scoring import score_leads

st.set_page_config(page_title="Lead Scoring Tool", layout="wide")
st.title("📊 Lead Scoring & Export Tool")

st.markdown("""
Upload your leads data to automatically get a priority score based on revenue, number of employees, and industry.
""")

# Function to clean and convert data types
def clean_data(df):
    df['Revenue ($M)'] = pd.to_numeric(df['Revenue ($M)'], errors='coerce')
    df['Employees'] = pd.to_numeric(df['Employees'], errors='coerce')
    df.dropna(subset=['Revenue ($M)', 'Employees'], inplace=True)
    return df

# File upload
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("data/sample_leads.csv")

# Clean data before scoring
df = clean_data(df)

# Calculate scores
scored_df = score_leads(df)

# Filter by lead score (label)
score_label_filter = st.selectbox("Filter by Lead Score", ["All", "High", "Medium", "Low"])

# Filter by score (numeric)
score_min = st.slider("Minimum Score", min_value=0, max_value=10, value=0)
score_max = st.slider("Maximum Score", min_value=0, max_value=10, value=10)

# Apply filters
if score_label_filter != "All":
    scored_df = scored_df[scored_df["Score Label"] == score_label_filter]

if score_min > 0 or score_max < 10:
    scored_df = scored_df[(scored_df["Score"] >= score_min) & (scored_df["Score"] <= score_max)]

# Reset index and add 'No.' column
scored_df = scored_df.reset_index(drop=True)
scored_df.insert(0, "No.", scored_df.index + 1)

# Pagination settings
PAGE_SIZES = [25, 50, 100, "All"]
page_size = st.selectbox("Items per page", PAGE_SIZES, index=0)

# Handle "All" option
if page_size == "All":
    page_size = len(scored_df)

# Calculate total pages
total_pages = (len(scored_df) + page_size - 1) // page_size

# Initialize session state for current page if not exists
if "current_page" not in st.session_state:
    st.session_state.current_page = 1

# Navigation buttons and page info
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("Previous"):
        st.session_state.current_page -= 1
        st.session_state.current_page = max(1, st.session_state.current_page)

with col2:
    st.write(f"Page {st.session_state.current_page} of {total_pages}")

with col3:
    if st.button("Next"):
        st.session_state.current_page += 1
        st.session_state.current_page = min(total_pages, st.session_state.current_page)

# Get current page data
start_idx = (st.session_state.current_page - 1) * page_size
end_idx = start_idx + page_size
page_data = scored_df.iloc[start_idx:end_idx]

# Display the data with formatted columns
st.data_editor(
    page_data,
    use_container_width=True,
    hide_index=True,
    column_config={
        "No.": st.column_config.NumberColumn("No.", format="%d"),
        "Company": st.column_config.TextColumn("Company"),
        "Industry": st.column_config.TextColumn("Industry"),
        "Revenue ($M)": st.column_config.NumberColumn("Revenue ($M)", format="$%.2fM"),
        "Employees": st.column_config.NumberColumn("Employees", format="%d"),
        "Location": st.column_config.TextColumn("Location"),
        "Score": st.column_config.NumberColumn("Score", format="%d"),
        "Score Label": st.column_config.TextColumn("Score Label"),
    },
)

# Download CSV
csv = scored_df.to_csv(index=False).encode('utf-8')
st.download_button("⬇️ Download Scored Leads as CSV", csv, "scored_leads.csv", "text/csv")