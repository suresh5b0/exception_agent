# output_file = "output/analyzed_output.xlsx"

# ROWS_PER_SHEET = 200000

# total_rows = len(df)

# total_sheets = (
#     total_rows // ROWS_PER_SHEET
# ) + 1

# with pd.ExcelWriter(
#     output_file,
#     engine="openpyxl"
# ) as writer:

#     for sheet_num in range(total_sheets):

#         start_row = (
#             sheet_num
#             * ROWS_PER_SHEET
#         )

#         end_row = (
#             start_row
#             + ROWS_PER_SHEET
#         )

#         chunk_df = df.iloc[
#             start_row:end_row
#         ]

#         sheet_name = (
#             f"Exceptions_"
#             f"{sheet_num + 1}"
#         )

#         chunk_df.to_excel(
#             writer,
#             sheet_name=sheet_name,
#             index=False
#         )

# st.success(
#     f"""
#     Analysis completed.
#     Generated {total_sheets} sheets.
#     """
# )

# with open(
#     output_file,
#     "rb"
# ) as f:

#     st.download_button(
#         label="Download Output Excel",
#         data=f,
#         file_name=output_file,
#         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#     )