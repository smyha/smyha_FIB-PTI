import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import os

def create_enriched_pdf():
    """Convert rentals.csv to an enriched PDF with additional context"""
    
    # Read the CSV data
    df = pd.read_csv("dataset/rentals.csv")
    
    # Create PDF document
    doc = SimpleDocTemplate("dataset/rentals.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1,  # Center alignment
        textColor=colors.darkblue
    )
    story.append(Paragraph("Car Rental Inventory Management System", title_style))
    story.append(Spacer(1, 20))
    
    # Introduction
    intro_text = """
    This document contains comprehensive information about our car rental inventory, 
    including detailed specifications, pricing, and availability data. Our fleet 
    consists of various vehicle types with different engine configurations, 
    customer ratings, rental durations, and special discount offers.
    
    The data presented here is essential for:
    • Inventory management and tracking
    • Customer service and recommendations
    • Pricing strategy and discount analysis
    • Fleet optimization and planning
    • Revenue forecasting and reporting
    """
    
    story.append(Paragraph(intro_text, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Data description
    desc_style = ParagraphStyle(
        'Description',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.darkgreen
    )
    story.append(Paragraph("Dataset Description", desc_style))
    
    description_text = """
    <b>Engine Types:</b> Our fleet includes Hybrid, Electric, Gasoline, and Diesel vehicles, 
    each offering different benefits in terms of fuel efficiency, environmental impact, and performance.
    
    <b>Rating System:</b> Vehicles are rated as High, Medium, or Low based on customer satisfaction, 
    reliability, and overall performance metrics.
    
    <b>Rental Duration:</b> Rental periods range from 3 to 8 days, with longer rentals often 
    offering better value and discounts.
    
    <b>Discount System:</b> Discounts are applied based on various factors including rental duration, 
    vehicle type, seasonal demand, and customer loyalty status.
    
    <b>Unit Availability:</b> The number of units available for each vehicle configuration, 
    updated in real-time based on current bookings and returns.
    """
    
    story.append(Paragraph(description_text, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Data table
    story.append(Paragraph("Detailed Inventory Data", desc_style))
    
    # Prepare table data
    table_data = [['Engine', 'Rating', 'Days', 'Discount (%)', 'Units Available']]
    for _, row in df.iterrows():
        table_data.append([
            row['engine'],
            row['rating'],
            str(row['days']),
            str(row['discount']),
            str(row['units'])
        ])
    
    # Create table
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    story.append(Spacer(1, 20))
    
    # Analysis section
    story.append(Paragraph("Fleet Analysis Summary", desc_style))
    
    # Calculate some statistics
    total_units = df['units'].sum()
    avg_discount = df['discount'].mean()
    engine_counts = df['engine'].value_counts()
    rating_counts = df['rating'].value_counts()
    
    analysis_text = f"""
    <b>Fleet Statistics:</b><br/>
    • Total vehicles in inventory: {total_units}<br/>
    • Average discount rate: {avg_discount:.1f}%<br/>
    • Most common engine type: {engine_counts.index[0]} ({engine_counts.iloc[0]} vehicles)<br/>
    • Most common rating: {rating_counts.index[0]} ({rating_counts.iloc[0]} vehicles)<br/>
    <br/>
    <b>Engine Type Distribution:</b><br/>
    """
    
    for engine, count in engine_counts.items():
        percentage = (count / len(df)) * 100
        analysis_text += f"• {engine}: {count} vehicles ({percentage:.1f}%)<br/>"
    
    analysis_text += f"""
    <br/>
    <b>Rating Distribution:</b><br/>
    """
    
    for rating, count in rating_counts.items():
        percentage = (count / len(df)) * 100
        analysis_text += f"• {rating}: {count} vehicles ({percentage:.1f}%)<br/>"
    
    story.append(Paragraph(analysis_text, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Business insights
    story.append(Paragraph("Business Insights and Recommendations", desc_style))
    
    insights_text = """
    <b>Revenue Optimization Opportunities:</b><br/>
    • High-rated vehicles with longer rental periods show the best discount-to-demand ratios<br/>
    • Electric vehicles are gaining popularity and may warrant increased inventory<br/>
    • Hybrid vehicles offer a good balance between efficiency and customer satisfaction<br/>
    <br/>
    <b>Customer Service Considerations:</b><br/>
    • Premium vehicles (High rating) should be prioritized for customer retention<br/>
    • Discount strategies should be aligned with vehicle availability and demand patterns<br/>
    • Regular inventory updates are crucial for accurate customer recommendations<br/>
    <br/>
    <b>Operational Efficiency:</b><br/>
    • Monitor unit availability closely to prevent overbooking<br/>
    • Implement dynamic pricing based on demand and availability<br/>
    • Consider seasonal adjustments to discount strategies
    """
    
    story.append(Paragraph(insights_text, styles['Normal']))
    
    # Footer
    story.append(Spacer(1, 30))
    timestamp = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    footer_text = f"Generated on: {timestamp}<br/>Total records: {len(df)}"
    story.append(Paragraph(footer_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    print("PDF created successfully: dataset/rentals.pdf")

if __name__ == "__main__":
    create_enriched_pdf()
