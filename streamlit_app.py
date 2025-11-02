import streamlit as st
import pandas as pd
from data_manager import (
    load_transceivers,
    get_transceivers_df,
    get_unique_values,
    add_transceiver,
    update_transceiver,
    delete_transceiver,
    get_transceiver
)
from auth import verify_password, change_password, get_default_password_info

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Page configuration
st.set_page_config(
    page_title="Ruckus Optical Transceivers Catalog",
    page_icon="🔶",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Ruckus Networks branding
st.markdown("""
<style>
    /* Import Open Sans font (Ruckus Networks official font) */
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700;800&display=swap');

    /* Ruckus Networks Official Colors */
    :root {
        --ruckus-orange: #F47920;
        --ruckus-dark: #101820;
        --ruckus-yellow: #FFDF7E;
        --ruckus-light-gray: #F5F5F5;
        --ruckus-gray: #6B6B6B;
    }

    /* Global font family */
    html, body, [class*="css"] {
        font-family: 'Open Sans', sans-serif;
    }

    /* Main container styling */
    .main {
        background-color: #FFFFFF;
    }

    /* Header styling */
    .ruckus-header {
        background: linear-gradient(135deg, var(--ruckus-dark) 0%, #1a2832 100%);
        padding: 2rem 2rem 1.5rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border-bottom: 4px solid var(--ruckus-orange);
    }

    .ruckus-logo-text {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--ruckus-orange);
        margin: 0;
        letter-spacing: -0.5px;
        text-transform: uppercase;
    }

    .ruckus-subtitle {
        font-size: 1.2rem;
        font-weight: 300;
        color: #FFFFFF;
        margin-top: 0.5rem;
        letter-spacing: 0.5px;
    }

    /* Navigation buttons */
    .stButton > button {
        background-color: var(--ruckus-orange);
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .stButton > button:hover {
        background-color: #E56A10;
        box-shadow: 0 4px 12px rgba(244, 121, 32, 0.3);
        transform: translateY(-2px);
    }

    /* Filter box styling */
    .filter-box {
        background: linear-gradient(135deg, var(--ruckus-light-gray) 0%, #FFFFFF 100%);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid var(--ruckus-orange);
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    /* Section headers */
    h1, h2, h3 {
        color: var(--ruckus-dark);
        font-weight: 700;
    }

    /* Info boxes */
    .stInfo {
        background-color: rgba(255, 223, 126, 0.2);
        border-left: 4px solid var(--ruckus-yellow);
    }

    .stWarning {
        background-color: rgba(244, 121, 32, 0.1);
        border-left: 4px solid var(--ruckus-orange);
    }

    .stSuccess {
        background-color: rgba(76, 175, 80, 0.1);
        border-left: 4px solid #4CAF50;
    }

    .stError {
        background-color: rgba(244, 67, 54, 0.1);
        border-left: 4px solid #F44336;
    }

    /* DataFrames and tables */
    .dataframe {
        border: 1px solid var(--ruckus-gray);
        border-radius: 4px;
    }

    .dataframe thead tr th {
        background-color: var(--ruckus-dark);
        color: white;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.85rem;
        letter-spacing: 0.5px;
    }

    .dataframe tbody tr:hover {
        background-color: rgba(244, 121, 32, 0.05);
    }

    /* Product cards */
    .product-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #E0E0E0;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }

    .product-card:hover {
        box-shadow: 0 4px 12px rgba(244, 121, 32, 0.15);
        border-color: var(--ruckus-orange);
    }

    /* Form elements */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        border: 2px solid #E0E0E0;
        border-radius: 4px;
        font-family: 'Open Sans', sans-serif;
    }

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--ruckus-orange);
        box-shadow: 0 0 0 1px var(--ruckus-orange);
    }

    /* Divider */
    hr {
        border-color: var(--ruckus-orange);
        opacity: 0.3;
    }

    /* Footer */
    .ruckus-footer {
        background-color: var(--ruckus-dark);
        color: white;
        padding: 2rem;
        margin: 3rem -1rem -1rem -1rem;
        text-align: center;
        font-size: 0.9rem;
        border-top: 3px solid var(--ruckus-orange);
    }

    .ruckus-footer a {
        color: var(--ruckus-orange);
        text-decoration: none;
        font-weight: 600;
    }

    /* Radio buttons */
    .stRadio > label {
        font-weight: 600;
        color: var(--ruckus-dark);
    }

    /* Login form styling */
    .login-container {
        background: linear-gradient(135deg, var(--ruckus-dark) 0%, #1a2832 100%);
        padding: 3rem;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
        border: 2px solid var(--ruckus-orange);
    }
</style>
""", unsafe_allow_html=True)

# Header section with Ruckus branding
st.markdown("""
<div class="ruckus-header">
""", unsafe_allow_html=True)

col_text, col_logo = st.columns([4, 1])
with col_text:
    st.markdown("""
    <div class="ruckus-logo-text">🔶 RUCKUS NETWORKS</div>
    <div class="ruckus-subtitle">Optical Transceivers Catalog</div>
    """, unsafe_allow_html=True)
with col_logo:
    st.image("Ruckus_logo_white-orange.png", width=180)

st.markdown("""
</div>
""", unsafe_allow_html=True)

# Navigation
st.markdown('<div style="margin-bottom: 2rem;">', unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns([1, 2, 0.5, 2, 4])
with col2:
    if st.button("🔷 PRODUCT CATALOG", use_container_width=True, key="nav_catalog"):
        st.session_state.current_page = "catalog"
with col4:
    if st.button("🔧 ADMIN PANEL", use_container_width=True, key="nav_admin"):
        st.session_state.current_page = "admin"
st.markdown('</div>', unsafe_allow_html=True)

# Initialize current page if not set
if 'current_page' not in st.session_state:
    st.session_state.current_page = "catalog"

st.markdown('<hr style="margin: 1.5rem 0; border-color: #F47920; opacity: 0.3;">', unsafe_allow_html=True)

# Display the appropriate page
if st.session_state.current_page == "catalog":
    st.markdown("""
    <div style="background: linear-gradient(90deg, #F47920 0%, #101820 100%); padding: 1rem 1.5rem; border-radius: 8px; margin-bottom: 1.5rem;">
        <h2 style="color: white; margin: 0; font-weight: 700; font-size: 1.8rem;">📦 PRODUCT CATALOG</h2>
    </div>
    """, unsafe_allow_html=True)

    # Filters section
    with st.container():
        st.markdown('<div class="filter-box">', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            form_factors = ["All"] + get_unique_values("form_factor")
            selected_form_factor = st.selectbox("Form Factor", form_factors)

        with col2:
            data_rates = ["All"] + get_unique_values("data_rate")
            selected_data_rate = st.selectbox("Data Rate", data_rates)

        with col3:
            connectors = ["All"] + get_unique_values("connector")
            selected_connector = st.selectbox("Connector", connectors)

        with col4:
            statuses = ["All"] + get_unique_values("status")
            selected_status = st.selectbox("Status", statuses)

        # Search box
        search_term = st.text_input("🔍 Search by SKU, Name, or Description", "")

        st.markdown('</div>', unsafe_allow_html=True)

    # Load and filter data
    df = get_transceivers_df()

    if not df.empty:
        # Apply filters
        if selected_form_factor != "All":
            df = df[df['form_factor'] == selected_form_factor]

        if selected_data_rate != "All":
            df = df[df['data_rate'] == selected_data_rate]

        if selected_connector != "All":
            df = df[df['connector'] == selected_connector]

        if selected_status != "All":
            df = df[df['status'] == selected_status]

        # Apply search filter
        if search_term:
            df = df[
                df['sku'].str.contains(search_term, case=False, na=False) |
                df['name'].str.contains(search_term, case=False, na=False) |
                df['description'].str.contains(search_term, case=False, na=False)
            ]

        # Display results count
        st.info(f"Found {len(df)} transceivers")

        # Display view options
        view_mode = st.radio("View Mode", ["Table View", "Card View"], horizontal=True)

        if view_mode == "Table View":
            # Display as table
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "sku": st.column_config.TextColumn("SKU", width="medium"),
                    "name": st.column_config.TextColumn("Name", width="large"),
                    "form_factor": st.column_config.TextColumn("Form Factor", width="small"),
                    "data_rate": st.column_config.TextColumn("Data Rate", width="small"),
                    "wavelength": st.column_config.TextColumn("Wavelength", width="medium"),
                    "reach": st.column_config.TextColumn("Reach", width="medium"),
                    "connector": st.column_config.TextColumn("Connector", width="small"),
                    "temperature": st.column_config.TextColumn("Temperature", width="medium"),
                    "power": st.column_config.TextColumn("Power", width="small"),
                    "description": st.column_config.TextColumn("Description", width="large"),
                    "status": st.column_config.TextColumn("Status", width="small")
                }
            )
        else:
            # Display as cards
            for idx, row in df.iterrows():
                st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 8px; border: 1px solid #E0E0E0;
                            margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                            transition: all 0.3s ease; border-left: 4px solid #F47920;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem;">
                        <div>
                            <div style="font-weight: 700; color: #F47920; font-size: 0.85rem; margin-bottom: 0.25rem;">SKU</div>
                            <div style="font-weight: 600; color: #101820; font-size: 1.1rem;">{row['sku']}</div>
                            <div style="font-weight: 600; color: #6B6B6B; font-size: 0.95rem; margin-top: 0.5rem;">{row['name']}</div>
                        </div>
                        <div>
                            <div style="margin-bottom: 0.5rem;">
                                <span style="font-weight: 700; color: #F47920;">Form Factor:</span>
                                <span style="color: #101820;">{row['form_factor']}</span>
                                <span style="margin: 0 0.5rem;">|</span>
                                <span style="font-weight: 700; color: #F47920;">Data Rate:</span>
                                <span style="color: #101820;">{row['data_rate']}</span>
                            </div>
                            <div style="margin-bottom: 0.5rem;">
                                <span style="font-weight: 700; color: #F47920;">Wavelength:</span>
                                <span style="color: #101820;">{row['wavelength']}</span>
                                <span style="margin: 0 0.5rem;">|</span>
                                <span style="font-weight: 700; color: #F47920;">Reach:</span>
                                <span style="color: #101820;">{row['reach']}</span>
                            </div>
                            <div>
                                <span style="font-weight: 700; color: #F47920;">Connector:</span>
                                <span style="color: #101820;">{row['connector']}</span>
                                <span style="margin: 0 0.5rem;">|</span>
                                <span style="font-weight: 700; color: #F47920;">Temp:</span>
                                <span style="color: #101820;">{row['temperature']}</span>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="margin-bottom: 0.5rem;">
                                <span style="font-weight: 700; color: #F47920;">Power:</span>
                                <span style="color: #101820;">{row['power']}</span>
                            </div>
                            <div style="display: inline-block; background: {'#4CAF50' if row['status'] == 'Active' else '#F44336'};
                                        color: white; padding: 0.25rem 0.75rem; border-radius: 20px;
                                        font-weight: 600; font-size: 0.85rem;">
                                {row['status']}
                            </div>
                        </div>
                    </div>
                    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #E0E0E0;
                                font-style: italic; color: #6B6B6B; font-size: 0.9rem;">
                        {row['description']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("No transceivers found in the catalog.")

# Admin Panel Page
elif st.session_state.current_page == "admin":
    # Check if user is authenticated
    if not st.session_state.authenticated:
        # Login Screen
        st.markdown("""
        <div style="background: linear-gradient(90deg, #101820 0%, #F47920 100%); padding: 1rem 1.5rem; border-radius: 8px; margin-bottom: 1.5rem;">
            <h2 style="color: white; margin: 0; font-weight: 700; font-size: 1.8rem;">🔐 ADMIN LOGIN</h2>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info("Please enter the admin password to access the admin panel.")

            with st.form("login_form"):
                password = st.text_input("Password", type="password", placeholder="Enter admin password")
                submit_login = st.form_submit_button("Login", use_container_width=True)

                if submit_login:
                    if password and verify_password(password):
                        st.session_state.authenticated = True
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid password!")

            st.markdown("---")
            st.caption("Default password: **admin123** (Please change after first login)")

    else:
        # User is authenticated - show admin panel
        st.markdown("""
        <div style="background: linear-gradient(90deg, #101820 0%, #F47920 100%); padding: 1rem 1.5rem; border-radius: 8px; margin-bottom: 1.5rem;">
            <h2 style="color: white; margin: 0; font-weight: 700; font-size: 1.8rem;">🔧 ADMIN PANEL</h2>
        </div>
        """, unsafe_allow_html=True)

        # Logout and password change buttons
        col1, col2, col3 = st.columns([2, 2, 6])
        with col1:
            if st.button("🔓 Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.success("Logged out successfully!")
                st.rerun()
        with col2:
            show_change_password = st.button("🔑 Change Password", use_container_width=True)

        # Show password change form if button clicked
        if show_change_password or 'show_password_change' in st.session_state:
            st.session_state.show_password_change = True

            with st.expander("Change Password", expanded=True):
                with st.form("change_password_form"):
                    old_password = st.text_input("Current Password", type="password")
                    new_password = st.text_input("New Password", type="password")
                    confirm_password = st.text_input("Confirm New Password", type="password")

                    submit_change = st.form_submit_button("Update Password")

                    if submit_change:
                        if not old_password or not new_password or not confirm_password:
                            st.error("❌ All fields are required!")
                        elif new_password != confirm_password:
                            st.error("❌ New passwords do not match!")
                        elif len(new_password) < 6:
                            st.error("❌ Password must be at least 6 characters long!")
                        elif change_password(old_password, new_password):
                            st.success("✅ Password changed successfully!")
                            if 'show_password_change' in st.session_state:
                                del st.session_state.show_password_change
                            st.rerun()
                        else:
                            st.error("❌ Current password is incorrect!")

        # Show warning if using default password
        default_pwd_warning = get_default_password_info()
        if default_pwd_warning:
            st.warning(default_pwd_warning)

        st.markdown("---")

        # Admin Actions (only visible when authenticated)
        admin_action = st.radio(
            "Select Action",
            ["Add New Transceiver", "Edit Transceiver", "Delete Transceiver"],
            horizontal=True
        )

        if admin_action == "Add New Transceiver":
            st.markdown("### Add New Transceiver")

            with st.form("add_transceiver_form"):
                col1, col2 = st.columns(2)

                with col1:
                    sku = st.text_input("SKU *", placeholder="e.g., RN-SFP-10G-SR")
                    name = st.text_input("Name *", placeholder="e.g., Ruckus 10GBASE-SR SFP+")
                    form_factor = st.selectbox("Form Factor *", ["SFP", "SFP+", "SFP28", "QSFP+", "QSFP28", "QSFP-DD"])
                    data_rate = st.selectbox("Data Rate *", ["1G", "10G", "25G", "40G", "100G", "400G"])
                    wavelength = st.text_input("Wavelength *", placeholder="e.g., 850nm")
                    reach = st.text_input("Reach *", placeholder="e.g., 300m (OM3)")

                with col2:
                    connector = st.selectbox("Connector *", ["LC", "SC", "MPO/MTP", "MPO-16"])
                    temperature = st.text_input("Temperature *", placeholder="e.g., 0 to 70°C")
                    power = st.text_input("Power *", placeholder="e.g., 1.5W max")
                    status = st.selectbox("Status *", ["Active", "EOL", "Discontinued"])
                    description = st.text_area("Description *", placeholder="Enter detailed description")

                submit_add = st.form_submit_button("Add Transceiver")

                if submit_add:
                    if all([sku, name, form_factor, data_rate, wavelength, reach, connector, temperature, power, description, status]):
                        new_transceiver = {
                            "sku": sku,
                            "name": name,
                            "form_factor": form_factor,
                            "data_rate": data_rate,
                            "wavelength": wavelength,
                            "reach": reach,
                            "connector": connector,
                            "temperature": temperature,
                            "power": power,
                            "description": description,
                            "status": status
                        }

                        if add_transceiver(new_transceiver):
                            st.success(f"✅ Successfully added transceiver: {sku}")
                            st.rerun()
                        else:
                            st.error(f"❌ Error: SKU '{sku}' already exists!")
                    else:
                        st.error("❌ Please fill in all required fields!")

        elif admin_action == "Edit Transceiver":
            st.markdown("### Edit Transceiver")

            df = get_transceivers_df()
            if not df.empty:
                selected_sku = st.selectbox("Select Transceiver to Edit", df['sku'].tolist())

                if selected_sku:
                    transceiver = get_transceiver(selected_sku)

                    with st.form("edit_transceiver_form"):
                        col1, col2 = st.columns(2)

                        with col1:
                            sku = st.text_input("SKU *", value=transceiver['sku'], disabled=True)
                            name = st.text_input("Name *", value=transceiver['name'])
                            form_factor = st.selectbox(
                                "Form Factor *",
                                ["SFP", "SFP+", "SFP28", "QSFP+", "QSFP28", "QSFP-DD"],
                                index=["SFP", "SFP+", "SFP28", "QSFP+", "QSFP28", "QSFP-DD"].index(transceiver['form_factor'])
                            )
                            data_rate = st.selectbox(
                                "Data Rate *",
                                ["1G", "10G", "25G", "40G", "100G", "400G"],
                                index=["1G", "10G", "25G", "40G", "100G", "400G"].index(transceiver['data_rate'])
                            )
                            wavelength = st.text_input("Wavelength *", value=transceiver['wavelength'])
                            reach = st.text_input("Reach *", value=transceiver['reach'])

                        with col2:
                            connector = st.selectbox(
                                "Connector *",
                                ["LC", "SC", "MPO/MTP", "MPO-16"],
                                index=["LC", "SC", "MPO/MTP", "MPO-16"].index(transceiver['connector'])
                            )
                            temperature = st.text_input("Temperature *", value=transceiver['temperature'])
                            power = st.text_input("Power *", value=transceiver['power'])
                            status = st.selectbox(
                                "Status *",
                                ["Active", "EOL", "Discontinued"],
                                index=["Active", "EOL", "Discontinued"].index(transceiver['status'])
                            )
                            description = st.text_area("Description *", value=transceiver['description'])

                        submit_edit = st.form_submit_button("Update Transceiver")

                        if submit_edit:
                            updated_transceiver = {
                                "sku": sku,
                                "name": name,
                                "form_factor": form_factor,
                                "data_rate": data_rate,
                                "wavelength": wavelength,
                                "reach": reach,
                                "connector": connector,
                                "temperature": temperature,
                                "power": power,
                                "description": description,
                                "status": status
                            }

                            if update_transceiver(sku, updated_transceiver):
                                st.success(f"✅ Successfully updated transceiver: {sku}")
                                st.rerun()
                            else:
                                st.error(f"❌ Error updating transceiver!")
            else:
                st.warning("No transceivers available to edit.")

        elif admin_action == "Delete Transceiver":
            st.markdown("### Delete Transceiver")

            df = get_transceivers_df()
            if not df.empty:
                selected_sku = st.selectbox("Select Transceiver to Delete", df['sku'].tolist())

                if selected_sku:
                    transceiver = get_transceiver(selected_sku)

                    st.warning(f"**Are you sure you want to delete this transceiver?**")
                    st.info(f"""
                    **SKU:** {transceiver['sku']}
                    **Name:** {transceiver['name']}
                    **Form Factor:** {transceiver['form_factor']}
                    **Data Rate:** {transceiver['data_rate']}
                    """)

                    col1, col2, col3 = st.columns([1, 1, 4])
                    with col1:
                        if st.button("🗑️ Confirm Delete", type="primary"):
                            if delete_transceiver(selected_sku):
                                st.success(f"✅ Successfully deleted transceiver: {selected_sku}")
                                st.rerun()
                            else:
                                st.error(f"❌ Error deleting transceiver!")

                    with col2:
                        if st.button("Cancel"):
                            st.info("Deletion cancelled.")
            else:
                st.warning("No transceivers available to delete.")

# Footer
st.markdown("""
<div class="ruckus-footer">
    <div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">
        🔶 RUCKUS NETWORKS
    </div>
    <div style="font-size: 0.9rem; color: #FFFFFF; opacity: 0.8;">
        Optical Transceivers Catalog | Powered by Streamlit
    </div>
    <div style="margin-top: 1rem; font-size: 0.85rem; opacity: 0.6;">
        © 2025 RUCKUS Networks. All rights reserved.
    </div>
</div>
""", unsafe_allow_html=True)
