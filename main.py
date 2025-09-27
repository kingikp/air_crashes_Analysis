import pandas as pd
import streamlit as st
import altair as alt

# ===============================
# Load Data
# ===============================
@st.cache_data
def load_data():
    df = pd.read_csv("Cleaned_Crashes.csv")
    df.insert(0, "Crash_ID", range(1, len(df) + 1))
    return df

df = load_data()


# Dashboard Title
st.title("✈ Air Crashes Analysis Dashboard")



# Sidebar Filters
st.sidebar.header("🔎 Filters")




filters = {
    "Year": df["Year"].dropna().unique(),
    "Quarter": df["Quarter"].dropna().unique(),
    "Country/Region": df["Country/Region"].dropna().unique(),
    "Operator": df["Operator"].dropna().unique(),
    "Month": df["Month"].dropna().unique(),
}

# Store selections
selected_filters = {}
for key, options in filters.items():
    selected_filters[key] = st.sidebar.multiselect(key, sorted(options))

# Apply filters
filtered_df = df.copy()
for key, selected_values in selected_filters.items():
    if selected_values:
        filtered_df = filtered_df[filtered_df[key].isin(selected_values)]

# ===========================
# Section 2: Calculations
# ===========================
total_crashes = len(filtered_df)
total_aboard = filtered_df["Aboard"].sum()
avg_fatalities_air = filtered_df["Fatalities (air)"].mean()
ground_fatalities = filtered_df["Ground"].sum()

st.dataframe(filtered_df)

# Display a quick overview using metrics
st.write("### Quick Overview")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Crashes: ", total_crashes)
with col2:
    st.metric("Total aboard: ", f"{total_aboard:,.2f}")
with col3:
    st.metric("Air Fatalities: ", f"{avg_fatalities_air:,.2f}")
with col4:
    st.metric("Ground fatalities: ", f"{ground_fatalities:,.2f}")
    




# RQ1. How many air crashes occurred per year?

st.write("### 1. How many air crashes occurred per year?")

temp = filtered_df.groupby("Year").size().reset_index(name="Total Crashes").sort_values(by="Year")

st.dataframe(temp)

chart = alt.Chart(temp).mark_line(point=True).encode(
    x=alt.X("Year:N", title="Year"),
    y=alt.Y("Total Crashes:Q", title="Crashes"),
    color=alt.value("steelblue")
).properties(height=400)

st.altair_chart(chart, use_container_width=True)



# RQ2. Which quarter or month records the most crashes?

st.write("### 2. Which quarter/month records the most crashes?")

quarter_data = filtered_df.groupby("Quarter").size().reset_index(name="Crashes")
month_data = filtered_df.groupby("Month").size().reset_index(name="Crashes")

st.dataframe(quarter_data)
st.dataframe(month_data)

chart_q = alt.Chart(quarter_data).mark_bar().encode(
    x=alt.X("Quarter:N"),
    y=alt.Y("Crashes:Q"),
    color=alt.Color("Quarter:N", legend=None)
).properties(height=300)

chart_m = alt.Chart(month_data).mark_bar().encode(
    x=alt.X("Month:N"),
    y=alt.Y("Crashes:Q"),
    color=alt.Color("Month:N", legend=None)
).properties(height=300)

st.altair_chart(chart_q, use_container_width=True)
st.altair_chart(chart_m, use_container_width=True)


# RQ3. Which countries/regions had the highest number of crashes?

st.write("### 3. Which countries/regions had the highest crashes?")
temp3 = filtered_df.groupby("Country/Region").size().reset_index(name="Crashes").sort_values(by="Crashes", ascending=False).head(15)
st.dataframe(temp3)
chart3 = alt.Chart(temp3).mark_bar().encode(
    x=alt.X("Crashes:Q"),
    y=alt.Y("Country/Region:N", sort='-x'),
    color=alt.Color("Country/Region:N", legend=None),
    tooltip=["Country/Region", "Crashes"]
).properties(height=500, title="Top Countries by Crashes")
st.altair_chart(chart3, use_container_width=True)


# RQ4. Which aircraft manufacturers appear most frequently?

st.write("### 4. Which aircraft manufacturers appear most in crashes?")
temp4 = filtered_df.groupby("Aircraft Manufacturer").size().reset_index(name="Crashes").sort_values(by="Crashes", ascending=False).head(15)
st.dataframe(temp4)
chart4 = alt.Chart(temp4).mark_bar().encode(
    x=alt.X("Crashes:Q"),
    y=alt.Y("Aircraft Manufacturer:N", sort='-x'),
    color=alt.Color("Aircraft Manufacturer:N", legend=None),
    tooltip=["Aircraft Manufacturer", "Crashes"]
).properties(height=500, title="Top Aircraft Manufacturers in Crashes")
st.altair_chart(chart4, use_container_width=True)



# RQ5. Which operators are most commonly involved?

st.write("### 5. Which operators are most commonly involved?")

temp = filtered_df.groupby("Operator").size().reset_index(name="Crashes").sort_values(by="Crashes", ascending=False)

st.dataframe(temp.head(10))

chart = alt.Chart(temp.head(15)).mark_bar().encode(
    x=alt.X("Crashes:Q"),
    y=alt.Y("Operator:N", sort='-x'),
    color=alt.Color("Operator:N", legend=None)
).properties(height=500)

st.altair_chart(chart, use_container_width=True)



# RQ6. Top 15 Operators with most fatalities
st.write("### 6. Average number aboard vs fatalities")
temp9 = (
    filtered_df.groupby("Operator")[["Fatalities (air)"]]
    .sum()
    .reset_index()
    .sort_values(by="Fatalities (air)", ascending=False)
    .head(15)
)

st.dataframe(temp9)

chart6 = alt.Chart(temp9).mark_bar(color="red").encode(
    x=alt.X("Fatalities (air):Q", title="Fatalities"),
    y=alt.Y("Operator:N", sort="-x"),
    tooltip=["Operator", "Fatalities (air)"]
)

st.altair_chart(chart6, use_container_width=True)


st.write("### Debug: Columns in dataset")
st.write(filtered_df.columns.tolist())

# RQ7.How does the fatality rate (fatalities + aboard) vary by manufacturer?

st.write("### 7 How does the fatality rate (fatalities + aboard) vary by manufacturer?")
temp = filtered_df[['Aboard', 'Fatalities (air)']].mean().reset_index()
temp.columns = ["Category", "Average"]

st.dataframe(temp)

chart = alt.Chart(temp).mark_bar().encode(
    x=alt.X("Category:N"),
    y=alt.Y("Average:Q"),
    color=alt.Color("Category:N", legend=None)
).properties(height=500)

st.altair_chart(chart, use_container_width=True)

# RQ 8. the deadliest crashes (Fatalities

st.write("### 8. Which year or country had the deadliest crashes?")
temp = filtered_df.groupby('Year')['Fatalities (air)'].sum().reset_index().sort_values(by='Fatalities (air)', ascending=False)
temp.columns = ["Year", "Total Fatalities"]

st.dataframe(temp)

chart = alt.Chart(temp).mark_bar().encode(
    x=alt.X("Year:N"),
    y=alt.Y("Total Fatalities:Q"),
    color=alt.Color("Year:N", legend=None)
).properties(height=500)

st.altair_chart(chart, use_container_width=True)


#    RQ9: Survival patterns (Aboard vs Fatalities) across regions ---
st.write("### 9. Survival Patterns (Aboard vs Fatalities) Across Regions")

# check which fatalities column exists
fatalities_col = None
if "Fatalities" in filtered_df.columns:
    fatalities_col = "Fatalities"
elif "Fatalities (air)" in filtered_df.columns:
    fatalities_col = "Fatalities (air)"

if fatalities_col and "Aboard" in filtered_df.columns and "Country/Region" in filtered_df.columns:
    # prepare data (using totals)
    temp9 = (
        filtered_df.groupby("Country/Region")[["Aboard", fatalities_col]]
        .sum()
        .reset_index()
        .sort_values(by="Aboard", ascending=False)
        .head(15)  # show top 15 regions
    )

    st.dataframe(temp9)

    # chart: side-by-side bars
    chart9 = alt.Chart(temp9).transform_fold(
        ["Aboard", fatalities_col],
        as_=["Measure", "Value"]
    ).mark_bar().encode(
        x=alt.X("Country/Region:N", sort="-y"),
        y=alt.Y("Value:Q"),
        color=alt.Color("Measure:N", title="Category"),
        tooltip=["Country/Region:N", "Measure:N", "Value:Q"]
    ).properties(
        height=500,
        width=700
    )

    st.altair_chart(chart9, use_container_width=True)
else:
    st.error("❌ Columns 'Aboard' or 'Fatalities' not found — check dataset headers.")


#   RQ10: Which operators have the most crashes on air? ---
st.write("### 10. What are the survival patterns (aboard vs fatalities) across regions?")

if "Operator" in filtered_df.columns:
    # count crashes per operator
    temp10 = (
        filtered_df.groupby("Operator")
        .size()
        .reset_index(name="Total Crashes")
        .sort_values(by="Total Crashes", ascending=False)
        .head(15)  # show top 15 operators
    )

    st.dataframe(temp10)

    # bar chart
    chart10 = alt.Chart(temp10).mark_bar().encode(
        x=alt.X("Operator:N", sort="-y"),
        y=alt.Y("Total Crashes:Q"),
        tooltip=["Operator:N", "Total Crashes:Q"],
        color=alt.Color("Total Crashes:Q", scale=alt.Scale(scheme="reds"))
    ).properties(
        width=700,
        height=500,
        title="Top 15 Operators with Most Crashes"
    )

    st.altair_chart(chart10, use_container_width=True)
else:
    st.error("❌ Column 'Operator' not found in dataset.")
