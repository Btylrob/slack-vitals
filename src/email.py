import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

emailpass = os.getenv("EMAILPASS")
emailpassword = os.getenv("EMAILPASSWORD")
email = os.getenv("EMAIL")
address = os.getenv("ADDRESS")

def create_grafana_style_body():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: 'Helvetica Neue', Arial, sans-serif;
                background-color: #0f1419;
                color: #d8d9da;
                margin: 0;
                padding: 20px;
                line-height: 1.6;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background-color: #1e2328;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            }}
            .header {{
                background: linear-gradient(135deg, #ff6b35, #f7931e);
                padding: 25px;
                text-align: center;
                color: white;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
                font-weight: 300;
            }}
            .header .subtitle {{
                margin: 5px 0 0 0;
                font-size: 14px;
                opacity: 0.9;
            }}
            .content {{
                padding: 30px;
            }}
            .metric-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }}
            .metric-card {{
                background-color: #262d33;
                border-radius: 6px;
                padding: 20px;
                border-left: 4px solid #52c41a;
                transition: transform 0.2s;
            }}
            .metric-card:hover {{
                transform: translateY(-2px);
            }}
            .metric-card.warning {{
                border-left-color: #faad14;
            }}
            .metric-card.error {{
                border-left-color: #ff4d4f;
            }}
            .metric-title {{
                font-size: 12px;
                color: #8c8c8c;
                text-transform: uppercase;
                margin-bottom: 8px;
                letter-spacing: 0.5px;
            }}
            .metric-value {{
                font-size: 32px;
                font-weight: bold;
                color: #d8d9da;
                margin-bottom: 5px;
            }}
            .metric-change {{
                font-size: 12px;
                color: #52c41a;
            }}
            .metric-change.negative {{
                color: #ff4d4f;
            }}
            .chart-placeholder {{
                background: linear-gradient(45deg, #262d33, #1e2328);
                border-radius: 6px;
                padding: 20px;
                margin: 20px 0;
                text-align: center;
                border: 1px dashed #52c41a;
            }}
            .status-section {{
                background-color: #262d33;
                border-radius: 6px;
                padding: 20px;
                margin: 20px 0;
            }}
            .status-item {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px 0;
                border-bottom: 1px solid #3a3a3a;
            }}
            .status-item:last-child {{
                border-bottom: none;
            }}
            .status-indicator {{
                width: 12px;
                height: 12px;
                border-radius: 50%;
                background-color: #52c41a;
                margin-right: 10px;
            }}
            .status-indicator.warning {{
                background-color: #faad14;
            }}
            .status-indicator.error {{
                background-color: #ff4d4f;
            }}
            .footer {{
                background-color: #0f1419;
                padding: 20px;
                text-align: center;
                font-size: 12px;
                color: #8c8c8c;
            }}
            .btn {{
                display: inline-block;
                padding: 10px 20px;
                background: linear-gradient(135deg, #1890ff, #52c41a);
                color: white;
                text-decoration: none;
                border-radius: 4px;
                margin: 10px 0;
                font-weight: 500;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>( ͡° ͜ʖ ͡°) Lenny - Nightly Report</h1>
                <div class="subtitle">Generated on {current_time}</div>
            </div>
            
            <div class="content">
                <h2 style="color: #d8d9da; margin-bottom: 20px;">📊 Key Events and Outages Log</h2>
                
                <div class="metric-grid">
                    <div class="metric-card">
                        <div class="metric-title">Metric 1</div>
                        <div class="metric-value">---</div>
                        <div class="metric-change">--- data goes here</div>
                    </div>
                    
                    <div class="metric-card warning">
                        <div class="metric-title">Metric 2</div>
                        <div class="metric-value">---</div>
                        <div class="metric-change negative">--- data goes here</div>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-title">Metric 3</div>
                        <div class="metric-value">---</div>
                        <div class="metric-change">--- data goes here</div>
                    </div>
                    
                    <div class="metric-card error">
                        <div class="metric-title">Metric 4</div>
                        <div class="metric-value">---</div>
                        <div class="metric-change negative">--- data goes here</div>
                    </div>
                </div>
                
                <div class="chart-placeholfrom datetime import datetimed9da; margin-top: 0;">🔧 System Status</h3>
                    
                    <div class="status-item">
                        <div style="display: flex; align-items: center;">
                            <div class="status-indicator"></div>
                            <span>Service 1</span>
                        </div>
                        <span style="color: #52c41a;">Status</span>
                    </div>
                    
                    <div class="status-item">
                        <div style="display: flex; align-items: center;">
                            <div class="status-indicator warning"></div>
                            <span>Service 2</span>
                        </div>
                        <span style="color: #faad14;">Status</span>
                    </div>
                    
                    <div class="status-item">
                        <div style="display: flex; align-items: center;">
                            <div class="status-indicator"></div>
                            <span>Service 3</span>
                        </div>
                        <span style="color: #52c41a;">Status</span>
                    </div>
                    
                    <div class="status-item">
                        <div style="display: flex; align-items: center;">
                            <div class="status-indicator error"></div>
                            <span>Service 4</span>
                        </div>
                        <span style="color: #ff4d4f;">Status</span>
                    </div>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="#" class="btn">View Full Dashboard</a>
                </div>
                
                <div style="background-color: #262d33; padding: 15px; border-radius: 6px; border-left: 4px solid #1890ff;">
                    <h4 style="color: #1890ff; margin: 0 0 10px 0;">💡 Key Insights</h4>
                    <ul style="margin: 0; padding-left: 20px; color: #d8d9da;">
                        <li>Insight point 1 - data goes here</li>
                        <li>Insight point 2 - data goes here</li>
                        <li>Insight point 3 - data goes here</li>
                        <li>Insight point 4 - data goes here</li>
                    </ul>
                </div>
            </div>
            
            <div class="footer">
                <p>This is an automated report generated by Lenny Monitoring System</p>
                <p>For questions or issues, contact via Github</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_body

def send_email_gmail(sender_email, sender_password, recipient_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))
    
    try:
        # Connect to Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() 
        server.login(sender_email, sender_password)  

        # Send email func
        server.send_message(msg)
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

    finally:
        server.quit()

if __name__ == "__main__":
    sender = email
    passworduser = emailpass
    password= emailpassword
    recipient = address
    subject = "Lenny - Nightly Report"
    body = create_grafana_style_body()

    send_email_gmail(sender, password, recipient, subject, body)