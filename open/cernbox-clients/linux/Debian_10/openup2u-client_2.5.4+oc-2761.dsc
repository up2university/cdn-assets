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
 6b52deff326370cd3a7b55a9819e4e8e5069f9f8 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 58e9f82c5b81afad15451f717d3edd335eb66986 5614 openup2u-client_2.5.4+oc-2761.diff.gz
Checksums-Sha256: 
 2dfb6d6fb2df8f31c394cff5a15374bad3722841cf4f3e1684d886b1ced90066 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 03122f4395353e9972c0cc4baf1e0f51cb37f5d53297142b295a7a4d38e8da67 5614 openup2u-client_2.5.4+oc-2761.diff.gz
Files: 
 6e0aed572b2c7a89e9b45e3fdce2ec56 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 5967be220d982b4d5ad20530a1d9c4d2 5614 openup2u-client_2.5.4+oc-2761.diff.gz

