# controller_otp.py

import time
import hashlib
import random
import string
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# otp-------------------------------------------------------------------

SENDER_EMAIL = "blazeeehuu1@gmail.com"  
APP_PASSWORD = "tusd gmgy nkri dqoe"    
OTP_EXPIRATION_SECONDS = 300 # 5 menit


otp_storage = {}

def _generate_otp(length=6):
    return "".join(random.choice(string.digits) for _ in range(length))

def _send_email_otp(receiver_email, otp_code):
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Kode Verifikasi Anda: {otp_code}"
        message["From"] = SENDER_EMAIL
        message["To"] = receiver_email
        html = f"""
        <!DOCTYPE html>
        <html lang="id">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Verifikasi OTP</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                    background-color: #f5f7fa;
                    margin: 0;
                    padding: 20px;
                    color: #333;
                    text-align: center;
                }}
                .container {{
                    max-width: 500px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    border-radius: 12px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                    padding: 30px;
                }}
                .otp-code {{
                    font-size: 42px;
                    font-weight: bold;
                    letter-spacing: 8px;
                    color: #4f46e5;
                    margin: 20px 0;
                    font-family: monospace;
                }}
                .info-text {{
                    font-size: 16px;
                    line-height: 1.6;
                    color: #4b5563;
                }}
                .warning {{
                    color: #ef4444;
                    font-weight: 500;
                }}
                .footer {{
                    margin-top: 30px;
                    font-size: 14px;
                    color: #6b7280;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2 style="color: #4f46e5; margin-top: 0;">Verifikasi Email</h2>

                <p class="info-text">Gunakan kode OTP berikut untuk verifikasi:</p>

                <div class="otp-code">{otp_code}</div>

                <p class="info-text">Kode ini berlaku selama <span class="warning">{OTP_EXPIRATION_SECONDS // 60} menit</span></p>
                <p class="info-text warning">Jangan berikan kode ini kepada siapapun!</p>

                <div class="footer">
                    <p>Jika Anda tidak meminta kode ini, abaikan email ini.</p>
                    <p>© {datetime.datetime.now().year} NamaPerusahaan. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        message.attach(MIMEText(html, "html"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())
        return True
    except Exception as e:
        print(f"Error sending email: {e}") # Log error ini di aplikasi nyata
        return False

def process_otp_request(email):
    otp = _generate_otp()
    otp_hash = hashlib.sha256(otp.encode()).hexdigest()
    
    otp_storage[email] = {
        'otp_hash': otp_hash,
        'created_at': time.time()
    }
    
    if _send_email_otp(email, otp):
        print(f"OTP untuk {email} adalah {otp}. Hash: {otp_hash[:10]}...")
        return True, f"OTP telah dikirim ke {email}", 200
    else:
        return False, "Gagal mengirim OTP. Coba lagi nanti.", 500

def process_otp_verification(email, user_otp):
    if email not in otp_storage:
        return False, "OTP tidak valid atau belum diminta", 401

    stored_data = otp_storage[email]
    
    if time.time() - stored_data['created_at'] > OTP_EXPIRATION_SECONDS:
        del otp_storage[email]
        return False, "OTP sudah kedaluwarsa", 401
        
    user_otp_hash = hashlib.sha256(user_otp.encode()).hexdigest()
    
    if user_otp_hash == stored_data['otp_hash']:
        del otp_storage[email]
        return True, "Verifikasi berhasil", 200
    else:
        return False, "Kode OTP salah", 401