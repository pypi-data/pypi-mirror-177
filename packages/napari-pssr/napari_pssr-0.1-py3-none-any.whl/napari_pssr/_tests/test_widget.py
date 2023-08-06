from napari_pssr.widgets.pssr import (
    ModelWidget
)
import numpy as np


def test_train_pssr_widget(make_napari_viewer, capsys):
    viewer = make_napari_viewer()
    model_widget = ModelWidget(viewer)
    my_widget = model_widget.create_train_widget(viewer)


