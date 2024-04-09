import streamlit as st
import subprocess
import os
import uuid
import numpy as np
import matplotlib.pyplot as plt


# Function to execute the Python code
def execute_python_code(code):
    # Create a unique filename
    unique_filename = f"code_{uuid.uuid4().hex}.py"
    with open(unique_filename, "w") as file:
        file.write(code)
    
    # Execute the code and capture the output
    try:
        output = subprocess.check_output(
            ["python", unique_filename], stderr=subprocess.STDOUT, timeout=5,env=os.environ
        )
        return output.decode(), False
    except subprocess.CalledProcessError as e:
        return e.output.decode(), True
    finally:
        # Make sure to remove the file after execution
        os.remove(unique_filename)

# Streamlit layout configuration to hide the hamburger menu and footer
st.set_page_config(page_title='Online Python IDE', layout='wide', initial_sidebar_state="collapsed", menu_items={'Get Help': None, 'Report a bug': None, 'About': None})

# Run button at the top
run_code = st.button('Run Code')

# Columns for the code input and output display
col1, col2 = st.columns(2)

with col1:
    code = st.text_area("", "Write your code here...", height=390)

with col2:
    output_placeholder = st.empty()  # Placeholder for output

if run_code and code.strip() != "":
    output, error = execute_python_code(code)
    with col2:
        output_placeholder.code(output, language='python')
        if error:
            st.error('Error in execution. Check the output for details.')
