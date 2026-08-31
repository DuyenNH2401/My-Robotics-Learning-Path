from setuptools import find_packages, setup

package_name = "my_py_pkg"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    package_data={"": ["py.typed"]},
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="DuyenNH2401",
    maintainer_email="duyennhce200017@gmail.com",
    description="TODO: Package description",
    license="TODO: License declaration",
    extras_require={
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [
            "number_publisher = my_py_pkg.number_publisher:main",
            "number_subscriber = my_py_pkg.number_subscriber:main",
        ],
    },
)
