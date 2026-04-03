# utils/helpers.py
import os
import tempfile
from typing import List


def save_uploaded_file(uploaded_file) -> str:
    """Save uploaded Streamlit file to temporary location and return path"""
    if uploaded_file is None:
        return None
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getbuffer())
        return tmp.name


def cleanup_temp_files(file_paths: List[str]):
    """Safely delete temporary files"""
    for path in file_paths:
        try:
            if path and os.path.exists(path):
                os.unlink(path)
        except Exception as e:
            print(f"[WARNING] Could not delete temp file {path}: {e}")


def format_response(text: str) -> str:
    """Basic formatting for LLM responses"""
    if not text:
        return "I couldn't generate a response. Please try again."
    return text.strip()


def get_match_color(score: str) -> str:
    """Return color based on match score (for future dashboard use)"""
    try:
        score_num = int(score.replace("%", ""))
        if score_num >= 80:
            return "🟢 Excellent"
        elif score_num >= 65:
            return "🟡 Good"
        else:
            return "🔴 Needs Improvement"
    except:
        return "⚪ Unknown"