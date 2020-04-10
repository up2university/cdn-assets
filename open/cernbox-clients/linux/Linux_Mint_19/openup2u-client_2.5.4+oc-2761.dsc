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
 dbac78842a5f0d7291d6f96c98e57a08592a6320 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 85e606ace8470c130359b4dbbd12918a8770b0c7 5615 openup2u-client_2.5.4+oc-2761.diff.gz
Checksums-Sha256: 
 4e4f94f305906ae702bb39a12649c7450a553cba52404985fa7f2ec0a91901b4 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 4754b13c3b3e1cefd147ad7efdfad4f5a9dfe94be9b13bb7d7cba1a35bbe9f4c 5615 openup2u-client_2.5.4+oc-2761.diff.gz
Files: 
 6b1a198bc7a564edee0e2fb776eba6a4 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 bec2b1ff5409e49b1e16c3f1858a146c 5615 openup2u-client_2.5.4+oc-2761.diff.gz

