def lysis_curve(csv, chemical_addition=False, png=False, title=False, related=False):
    '''
    **Given:** CSV, passed as the name of the file in the present directory
    **Returns:** Lysis curve line graph
    *This function always assumes your first column is your time column (x-axis).*
    *Your x-axis data must also be ints not strings if you want the annotations to work properly*
    '''
    import pandas as pd
    import plotly.graph_objs as go

    # Converts csv to dataframe
    data = pd.read_csv(csv)
    # Gets column names as list
    columns = list(data.columns)

    # Curated colors to use. Picked for decent contrast
    colors = ['black', 'pink', 'cornflowerblue', 'grey', 'blue', 'crimson', 'darkgreen', 'lightseagreen', 'navy']

    # **Improvement** Add the ability for the user to input when columns are related. For instance, cols 2 and 3 are
    # related, thus they would use the same color, but one should be a solid line and the other a dashed line
    # Idea: user enters in numbers telling which of the columns are related (in a while loop until they enter 'exit'?)
    # Then the function takes those column pairs and makes their colors nearly the same, while making their lines
    # either solid (by default), 'dash', 'dot', or 'dashdot' (those are all 4 line options)
    # Ideally a third or fourth line option in the case of triple or quadruple relations

    # Creates the plot
    fig = go.Figure()

    if related:
        num_groups = input("Enter the number of related groups (if cols 1/2, 3/4, and 5/6 are related, enter 3): ")
        # loop here over related_cols, append to a list of pairs
        # for i, _ in enumerate(num_groups):
        pairs = []
        for i in range(int(num_groups)):
            related_cols = input("Enter a related column group with each column separated by a comma (ex: 1,2): ")
            pairs.append(related_cols)

        for i, col in enumerate():
            # needs to loop through and add the pairs as the same (or nearly the same) colors,
            # but with different line markers
            fig.add_trace(go.Scatter(
                x=data[columns[0]],
                y=data[col],
                name=col,
                line=dict(color=)
            )
            )
    else:
        # Adds each column to the plot except the first (which is assumed to be the x-axis/time data)
        for i, col in enumerate(columns[1:]):
            fig.add_trace(go.Scatter(
                x=data[columns[0]],
                y=data[col],
                name=col,
                line=dict(color=colors[i])
                                    )
                         )
    fig.update_yaxes(title_text='OD550 (log)', type='log', nticks=2, ticks='inside', tickmode='linear', showgrid=False)
    fig.update_xaxes(title_text='Time (min)')

    # Adds annotations to the graph based on the user's input data
    # (i.e. what chemical they used, and when it was added)
    if chemical_addition:
        num_timepoints = int(
            input('''Enter the number of timepoints in which addition of a chemical occurred 
                    (Ex: if you added DNP to any samples at 10 min and 20 min, enter 2): '''))
        chemical_addition_timepoints = [
            input('Enter your timepoints (Ex: if you added DNP at 40 min and 50 min, enter 40 then 50): ') for i in
            range(num_timepoints)]
        chemical_name = input('Enter the chemical added (Ex: if DNP added enter DNP): ')

        # creates list of dictionaries for update_layout() detailing where on the x-axis to place the annotations
        chem_annotations = [dict(x=i, y=0.3, text=chemical_name, showarrow=True, arrowhead=4, ax=0, ay=-40) for i in
                            chemical_addition_timepoints]

        fig.update_layout(annotations=chem_annotations)

    # Gives user the option to enter a custom graph title. By default, uses the filename
    if title:
        user_title = input('Enter a custom title for your graph: ')
        fig.update_layout(
            title={
                'text': f'{user_title}',
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'})
    else:
        # Gets csv filename by indexing all but the last 4 characters, the ".csv" part
        csv_name: str = csv[:-4]
        fig.update_layout(
            title={
                'text': f'{csv_name}',
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'})

    if png:
        csv_name: str = csv[:-4]
        # saves the graph as a png in the current directory
        return fig.write_image(f"{csv_name}.png")
    else:
        # shows the graph (for jupyter or a web page)
        return fig.show()