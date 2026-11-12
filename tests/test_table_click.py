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


@pytest.mark.parametrize("ascending", [False, True])
def test_click_selects_displayed_label_when_sorted(viewer, ascending):
    lab = np.zeros((20, 20), int)
    lab[0:2, 0:2] = 1
    lab[5:8, 5:8] = 2
    lab[10:15, 10:15] = 3
    layer = viewer.add_labels(lab)
    widget = ConfigurableFeaturesTableWidget(viewer)
    if ascending:
        widget.sort_ascending.setChecked(True)

    displayed = [widget.table.item(i, 0).text() for i in range(widget.table.rowCount())]
    for row, text in enumerate(displayed):
        widget.table.setCurrentCell(row, 0)
        widget._table_clicked()
        assert layer.selected_label == int(text)
