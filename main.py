import streamlit as st
import subprocess
import os
import uuid
st.set_page_config(page_title='Online Python IDE', layout='wide', initial_sidebar_state="collapsed")

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

    # Execute the code and capture the output
    try:
        env = os.environ.copy()
        env['PATH'] = '/usr/local/bin/python:' + env['PATH']
        python_executable = "/usr/local/bin/python"
        output = subprocess.check_output(
            [python_executable, unique_filename], stderr=subprocess.STDOUT, timeout=10, env=env
        )
        return output.decode(), False
    except subprocess.CalledProcessError as e:
        return e.output.decode(), True
    finally:
        # Make sure to remove the file after execution
        os.remove(unique_filename)

# Streamlit layout configuration

# Button and code input at the top
run_code = st.button('Run Code')
code = st.text_area("", "Write your code here...", height=300, key="code_editor")

# Columns for the code input and output display
col1, col2 = st.columns(2)

# Code execution
if run_code and code.strip() != "":
    with col1:
        output, error = execute_python_code(code)
        st.code(output, language='python')
        if error:
            st.error('Error in execution. Check the output for details.')
