#!/bin/bash

if [ -f "./libdrm.so.2.4.0" ]; then
    ln -sf libdrm.so.2.4.0 libdrm.so.2
    ln -sf libdrm.so.2 libdrm.so
fi

if [ -f "./libdrm_amdgpu.so.1.0.0" ]; then
    ln -sf libdrm_amdgpu.so.1.0.0 libdrm_amdgpu.so.1
    ln -sf libdrm_amdgpu.so.1 libdrm_amdgpu.so
fi

if [ -f "./libdrm_intel.so.1.0.0 " ]; then
    ln -sf libdrm_intel.so.1.0.0 libdrm_intel.so.1
    ln -sf libdrm_intel.so.1 libdrm_intel.so
fi

if [ -f "./libdrm_nouveau.so.2.0.0" ]; then
    ln -sf libdrm_nouveau.so.2.0.0 libdrm_nouveau.so.2
    ln -sf libdrm_nouveau.so.2 libdrm_nouveau.so
fi

if [ -f "./libdrm_radeon.so.1.0.1" ]; then
    ln -sf libdrm_radeon.so.1.0.1 libdrm_radeon.so.1
    ln -sf libdrm_radeon.so.1 libdrm_radeon.so
fi

if [ -f "./libigdgmm.so.11.1.0" ]; then
    ln -sf libigdgmm.so.11.1.0 libigdgmm.so.11.1
    ln -sf libigdgmm.so.11.1 libigdgmm.so.11
    ln -sf libigdgmm.so.11 libigdgmm.so
fi

if [ -f "./libmfx.so.1.32" ]; then
    ln -sf libmfx.so.1.32 libmfx.so.1
    ln -sf libmfx.so.1 libmfx.so
fi
if [ -f "./libmfxhw64.so.1.32" ]; then
    ln -sf libmfxhw64.so.1.32 libmfxhw64.so.1
    ln -sf libmfxhw64.so.1 libmfxhw64.so
fi

if [ -f "./libva.so.2.700.0" ]; then
    ln -sf libva.so.2.700.0 libva.so.2
    ln -sf libva.so.2 libva.so
fi

if [ -f "./libva-drm.so.2.700.0" ]; then
    ln -sf libva-drm.so.2.700.0 libva-drm.so.2
    ln -sf libva-drm.so.2 libva-drm.so
fi

if [ -f "./libpaho-mqtt3cs.so.1.3" ]; then
    ln -sf libpaho-mqtt3cs.so.1.3 libpaho-mqtt3cs.so.1
    ln -sf libpaho-mqtt3cs.so.1 libpaho-mqtt3cs.so
fi

if [ -f "./libopencv_calib3d.so.4.5.2" ]; then
    ln -sf libopencv_calib3d.so.4.5.2 libopencv_calib3d.so.4.5
    ln -sf libopencv_calib3d.so.4.5 libopencv_calib3d.so.4
    ln -sf libopencv_calib3d.so.4 libopencv_calib3d.so
fi

if [ -f "./libopencv_dnn.so.4.5.2" ]; then
    ln -sf libopencv_dnn.so.4.5.2 libopencv_dnn.so.4.5
    ln -sf libopencv_dnn.so.4.5 libopencv_dnn.so.4
    ln -sf libopencv_dnn.so.4 libopencv_dnn.so
fi

if [ -f "./libopencv_core.so.4.5.2" ]; then
ln -sf libopencv_core.so.4.5.2 libopencv_core.so.4.5
ln -sf libopencv_core.so.4.5 libopencv_core.so.4
ln -sf libopencv_core.so.4 libopencv_core.so
fi
if [ -f "./libopencv_features2d.so.4.5.2" ]; then
    ln -sf libopencv_features2d.so.4.5.2 libopencv_features2d.so.4.5
    ln -sf libopencv_features2d.so.4.5 libopencv_features2d.so.4
    ln -sf libopencv_features2d.so.4 libopencv_features2d.so
fi

if [ -f "./libopencv_flann.so.4.5.2" ]; then
    ln -sf libopencv_flann.so.4.5.2 libopencv_flann.so.4.5
    ln -sf libopencv_flann.so.4.5 libopencv_flann.so.4
    ln -sf libopencv_flann.so.4 libopencv_flann.so
fi

if [ -f "./libopencv_imgcodecs.so.4.5.2" ]; then
    ln -sf libopencv_imgcodecs.so.4.5.2 libopencv_imgcodecs.so.4.5
    ln -sf libopencv_imgcodecs.so.4.5 libopencv_imgcodecs.so.4
    ln -sf libopencv_imgcodecs.so.4 libopencv_imgcodecs.so
fi

if [ -f "./libopencv_imgproc.so.4.5.2" ]; then
    ln -sf libopencv_imgproc.so.4.5.2 libopencv_imgproc.so.4.5
    ln -sf libopencv_imgproc.so.4.5 libopencv_imgproc.so.4
    ln -sf libopencv_imgproc.so.4 libopencv_imgproc.so
fi

if [ -f "./libopencv_video.so.4.5.2" ]; then
    ln -sf libopencv_video.so.4.5.2 libopencv_video.so.4.5
    ln -sf libopencv_video.so.4.5 libopencv_video.so.4
    ln -sf libopencv_video.so.4 libopencv_video.so
fi

if [ -f "./libboost_filesystem.so.1.80.0" ]; then
    ln -sf libboost_filesystem.so.1.80.0 libboost_filesystem.1.80
    ln -sf libboost_system.so.1.80 libboost_system.so
fi

if [ -f "./libboost_filesystem.so.1.71.0" ]; then
    ln -sf libboost_filesystem.so.1.71.0 libboost_filesystem.1.71
    ln -sf libboost_system.so.1.71 libboost_system.so
fi

if [ -f "./libjsoncpp.so.1.9.5" ]; then
    ln -sf libjsoncpp.so.1.9.5 libjsoncpp.so.25
    ln -sf libjsoncpp.so.25 libjsoncpp.so
fi

if [ -f "./libjsoncpp.so.1.9.0" ]; then
    ln -sf libjsoncpp.so.1.9.0 libjsoncpp.so.21
    ln -sf libjsoncpp.so.21 libjsoncpp.so
fi

exit 0
