import streamlit as st
from model_utils import build_top10_team_multiple, df
import plotly.graph_objects as go

st.set_page_config(page_title="Pokémon Team Builder", layout="wide")
st.title("Pokémon Team Builder")

# -------------------------------
# Type Colors
# -------------------------------
TYPE_COLORS = {
    "normal": "#A8A77A", "fire": "#EE8130", "water": "#6390F0",
    "electric": "#F7D02C", "grass": "#7AC74C", "ice": "#96D9D6",
    "fighting": "#C22E28", "poison": "#A33EA1", "ground": "#E2BF65",
    "flying": "#A98FF3", "psychic": "#F95587", "bug": "#A6B91A",
    "rock": "#B6A136", "ghost": "#735797", "dragon": "#6F35FC",
    "dark": "#705746", "steel": "#B7B7CE", "fairy": "#D685AD",
    "none": "#AAAAAA"
}

# -------------------------------
# Radar Chart Function
# -------------------------------
def plot_pokemon_stats(pokemon_name):
    stats = df[df['name'].str.lower() == pokemon_name.lower()][
        ["hp","attack","defense","sp_attack","sp_defense","speed"]
    ].iloc[0]
    categories = ["HP","Attack","Defense","Sp. Atk","Sp. Def","Speed"]
    values = stats.values.tolist() + [stats.values[0]]  # close loop
    fig = go.Figure(go.Scatterpolar(
        r=values, theta=categories + [categories[0]],
        fill='toself', line=dict(color="#FF6363")
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, df[["hp","attack","defense","sp_attack","sp_defense","speed"]].max().max()])),
                      showlegend=False)
    return fig

# -------------------------------
# Pokémon Selection
# -------------------------------
selected_pokemons = st.multiselect("Select your Pokémon:", df['name'].tolist())
allow_legendary = st.checkbox("Include Legendary Pokémon?", value=False)
max_generation = st.slider("Max Generation:", 1, 7, 7)

# -------------------------------
# Build Team
# -------------------------------
if st.button("Build Top 10 Team"):
    if not selected_pokemons:
        st.warning("Please select at least one Pokémon.")
    else:
        # ---- Show User Pokémon ----
        st.subheader("Your Pokémon")
        for pkmn in selected_pokemons:
            orig_row = df[df['name'].str.lower()==pkmn.lower()].iloc[0]
            left_col, right_col = st.columns([1,2])
            type1_color = TYPE_COLORS.get(orig_row['type1'].lower(), "#AAAAAA")
            type2_color = TYPE_COLORS.get(str(orig_row['type2']).lower(), "#AAAAAA")

            left_col.markdown(f"### {orig_row['name']}")
            left_col.markdown(
                f"**Type:** <span style='background-color:{type1_color};padding:3px;border-radius:5px'>{orig_row['type1']}</span> "
                f"<span style='background-color:{type2_color};padding:3px;border-radius:5px'>{orig_row['type2']}</span>",
                unsafe_allow_html=True
            )
            left_col.markdown(f"**Predicted Power:** {orig_row['battle_power']:.2f}")
            left_col.markdown(
                f"**Stats:**\n"
                f"- HP: {orig_row['hp']}\n"
                f"- Attack: {orig_row['attack']}\n"
                f"- Defense: {orig_row['defense']}\n"
                f"- Sp. Atk: {orig_row['sp_attack']}\n"
                f"- Sp. Def: {orig_row['sp_defense']}\n"
                f"- Speed: {orig_row['speed']}"
            )
            right_col.plotly_chart(
                plot_pokemon_stats(orig_row['name']),
                use_container_width=True,
                key=f"chart_{orig_row['name']}"
            )

        # ---- Suggested Team ----
        team = build_top10_team_multiple(selected_pokemons, allow_legendary, max_generation)
        if team.empty:
            st.warning("No Pokémon found for the selected criteria.")
        else:
            st.subheader("Top 10 Suggested Team")
            for _, row in team.iterrows():
                orig_row = df[df['name'].str.lower()==row['name'].lower()].iloc[0]
                left_col, right_col = st.columns([1,2])
                type1_color = TYPE_COLORS.get(orig_row['type1'].lower(), "#AAAAAA")
                type2_color = TYPE_COLORS.get(str(orig_row['type2']).lower(), "#AAAAAA")

                left_col.markdown(f"### {orig_row['name']}")
                left_col.markdown(
                    f"**Type:** <span style='background-color:{type1_color};padding:3px;border-radius:5px'>{orig_row['type1']}</span> "
                    f"<span style='background-color:{type2_color};padding:3px;border-radius:5px'>{orig_row['type2']}</span>",
                    unsafe_allow_html=True
                )
                left_col.markdown(f"**Predicted Power:** {orig_row['battle_power']:.2f}")
                left_col.markdown(
                    f"**Stats:**\n"
                    f"- HP: {orig_row['hp']}\n"
                    f"- Attack: {orig_row['attack']}\n"
                    f"- Defense: {orig_row['defense']}\n"
                    f"- Sp. Atk: {orig_row['sp_attack']}\n"
                    f"- Sp. Def: {orig_row['sp_defense']}\n"
                    f"- Speed: {orig_row['speed']}"
                )
                right_col.plotly_chart(
                    plot_pokemon_stats(orig_row['name']),
                    use_container_width=True,
                    key=f"chart_{orig_row['name']}"
                )
