"""
WTA 2024 Points Dataset Analysis in Python


"""

# Import necessary libraries

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Use a nice default seaborn style for plots
sns.set_theme()

# So that large tables print more nicely
pd.set_option("display.max_columns", 50)
pd.set_option("display.width", 120)


# Load the Excel dataset

file_path = "2024-WTA-Women-Points-Dataset.xlsx"
df = pd.read_excel(file_path, header=1)

print("Data loaded successfully!")
print("\nFirst 5 rows of the dataset:")
print(df.head())

print("\nColumns in the dataset:")
print(df.columns.tolist())


# cleaning / formatting

df["MATCH DATE"] = pd.to_datetime(df["MATCH DATE"], errors="coerce")
df["MONTH"] = df["MATCH DATE"].dt.to_period("M")
df["hold"] = (df["WON SERVE"] == "WON").astype(int)
df["is_service_game"] = df["WON SERVE"].isin(["WON", "LOST"]).astype(int)

print("\n Basic cleaning done (dates parsed, helper columns added).")


# Ask some basic questions

num_rows = len(df)
num_tournaments = df["TOURNAMENT ID"].nunique()
num_matches = df["MATCH ID"].nunique()

print("\n--- BASIC STRUCTURE QUESTIONS ---")
print(f"Total rows (roughly individual games): {num_rows}")
print(f"Number of tournaments: {num_tournaments}")
print(f"Number of matches: {num_matches}")

surface_counts = df["SURFACE"].value_counts()
print("\nGames by surface:")
print(surface_counts)

serve_games = df[df["is_service_game"] == 1]
overall_hold_rate = serve_games["hold"].mean()

print("\n--- SERVE PERFORMANCE ---")
print(f"Total service games in dataset: {len(serve_games)}")
print(f"Overall hold percentage: {overall_hold_rate:.1%}")

hold_by_surface = (
    serve_games
    .groupby("SURFACE")["hold"]
    .mean()
    .sort_values(ascending=False)
)

print("\nHold percentage by surface:")
print((hold_by_surface * 100).round(1).astype(str) + "%")


# Plot 1: Games by surface
print("\nCreating Plot 1: Number of games by surface...")

plt.figure(figsize=(8, 5))
sns.barplot(
    x=surface_counts.index,
    y=surface_counts.values
)
plt.title("Number of Games by Surface")
plt.xlabel("Surface")
plt.ylabel("Number of Games")
plt.tight_layout()
plt.show()


# Plot 2: Hold % by surface
print("Creating Plot 2: Serve hold percentage by surface...")

hold_surface_df = hold_by_surface.reset_index()
hold_surface_df.columns = ["SURFACE", "HOLD_RATE"]

plt.figure(figsize=(8, 5))
sns.barplot(
    data=hold_surface_df,
    x="SURFACE",
    y="HOLD_RATE"
)
plt.title("Serve Hold Percentage by Surface")
plt.xlabel("Surface")
plt.ylabel("Hold Rate (fraction of service games held)")
plt.ylim(0, 1)  # Because it's a rate between 0 and 1
plt.tight_layout()
plt.show()


# Plot 3: Number of games over time
print("Creating Plot 3: Number of games per month...")

games_per_month = (
    df.dropna(subset=["MONTH"])
      .groupby("MONTH")["MATCH ID"]
      .count()
      .reset_index(name="NUM_GAMES")
)

games_per_month["MONTH"] = games_per_month["MONTH"].astype(str)

plt.figure(figsize=(10, 5))
sns.lineplot(data=games_per_month, x="MONTH", y="NUM_GAMES", marker="o")
plt.title("Number of Games per Month (2024 WTA Season)")
plt.xlabel("Month")
plt.ylabel("Number of Games")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


#  A couple of concrete "insight" questions

print("\n--- INSIGHT QUESTIONS ---")

top_tournaments = (
    df.groupby(["TOURNAMENT ID", "TOURNAMENT NAME"])["MATCH ID"]
      .count()
      .reset_index(name="NUM_GAME_ROWS")
      .sort_values(by="NUM_GAME_ROWS", ascending=False)
      .head(10)
)

print("\nTop 10 tournaments by number of game-rows:")
print(top_tournaments)

print("\nText summary of serve strength by surface:")
for surface, rate in hold_by_surface.items():
    print(f"- On {surface}, players hold serve about {rate:.1%} of the time.")

print("\n Analysis finished. You should see three plots and the printed summaries above.")
