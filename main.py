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

col1, col2 = st.columns(2)

with col1:
    code = st.text_area("", height=300, key="code")

with col2:
    output_area = st.empty()  # Placeholder for output

# Sidebar for run button
with st.sidebar:
    run_code = st.button('Run Code')

# Execute the code when the button is clicked
if run_code:
    if code.strip() != "":
        with output_area:
            with st.spinner('Running...'):
                output, error = execute_python_code(code)
            st.code(output, language='python')
            # Highlight if there's an error
            if error:
                st.error('Error in execution. See output for details.')
    else:
        st.sidebar.warning('Please enter some code to execute.')

# Instructions on the sidebar
st.sidebar.info('Enter Python code in the left column and press "Run Code" to see the output on the right.')
