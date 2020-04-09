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
 4fb4e75929d7a6dad02665bad38d5deb64ab8207 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 cd480a048737a87debf689ccb8472de5bec9c4af 5615 openup2u-client_2.5.4+oc-2761.diff.gz
Checksums-Sha256: 
 a321d39778789acfc9022c9e317d7a36b6a2be483be1d5fde7be4c9ce3b75810 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 06d593eecbb8cbab16ff15b15f091ec22782695a60177c58bd76f273ac118684 5615 openup2u-client_2.5.4+oc-2761.diff.gz
Files: 
 64b13233eed3ea7d4a21ef8423bc22ba 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 2ade4b7c8415c08fb07d4d00849c41fb 5615 openup2u-client_2.5.4+oc-2761.diff.gz

