import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from decimal import Decimal, ROUND_HALF_UP

st.set_page_config(
    page_title="Semestral_and_Cumulative_QPI",
    page_icon="🏅"
    )

st.title("Semestral and Cumulative QPI Calculator")
st.divider()

grades_input = st.text_area("Paste your grades from AISIS:", label_visibility="collapsed", placeholder = "Paste your grades from AISIS.")

weight = {"A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5, "C": 2.0, "D": 1.0, "F": 0, "W": 0}

if st.button("Submit"):
    if grades_input:
        data = [row.split("\t") for row in grades_input.split("\n") if row.strip()]
        headers = data[0]
        rows = data[1:]
        grades_df = pd.DataFrame(rows, columns=headers)

        delete_cols = [2,4]
        grades_df = grades_df.drop(grades_df.columns[delete_cols], axis=1)
        grades_df["Department"] = grades_df["Subject Code"].str.split().str[0]

        delete_subs = ["INTACT", "PHYED", "NSTP"]
        grades_df = grades_df[~grades_df[["Department"]].isin(delete_subs).any(axis=1)]

        grades_df = grades_df.iloc[:, [0,1,2,5,3,4]]

        weight = {"A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5, "C": 2.0, "D": 1.0, "F": 0, "W": 0}

        grades_df["Units"] = pd.to_numeric(grades_df["Units"], errors="coerce")
        grades_df["Quality Point (QP)"] = grades_df["Final Grade"].map(weight)
        grades_df = grades_df.dropna(subset=["Units", "Final Grade"])
        grades_df["Weighted QP"] = grades_df["Units"] * grades_df["Quality Point (QP)"]

        total_units_per_sem = grades_df.groupby(["School Year", "Sem"])["Units"].sum()
        weighted_sum_per_sem = grades_df.groupby(["School Year", "Sem"])["Weighted QP"].sum()
        
        semestral_qpi = ((weighted_sum_per_sem / total_units_per_sem)
            .apply(lambda x: Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) if x > 0 else Decimal("0.00")))

        cum_units = grades_df["Units"].sum()
        cum_weighted_sum = grades_df["Weighted QP"].sum()

        if cum_units > 0:
            cum_qpi = Decimal(str(cum_weighted_sum / cum_units)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        else:
            cum_qpi = Decimal("0.00")

        # cumulative_qpi = 

        # st.dataframe(grades_df)

        # Extract unique semester combinations
        unique_semesters = grades_df[["School Year", "Sem"]].drop_duplicates()

        if len(unique_semesters) == 1:
            # Single semester case
            single_semester = unique_semesters.iloc[0]
            school_year, sem = single_semester["School Year"], single_semester["Sem"]
            
            # Extract the QPI for the specific semester from semestral_qpi
            qpi = semestral_qpi.loc[(school_year, sem)]
            
            st.header(f"{school_year} Sem {sem} QPI: {qpi}")
        else:
            # Multiple semesters
            st.header(f"Cumulative QPI: {cum_qpi}")

            st.subheader("QPI per Semester")
            fig, ax = plt.subplots()
            x_labels = [f"{year} Sem {sem}" for year, sem in semestral_qpi.index]
            ax.plot(x_labels, semestral_qpi, marker="o")
            ax.set_title("QPI per Semester")
            ax.set_xlabel("School Year and Semester")
            ax.set_ylabel("QPI")
            ax.grid(True)
            plt.xticks(rotation=45)
            st.pyplot(fig)

    else:
        st.write("No courses to calculate.")