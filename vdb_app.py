import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image



# Function to calculate costs (same as the one I provided in the previous response)
def calculate_costs(data_models, data_volume, code_changes, env_count, rollbacks, compute_to_storage_ratio):
    # Constants
    storage_cost_per_tb = 23
    gb_to_tb = 1 / 1000

    # Calculate costs with VDB disabled
    storage_cost_vdb_disabled = round(data_volume * gb_to_tb * storage_cost_per_tb,2)
    compute_cost_vdb_disabled = round(storage_cost_vdb_disabled * compute_to_storage_ratio,2)
    total_cost_vdb_disabled = round(storage_cost_vdb_disabled + compute_cost_vdb_disabled,2)

    # Calculate costs with VDB enabled
    storage_cost_vdb_enabled = round((data_volume + ((data_volume / data_models) * code_changes)) * gb_to_tb * storage_cost_per_tb,2)
    compute_units = round(code_changes,2)
    compute_unit_price = round((storage_cost_vdb_disabled * compute_to_storage_ratio) / ((code_changes + rollbacks) * env_count),2)
    compute_cost_vdb_enabled = round(compute_units * compute_unit_price,2)
    total_cost_vdb_enabled = round(storage_cost_vdb_enabled + compute_cost_vdb_enabled,2)
    
    # Calculate savings percentage
    saving_percentage = round(((total_cost_vdb_disabled - total_cost_vdb_enabled) / total_cost_vdb_disabled) * 100,2)
    total_savings = total_cost_vdb_disabled * (saving_percentage / 100)

    #Calculate ROI
    roi = round(total_savings/tooling_invest)

    return {
        'Data Models': data_models,
        'Data Volume': data_volume,
        'Code changes': code_changes,
        'Env.': env_count,
        'Rollbacks': rollbacks,
        'CS ratio*': compute_to_storage_ratio,
        'Storage': storage_cost_vdb_disabled,
        'Storage (VDB)': storage_cost_vdb_enabled,
        'Compute': compute_cost_vdb_disabled,
        'Compute (VDB)': compute_cost_vdb_enabled,
        'Total': total_cost_vdb_disabled,
        'Total (VDB)': total_cost_vdb_enabled,
        'Savings %': saving_percentage,
        'Savings $': total_savings,
        'Tool Investment (per month)': tooling_invest,
        'ROI': roi,
    }



# Define the default values and presets
# DEFAULT_VALUES = [200, 100, 40, 2, 1, 7]
PRESET_VALUES = {
    "X-Small": [50, 100, 15, 2, 1, 7],
    "Small": [200, 100, 40, 2, 1, 7],
    "Medium": [1000, 10000, 300, 3, 3, 7],
    "Medium 2": [5000, 30000, 400, 4, 3, 8],
    "Large": [3000, 100000, 600, 5, 5, 7],
    "Large 2": [1500, 800000, 1000, 5, 30, 12]
}

# Function to set team size to Custom
def set_custom():
    st.session_state['team_size'] = "Custom"

# # Sidebar with inputs
# st.sidebar.selectbox("Select Team Size", ["Small", "Medium", "Large", "Custom"], key='team_size')
# st.sidebar.markdown("### Input Parameters")
# data_models = st.sidebar.number_input("Data Models", value=PRESET_VALUES.get(st.session_state['team_size'], DEFAULT_VALUES)[0], on_change=set_custom)
# data_volume = st.sidebar.number_input("Data Volume (GB)", value=PRESET_VALUES.get(st.session_state['team_size'], DEFAULT_VALUES)[1], on_change=set_custom)
# code_changes = st.sidebar.number_input("Monthly Code Changes", value=PRESET_VALUES.get(st.session_state['team_size'], DEFAULT_VALUES)[2], on_change=set_custom)
# env_count = st.sidebar.number_input("Number of Environments", value=PRESET_VALUES.get(st.session_state['team_size'], DEFAULT_VALUES)[3], on_change=set_custom)
# rollbacks = st.sidebar.number_input("Rollbacks", value=PRESET_VALUES.get(st.session_state['team_size'], DEFAULT_VALUES)[4], on_change=set_custom)
# compute_to_storage_ratio = st.sidebar.number_input("Current Compute to Storage Ratio", value=PRESET_VALUES.get(st.session_state['team_size'], DEFAULT_VALUES)[5], on_change=set_custom)

st.set_page_config(layout="wide")


image = Image.open('OnDark.png')
st.image(image)
st.title("Benchmarking Virtual Data Builds")

with st.expander("What are Virtual Data Builds?", expanded=False):
    st.markdown("""
    Virtual Data Build (VDB) allows you to manage code changes and the state of your data warehouse from **a single system driven by git**. 
    VDB facilitates the creation of virtual data warehouse environments for each Git commit in your codebase **without the need to duplicate data or set up new physical environments**. This is achieved through a smart view pointer swap mechanism at the data warehouse level, optimizing the compute costs.
    This deep integration between your codebase and your data warehouse state brings several benefits:
    - **Instant deployment and rollback of your code changes**. Your asset’s view definition can be updated to reference any previous materialization (from any branch). 
    - **Work on production data in your feature branch** without duplicating data or impacting the production environment/branch with no additional cost.
    - **Less mental overhead**: VDB converts your code operations into data warehouse assets, saving you the pain of managing environments and promoting code through. 
    - **Significant savings on warehouse costs, ranging from 40% to 70%** depending on your setup, as we will see in this benchmark.
    
    You can find out more about Virtual Data Builds in [this article](https://www.y42.com/blog/virtual-data-builds-one-data-warehouse-environment-for-every-git-commit/)
    """)


# Use columns to create a row of filters at the top
st.markdown("### Simulation Parameters")
st.write("Here, you can adjust the parameters to define your data model, data volume, code changes frequency, number of environments, and the number of rollbacks. You can also set the compute to storage ratio.")


col1, col2, col3, col4 = st.columns(4)

# Now add your filters inside these columns
with col1:
    data_models = st.number_input('Data Models', value=200, step=100)  # Adjust the value and label accordingly

with col2:
    data_volume = st.number_input('Data Volume (GB)', value=100, step=100)  # Adjust the value and label accordingly

with col3:
    code_changes = st.number_input('Monthly Code Changes', value=40, step=100)  # Adjust the value and label accordingly

with col4:
    env_count = st.number_input('Environments', value=2, step=1)  # Adjust the value and label accordingly

col1, col2, col3, col4 = st.columns(4)

with col1:
    rollbacks = st.number_input('Rollbacks', value=1, step=1)  # Adjust the value and label accordingly

with col2:
    compute_to_storage_ratio = st.number_input('Compute to Storage ratio', value=7, step=1)  # Adjust the value and label accordingly

with col3:
    tooling_invest = st.number_input('Tool Investment (per month)', value = 1000, step=100) # Adjust the value and label accordingly

# Initialize session state
if 'df' not in st.session_state:
    # Initialize your DataFrame here with your predefined data
    small_values = calculate_costs(*PRESET_VALUES["X-Small"])
    small_values_2 = calculate_costs(*PRESET_VALUES["Small"])
    medium_values = calculate_costs(*PRESET_VALUES["Medium"])
    medium_values_2 = calculate_costs(*PRESET_VALUES["Medium 2"])
    large_values = calculate_costs(*PRESET_VALUES["Large"])
    large_values_2 = calculate_costs(*PRESET_VALUES["Large 2"])

    st.session_state['df'] = pd.DataFrame([small_values, small_values_2, medium_values, medium_values_2, large_values, large_values_2])

def add_entry(data_models, data_volume, code_changes, env_count, rollbacks, compute_to_storage_ratio):
    new_entry = calculate_costs(data_models, data_volume, code_changes, env_count, rollbacks, compute_to_storage_ratio)

    # Ensuring the saving_percentage is not negative
    if new_entry['Savings %'] < 0:
        new_entry['Savings %'] = 0


    st.session_state['df'] = pd.concat([st.session_state['df'], pd.DataFrame([new_entry])], ignore_index=True)


def remove_entry(index):
    if st.session_state['df'].empty:
        st.warning('No more entries to remove.')
    else:
        st.session_state['df'] = st.session_state['df'].drop(index)


if st.button("Add New Entry"):
    add_entry(data_models, data_volume, code_changes, env_count, rollbacks, compute_to_storage_ratio)

st.markdown('---')

col1, col2, col3 = st.columns(3)

with col1:
   st.header(tooling_invest)

with col2:
  st.header(total_savings)

with col3:
   st.header(roi)

st.markdown('---')

# Scenarios section 
st.markdown("### Scenarios overview")
st.write("In this section, you can view the table containing details about different configurations. Each entry in the table represents a configuration with details like data model, data volume, code changes frequency, number of environments, and rollbacks. You can add new entries or remove existing ones.")

with st.expander("Storage and Compute cost formulas", expanded=False):
    st.markdown("""
    #### VDB Disabled
    - **Compute cost** = (Code changes + Rollbacks) × No. of Environments
    - **Storage cost** = Data Volume
    """)

    st.markdown("""
    #### VDB Enabled
    - **Compute cost** = Code changes <span style='color: red;'>~~+ Rollbacks~~ × ~~No. of Environments~~</span>
    - **Storage cost** = Data Volume + <span style='color: green;'>New materializations as a result of code changes</span>
    """, unsafe_allow_html=True)

st.dataframe(
    st.session_state['df'],
    column_config={
        "Storage": st.column_config.NumberColumn(format="$%d"),
        "Storage (VDB)": st.column_config.NumberColumn(format="$%d"),
        "Compute": st.column_config.NumberColumn(format="$%d"),
        "Compute (VDB)": st.column_config.NumberColumn(format="$%d"),
        "Total": st.column_config.NumberColumn(format="$%d"),
        "Total (VDB)": st.column_config.NumberColumn(format="$%d"),
        "Savings %": st.column_config.NumberColumn(format="%d%%"),
        "Savings $": st.column_config.NumberColumn(format="$%d"),
        "Tool Investment (per month)": st.column_config.NumberColumn(format="$%d"),
        "ROI": st.column_config.NumberColumn(format="%d%%"),
    },
    hide_index=False,
)

st.caption('CS ratio = Compute to Storage ratio')

# Removing an entry from the main content area
remove_option = st.selectbox('Select an entry to remove:', st.session_state['df'].index)
if st.button('Remove Entry'):
    with st.empty():
        st.write("Removing entry, please wait...")
        remove_entry(remove_option)
        st.write("Entry removed!")
        st.experimental_rerun()

st.markdown('---')

# Chart Section
st.markdown("### Savings analysis plots")
st.write("This chart visualizes the size of savings as a function of the number of environments and the frequency of code changes. Each point on the chart represents a configuration, with the X-axis representing the code changes and the Y-axis representing the environments.")

fig = px.scatter(st.session_state['df'], x='Code changes', y='Env.', size='Savings %', color='Savings %',
                 hover_name='Savings %', size_max=50, labels={'Env.': 'Environments'})

fig.update_xaxes(type='category')
fig.update_yaxes(type='category')

st.plotly_chart(fig, use_container_width=True)


st.markdown('---')

# Cost analysis breakdown for one configuration
st.markdown("### Cost analysis breakdown for one configuration")
st.write("In this section, we analyze the compute and storage costs associated with different configurations: with VDB enabled and with VDB disabled. You can select an entry from the dataframe to view the respective costs in a bar chart format. This visualization aids in quickly comparing the costs associated with each setup.")
selected_index = st.selectbox('Select an index to plot:', st.session_state['df'].index)

df_filtered = st.session_state['df'].loc[[selected_index]]

data = [
    {'Category': 'VDB Disabled', 'Compute': df_filtered['Compute'].values[0], 'Storage': df_filtered['Storage'].values[0]},
    {'Category': 'VDB Enabled', 'Compute': df_filtered['Compute (VDB)'].values[0], 'Storage': df_filtered['Storage (VDB)'].values[0]}
]
df_plot = pd.DataFrame(data)

st.write('Configuration for index %s: Data models: %s, Data volume: %s (GB), Monthly code changes: %s, Environments: %s, Rollback: %s, Compute to storage ratio: %s' % (selected_index, df_filtered.loc[selected_index, 'Data Models'], df_filtered.loc[selected_index, 'Data Volume'], df_filtered.loc[selected_index, 'Code changes'], df_filtered.loc[selected_index, 'Env.'], df_filtered.loc[selected_index, 'Rollbacks'], df_filtered.loc[selected_index, 'CS ratio*']))


# Create the bar chart
fig = px.bar(df_plot, x='Category', y=['Compute', 'Storage'], title='Compute and Storage Costs for index: %s' %(selected_index), height=400)

# Adding text annotations
fig.update_traces(texttemplate='%{y:$}', textposition='inside')

# Display the bar chart
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
### **Conclusions**
- The **compute cost** decreases significantly 📉, while the **storage cost** increases only marginally 📈.
- Since compute costs are typically an order of magnitude higher than storage costs, utilizing VDB can significantly reduce the total expenditure by lowering compute costs.
- The more code changes you make and the more environments you have to promote your changes through, the bigger the cost impact will be when enabling VDB.
""")

st.markdown("")
st.markdown("### Got Curious?")

m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #421f8e;
    color:#ffffff;
}
div.stButton > button:hover {
    background-color: #7d33ff;
    color:#ffffff;
    border: #7d33ff;
    }
</style>""", unsafe_allow_html=True)

b = st.button("Try Y42 for free and save DWH cost today")


