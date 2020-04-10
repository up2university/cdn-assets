Format: 1.0
# CAUTION: Keep in sync with genbranding.pl:addDebChangelog(...)
Source: openup2u-client
Version: 2.5.4+oc-2761
Binary: openup2u-client
Maintainer: Jürgen Weigert <jw@owncloud.com>
Architecture: any
Standards-Version: 3.9.6
# we need qt5 >= 5.5.1 https: //github.com/owncloud/client/issues/5432
# Reverted according to https: //github.com/owncloud/client/issues/5470#issuecomment-275680311
Build-Depends: debhelper (>= 9), cmake, sed, doxygen, unzip | bash,
 libsqlite3-dev, python-sphinx | python3-sphinx, libssl-dev (>= 1.0.0), zlib1g-dev,
 ocqt5121-qt5-qmake,
 ocqt5121-qttools5-dev-tools,
 ocqt5121-qtbase5-dev,
 ocqt5121-qt5keychain-dev (>= 0.7.0),
 ocqt5121-libqt5webkit5-dev (>= 2.2.0),
 ocqt5121-qtsvg5
Checksums-Sha1: 
 07643ece9e958208e6b67462cefb21ae62e8642f 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 8bde60964290c1a64f5b93d5834e1b3fa7860cd2 5615 openup2u-client_2.5.4+oc-2761.diff.gz
Checksums-Sha256: 
 4f7b87fe76270e68e33311767cb5dc1441f5c477102a411b75bd3c3c7c2919fc 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 580995d95e23ed15dba550565e61e0c3f98fe9c1f66a24dd518605695d8f14a5 5615 openup2u-client_2.5.4+oc-2761.diff.gz
Files: 
 44717920bae7f8761800c8a8d50949a8 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 c4eada0d6de916a76b4e758be84836cc 5615 openup2u-client_2.5.4+oc-2761.diff.gz

