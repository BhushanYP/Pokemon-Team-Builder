import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor

# -------------------------------
# Load Pokémon Data
# -------------------------------
df = pd.read_csv("pokemon.csv")

# Compute stats
df["total_stats"] = df[["hp","attack","defense","sp_attack","sp_defense","speed"]].sum(axis=1)
df["avg_stats"] = df["total_stats"] / 6

# Average damage taken
against_cols = [col for col in df.columns if col.startswith("against_")]
df["avg_against"] = df[against_cols].mean(axis=1)

# Battle power metric
df["battle_power"] = df["avg_stats"] / df["avg_against"]

# Encode types
type_encoder = LabelEncoder()
df["type1_encoded"] = type_encoder.fit_transform(df["type1"].str.lower())
df["type2_encoded"] = type_encoder.fit_transform(df["type2"].fillna('none').str.lower())
df["legendary_flag"] = df["is_legendary"].astype(int)

# Features for model
features = ["hp","attack","defense","sp_attack","sp_defense","speed",
            "type1_encoded","type2_encoded","legendary_flag","generation"] + against_cols

X = df[features]
y = df["battle_power"]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train RandomForest
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_scaled, y)

# -------------------------------
# Load Type Advantage Data
# -------------------------------
type_df = pd.read_csv("type_advantage.csv")  # Columns: T1, T2
type_df['T1'] = type_df['T1'].str.lower().str.strip()
type_df['T2'] = type_df['T2'].str.lower().str.strip()
type_lookup = type_df.groupby('T1')['T2'].apply(list).to_dict()

# -------------------------------
# Type Recommendation Function
# -------------------------------
def suggest_team_types(start_types, top_n=10):
    """
    Given a list of starting Pokémon types, suggest a list of diverse types.
    """
    team_types = [t.lower() for t in start_types]

    while len(team_types) < top_n:
        # Find next type with advantage over last added type
        last_type = team_types[-1]
        possible_next = type_lookup.get(last_type, [])
        next_type = next((t for t in possible_next if t not in team_types), None)

        # If no new type, pick any type not in team
        if next_type is None:
            remaining = list(set(type_lookup.keys()) - set(team_types))
            if remaining:
                next_type = remaining[0]
            else:
                break
        team_types.append(next_type)
    return team_types[:top_n]

# -------------------------------
# Pick Pokémon by types
# -------------------------------
def pick_best_pokemon_by_types(team_types, top_n=10, allow_legendary=True, max_gen=7):
    """
    Picks the best Pokémon ensuring type diversity.
    """
    selected = []
    used_names = set()
    used_types = set()

    for t in team_types:
        candidates = df[((df['type1'].str.lower()==t) | (df['type2'].str.lower()==t)) &
                        (df['generation']<=max_gen)]
        if not allow_legendary:
            candidates = candidates[candidates['is_legendary']==False]

        if candidates.empty:
            continue

        X_cand = candidates[features]
        X_cand_scaled = scaler.transform(X_cand)
        candidates = candidates.copy()
        candidates['predicted_power'] = model.predict(X_cand_scaled)

        # Sort by predicted power
        for _, row in candidates.sort_values('predicted_power', ascending=False).iterrows():
            # ensure no duplicate Pokémon or duplicate primary type
            if (row['name'] not in used_names) and (row['type1'].lower() not in used_types):
                selected.append(row)
                used_names.add(row['name'])
                used_types.add(row['type1'].lower())
                break  # move to next type

        if len(selected) >= top_n:
            break

    # If still not enough, fill remaining spots with other strong, unique-type Pokémon
    if len(selected) < top_n:
        remaining = df.copy()
        if not allow_legendary:
            remaining = remaining[remaining['is_legendary']==False]
        remaining = remaining[~remaining['type1'].str.lower().isin(used_types)]

        X_rem = remaining[features]
        X_rem_scaled = scaler.transform(X_rem)
        remaining = remaining.copy()
        remaining['predicted_power'] = model.predict(X_rem_scaled)

        for _, row in remaining.sort_values('predicted_power', ascending=False).iterrows():
            if (row['name'] not in used_names) and (row['type1'].lower() not in used_types):
                selected.append(row)
                used_names.add(row['name'])
                used_types.add(row['type1'].lower())
            if len(selected) >= top_n:
                break

    return pd.DataFrame(selected).reset_index(drop=True)

# -------------------------------
# Build Top N Team from selected Pokémon
# -------------------------------
def build_top10_team_multiple(selected_pokemons, allow_legendary=True, max_gen=7):
    # Get starting types from selected Pokémon
    start_types = []
    for p in selected_pokemons:
        row = df[df['name'].str.lower() == p.lower()]
        if not row.empty:
            start_types.append(row.iloc[0]['type1'])

    # Suggest diverse team types
    team_types = suggest_team_types(start_types, top_n=10)

    # Pick best Pokémon
    team = pick_best_pokemon_by_types(team_types, top_n=10, allow_legendary=allow_legendary, max_gen=max_gen)

    # Sort by predicted power (highest → lowest)
    if not team.empty and "predicted_power" in team.columns:
        team = team.sort_values("predicted_power", ascending=False).reset_index(drop=True)

    return team
