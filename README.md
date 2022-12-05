## [PyQt5无法播放视频](https://stackoverflow.com/questions/60585605/why-media-player-pyqt5-is-not-working-on-windows-10-python)
安装[K-Lite Codec](https://www.codecguide.com/download_kl.htm) 视频解码库


## NIS Edit制作安装程序
    NSIS是一个开源的Windows系统下安装程序制作程序。它提供了安装、卸载、系统设置、文件解压缩等功能。    

安装包列表(两个都要安装):
 - [Nullsoft Scriptable Install System(NSIS)](https://nsis.sourceforge.io/Main_Page)
 - [HM NIS EDIT: A Free NSIS Editor/IDE](https://hmne.sourceforge.net/)

### QA
 - pyinstaller必须使用`--onedir`参数而非`--onefile`
 - License文件需为.rtf文件，txt文件每次compile都会被清空导致warning，原因未知
 - License文件编码必须保存为"带有 BOM 的UTF-8"，否则可能会出现乱码
 

