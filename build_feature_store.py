from pathlib import Path

from dataset_builder import build_master_dataset

master_df = build_master_dataset(
    Path("training data")
)

master_df.to_csv(
    "feature_store.csv",
    index=False
)

print(master_df.head())

print(
    f"\nSaved {len(master_df)} monthly records."
)