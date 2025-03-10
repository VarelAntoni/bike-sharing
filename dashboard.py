import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

sns.set(style='dark')

st.title('Bike Sharing Analysis 🚲')

add_selectitem = st.selectbox("Pilih jenis dataset yang ingin dilihat?", ("All Dataset", "Day Dataset", "Hour Dataset"))

if add_selectitem == "All Dataset":
# Load dataset
    df = pd.read_csv("all_data.csv")

    # Menampilkan data di Streamlit
    st.write("### Dataset Bike Sharing ")
    st.write(df)

elif add_selectitem == "Day Dataset":
    df = pd.read_csv("day_df.csv") 

    # Menampilkan data di Streamlit
    st.write("### Dataset Bike Sharing by Day")
    st.write(df)

elif add_selectitem == "Hour Dataset":
    df = pd.read_csv("hour_df.csv")  

    # Menampilkan data di Streamlit
    st.write("### Dataset Bike Sharing by Hour")
    st.write(df)

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("all_data.csv")

# Load the data
all_df = load_data()

# Create month order mapping
month_order = {
    'January': 0, 'February': 1, 'March': 2, 'April': 3, 'May': 4, 'June': 5,
    'July': 6, 'August': 7, 'September': 8, 'October': 9, 'November': 10, 'December': 11
}


st.title("Total Bike Rentals by Month")
# Ensure the dataset has the required columns
if 'month_day' in all_df.columns and 'cnt_day' in all_df.columns and 'month_hour' in all_df.columns and 'cnt_hour' in all_df.columns:
    # Aggregate data
    monthly_day_rentals = all_df.groupby('month_day')['cnt_day'].sum()
    monthly_hour_rentals = all_df.groupby('month_hour')['cnt_hour'].sum()
    total_monthly_rentals = monthly_day_rentals.add(monthly_hour_rentals, fill_value=0)
    total_monthly_rentals = total_monthly_rentals.dropna().sort_index()

    # Add slider for selecting month range
    min_month, max_month = st.slider("Select month range:", 0, 11, (0, 11))
    filtered_rentals = total_monthly_rentals[min_month:max_month + 1]
    
    # Plot the data
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=filtered_rentals.index, y=filtered_rentals.values, marker='o', linewidth=2.5, ax=ax)
    ax.set_xticks(range(min_month, max_month + 1))
    ax.set_xticklabels(list(month_order.keys())[min_month:max_month + 1], rotation=30)
    ax.set_title("Total Bike Rentals by Month", fontsize=14)
    ax.set_xlabel("Month", fontsize=12)
    ax.set_ylabel("Total Rentals", fontsize=12)
    ax.grid(True)
    
    st.pyplot(fig)
else:
    st.error("Dataset does not contain the required columns: 'month_day', 'cnt_day', 'month_hour', 'cnt_hour'")


st.title("Total Bike Rentals by Weather Condition")
# Ensure dataset has required weather columns
if 'weather_day' in all_df.columns and 'cnt_day' in all_df.columns and 'weather_hour' in all_df.columns and 'cnt_hour' in all_df.columns:
    # Weather condition mapping
    weather_options = ['Clear', 'Mist/Cloudy', 'Light Snow/Rain', 'Heavy Rain/Snow']
    
    # Aggregate data by weather condition
    weather_day_rentals = all_df.groupby('weather_day')['cnt_day'].sum()
    weather_hour_rentals = all_df.groupby('weather_hour')['cnt_hour'].sum()
    total_weather_rentals = weather_day_rentals.add(weather_hour_rentals, fill_value=0)
    
    # Convert to DataFrame
    weather_df = total_weather_rentals.reset_index()
    weather_df.columns = ['Weather Condition', 'Total Rentals']
    
    # Multi-select for filtering weather conditions
    selected_weather = st.multiselect("Select Weather Conditions:", weather_options, default=weather_options, key="weather_selector")
    filtered_weather_df = weather_df[weather_df['Weather Condition'].isin(selected_weather)]
    
    # Plot weather condition data
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=filtered_weather_df, x='Weather Condition', y='Total Rentals', hue='Weather Condition', dodge=False, ax=ax)
    ax.set_title("Total Bike Rentals by Weather Condition")
    ax.set_xlabel("Weather Condition")
    ax.set_ylabel("Total Rentals")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30)
    ax.legend(title="Weather Condition")
    
    st.pyplot(fig)
else:
    st.error("Dataset does not contain the required columns: 'weather_day', 'cnt_day', 'weather_hour', 'cnt_hour'")

st.write("\n")
st.write("## Conclusion")
st.write("- Dari pertanyaan pertama dapat disimpulkan bahwa mayoritas user meminjam sepeda pada bulan Februari, juli dan november, hanya sedikit yang meminjam pada bulan april dan mei, jadi penyewaan sepeda bisa menyediakan stok lebih banyak pada bulan april dan memaksimalkannya pada bulan tersebut")
st.write("- dari pertanyaan kedua dapat dilihat bahwa user lebih sering meminjam sepeda ketika cuaca sedang baik dan bersih, penyediaan sepeda pada cuaca buruk mungkin dapat dikurangin untuk meminimalisir kerusakan pada sepeda peminjaman karena cuaca buruk memiliki potensi kecil sebagai pemicu bencana alam")
