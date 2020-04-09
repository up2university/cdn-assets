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
 20e9526783a82e18a88f281a199c2ded2ada71b4 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 c775c3906bd5fa803ff6ab668e76791e929569a9 5614 openup2u-client_2.5.4+oc-2761.diff.gz
Checksums-Sha256: 
 08260bddda9c486c63a8dad44ac88ae93c16452a7e9fdfb41adec975bcf072a4 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 ae8b2e71d92086bd242a4027ebe9e35c7909e14a2479e9ae258fe2b7eb6183df 5614 openup2u-client_2.5.4+oc-2761.diff.gz
Files: 
 c9ab3d883bced820563cf7bcb5c482a2 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 29388bb236ed1f509f8be7e2a05b3a57 5614 openup2u-client_2.5.4+oc-2761.diff.gz

