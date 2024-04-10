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
import matplotlib.pyplot as plt
import numpy as np
import tempfile
import os

def execute_python_code(code):
    # Directory for saving plots
    plot_dir = tempfile.mkdtemp()
    modified_code = code.replace("plt.show()", f"plt.savefig(os.path.join('{plot_dir}', str(uuid.uuid4()) + '.png'))")

    unique_filename = f"code_{uuid.uuid4().hex}.py"
    with open(unique_filename, "w") as file:
        file.write(modified_code)

    python_executable = "/home/adminuser/venv/bin/python"

    try:
        output = subprocess.check_output(
            [python_executable, unique_filename], stderr=subprocess.STDOUT, timeout=10
        ).decode()

        # Check for generated plot files
        plot_files = os.listdir(plot_dir)
        return output, plot_files, False
    except subprocess.CalledProcessError as e:
        return e.output.decode(), [], True
    finally:
        os.remove(unique_filename)
        # Optionally, remove the plot directory and its contents if you don't want to keep the plots
        # for os.path.join(plot_dir, file) in plot_files:
        #     os.remove(file)
        # os.rmdir(plot_dir)

    return "", [], False

# Input in the sidebar
run_code = st.sidebar.button('Run Code')
code = st.sidebar.text_area("",height=200, key="code_editor")

if run_code and code.strip() != "":
    output, plot_files, error = execute_python_code(code)
    if error:
        st.error('Error in execution. Check the output for details.')
    else:
        st.code(output, language='python')
        for plot_file in plot_files:
            plot_path = os.path.join(tempfile.gettempdir(), plot_file)
            st.image(plot_path, caption="Plot")
