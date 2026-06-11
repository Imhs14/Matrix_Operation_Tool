import streamlit as st
import numpy as np

# Page config
st.set_page_config(page_title="Matrix Operations Tool", page_icon="🧮", layout="wide")

def parse_matrix(input_string):
    """Converts a multi-line string input into a NumPy array."""
    if not input_string.strip():
        return None
    try:
        # Split by newlines, then by commas or spaces
        lines = input_string.strip().split('\n')
        matrix = []
        for line in lines:
            if line.strip():
                # Replace commas with spaces to handle both '1,2' and '1 2' formats
                row = [float(x) for x in line.replace(',', ' ').split()]
                matrix.append(row)
        return np.array(matrix)
    except Exception:
        return "ERROR"

def main():
    st.title("🧮 Matrix Operations Tool")
    st.markdown("Enter your matrices below. You can separate numbers with **spaces** or **commas**, and use **Enter** for new rows.")
    st.markdown("---")

    # Sidebar for Operation Selection
    st.sidebar.header("Settings")
    operation = st.sidebar.radio(
        "Choose an Operation:",
        ["Addition (A + B)", "Subtraction (A - B)", "Multiplication (A × B)", "Transpose (Aᵀ)", "Determinant (|A|)"]
    )

    # Determine how many inputs are needed
    needs_two_matrices = operation in ["Addition (A + B)", "Subtraction (A - B)", "Multiplication (A × B)"]

    # Input Layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Matrix A")
        matrix_a_input = st.text_area(
            "Input Matrix A", 
            value="1, 2\n3, 4", 
            height=150,
            help="Example:\n1, 2\n3, 4"
        )
    
    if needs_two_matrices:
        with col2:
            st.subheader("Matrix B")
            matrix_b_input = st.text_area(
                "Input Matrix B", 
                value="5, 6\n7, 8", 
                height=150
            )

    st.markdown("---")

    # Process and Calculate
    if st.button("Calculate Result", type="primary"):
        matrix_a = parse_matrix(matrix_a_input)
        
        # Validate Matrix A
        if matrix_a is None or isinstance(matrix_a, str):
            st.error("Invalid input for Matrix A. Please check your formatting.")
            return

        # Handle Single Matrix Operations (Transpose & Determinant)
        if not needs_two_matrices:
            st.subheader("Result")
            if operation == "Transpose (Aᵀ)":
                result = np.transpose(matrix_a)
                st.write("Transposed Matrix:")
                st.dataframe(result)
                
            elif operation == "Determinant (|A|)":
                if matrix_a.shape[0] != matrix_a.shape[1]:
                    st.error(f"Determinant requires a square matrix. Matrix A is {matrix_a.shape[0]}x{matrix_a.shape[1]}.")
                else:
                    det = np.linalg.det(matrix_a)
                    st.success(f"The determinant is: **{det:.4f}**")
            return

        # Handle Two Matrix Operations
        matrix_b = parse_matrix(matrix_b_input)
        
        # Validate Matrix B
        if matrix_b is None or isinstance(matrix_b, str):
            st.error("Invalid input for Matrix B. Please check your formatting.")
            return

        st.subheader("Result")
        
        try:
            if operation == "Addition (A + B)":
                if matrix_a.shape != matrix_b.shape:
                    st.error(f"Dimension Mismatch: Cannot add matrices of shape {matrix_a.shape} and {matrix_b.shape}.")
                else:
                    result = np.add(matrix_a, matrix_b)
                    st.dataframe(result)

            elif operation == "Subtraction (A - B)":
                if matrix_a.shape != matrix_b.shape:
                    st.error(f"Dimension Mismatch: Cannot subtract matrices of shape {matrix_a.shape} and {matrix_b.shape}.")
                else:
                    result = np.subtract(matrix_a, matrix_b)
                    st.dataframe(result)

            elif operation == "Multiplication (A × B)":
                if matrix_a.shape[1] != matrix_b.shape[0]:
                    st.error(f"Dimension Mismatch: Cannot multiply {matrix_a.shape} by {matrix_b.shape}. Number of columns in A must equal number of rows in B.")
                else:
                    result = np.dot(matrix_a, matrix_b)
                    st.dataframe(result)
                    
        except Exception as e:
            st.error(f"An error occurred during calculation: {str(e)}")

if __name__ == "__main__":
    main()