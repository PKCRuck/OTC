import json
import os
from typing import List, Dict, Optional
import pandas as pd

DATA_FILE = "data/transceivers.json"

def ensure_data_file():
    """Ensure the data file exists."""
    if not os.path.exists(DATA_FILE):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)

def load_transceivers() -> List[Dict]:
    """Load all transceivers from the data file."""
    ensure_data_file()
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_transceivers(transceivers: List[Dict]):
    """Save transceivers to the data file."""
    ensure_data_file()
    with open(DATA_FILE, 'w') as f:
        json.dump(transceivers, f, indent=2)

def add_transceiver(transceiver: Dict) -> bool:
    """Add a new transceiver."""
    transceivers = load_transceivers()

    # Check if SKU already exists
    if any(t['sku'] == transceiver['sku'] for t in transceivers):
        return False

    transceivers.append(transceiver)
    save_transceivers(transceivers)
    return True

def update_transceiver(sku: str, updated_data: Dict) -> bool:
    """Update an existing transceiver by SKU."""
    transceivers = load_transceivers()

    for i, t in enumerate(transceivers):
        if t['sku'] == sku:
            transceivers[i] = updated_data
            save_transceivers(transceivers)
            return True

    return False

def delete_transceiver(sku: str) -> bool:
    """Delete a transceiver by SKU."""
    transceivers = load_transceivers()
    initial_length = len(transceivers)

    transceivers = [t for t in transceivers if t['sku'] != sku]

    if len(transceivers) < initial_length:
        save_transceivers(transceivers)
        return True

    return False

def get_transceiver(sku: str) -> Optional[Dict]:
    """Get a specific transceiver by SKU."""
    transceivers = load_transceivers()

    for t in transceivers:
        if t['sku'] == sku:
            return t

    return None

def get_transceivers_df() -> pd.DataFrame:
    """Get transceivers as a pandas DataFrame."""
    transceivers = load_transceivers()
    if not transceivers:
        return pd.DataFrame(columns=[
            'sku', 'name', 'form_factor', 'data_rate', 'wavelength',
            'reach', 'connector', 'temperature', 'power', 'description', 'status'
        ])
    return pd.DataFrame(transceivers)

def get_unique_values(field: str) -> List[str]:
    """Get unique values for a specific field."""
    df = get_transceivers_df()
    if field in df.columns:
        return sorted(df[field].dropna().unique().tolist())
    return []
