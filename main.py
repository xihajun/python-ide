import streamlit as st
import subprocess
import os
import uuid

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

# Set the page layout to wide mode
st.set_page_config(layout="wide")

# Streamlit interface
st.title('Online Python IDE')
st.sidebar.header('Controls')
run_code = st.sidebar.button('Run Code')

# Use expander for the code input area with syntax highlighting
with st.expander("Write your Python code here:", expanded=True):
    code = st.text_area("", height=350, key="code")

# Execute the code when the button is clicked
if run_code:
    if code.strip() != "":
        with st.spinner('Running...'):
            output, error = execute_python_code(code)
        st.subheader('Output:')
        st.code(output, language='python')

        # Highlight if there's an error
        if error:
            st.error('Error in execution. See output for details.')
    else:
        st.warning('Please enter some code to execute.')

# Add instructions on the sidebar
st.sidebar.info('Enter Python code in the expander and click "Run Code" to execute.')
