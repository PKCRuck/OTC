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

# Page configuration
st.set_page_config(
    page_title="Ruckus Optical Transceivers Catalog",
    page_icon="📡",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .filter-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .product-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<div class="main-header">📡 Ruckus Optical Transceivers</div>', unsafe_allow_html=True)

# Create tabs for different views
tab1, tab2 = st.tabs(["📦 Product Catalog", "⚙️ Admin Panel"])

# Tab 1: Product Catalog
with tab1:
    st.subheader("Product Catalog")

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
                with st.container():
                    col1, col2, col3 = st.columns([2, 3, 1])

                    with col1:
                        st.markdown(f"**SKU:** {row['sku']}")
                        st.markdown(f"**Name:** {row['name']}")

                    with col2:
                        st.markdown(f"**Form Factor:** {row['form_factor']} | **Data Rate:** {row['data_rate']}")
                        st.markdown(f"**Wavelength:** {row['wavelength']} | **Reach:** {row['reach']}")
                        st.markdown(f"**Connector:** {row['connector']} | **Temperature:** {row['temperature']}")

                    with col3:
                        st.markdown(f"**Power:** {row['power']}")
                        status_color = "🟢" if row['status'] == "Active" else "🔴"
                        st.markdown(f"**Status:** {status_color} {row['status']}")

                    st.markdown(f"_{row['description']}_")
                    st.divider()
    else:
        st.warning("No transceivers found in the catalog.")

# Tab 2: Admin Panel
with tab2:
    st.subheader("Admin Panel")

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
st.markdown("---")
st.markdown("**Ruckus Optical Transceivers Catalog** | Powered by Streamlit")
