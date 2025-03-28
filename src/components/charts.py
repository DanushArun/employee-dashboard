import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

def create_performance_chart(df, employee_id):
    """Create a performance radar chart for the selected employee"""
    if employee_id and not df.empty:
        # Filter data for the selected employee
        emp_data = df[df['employee_id'] == employee_id]
        
        if emp_data.empty:
            st.warning("No data available for the selected employee.")
            return None
        
        # Prepare data for radar chart
        categories = [
            'Trainer Grade', 'Training Count', 'UL Score', 'PL Score',
            'Error Count', 'Kaizen', 'Flexibility', 'Teamwork'
        ]
        
        # Normalize values between 0 and 1 for radar chart
        values = [
            emp_data['trainer_grade'].values[0] / 4.0,  # Normalized to 0-1 range
            min(1.0, emp_data['training_count'].values[0] / 10.0),  # Assuming max is 10
            1.0 - min(1.0, emp_data['ul'].values[0] / 5.0),  # Lower is better
            1.0 - min(1.0, emp_data['pl'].values[0] / 5.0),  # Lower is better
            1.0 - min(1.0, emp_data['error_count'].values[0] / 5.0),  # Lower is better
            min(1.0, emp_data['kaizen_responsible'].values[0] / 4.0),
            min(1.0, emp_data['flexibility_credit'].values[0] / 4.0),
            min(1.0, emp_data['teamwork_credit'].values[0] / 4.0)
        ]
        
        # Create data for the radar chart
        angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
        
        # Close the loop
        values.append(values[0])
        angles.append(angles[0])
        categories.append(categories[0])
        
        # Create DataFrame for Altair
        radar_data = pd.DataFrame({
            'category': categories,
            'value': values,
            'angle': angles,
            'x': [np.cos(angle) * value for angle, value in zip(angles, values)],
            'y': [np.sin(angle) * value for angle, value in zip(angles, values)]
        })
        
        # Create the radar chart using Altair
        radar_chart = alt.Chart(radar_data).mark_line(color='#00FF9D', strokeWidth=2).encode(
            x=alt.X('x', axis=None),
            y=alt.Y('y', axis=None)
        ).properties(
            width=300,
            height=300
        )
        
        # Add points
        points = alt.Chart(radar_data).mark_circle(color='#00FF9D', size=80).encode(
            x='x',
            y='y',
            tooltip=['category', alt.Tooltip('value', format='.2f')]
        )
        
        # Add background circles for reference
        background_data = pd.DataFrame({
            'radius': [0.25, 0.5, 0.75, 1.0],
        })
        
        background = alt.Chart(background_data).mark_circle(color='#333333', opacity=0.3).encode(
            x=alt.value(0),
            y=alt.value(0),
            size=alt.Size('radius', scale=None, legend=None)
        )
        
        # Add category labels
        label_data = pd.DataFrame({
            'category': categories[:-1],  # Remove the duplicated last category
            'angle': angles[:-1],  # Remove the duplicated last angle
            'x': [np.cos(angle) * 1.2 for angle in angles[:-1]],
            'y': [np.sin(angle) * 1.2 for angle in angles[:-1]]
        })
        
        labels = alt.Chart(label_data).mark_text(
            color='#FFFFFF',
            fontSize=12,
            fontWeight='bold',
            align='center',
            baseline='middle'
        ).encode(
            x='x',
            y='y',
            text='category'
        )
        
        # Combine all layers
        final_chart = (background + radar_chart + points + labels).configure_view(
            strokeWidth=0
        )
        
        return final_chart
    
    return None

def create_trend_chart(df, employee_id, metric):
    """Create a trend chart for a specific metric over time"""
    if employee_id and metric and not df.empty:
        # Filter data for the selected employee
        emp_data = df[df['employee_id'] == employee_id]
        
        if emp_data.empty or metric not in emp_data.columns:
            return None
        
        # Create a simple line chart
        chart = alt.Chart(emp_data).mark_line(point=True, color='#00FF9D').encode(
            x=alt.X('date:T', title='Date'),
            y=alt.Y(f'{metric}:Q', title=metric.replace('_', ' ').title()),
            tooltip=['date:T', alt.Tooltip(f'{metric}:Q', title=metric.replace('_', ' ').title())]
        ).properties(
            width='container',
            height=250
        ).configure_axis(
            grid=False,
            labelColor='#FFFFFF',
            titleColor='#FFFFFF'
        ).configure_view(
            strokeWidth=0
        )
        
        return chart
    
    return None

def create_comparison_chart(df, employee_id, metric):
    """Create a chart comparing employee's metric with average"""
    if employee_id and metric and not df.empty:
        # Filter data for the selected employee
        emp_data = df[df['employee_id'] == employee_id]
        
        if emp_data.empty or metric not in emp_data.columns:
            return None
        
        # Calculate average for the metric
        avg_value = df[metric].mean()
        emp_value = emp_data[metric].values[0]
        
        # Create comparison data
        comp_data = pd.DataFrame({
            'Category': ['Employee', 'Average'],
            'Value': [emp_value, avg_value]
        })
        
        # Create bar chart
        chart = alt.Chart(comp_data).mark_bar().encode(
            x=alt.X('Category:N', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('Value:Q', title=metric.replace('_', ' ').title()),
            color=alt.Color('Category:N', scale=alt.Scale(
                domain=['Employee', 'Average'],
                range=['#00FF9D', '#888888']
            )),
            tooltip=['Category:N', alt.Tooltip('Value:Q', format='.2f')]
        ).properties(
            width='container',
            height=250
        ).configure_axis(
            grid=False,
            labelColor='#FFFFFF',
            titleColor='#FFFFFF'
        ).configure_view(
            strokeWidth=0
        )
        
        return chart
    
    return None

def create_status_distribution(df):
    """Create a pie chart showing the distribution of pass/fail status"""
    if not df.empty and 'status' in df.columns:
        # Count status values
        status_counts = df['status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        
        # Create pie chart
        chart = alt.Chart(status_counts).mark_arc().encode(
            theta=alt.Theta(field="Count", type="quantitative"),
            color=alt.Color(field="Status", type="nominal", scale=alt.Scale(
                domain=['Pass', 'Fail'],
                range=['#00FF9D', '#FF4757']
            )),
            tooltip=['Status', 'Count']
        ).properties(
            width=250,
            height=250
        )
        
        return chart
    
    return None

def create_zone_distribution(df):
    """Create a bar chart showing the distribution of employees by zone"""
    if not df.empty and 'zone' in df.columns:
        # Count employees by zone
        zone_counts = df['zone'].value_counts().reset_index()
        zone_counts.columns = ['Zone', 'Count']
        
        # Create bar chart
        chart = alt.Chart(zone_counts).mark_bar(color='#00FF9D').encode(
            x=alt.X('Zone:N', title='Zone'),
            y=alt.Y('Count:Q', title='Number of Employees'),
            tooltip=['Zone:N', 'Count:Q']
        ).properties(
            width='container',
            height=250
        ).configure_axis(
            grid=False,
            labelColor='#FFFFFF',
            titleColor='#FFFFFF'
        ).configure_view(
            strokeWidth=0
        )
        
        return chart
    
    return None