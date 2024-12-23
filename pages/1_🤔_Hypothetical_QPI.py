import streamlit as st
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP

# Page Layout
st.set_page_config(
    page_title="Hypothetical_QPI",
    page_icon="🤔"
    )

st.title("Hypothetical QPI Calculator")
st.divider()

# Default states
if "courses_data" not in st.session_state:
    st.session_state.courses_data = [
        {"Course Code": "", "Letter Grade": "A", "Units": 3}
    ]

# Add and reset buttons
btn_cols = st.columns([1, 9])
with btn_cols[0]:
    add_course = st.button("Add")
with btn_cols[1]:
    reset_button = st.button("Reset")

# Add a new course row with default values
if add_course:
    st.session_state.courses_data.append({
        "Course Code": "",
        "Letter Grade": "A",
        "Units": 3,
    })

# Resetting to default states
if reset_button:
    st.session_state.courses_data = [
        {"Course Code": "", "Letter Grade": "A", "Units": 3}
    ]
    st.rerun()

# Layout of user input
grid = st.columns(4)

with grid[0]:
    st.write("**Course Code**")
with grid[1]:
    st.write("**Letter Grade**")
with grid[2]:
    st.write("**Units**")
with grid[3]:
    st.markdown("<p style='color:white'>Delete</p>", unsafe_allow_html=True)

# Display rows dynamically
def display_rows():
    updated_data = []

    for index, row in enumerate(st.session_state.courses_data):
        with grid[0]:
            course_code = st.text_input(
                "Course",
                value=row["Course Code"],
                label_visibility="collapsed",
                key=f"course_{index}",
            )
        with grid[1]:
            letter_grade = st.selectbox(
                "Grade",
                ("A", "B+", "B", "C+", "C", "D", "F", "W"),
                index=["A", "B+", "B", "C+", "C", "D", "F", "W"].index(row["Letter Grade"]),
                label_visibility="collapsed",
                key=f"grade_{index}",
            )
        with grid[2]:
            units = st.selectbox(
                "Units",
                (1, 2, 3, 4, 5, 6),
                index=row["Units"] - 1,
                label_visibility="collapsed",
                key=f"units_{index}",
            )
        with grid[3]:
            if st.button("Delete", key=f"delete_{index}"):
                st.session_state.courses_data.pop(index)
                st.rerun()

        updated_data.append({
            "Course Code": course_code,
            "Letter Grade": letter_grade,
            "Units": units,
        })

    # Update session state with modified data
    st.session_state.courses_data = updated_data

# Call to display all rows
display_rows()

# Calculate QPI
def calculate_qpi():
    if not st.session_state.courses_data:
        st.write("No courses to calculate.")
        return

    grades_df = pd.DataFrame(st.session_state.courses_data)
    weight = {"A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5, "C": 2.0, "D": 1.0, "F": 0.0, "W": 0.0}
    grades_df["Quality Point (QP)"] = grades_df["Letter Grade"].map(weight)
    grades_df["Weighted QP"] = grades_df["Units"].astype(float) * grades_df["Quality Point (QP)"]

    total_units = grades_df["Units"].sum()
    qpi = (
        Decimal(str(grades_df["Weighted QP"].sum() / total_units))
        .quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if total_units > 0
        else Decimal("0.00")
    )

    st.header(f"QPI: {qpi}")

# Show results
calculate_qpi()