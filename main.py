import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import io
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# Example data
data = {
    'Category': ['A', 'B', 'C', 'D'],
    'Value': [10, 20, 30, 45],
}

df = pd.DataFrame(data)

# Create bar chart
fig = go.Figure(data=[go.Bar(
            x=df['Category'], y=df['Value'],
            text=df['Value'],
            textposition='outside'
        )])
fig.update_layout(
    #plot_bgcolor='rgba(0,0,0,0)',
    #paper_bgcolor='rgba(0,0,0,0)',
    #xaxis=dict(showgrid=False),
    #yaxis=dict(showgrid=False)
)
#fig.update_traces(textposition='outside')

# Show the figure
buffer = io.BytesIO()
fig.write_image(buffer, format='png')
buffer.seek(0)

# Encode the image in Base64
image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

# HTML content with the image embedded
html_content = f"""
<html>
    <body>
        <h1>Bar Chart Example</h1>
        <p>Here is the bar chart you requested:</p>
        <table style="border-spacing: 20px;">
                    <tr>
                        <td>
                            <img src="data:image/png;base64,{image_base64}" alt="Bar Chart 1" style="width:300px;">
                        </td>
                        <td>
                            <img src="data:image/png;base64,{image_base64}" alt="Line Chart 2" style="width:300px;">
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <img src="data:image/png;base64,{image_base64}" alt="Bar Chart 3" style="width:300px;">
                        </td>
                        <td>
                            <img src="data:image/png;base64,{image_base64}" alt="Line Chart 4" style="width:300px;">
                        </td>
                    </tr>
                </table>
    </body>
</html>
"""

def send_email_with_embedded_image(sender_email, sender_password, recipient_email, subject, html_body):
    # Create the email
    msg = MIMEMultipart("alternative")
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the HTML body
    msg.attach(MIMEText(html_body, "html"))

    # Send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()  # Encrypt the connection
        smtp.login(sender_email, sender_password)  # Log in
        smtp.send_message(msg)  # Send the email

sender_email = "sample@gmail.com"
sender_password = "sample"
recipient_email = "sample@gmail.com"
subject = "Bar Chart Example"

send_email_with_embedded_image(sender_email, sender_password, recipient_email, subject, html_content)
