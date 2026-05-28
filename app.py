import streamlit as st
import pandas as pd
import asyncio

from duplicate_detector import group_duplicates
from normalization import normalize_text
from processor import process_all

# ---------------- CONFIG ----------------
MAX_FILE_SIZE_MB = 800
PREVIEW_ROWS = 50
ROWS_PER_PAGE = 500

st.set_page_config(
    page_title="Enterprise Exception Analyzer",
    layout="wide"
)

st.title("AI Exception Analyzer (800MB Production Mode)")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload Excel File (Max 800MB)",
    type=["xlsx"]
)

if uploaded_file:

    file_size_mb = uploaded_file.size / (1024 * 1024)
    st.write(f"File size: {file_size_mb:.2f} MB")

    if file_size_mb > MAX_FILE_SIZE_MB:
        st.error("File too large! Max allowed is 800MB")
        st.stop()

    df = pd.read_excel(uploaded_file)

    if "exception_details" not in df.columns:
        st.error("Missing required column: exception_details")
        st.stop()

    # ---------------- SUMMARY ----------------
    st.subheader("File Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Exceptions", len(df))
    col2.metric("Columns", len(df.columns))
    col3.metric(
        "Memory (MB)",
        round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2)
    )

    # ---------------- PREVIEW ----------------
    st.subheader("Preview (First 50 Rows)")

    st.info(
        f"Total Records: {len(df)} | Showing first {min(PREVIEW_ROWS, len(df))}"
    )

    st.dataframe(
        df[["exception_details"]].head(PREVIEW_ROWS),
        width="stretch",
        height=400
    )

    # ---------------- PAGINATION ----------------
    st.subheader("Paginated Data Explorer")

    total_rows = len(df)
    total_pages = (total_rows // ROWS_PER_PAGE) + 1

    page = st.number_input(
        "Page",
        min_value=1,
        max_value=total_pages,
        value=1
    )

    start = (page - 1) * ROWS_PER_PAGE
    end = start + ROWS_PER_PAGE

    page_df = df.iloc[start:end]

    st.write(
        f"Showing {start + 1} to {min(end, total_rows)} of {total_rows}"
    )

    st.dataframe(
        page_df,
        width="stretch",
        height=600
    )

    # ---------------- DUPLICATES ----------------
    st.subheader("Unique Exception View")

    grouped_df = group_duplicates(df)

    st.success(
        f"Total: {len(df)} | Unique: {len(grouped_df)}"
    )

    st.dataframe(
        grouped_df.head(200),
        width="stretch",
        height=400
    )

    # ---------------- TOP FREQUENT EXCEPTIONS ----------------
    st.subheader("Top Frequent Exceptions (High Impact)")

    top_exceptions = grouped_df.sort_values(
        by="duplicate_count",
        ascending=False
    )

    TOP_N = 20

    st.info(f"Showing Top {TOP_N} Exceptions")

    st.dataframe(
        top_exceptions[
            ["exception_details", "duplicate_count"]
        ].head(TOP_N),
        width="stretch",
        height=500
    )

    # ---------------- HIGH IMPACT FILTER ----------------
    st.subheader("High Impact Exceptions (duplicate_count > 100)")

    high_impact = grouped_df[
        grouped_df["duplicate_count"] > 100
    ].sort_values(
        "duplicate_count",
        ascending=False
    )

    st.write(
        f"Total High Impact: {len(high_impact)}"
    )

    st.dataframe(
        high_impact[
            ["exception_details", "duplicate_count"]
        ],
        width="stretch",
        height=500
    )

    # ---------------- RUN ANALYSIS ----------------
    if st.button("Run AI Analysis"):

        with st.spinner("Processing exceptions..."):

            results = asyncio.run(process_all(grouped_df))

        result_map = {
            r["normalized"]: r for r in results
        }

        df["normalized"] = df["exception_details"].apply(normalize_text)

        df["root_cause"] = df["normalized"].map(
            lambda x: result_map[x]["root_cause"]
        )

        df["comments"] = df["normalized"].map(
            lambda x: result_map[x]["comments"]
        )

        df["severity"] = df["normalized"].map(
            lambda x: result_map[x]["severity"]
        )

        df.drop(columns=["normalized"], inplace=True)

        st.success("Analysis Completed")

        st.subheader("Output Preview")

        st.dataframe(
            df.head(100),
            width="stretch",
            height=500
        )

        # ---------------- MULTI-SHEET EXPORT ----------------
        output_file = "output/analyzed_output.xlsx"
        ROWS_PER_SHEET = 200000

        total_rows = len(df)
        total_sheets = (total_rows // ROWS_PER_SHEET) + 1

        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:

            for i in range(total_sheets):

                start = i * ROWS_PER_SHEET
                end = start + ROWS_PER_SHEET

                chunk = df.iloc[start:end]

                chunk.to_excel(
                    writer,
                    sheet_name=f"Sheet_{i+1}",
                    index=False
                )

        with open(output_file, "rb") as f:

            st.download_button(
                label="Download Result Excel",
                data=f,
                file_name=output_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )