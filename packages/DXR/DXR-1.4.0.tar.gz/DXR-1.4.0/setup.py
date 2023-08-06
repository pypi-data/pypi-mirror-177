from setuptools import setup

setup(
    name='DXR',
    version='1.4.0',
    packages=['Dxr_mqtt', 'Dxr_log', 'Dxr_bytes', 'Dxr_utils', 'Dxr_video', 'Dxr_serial', 'Dxr_yaml', 'Dxr_file'],
    install_requires=['paho-mqtt', 'pyyaml', 'pyserial', 'loguru','tabulate', 'pymysql', 'sqlalchemy', 'oss2', 'imagezmq', 'simplejpeg'],
    author='luzhipeng',
    author_email='402087139@qq.com',
    license='MIT',
    url='http://pycn.me',
    description='DXR is a python library for DXR_mqtt',
)
