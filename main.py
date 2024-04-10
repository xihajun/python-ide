import streamlit as st
import subprocess
import os
import uuid

st.set_page_config(page_title='Online Python IDE', layout='wide', initial_sidebar_state="expanded")

# Custom styles
st.markdown(
    """
    <style>
    .reportview-container .markdown-text-container {
        flex: 1;
        padding-top: 0rem;
        padding-right: 2rem;
    }
    .sidebar .sidebar-content {
        padding: 0rem;
    }
    .reportview-container .main .block-container {
        padding-top: 0rem;
        padding-right: 1rem;
        padding-left: 1rem;
    }
    .reportview-container .main {
        color: white;
    }
    textarea {
        min-height: 250px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to execute the Python code
def execute_python_code(code):
    # Create a unique filename
    unique_filename = f"code_{uuid.uuid4().hex}.py"
    with open(unique_filename, "w") as file:
        file.write(code)

    # Specify the path to the Python executable within the virtual environment
    python_executable = "/home/adminuser/venv/bin/python"

    # Execute the code and capture the output
    try:
        output = subprocess.check_output(
            [python_executable, unique_filename], stderr=subprocess.STDOUT, timeout=10
        )
        return output.decode(), False
    except subprocess.CalledProcessError as e:
        return e.output.decode(), True
    finally:
        # Make sure to remove the file after execution
        os.remove(unique_filename)

# Input in the sidebar
run_code = st.sidebar.button('Run Code')
code = st.sidebar.text_area(height=200, key="code_editor")

# Output in the main area
if run_code and code.strip() != "":
    output, error = execute_python_code(code)
    if error:
        st.error('Error in execution. Check the output for details.')
    else:
        st.code(output, language='python')
