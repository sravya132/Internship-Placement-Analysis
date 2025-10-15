import os
import pandas as pd
import numpy as np
import random
from dash import Dash, dcc, html
import plotly.express as px

# -----------------------------
# 1️⃣ Determine the file path
# -----------------------------
# Use the same folder as this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "internship_placement_analysis_dataset.xlsx")

# Check if file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Dataset not found at {file_path}. Please add the dataset in this folder.")

# Load dataset
df = pd.read_excel(file_path)

# -----------------------------
# 2️⃣ Create Synthetic Data
# -----------------------------
random.seed(42)
np.random.seed(42)

companies = ["Amazon", "Google", "Microsoft", "Infosys", "TCS", "Wipro", "Capgemini"]
positions = ["Internship", "Full-Time"]

n = len(df)
df['Company'] = [random.choice(companies) for _ in range(n)]
df['Position'] = [random.choice(positions) for _ in range(n)]
df['Package_LPA'] = np.round(np.random.uniform(3, 50, n), 2)
df['Internship_Duration_Months'] = [random.randint(1, 6) for _ in range(n)]
df['Placement_Year'] = [random.choice([2023, 2024, 2025]) for _ in range(n)]

# -----------------------------
# 3️⃣ Create Interactive Figures
# -----------------------------
fig_dept = px.histogram(df, x='Department', title="Department-wise Placement Count",
                        color='Department', template="plotly_dark")
fig_company = px.histogram(df, x='Company', title="Company-wise Placement Count",
                           color='Company', template="plotly_dark")
fig_package = px.histogram(df, x='Package_LPA', nbins=15, title="Package Distribution (LPA)",
                           color_discrete_sequence=['#00ccff'], template="plotly_dark")
fig_box = px.box(df, x='Department', y='Package_LPA', color='Department',
                 title="Package Distribution by Department", template="plotly_dark")
fig_pie = px.pie(df, names='Position', title="Position-wise Distribution",
                 color_discrete_sequence=['#ff9999','#66b3ff'], template="plotly_dark")
fig_year = px.histogram(df, x='Placement_Year', color='Placement_Year',
                        title="Placements Over the Years", template="plotly_dark")
fig_scatter = px.scatter(df, x='Internship_Duration_Months', y='Package_LPA', color='Department',
                         size='Package_LPA', hover_data=['Company'],
                         title="Internship Duration vs Package (LPA)", template="plotly_dark")
fig_corr = px.imshow(df[['Package_LPA','Internship_Duration_Months']].corr(),
                     text_auto=True, color_continuous_scale='Tealrose',
                     title="Correlation Heatmap", template="plotly_dark")

# -----------------------------
# 4️⃣ Initialize App
# -----------------------------
app = Dash(__name__)
app.title = "Internship & Placement Insights Dashboard"

# -----------------------------
# 5️⃣ App Layout with Styling
# -----------------------------
app.layout = html.Div(
    style={
        "background": "linear-gradient(135deg, #0f2027, #203a43, #2c5364)",
        "color": "white",
        "fontFamily": "Segoe UI, sans-serif",
        "padding": "30px"
    },
    children=[
        html.H1("🎓 Internship & Placement Trends Dashboard",
                style={
                    "textAlign": "center",
                    "fontSize": "40px",
                    "marginBottom": "30px",
                    "color": "#00e6e6",
                    "textShadow": "2px 2px 5px #000"
                }),
        html.Hr(style={"borderColor": "#00cccc"}),

        # First row
        html.Div([
            html.Div([dcc.Graph(figure=fig_dept)], style={"flex": "1", "padding": "10px"}),
            html.Div([dcc.Graph(figure=fig_company)], style={"flex": "1", "padding": "10px"}),
        ], style={"display": "flex", "flexWrap": "wrap"}),

        # Second row
        html.Div([
            html.Div([dcc.Graph(figure=fig_package)], style={"flex": "1", "padding": "10px"}),
            html.Div([dcc.Graph(figure=fig_box)], style={"flex": "1", "padding": "10px"}),
        ], style={"display": "flex", "flexWrap": "wrap"}),

        # Third row
        html.Div([
            html.Div([dcc.Graph(figure=fig_pie)], style={"flex": "1", "padding": "10px"}),
            html.Div([dcc.Graph(figure=fig_year)], style={"flex": "1", "padding": "10px"}),
        ], style={"display": "flex", "flexWrap": "wrap"}),

        # Fourth row
        html.Div([
            html.Div([dcc.Graph(figure=fig_scatter)], style={"flex": "1", "padding": "10px"}),
            html.Div([dcc.Graph(figure=fig_corr)], style={"flex": "1", "padding": "10px"}),
        ], style={"display": "flex", "flexWrap": "wrap"}),

        html.Footer("© 2025 Internship & Placement Analytics | Designed by Sravya",
                    style={"textAlign": "center", "marginTop": "40px", "color": "#00cccc"})
    ]
)

# -----------------------------
# 6️⃣ Run the App
# -----------------------------
server = app.server  # expose server for Render
if __name__ == '__main__':
    app.run(debug=True)
