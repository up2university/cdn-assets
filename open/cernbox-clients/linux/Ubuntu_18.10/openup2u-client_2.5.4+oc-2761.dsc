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
 8e750ec5c59a4f861c7d470d244113ec29885d3e 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 7ea555ada915264188656aad15b76fabcecd29b2 5612 openup2u-client_2.5.4+oc-2761.diff.gz
Checksums-Sha256: 
 e50011a2a61aee3094295103d9379ac839f01c73732bec1939fca18d3713f88c 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 1c057355b4cb816ab7d28624411dababe9ee0a2aff11950de8fa0481e044c8c9 5612 openup2u-client_2.5.4+oc-2761.diff.gz
Files: 
 92dffea2a80b6e4d2cefc556eb888501 15304354 openup2u-client_2.5.4+oc.orig.tar.gz
 1201867d0d6d1a17fd98a5a29ddf06d3 5612 openup2u-client_2.5.4+oc-2761.diff.gz

