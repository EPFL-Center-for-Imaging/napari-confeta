import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import napari
import numpy as np
import pytest

from napari_confeta._featurizer import Featurizer


@pytest.fixture
def viewer():
    v = napari.Viewer(show=False)
    yield v
    v.close()


def test_default_featurizer_tracks_label_changes(viewer):
    lab = np.zeros((10, 10), int)
    lab[0, 0] = 1
    lab[2, 2] = 2
    layer = viewer.add_labels(lab)
    featurizer = Featurizer()
    featurizer.recompute_features(layer)
    assert layer.features["label"].tolist() == [0, 1, 2]

    # A newly painted label appears in the features
    layer.data[5, 5] = 7
    featurizer.recompute_features(layer)
    assert 7 in layer.features["label"].tolist()

    # A label erased from the data no longer carries features
    layer.features = layer.features.assign(area=1.0)
    layer.data[2, 2] = 0
    featurizer.recompute_features(layer)
    feats = layer.features.set_index("label")
    assert np.isnan(feats.loc[2, "area"])
    assert feats.loc[1, "area"] == 1.0


def test_empty_labels_with_custom_featurizer(viewer):
    import pandas as pd
    from skimage.measure import regionprops_table

    def area(labels):
        return pd.DataFrame(regionprops_table(labels, properties=["label", "area"]))

    layer = viewer.add_labels(np.zeros((10, 10), int))
    Featurizer([area]).recompute_features(layer)
    assert layer.features["label"].tolist() == [0]
