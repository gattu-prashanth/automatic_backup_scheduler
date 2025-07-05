import os
import shutil
import boto3
import schedule
import time
from datetime import datetime
from cryptography.fernet import Fernet

# === CONFIG ===
FOLDER_TO_BACKUP = "data_to_backup"
OUTPUT_FOLDER = "backups"
BUCKET_NAME = "my-mtech-backup-bucket"  # Replace with your S3 bucket
ENCRYPT = False
REGION = "ap-south-1"  # Change based on region

# === Setup ===
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def create_backup():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"backup_{timestamp}.zip"
    zip_path = os.path.join(OUTPUT_FOLDER, zip_name)

    # Compress files
    shutil.make_archive(zip_path.replace('.zip', ''), 'zip', FOLDER_TO_BACKUP)
    print(f"✅ Created ZIP: {zip_path}")

    # Optional: Encrypt
    if ENCRYPT:
        key = Fernet.generate_key()
        cipher = Fernet(key)
        with open(zip_path, 'rb') as f:
            encrypted = cipher.encrypt(f.read())
        with open(zip_path, 'wb') as f:
            f.write(encrypted)
        with open(zip_path + ".key", 'wb') as f:
            f.write(key)
        print("🔐 Encrypted file & saved key")

    # Upload to S3
    s3 = boto3.client('s3', region_name=REGION)
    s3.upload_file(zip_path, BUCKET_NAME, f"backups/{zip_name}")
    print(f"☁️ Uploaded to S3: backups/{zip_name}")

# === Schedule daily backup ===

#schedule.every().day.at("02:00").do(create_backup)
# Run once immediately
create_backup()

# Start the scheduler (runs daily at 2:00 AM)
#schedule.every().day.at("02:00").do(create_backup)


print("⏰ Scheduler started. Waiting for next run...")
# while True:
#     schedule.run_pending()
#     time.sleep(60)
