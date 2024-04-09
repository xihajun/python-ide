import streamlit as st
import subprocess
import os
import uuid

# Disable Streamlit's menu and footer
st.set_page_config(page_title='Online Python IDE', layout="wide", initial_sidebar_state="collapsed", menu_items={
    'Get Help': None,
    'Report a bug': None,
    'About': None
})

def execute_python_code(code):
    # Create a unique filename
    unique_filename = f"code_{uuid.uuid4().hex}.py"
    with open(unique_filename, "w") as file:
        file.write(code)
    
    # Execute the code and capture the output
    try:
        output = subprocess.check_output(
            ["python", unique_filename], stderr=subprocess.STDOUT, timeout=10
        )
        return output.decode(), False
    except subprocess.CalledProcessError as e:
        return e.output.decode(), True
    except subprocess.TimeoutExpired:
        return "Error: Execution time exceeded limit.", True
    finally:
        # Make sure to remove the file after execution
        os.remove(unique_filename)

# Main interface
code = st.text_area("", height=400, key="code")
run_code = st.button('Run Code')

if run_code:
    if code.strip() != "":
        output, error = execute_python_code(code)
        st.code(output, language='python')
        if error:
            st.error('Error in execution. Check the output for details.')
    else:
        st.warning('Please enter some code to execute.')
