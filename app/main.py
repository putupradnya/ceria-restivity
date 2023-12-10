import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# Function to create a placeholder plot
def create_placeholder_plot():
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1], 'o')
    ax.annotate('A/N', xy=(0.5, 0.5), xytext=(0.5, 0.5), textcoords='axes fraction')
    plt.close(fig)
    return fig

def load_txt(file):
    # Assuming the .txt file is a CSV without a header
    # You may need to adjust this depending on the structure of your .txt file
    return pd.read_csv(file, header=None)
    
# Set up the Streamlit layout according to the sketch
def main():
    st.set_page_config(page_title="Optimization App", layout="wide")

    # Main area with input fields, plot and model parameters
    col1, col2, col3 = st.columns((1.5, 1.5, 4))
    with col1:
        uploadFile = st.file_uploader("DATASET", type="txt")
        
        if uploadFile is not None:
            try:
                if uploadFile.name.endswith('.txt'):
                    df = pd.read_csv(uploadFile, delimiter=' ')

                height_per_row = 25
                nrows = 20
                st.dataframe(df, use_container_width=True)

            except Exception as e:
                st.error(f'Error loading your data')

    with col2:
        optionFilter = st.selectbox('FORWARD FILTER', ('7', '11'))
        
        containerInversion = st.container(border=True)
        with containerInversion:
            optionInversion = st.selectbox('INVERSION METHODS', ('-', 'SVD', 'LM'))

            if optionInversion == 'SVD':
                numIter = st.number_input('Number of Iter')
                epsilon = st.number_input('Epsilon')
                

            if optionInversion == 'LM':
                numIter = st.number_input('Number of Iter')
                dumping = st.number_input('Damping Factor')
            

        model_data = pd.DataFrame({
        'Model Number': range(1, 6),
        'Thickness': np.random.rand(5) * 10  # Random thickness for demonstration
        })
        st.data_editor(model_data)
    with col3:
        containerPlot = st.container(border=True)

        with containerPlot:

            tab1, tab2 = st.tabs(['Inversion Model', 'Earth Model'])
            
            with tab1:
                if uploadFile is not None:
                    # fig, ax = plt.subplots()
                    # ax.plot(df['AB/2'], df['RhoApp'])
                    # ax.set_xlabel(f'AB/2')
                    # ax.set_ylabel(f'RhoApp')
                    # st.pyplot(fig)
                    fig = px.scatter(df, x='AB/2', y='RhoApp', title='Resistivity Curve')
                    fig.update_layout(
                        xaxis_type="log",
                        yaxis_type="log",
                        xaxis_title="AB/2",
                        yaxis_title="RhoApp"
                    )
                    
                    # Display the figure in Streamlit
                    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
