from normalization import normalize_text

def group_duplicates(df):

    df["normalized"] = df["exception_details"].apply(normalize_text)

    counts = df["normalized"].value_counts().to_dict()

    grouped = df.groupby("normalized").agg({
        "exception_details": "first"
    }).reset_index()

    grouped["duplicate_count"] = grouped["normalized"].map(counts)

    return grouped