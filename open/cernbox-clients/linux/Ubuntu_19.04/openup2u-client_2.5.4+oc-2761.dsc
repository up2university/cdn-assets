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
 57b2df15db32891ee3d8f2ac42d0730306f6a676 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 789dfb71b7af7607e8475d563cd5d225aae14fc6 5611 openup2u-client_2.5.4+oc-2761.diff.gz
Checksums-Sha256: 
 f76349893bd85c31061f318b0084dca8f132b555b1f359bec06d9fa9daea880a 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 a812bf2e0485a70e4ace3b9fcefe446a8c59d1669d5f5dc0c68b8aac3c86e300 5611 openup2u-client_2.5.4+oc-2761.diff.gz
Files: 
 3ab3c209002abb2638e70a1fcca4f1dc 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 2f05550daf50bab59971835c190e24b1 5611 openup2u-client_2.5.4+oc-2761.diff.gz

