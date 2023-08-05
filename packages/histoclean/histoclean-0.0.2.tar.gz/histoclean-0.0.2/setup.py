from setuptools import setup

setup(
    name='histoclean',
    version='0.0.2',
    description='Histoclean (initial package setup)',
    py_modules=["histoclean"],
    package_dir={'': 'src'},
    install_requires=[
        "Pillow", "opencv-python", "imageio",
        "numpy", "numba", "imagecorruptions",
        "openslide-python", "scipy", "imgaug",
        "scikit-image"
    ],
)