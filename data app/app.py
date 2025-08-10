import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import altair as alt
import plotly.express as px
import math

#To look at more streamlit additions, go to: docs.streamlit.io/develop/api-reference/widgets

#fill nulls with defaults
def fill_nulls(df):

    def default_for_dtype(dtype):
        if pd.api.types.is_numeric_dtype(dtype):
            return 0
        elif pd.api.types.is_bool_dtype(dtype):
            return False
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            return #pd.Timestamp("2000-01-01")
        else:
            return "N/A"  #default

    #dict of defaults for the fillna call
    fill_values = {
        col: default_for_dtype(dtype)
        for col, dtype in df.dtypes.items()
    }

    return df.fillna(fill_values)

#ingest data
def ingest_data(df):
    if any(col.startswith("Unnamed") for col in df.columns):
        st.warning("Databse ingestion stopped: There are unnamed columns, make sure all columns in Excel sheet have a name")
        return
    
    if df.empty:
        st.warning("Excel sheet is empty, make sure you uploaded the correct file")
        return

    #should it check for nulls? ensuring no null spaces would help with creating graphs later on, but will require more work on the user at the start
    #df = fill_nulls(df)

    # Database connection
    engine = create_engine("sqlite:///data/database.db")
    df.to_sql(table_name, engine, if_exists="append", index=False)
    st.success("Data saved to SQLite database.")

#------------------------------------------------------------------------------------------------------
#App code starts here
#------------------------------------------------------------------------------------------------------

# Title
st.title("DA MVP Dashboard")

st.text("Upload your file and fill in the text field for the\nname of the table you want your data added to.")
# File uploader
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
# Text input - This is used for the name of the table in the database
table_name = st.text_input("Name of Table in Database")

# text warning before clicking read file
st.subheader("WARNING: Make sure you have the table name text field filled out and a file uploaded before clicking the Read File button.")

#if uploaded_file:
if st.button("Read File"):
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    st.success("File uploaded successfully!")
    st.write(df.head())

    ingest_data(df)

#choose which table to graph
engine = create_engine("sqlite:///data/database.db")
table_names = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'", engine)
table_names = table_names["name"].to_list()
#print(table_names)
choice = st.selectbox("Select table you want to view", table_names)

if len(table_names) == 0:
    st.warning("No tables in the database, add one to use the graphing features!")

else:
    column_names = pd.read_sql("SELECT * FROM " + choice, engine)
    #print(column_names)
    column1 = st.selectbox("Select column you want to view", column_names.columns.to_list())

    chart_type = st.radio("Choose chart type:", ["Bar Chart", "Pie Chart"])

    # Display stored data
    if st.button("View All Transactions"):
        engine = create_engine("sqlite:///data/database.db")
        df = pd.read_sql("SELECT * FROM " + choice, engine)
        

        # chart test stuff
        # if(choice == "xycoords"):
        #     #df = df.drop(columns=["index"])
        #     xy = df[["X-Coord", "Y-Coord"]].rename(columns={"X-Coord": "x", "Y-Coord": "y"})

        #     chart = alt.Chart(xy).mark_circle().encode(
        #         x="x",
        #         y="y"
        #     )

        #     st.altair_chart(chart, use_container_width=True)
        #     st.scatter_chart(xy)

        # if(choice == "crossroads1"):
        #freq = pd.read_sql("SELECT Gender, COUNT(*) AS frequency FROM crossroads1 GROUP BY Gender ORDER BY frequency DESC", engine)
        freq = pd.read_sql("SELECT \"" + column1 + "\", COUNT(*) AS frequency FROM \"" + choice + "\" WHERE \"" + column1 + "\" != 'unknown' GROUP BY \"" + column1 + "\" ORDER BY frequency DESC", engine)

        #grouping for numbers
        try:
            freq[column1] = pd.to_numeric(freq[column1])
            print("numeric!")
            max = freq[column1].max()
            max = math.ceil(max / 5) * 5
            bin_size = int(max / 10)
            #cuts
            bins = list(range(0, max, bin_size))
            freq[column1] = pd.cut(freq[column1], bins=bins)

            #freq[column1] = pd.cut(freq[column1], bins=10)
            freq = freq.groupby(column1, observed=False)['frequency'].sum().reset_index()
            freq[column1] = freq[column1].astype(str)
        except ValueError:
            #can ignore since its not numeric! im so smart
            pass
        
        #grouping for dates
        try:
            freq[column1] = pd.to_datetime(freq[column1])
            print("datatime!")
            min_date = freq[column1].min()
            max_date = freq[column1].max()

            rounded_min = pd.Timestamp(year=min_date.year, month=1, day=1)
            rounded_max = pd.Timestamp(year=max_date.year + 1, month=1, day=1)

            date_range = max_date - min_date

            bin_size = ''
            if date_range <= pd.Timedelta(days=365):
                bin_size = 'MS' # month start
            elif date_range <= pd.Timedelta(days=365*5):
                bin_size = 'QS' #quarter start
            
            else:
                bin_size = 'YS' #year start

            bins = pd.date_range(start=rounded_min, end=rounded_max + pd.Timedelta(days=1), freq=bin_size)

            freq[column1] = pd.cut(freq[column1], bins=bins)
            freq = freq.groupby(column1, observed=False)['frequency'].sum().reset_index()
            #freq[column1] = freq[column1].astype(str)

            freq[column1] = freq[column1].apply(lambda x: f"Year: {x.left.year}")
        except:
            pass

        #freq[column1] = pd

        if chart_type == "Bar Chart":
            freq[column1] = freq[column1].astype(str)

            freq = freq.sort_values(by="frequency", ascending=False).reset_index(drop=True)

            categories = freq[column1].drop_duplicates().tolist()

            fig = px.bar(freq, x=column1, y="frequency", title="User Count by " + column1, category_orders={column1: categories})

            fig.update_layout(xaxis_tickangle=-45, xaxis={'type': 'category'})
        else:
            fig = px.pie(freq, names=column1, values="frequency", title="User Count by " + column1)
            
        st.plotly_chart(fig)
        st.dataframe(freq)
        st.dataframe(df)