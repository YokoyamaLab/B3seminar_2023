#　エラーと解決法

## 1つめ
Traceback (most recent call last):
  File "/mnt/c/Users/hirot/programing/B3seminar/main.py", line 2, in <module>
    from ultralytics import YOLO
  File "/mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/ultralytics/__init__.py", line 5, in <module>
    from ultralytics.data.explorer.explorer import Explorer
  File "/mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/ultralytics/data/__init__.py", line 3, in <module>
    from .base import BaseDataset
  File "/mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/ultralytics/data/base.py", line 12, in <module>
    import cv2
  File "/mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/cv2/__init__.py", line 181, in <module>
    bootstrap()
  File "/mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/cv2/__init__.py", line 153, in bootstrap
    native_module = importlib.import_module("cv2")
  File "/usr/lib/python3.10/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
ImportError: libGL.so.1: cannot open shared object file: No such file or directory

### 解決策
```
apt-get install -y libgl1-mesa-dev

```
https://qiita.com/toshitanian/items/5da24c0c0bd473d514c8



## 2つめ

qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "/mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/cv2/qt/plugins" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

Available platform plugins are: xcb.

### 解決策
```
sudo apt install libsm6 
```
https://qiita.com/fukasawah/items/99219e1ff7d08915952f
https://omohikane.com/python3_open_cv_libsm/

####　解決まで
依存関係を調べてnotfoundがないようにするとよさそう
ldd /mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/cv2/qt/plugins/platforms/libqxcb.so
        linux-vdso.so.1 (0x00007ffe3e338000)
        libQt5XcbQpa-5b2d853e.so.5.15.0 => /mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/cv2/qt/plugins/platforms/../../../../opencv_python.libs/libQt5XcbQpa-5b2d853e.so.5.15.0 (0x00007f4b32cb1000)
        libpng16-7379b3c3.so.16.40.0 => /mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/cv2/qt/plugins/platforms/../../../../opencv_python.libs/libpng16-7379b3c3.so.16.40.0 (0x00007f4b32c7a000)
        libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007f4b32c59000)
        libQt5Gui-a7aedf18.so.5.15.0 => /mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/cv2/qt/plugins/platforms/../../../../opencv_python.libs/libQt5Gui-a7aedf18.so.5.15.0 (0x00007f4b323db000)
        libQt5Core-39545cc7.so.5.15.0 => /mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/cv2/qt/plugins/platforms/../../../../opencv_python.libs/libQt5Core-39545cc7.so.5.15.0 (0x00007f4b31cd6000)
        libGL.so.1 => /lib/x86_64-linux-gnu/libGL.so.1 (0x00007f4b31c4f000)
        libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007f4b31c4a000)
        libX11-xcb-69166bdf.so.1.0.0 => /mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/cv2/qt/plugins/platforms/../../../../opencv_python.libs/libX11-xcb-69166bdf.so.1.0.0 (0x00007f4b31a00000)
        libxcb-icccm-413c9f41.so.4.0.0 => /mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/cv2/qt/plugins/platforms/../../../../opencv_python.libs/libxcb-icccm-413c9f41.so.4.0.0 (0x00007f4b31600000)
        libxcb-image-e82a276d.so.0.0.0 => /mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/cv2/qt/plugins/platforms/../../../../opencv_python.libs/libxcb-image-e82a276d.so.0.0.0 (0x00007f4b31200000)
        libxcb-shm-7a199f70.so.0.0.0 => /mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/cv2/qt/plugins/platforms/../../../../opencv_python.libs/libxcb-shm-7a199f70.so.0.0.0 (0x00007f4b30e00000)
        libxcb-keysyms-21015570.so.1.0.0 => /mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/cv2/qt/plugins/platforms/../../../../opencv_python.libs/libxcb-keysyms-21015570.so.1.0.0 (0x00007f4b30a00000)
        libxcb-randr-a96a5a87.so.0.1.0 => /mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/cv2/qt/plugins/platforms/../../../../opencv_python.libs/libxcb-randr-a96a5a87.so.0.1.0 (0x00007f4b30600000)
        libxcb-render-util-43ce00f5.so.0.0.0 => /mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/cv2/qt/plugins/platforms/../../../../opencv_python.libs/libxcb-render-util-43ce00f5.so.0.0.0 (0x00007f4b30200000)
        libxcb-render-637b984a.so.0.0.0 => /mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/cv2/qt/plugins/platforms/../../../../opencv_python.libs/libxcb-render-637b984a.so.0.0.0 (0x00007f4b2fe00000)
        libxcb-shape-25c2b258.so.0.0.0 => /mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/cv2/qt/plugins/platforms/../../../../opencv_python.libs/libxcb-shape-25c2b258.so.0.0.0 (0x00007f4b2fa00000)
        libxcb-sync-89374f40.so.1.0.0 => /mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/cv2/qt/plugins/platforms/../../../../opencv_python.libs/libxcb-sync-89374f40.so.1.0.0 (0x00007f4b2f600000)
        libxcb-xfixes-9be3ba6f.so.0.0.0 => /mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/cv2/qt/plugins/platforms/../../../../opencv_python.libs/libxcb-xfixes-9be3ba6f.so.0.0.0 (0x00007f4b2f200000)
        libxcb-xinerama-ae147f87.so.0.0.0 => /mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/cv2/qt/plugins/platforms/../../../../opencv_python.libs/libxcb-xinerama-ae147f87.so.0.0.0 (0x00007f4b2ee00000)
        libxcb-xkb-9ba31ab3.so.1.0.0 => /mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/cv2/qt/plugins/platforms/../../../../opencv_python.libs/libxcb-xkb-9ba31ab3.so.1.0.0 (0x00007f4b2ea00000)
        libxcb.so.1 => /lib/x86_64-linux-gnu/libxcb.so.1 (0x00007f4b31c1a000)
        libXext.so.6 => /lib/x86_64-linux-gnu/libXext.so.6 (0x00007f4b31c05000)
        libX11.so.6 => /lib/x86_64-linux-gnu/libX11.so.6 (0x00007f4b318c0000)
        libSM.so.6 => not found
        libICE.so.6 => not found
        libxkbcommon-x11-c65ed502.so.0.0.0 => /mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/cv2/qt/plugins/platforms/../../../../opencv_python.libs/libxkbcommon-x11-c65ed502.so.0.0.0 (0x00007f4b2e600000)
        libxkbcommon-71ae2972.so.0.0.0 => /mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/cv2/qt/plugins/platforms/../../../../opencv_python.libs/libxkbcommon-71ae2972.so.0.0.0 (0x00007f4b2e200000)
        libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007f4b318bb000)
        libstdc++.so.6 => /lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007f4b2dfd4000)
        libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007f4b31519000)
        libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007f4b31899000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f4b2ddab000)
        libSM.so.6 => not found
        libICE.so.6 => not found
        libgthread-2.0.so.0 => /lib/x86_64-linux-gnu/libgthread-2.0.so.0 (0x00007f4b31894000)
        libglib-2.0.so.0 => /lib/x86_64-linux-gnu/libglib-2.0.so.0 (0x00007f4b310c6000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f4b32e75000)
        libGLdispatch.so.0 => /lib/x86_64-linux-gnu/libGLdispatch.so.0 (0x00007f4b31461000)
        libGLX.so.0 => /lib/x86_64-linux-gnu/libGLX.so.0 (0x00007f4b3185e000)
        libxcb-util-4d666913.so.1.0.0 => /mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/cv2/qt/plugins/platforms/../../../../opencv_python.libs/libxcb-util-4d666913.so.1.0.0 (0x00007f4b2da00000)
        libXau-00ec42fe.so.6.0.0 => /mnt/c/Users/hirot/programing/B3seminar/.venv/lib/python3.10/site-packages/cv2/qt/plugins/platforms/../../../../opencv_python.libs/libXau-00ec42fe.so.6.0.0 (0x00007f4b2d600000)
        libXau.so.6 => /lib/x86_64-linux-gnu/libXau.so.6 (0x00007f4b31856000)
        libXdmcp.so.6 => /lib/x86_64-linux-gnu/libXdmcp.so.6 (0x00007f4b3184e000)
        libpcre.so.3 => /lib/x86_64-linux-gnu/libpcre.so.3 (0x00007f4b31050000)
        libbsd.so.0 => /lib/x86_64-linux-gnu/libbsd.so.0 (0x00007f4b31834000)
        libmd.so.0 => /lib/x86_64-linux-gnu/libmd.so.0 (0x00007f4b31827000)

sudo apt install libsm6 で動いた！！！！！！！！！！！
やはりここらへんが悪さしてたみたい
        libSM.so.6 => not found
        libICE.so.6 => not found
