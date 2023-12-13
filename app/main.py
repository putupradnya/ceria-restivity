import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


def runInversion(initModel):
    initModel.to_excel('output.xlsx')

    
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
            

        modelData = pd.DataFrame(columns = ['Thickness', 'Rho Apparent'])
        configs = {
                    'Thickness' : st.column_config.NumberColumn('Thickness'), 
                    'Rho Apparent' : st.column_config.NumberColumn('Rho Apparent', required=True, min_value=0, max_value=1000) 
                    }
        initModel = st.data_editor(modelData, hide_index=True, column_config=configs, num_rows='dynamic')
        
        df =  pd.DataFrame(columns = ['Thickness', 'Rho Apparent'])
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            num_rows="dynamic",
        )
        if (uploadFile is None) and (optionInversion == '-'):
            st.button('RUN INVERSION', disabled=True)
        else:
            st.button('RUN INVERSION', on_click = runInversion(initModel))


    with col3:
        containerPlot = st.container(border=True)

        with containerPlot:

            tab1, tab2, tab3 = st.tabs(['Resistivity Curve', 'RMS Error', 'Earth Model'])
            
            with tab1:
                if uploadFile is not None:
                    fig = px.scatter(df, x='AB/2', y='RhoApp', title='Resistivity Curve')
                    fig.update_layout(
                        xaxis_type="log",
                        yaxis_type="log",
                        xaxis_title="AB/2",
                        yaxis_title="RhoApp"
                    )
                    
                    # Display the figure in Streamlit
                    st.plotly_chart(fig, use_container_width=True)

            with tab2:
                # Generate some sample data
                x2 = np.arange(100)
                y2 = -np.log(x2)

                # Create a step plot using Plotly
                fig2 = go.Figure(data=go.Scatter(x=x2, y=y2, mode='lines+markers', line_shape='hv'))

                # Set plot layout
                fig2.update_layout(
                    title='Iteration Vs RMSE',
                    xaxis_title='N Iter',
                    yaxis_title='RMSE'
                )
                st.plotly_chart(fig2)

            with tab3:
                # Generate some sample data
                x3 = np.linspace(0, 10, 5)
                y3 = np.random.uniform(5, 100, len(x3))

                # Create a step plot using Plotly
                fig3 = go.Figure(data=go.Scatter(x=y3, y=x3, mode='lines+markers', line_shape='vh'))

                # Set plot layout
                fig3.update_layout(
                    title='Resistivity Model',
                    xaxis_title=f'Resistivity [Ω.m]',
                    yaxis_title='Depth [m]',
                    yaxis=dict(autorange="reversed")
                )
                st.text('MODEL')
                st.plotly_chart(fig3)

if __name__ == "__main__":
    main()
