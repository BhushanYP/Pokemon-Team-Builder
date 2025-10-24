# 🧠 Pokémon Team Builder (AI-Powered)

This project is an **AI-powered Pokémon Team Builder** that helps players create the most balanced and powerful teams using data-driven insights.  
It uses machine learning to predict Pokémon battle power and recommend team members that **complement each other's types** — ensuring full team coverage and strategic advantage.

---

## 🚀 Features

- 🔍 Predicts **Pokémon battle power** using trained Random Forest model  
- 🧩 Suggests **team combinations** based on type advantage relationships  
- 🧠 Ensures **diverse type coverage** — no more one-type-dominated teams  
- 📊 Visualizes each Pokémon’s stats with **interactive radar charts**  
- 💬 Provides **reasoning** behind each Pokémon recommendation  
- 🖥️ Built with **Streamlit** for a clean, interactive web app experience  

---

## ⚙️ How It Works

1. **Model Training**
   - Trains a `RandomForestRegressor` on Pokémon stats, types, and battle effectiveness.
   - Calculates a custom metric called **Battle Power** based on average stats and type resistances.

2. **Type Advantage System**
   - Uses a secondary dataset (`type_advantage.csv`) to understand which types are strong or weak against others.
   - Suggests next team members based on **type synergy**.

3. **Team Recommendation**
   - Starts from one or more selected Pokémon.
   - Predicts and ranks other Pokémon that best complement the team.
   - Returns the **Top 10 Pokémon** ordered by predicted power.

4. **Visualization**
   - Each Pokémon’s individual stats are displayed as a **hexagonal radar chart**.
   - Helps users visually compare strengths and weaknesses.

---
## 📊 Example Output

- When you select a Pokémon like Bulbasaur, the system:
- Predicts its strengths and weaknesses.
- Recommends Pokémon of complementary types (e.g., Water, Fire, Steel).
- Displays a visual breakdown of each suggested Pokémon.

## 🧩 Tech Stack

- Python
- Streamlit – UI framework
- scikit-learn – Machine Learning (Random Forest)
- Pandas / NumPy – Data processing
- Plotly – Radar charts for visualization

## 🧠 Future Improvements

- 🏆 Add synergy scoring between recommended Pokémon
- 🕹️ Integrate live Pokémon images
- ⚔️ Add simulated battle testing mode
- 🌐 Deploy the app online using Streamlit Cloud or Hugging Face Spaces

---

## 👨‍💻 Author

**Bhushan Yashwant Patil**  
📧  Email: patilbhushan1086@gmail.com  
💼  LinkedIn Profile: https://www.linkedin.com/in/bhushan-patil-381601293/  
📂  GitHub Portfolio: https://bhushanyp.github.io/portfolio/

---
