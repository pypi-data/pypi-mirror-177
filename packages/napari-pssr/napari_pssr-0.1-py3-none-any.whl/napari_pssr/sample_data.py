import tifffile

from pathlib import Path

LR_LARGE= "/home/skar/Work/Code/Projects/Napari/napari-pssr/src/napari_pssr/sample_data/LR/HitachiRegulus_ssEM_rat/HitachiRegulus_ssEM_rat_LR_1.tif"
LR_8NM_EM = "/home/skar/Downloads/testing/LR/semi-synthetic_tSEM/semisynth_tSEM_test_LR_56.tif"
HR_2NM_EM = "/home/skar/Downloads/testing/HR/semi-synthetic_tSEM/semisynth_tSEM_test_HR_56.tif"


def lr_em():
    lr = tifffile.imread(LR_8NM_EM)
    return [
        (
            lr[:, :],
            {
                "name": "Low Res",
                "metadata": {"axes": ["y", "x"]},
                "scale": [8, 8],
            },
            "image",
        )
    ]


def hr_em():
    hr = tifffile.imread(HR_2NM_EM)
    return [
        (
            hr[:, :],
            {
                "name": "High Res",
                "metadata": {"axes": ["y", "x"]},
                "scale": [2, 2],
            },
            "image",
        ),
    ]

def lr_large():
    hr = tifffile.imread(LR_LARGE)
    return [
        (
            hr[:, :],
            {
                "name": "Low Res Large",
                "metadata": {"axes": ["y", "x"]},
                "scale": [8, 8],
            },
            "image",
        ),
    ]