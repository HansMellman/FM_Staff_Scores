# import pandas as pd
import pandas as pd
import streamlit as st

from attr_dict import staff_weights

# Set page configuration
st.set_page_config(
    page_title="FM Staff Calculator",
    page_icon="⚽",
    # layout="wide"  # Uncomment if you want a wide layout
)

# Page title and information
st.title("⚽FM Staff Calculator⚽")
original_post = "https://www.reddit.com/r/footballmanagergames/comments/1bp08lg/football_manager_2024_staff_attributes_weighting/"
st.markdown(f"Please note that all credit for the ratings used in this calculator go to the Author of the original post [here]({original_post}).")

filter_link = "https://drive.google.com/drive/folders/1uJR9m2Z08lUyL5UAWVttiKOYT8VsZfnC?usp=sharing"
st.markdown(f"Please download [this custom view]({filter_link}) and import into your game before attempting to use this calculator.")
st.write("**NOTE** - Failure to do so will render attempts to use this tool unsuccessful as the columns will not contain the information needed, nor be ordered correctly.")

# Define helper function for calculating role scores
def calculate_role_scores(df, weights):
    """Calculate the weighted average score for a role given the DataFrame and corresponding weights."""
    weighted_scores = df.apply(lambda row: sum(weights[attr] * row[attr] for attr in weights), axis=1)
    total_weights = sum(weights.values())
    return weighted_scores / total_weights

# Upload file
file = st.file_uploader(
    "Upload the HTML file exported from your game:",
    type='.html',
    accept_multiple_files=False,
    help="This data should be exported from the staff search screen using the view provided above and saved as a .html file."
)

if file is not None:
    try:
        staff_rawdata_list = pd.read_html(file, header=0, encoding='utf-8', keep_default_na=False)
        staff_rawdata = staff_rawdata_list[0]
    

        # Check for expected columns (adjust the list as needed)
        expected_columns = ['Inf', 'Name', 'Preferred Job', 'Personality', 'Applied For Job', 'Age']
        missing_cols = [col for col in expected_columns if col not in staff_rawdata.columns]
        if missing_cols:
            st.error(f"Missing expected columns: {', '.join(missing_cols)}. Please ensure you use the correct custom view when exporting data from FM.")
            st.stop()

        # Calculate role scores using a mapping to reduce repetition
        role_mapping = {
            'Manager_score': 'manager_weights',
            'AssMan_score': 'assman_weights',
            'HOYD_score': 'hoyd_weights',
            'Coach_score': 'coach_weights',
            'FitnessCoach_score': 'fitnesscoach_weights',
            'gkCoach_score': 'gkcoach_weights',
            'Spc_score': 'setpiececoach_weights',
            'PerfAn_score': 'PerfAnalyst_weights',
            'dof_score': 'dof_weights',
            'TecDir_score': 'TecDir_weights',
            'Scout_score': 'scout_weights',
            'RecAn_score': 'RecAnalyst_weights',
            'LoanMgr_score': 'LoanManager_weights',
            'physio_score': 'physio_weights',
            'sps_score': 'sportsscience_weights'
        }

        for new_col, weight_key in role_mapping.items():
            staff_rawdata[new_col] = calculate_role_scores(staff_rawdata, staff_weights[weight_key]).round(1)

        # Define the final column order
        cols = ['Inf', 'Name', 'Preferred Job', 'Personality', 'Applied For Job', 'Age', 
                'Manager_score', 'AssMan_score', 'HOYD_score', 'Coach_score', 'FitnessCoach_score',
                'gkCoach_score', 'Spc_score', 'PerfAn_score', 'dof_score',
                'TecDir_score', 'Scout_score', 'RecAn_score', 'LoanMgr_score',
                'physio_score', 'sps_score']
        staff_rawdata = staff_rawdata[cols]

        # Select columns from which to apply numeric formatting (from column index 6 onward)
        subset_cols = staff_rawdata.columns[6:]
        format_dict = {col: "{:.1f}" for col in subset_cols}

        # Display the styled DataFrame in Streamlit
        st.dataframe(
            staff_rawdata.style
                .format(format_dict)
                .highlight_max(subset=subset_cols, axis=0),
            hide_index=True
        )
    
    
    except Exception as e:
        st.error(f"Error reading file: {e}. Please ensure that you have follow the instructions above and imported the correct file.")
        st.stop() 
