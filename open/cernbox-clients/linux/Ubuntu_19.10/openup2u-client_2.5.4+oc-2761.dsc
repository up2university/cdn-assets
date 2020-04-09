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
 157292619920a9ed4cb31c18969b792cffb7c196 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 e684436b2670f6f9ccf91ffdcea74ce735862e6e 5613 openup2u-client_2.5.4+oc-2761.diff.gz
Checksums-Sha256: 
 9a43f2b65cefd5a9804a556b900c34933d40f5f720d9a7e0dc85334a34745bb2 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 7850ce0b3fb1439f52c8242d7a4d259336bc8653f980714b27c4c08e83d5d332 5613 openup2u-client_2.5.4+oc-2761.diff.gz
Files: 
 1071ca7e4e37c18b895e2af1ca04e89d 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 e4b2a543022a9e1f20cc9b405baf8e14 5613 openup2u-client_2.5.4+oc-2761.diff.gz

