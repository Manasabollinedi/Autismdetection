from flask import Flask, render_template
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# Load data
df = pd.read_csv('Toddler Autism dataset July 2018.csv')

# Clean up column names if needed
df.columns = df.columns.str.strip()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/visualizations')
def visualizations():
    # Check if the 'Class/ASD Traits' column exists
    if 'Class/ASD Traits' not in df.columns:
        return "Error: 'Class/ASD Traits' column not found", 404
    
    # 1. ASD vs Non-ASD
    asd_count = df['Class/ASD Traits'].value_counts().reset_index()
    asd_chart = px.pie(asd_count, names='index', values='Class/ASD Traits', title='ASD vs Non-ASD')
    asd_chart_html = asd_chart.to_html(full_html=False)

    # 2. Gender Distribution
    gender_pie = px.pie(df, names='Sex', title='Gender Distribution')
    gender_pie_html = gender_pie.to_html(full_html=False)

    # 3. Average Score by Gender (Changed 'A score' to 'Qchat-10-Score')
    score_gender = df.groupby('Sex')['Qchat-10-Score'].mean().reset_index()  # Adjusted column name
    score_gender_chart = px.bar(score_gender, x='Sex', y='Qchat-10-Score', title='Average Score by Gender')
    score_gender_html = score_gender_chart.to_html(full_html=False)

    # 4. Box Plot by ASD Traits
    box_plot = px.box(df, x='Class/ASD Traits', y='Qchat-10-Score', title='Score Distribution by ASD Traits')  # Adjusted column name
    box_plot_html = box_plot.to_html(full_html=False)

    # 5. Age Distribution
    age_histogram = px.histogram(df, x='Age_Months', nbins=10, title='Age Distribution')
    age_histogram_html = age_histogram.to_html(full_html=False)

    return render_template('visualizations.html',
                           asd_chart=asd_chart_html,
                           gender_pie=gender_pie_html,
                           score_gender=score_gender_html,
                           box_plot=box_plot_html,
                           age_histogram=age_histogram_html
                           )

if __name__ == '__main__':
    app.run(debug=True)
