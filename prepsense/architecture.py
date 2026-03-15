"""
Architecture Visualization - Microservice Architecture Diagram

Displays PrepSense system architecture.
"""

import plotly.graph_objects as go


def create_architecture_diagram():
    """
    Create PrepSense microservice architecture diagram.
    
    Pipeline:
    Order Events → Telemetry Service → Ground Level Reconstruct →
    Prediction Service → Redis Cache → Dispatch System → Monitoring
    
    Returns:
    --------
    go.Figure
        Architecture diagram
    """
    # Horizontal flow: light purple (left) to dark purple (right) gradient
    services = [
        ('ORDER EVENTS', '#B39DDB'),
        ('TELEMETRY SERVICE', '#9C7BC2'),
        ('GROUND LEVEL RECONSTRUCT', '#7E57C2'),
        ('PREDICTION SERVICE', '#673AB7'),
        ('REDIS CACHE', '#5E35B1'),
        ('DISPATCH SYSTEM', '#4527A0'),
        ('MONITORING', '#311B92')
    ]
    
    n = len(services)
    spacing = 3
    node_x = [i * spacing for i in range(n)]
    node_y = [0] * n
    node_colors = [s[1] for s in services]
    node_text = [s[0] for s in services]
    
    fig = go.Figure()
    
    # Add connecting lines between nodes
    for i in range(n - 1):
        fig.add_trace(go.Scatter(
            x=[node_x[i], node_x[i + 1]],
            y=[0, 0],
            mode='lines',
            line=dict(width=4, color='#7E57C2'),
            hoverinfo='none',
            showlegend=False
        ))
    
    # Add nodes as circles with white text
    fig.add_trace(go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        marker=dict(
            size=120,
            color=node_colors,
            symbol='circle',
            line=dict(width=2, color='rgba(255,255,255,0.3)')
        ),
        text=node_text,
        textposition="middle center",
        textfont=dict(size=10, color='white', family='Poppins', weight='bold'),
        hoverinfo='text',
        showlegend=False
    ))
    
    fig.update_layout(
        title=dict(
            text="PrepSense MicroService Architecture",
            font=dict(family='Poppins', size=24, color='white', weight='bold')
        ),
        showlegend=False,
        hovermode='closest',
        margin=dict(b=80, l=60, r=60, t=100),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.5, (n - 1) * spacing + 1.5]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-2, 2]),
        plot_bgcolor='#2C2C2C',
        paper_bgcolor='#2C2C2C',
        height=500
    )
    
    return fig


def create_data_flow_diagram():
    """
    Create data flow diagram showing signal processing pipeline with improved formatting.
    
    Returns:
    --------
    go.Figure
        Data flow diagram
    """
    fig = go.Figure()
    
    # Define stages with better spacing and shorter labels
    stages = [
        ('Raw\nTelemetry', 0, '#EF4F5F'),
        ('Signal\nFiltering', 2.5, '#FF9800'),
        ('Ground Truth\nReconstruction', 5, '#2196F3'),
        ('Survival\nPrediction', 7.5, '#4CAF50'),
        ('Confidence\nIntervals', 10, '#9C27B0'),
        ('Dispatch\nOptimization', 12.5, '#00BCD4')
    ]
    
    # Add nodes with larger size
    for stage_name, x_pos, color in stages:
        fig.add_trace(go.Scatter(
            x=[x_pos],
            y=[0],
            mode='markers+text',
            marker=dict(size=150, color=color, line=dict(width=4, color='white')),
            text=[stage_name],
            textposition="middle center",
            textfont=dict(size=12, color='white', family='Poppins', weight='bold'),
            name=stage_name,
            showlegend=False
        ))
    
    # Add arrows with better styling
    for i in range(len(stages) - 1):
        x0 = stages[i][1]
        x1 = stages[i+1][1]
        fig.add_annotation(
            x=(x0 + x1) / 2,
            y=0,
            ax=x0 + 0.4,
            ay=0,
            xref="x",
            yref="y",
            axref="x",
            ayref="y",
            arrowhead=3,
            arrowsize=2,
            arrowwidth=3,
            arrowcolor="#666"
        )
    
    fig.update_layout(
        title=dict(text="Signal Processing Pipeline",
                  font=dict(family='Poppins', size=22, color='#1C1C1C', weight='bold')),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1, 14]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.5, 1.5]),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=400,
        margin=dict(b=40, l=40, r=40, t=60)
    )
    
    return fig
