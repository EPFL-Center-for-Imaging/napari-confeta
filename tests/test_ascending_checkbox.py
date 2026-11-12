import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import napari
import numpy as np
import pytest

from napari_confeta import ConfigurableFeaturesTableWidget


@pytest.fixture
def viewer():
    v = napari.Viewer(show=False)
    yield v
    v.close()


def test_ascending_checkbox_follows_selected_layer(viewer):
    lab = np.zeros((20, 20), int)
    lab[0:2, 0:2] = 1
    lab[5:8, 5:8] = 2
    layer_a = viewer.add_labels(lab, name="A")
    layer_b = viewer.add_labels(lab.copy(), name="B")
    widget = ConfigurableFeaturesTableWidget(viewer)

    viewer.layers.selection.active = layer_a
    widget.sort_ascending.setChecked(True)
    assert widget.sort_ascending.isChecked()

    viewer.layers.selection.active = layer_b
    assert not widget.props_ui_store.get_ascending(layer_b)
    assert not widget.sort_ascending.isChecked()

    # Switching back restores A's state
    viewer.layers.selection.active = layer_a
    assert widget.sort_ascending.isChecked()
