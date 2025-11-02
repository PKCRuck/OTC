# 📡 Ruckus Optical Transceivers Catalog

A comprehensive web application for viewing and managing Ruckus Optical Transceivers. Built with Streamlit, this application provides a user-friendly interface similar to Juniper's HCT catalog, featuring filtering, searching, and full CRUD operations.

## Features

### Product Catalog View
- **Advanced Filtering**: Filter by form factor, data rate, connector type, and status
- **Search Functionality**: Search across SKU, name, and description fields
- **Multiple View Modes**: Switch between table view and card view
- **Real-time Results**: Dynamic filtering with instant result counts

### Admin Panel
- **Add New Transceivers**: Create new optical transceiver entries with all specifications
- **Edit Existing Transceivers**: Update any transceiver information (SKU cannot be changed)
- **Delete Transceivers**: Remove transceivers with confirmation prompts
- **Data Validation**: Ensures all required fields are filled before saving

### Pre-loaded Sample Data
The application comes with 15 pre-configured Ruckus optical transceivers including:
- SFP, SFP+, SFP28 modules (1G, 10G, 25G)
- QSFP+, QSFP28 modules (40G, 100G)
- QSFP-DD modules (400G)
- Various wavelengths and reach distances
- Different connector types (LC, MPO/MTP, MPO-16)

## Installation

1. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   streamlit run streamlit_app.py
   ```

3. Open your browser to the URL shown in the terminal (typically http://localhost:8501)

## Usage

### Viewing Transceivers
1. Navigate to the "Product Catalog" tab
2. Use the filter dropdowns to narrow down results by:
   - Form Factor (SFP, SFP+, SFP28, QSFP+, QSFP28, QSFP-DD)
   - Data Rate (1G, 10G, 25G, 40G, 100G, 400G)
   - Connector Type (LC, SC, MPO/MTP, MPO-16)
   - Status (Active, EOL, Discontinued)
3. Use the search box to find specific SKUs, names, or descriptions
4. Toggle between "Table View" and "Card View" for different display options

### Managing Transceivers
1. Navigate to the "Admin Panel" tab
2. Select your desired action:
   - **Add New Transceiver**: Fill in all required fields and click "Add Transceiver"
   - **Edit Transceiver**: Select a transceiver from the dropdown, modify fields, and click "Update Transceiver"
   - **Delete Transceiver**: Select a transceiver and confirm deletion

## Data Storage

Transceiver data is stored in JSON format at `data/transceivers.json`. This file is automatically created on first run and persists all changes made through the admin panel.

## Project Structure

```
OTC/
├── streamlit_app.py        # Main Streamlit application
├── data_manager.py         # Data operations and utilities
├── requirements.txt        # Python dependencies
├── data/
│   └── transceivers.json   # Transceiver database (JSON)
└── README.md              # This file
```

## Technology Stack

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and filtering
- **Python 3.x**: Core programming language

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.
