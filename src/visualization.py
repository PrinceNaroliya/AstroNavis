import plotly.graph_objects as go
import tracker

def plot_satellites(satellites):

    fig = go.Figure()

    # sirf first 20 satellites test ke liye
    for sat in satellites[:100]:

        traj = tracker.future_propagation(
            sat["line1"],
            sat["line2"],
            10
        )

        x = []
        y = []
        z = []

        for point in traj:
            pos = point["position"]

            x.append(pos[0])
            y.append(pos[1])
            z.append(pos[2])

        fig.add_trace(
            go.Scatter3d(
                x=x,
                y=y,
                z=z,
                mode="lines",
                name=sat["name"]
            )
        )

    fig.update_layout(
        title="AstroNavis Orbit Visualization",
        scene=dict(
            xaxis_title="X (km)",
            yaxis_title="Y (km)",
            zaxis_title="Z (km)"
        )
    )

    fig.show()

