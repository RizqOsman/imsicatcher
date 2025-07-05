import re
from datetime import datetime
from typing import List
from app.models import IMSIRecord

def extract_imsis_from_log(log_path: str) -> List[IMSIRecord]:
    imsis = []
    try:
        with open(log_path, 'r') as f:
            for line in f:
                match = re.search(r'IMSI\s+(\d+)', line)
                if match:
                    imsis.append(IMSIRecord(
                        imsi=match.group(1),
                        timestamp=datetime.now()
                    ))
    except FileNotFoundError:
        print("Log file tidak ditemukan.")
    return imsis