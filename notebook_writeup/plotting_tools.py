'''
Plotting code for visualising win probabilities and reachable states as 3D isosurfaces.
'''

import numpy as np
import plotly.graph_objects as go
from typing import List, Optional


def plot_isosurface_from_array(
    array: np.ndarray,
    isovalues: List[float] = [0.2, 0.4, 0.6, 0.8],
    save_as: Optional[str] = None,
    perspective: List[float] = [1, 1, 1]
) -> None:
    """
    Plots multiple isosurfaces from a 3D array of values using Plotly.

    Args:
        array (np.ndarray): 3D numpy array containing scalar values (e.g. win probabilities).
        isovalues (List[float]): Contour values to extract as surfaces.
        save_as (Optional[str]): Optional file path to save image output.
        perspective (List[float]): 3D camera perspective [x, y, z].
    """
    array = array[:, :-1, :]  # Drop last slice in j-dimension
    i_dim, j_dim, k_dim = array.shape
    i, j, k = np.meshgrid(np.arange(i_dim), np.arange(j_dim), np.arange(k_dim), indexing='ij')

    fig = go.Figure()

    for iso_val in isovalues:
        fig.add_trace(go.Isosurface(
            x=i.flatten(),
            y=j.flatten(),
            z=k.flatten(),
            value=array.flatten(),
            isomin=iso_val,
            isomax=iso_val,
            surface_count=1,
            caps=dict(x_show=False, y_show=False, z_show=False),
            opacity=0.8,
            colorscale='Viridis',
            showscale=False,
            name=f'Iso {iso_val:.2f}'
        ))

    fig.update_layout(
        font=dict(family='serif'),
        title=dict(
            text='Contours of Equal Win Probability',
            x=0.5,
            y=0.75,
            xanchor='center',
            font=dict(size=20, family='serif')
        ),
        scene=dict(
            xaxis=dict(title='Player Score', showgrid=True, gridcolor='lightgrey', showbackground=True, backgroundcolor='rgba(240,240,240,0.5)'),
            yaxis=dict(title='Opponent Score', showgrid=True, gridcolor='lightgrey', showbackground=True, backgroundcolor='rgba(240,240,240,0.5)'),
            zaxis=dict(title='Turn Total', showgrid=True, gridcolor='lightgrey', showbackground=True, backgroundcolor='rgba(240,240,240,0.5)')
        ),
        scene_camera=dict(eye=dict(x=perspective[0], y=perspective[1], z=perspective[2]))
    )

    if save_as:
        fig.write_image(save_as, scale=3)

    fig.show()


def generate_box_plots(
    array: np.ndarray,
    title: str = 'Isosurface Plot of Reachable States',
    pad: bool = False,
    save_as: Optional[str] = None,
    perspective: List[float] = [1, 1, 1]
) -> None:
    """
    Generates a box-style isosurface plot for reachable states/ policies.

    Args:
        array (np.ndarray): 3D binary array where 1 = reachable state.
        title (str): Plot title to display.
        pad (bool): Whether to pad the array borders with zeros for better edge rendering.
        save_as (Optional[str]): Optional file path to save image output.
        perspective (List[float]): 3D camera perspective [x, y, z].
    """
    padded = np.pad(array, pad_width=1, mode='constant', constant_values=0) if pad else array

    i_dim, j_dim, k_dim = padded.shape
    i, j, k = np.meshgrid(np.arange(i_dim), np.arange(j_dim), np.arange(k_dim), indexing='ij')

    fig = go.Figure(data=go.Isosurface(
        x=i.flatten(),
        y=j.flatten(),
        z=k.flatten(),
        value=padded.flatten(),
        isomin=0.75,
        isomax=1.0,
        surface_count=1,
        caps=dict(x_show=False, y_show=False, z_show=False),
        opacity=1,
        colorscale=[(0, 'darkgray'), (1, 'gray')],
        showscale=False
    ))

    fig.update_layout(
        font=dict(family='serif'),
        title=dict(
            text=title,
            x=0.5,
            y=0.75,
            xanchor='center',
            font=dict(size=20, family='serif')
        ),
        scene=dict(
            xaxis=dict(title='Player Score', showgrid=True, gridcolor='lightgrey', showbackground=True, backgroundcolor='rgba(240,240,240,0.5)'),
            yaxis=dict(title='Opponent Score', showgrid=True, gridcolor='lightgrey', showbackground=True, backgroundcolor='rgba(240,240,240,0.5)'),
            zaxis=dict(title='Turn Total', showgrid=True, gridcolor='lightgrey', showbackground=True, backgroundcolor='rgba(240,240,240,0.5)')
        ),
        scene_camera=dict(eye=dict(x=perspective[0], y=perspective[1], z=perspective[2]))
    )

    if save_as:
        fig.write_image(save_as, scale=3)

    fig.show()
