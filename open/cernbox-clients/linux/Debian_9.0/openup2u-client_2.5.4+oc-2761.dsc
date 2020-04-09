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
 bd7a2e02f7b4bd84534d7cd99306c9b27311b9c9 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 1bf2455419a97932a18cd149ae60dd3d39b83cde 5613 openup2u-client_2.5.4+oc-2761.diff.gz
Checksums-Sha256: 
 1da983108e3f9aba4788d02c854b2210a7f05f338bc9b3e543cc67285d1ca834 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 cc2125968c21cdd5824701d0180d54418ee29cd94d392f49f8d4b9b0741f5866 5613 openup2u-client_2.5.4+oc-2761.diff.gz
Files: 
 c44d6fbace3468ee4cb23c623edaf166 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 266a9fa081ecbf7d9e40859984a78ff4 5613 openup2u-client_2.5.4+oc-2761.diff.gz

