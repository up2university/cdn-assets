#!/usr/bin/python
#
# 2015-04-08   Stefan Hartnagel <stefan@owncloud.com>
# 2015-2019    Juergen Weigert  <jw@owncloud.com>
#
# added -d foldername option.
# V1.1 code refactoring: FindPackages(), class ParseUrl(), BuildHtml()
# 2015-05-29, jw v1.2   refactored: +enable_gpg_check (must be False), fixup_repomd_xml_location(), fixup_repo_files()
#                       fixed namespace-stripper code to use [-1] instead of [1] to survive tags without namespace.
# 2015-06-01, jw v1.3   refactored createYmp() into ymp_write(), RepoTemplate, YmpTemplate, ymp_added_repos()
#                       ported ymp-mapping.txt from server to client/ymp-added-repos.txt updated the descriptions to
#                       not raise security concerns.
# 2015-06-17, jw v1.4   refactored BuildHtml() into replace_commented_html(), write_ymp_html(), update_html()
# 2015-06-24, jw v1.5   yaml_load_expand() for repo_usage.yaml, write_platform_html() added.
# 2015-06-25, jw v1.6   HideButtonsCSS added to update_html(). list_packagenames() added.
#                       All unused code removed.
# 2015-06-29, jw v1.7   option --example added to copy everything into the workspace area.
# 2015-07-01, jw v1.8   option --script added. renamed repo-admin.py
# 2015-07-07, jw v1.9   refactored refresh_url() from main()
# 2015-07-15, jw v1.10  obsoleted yaml_load_expand() with config_load_expand(),
#                       repo_usage.yaml with repo_config_data.py
# 2015-07-15, jw v1.11  ConfigParser() ini instead of plain python source.
#                       Python3 safe. expandtabs.
# 2015-07-16, jw v1.12  strip hex checksum from primary and friends.
#                       fixup_repomd_xml_location() obsoleted by write_repomd_xml()
#                       Dummy sign_repomd_file() added with instructive comment.
# 2015-09-28, jw v1.13  Cleanup old credentials.
# 2015-10-15, jw v1.14  No rewrite of repomd.xml -- that is signed!
#                       https://github.com/owncloud/administration-internal/issues/2
#                       https://github.com/owncloud/administration-internal/issues/3
# 2015-10-19, jw v1.15  handle missing destdir in fillup_destdir()
# 2015-10-21, jw v1.16  rearranged layout. DEfault confdir also searches 'client' and default indexfile
#                       is now 'index.html'
# 2015-10-27, jw v1.17  Try assets in three different well known locations.
# 2015-11-19, jw v1.18  Allow 1.oc20151119 as buildrelease number.
# 2016-01-28, jw v1.19  sort order reverse, show Ubuntu instead of xUbuntu
# 2016-03-17, jw v1.20  Allow comma-seperated list with -p . Added FindPackagesList() as a wrapper to FindPackages().
#                       Added merge_packnames() and merge_dict() more for loops, so that muliple packages
#                       per html file can show up. Fixes https://github.com/owncloud/core/issues/23188#issuecomment-198272725
#                       https://github.com/owncloud/owncloud.org/issues/910
# 2016-03-17, jw v1.21  Hide Platform Buttons dependening on existing packages.
#                       No more confusion about empty Fedora tab.
#                       Done: check_primary_xml_location() boldly warns when there is xml:base url. -- this is not relocatable.
# 2016-05-21, jw v1.22  Fixed https://github.com/owncloud/core/issues/24764
#                       Reverse sort of platforms, repo.cfg fully html-escaped.
# 2017-09-28, jw v1.23  Added --project reponame parameter. Used in refresh-client-cl-oc-pages.sh
#                       renaming *.repo files accordingly.
# 2017-10-05, jw v1.24  write_download_json() added.
# 2017-10-05, jw v1.25  option --delrepofile added. SUSE: /etc/zypp/repos.d/*.repo,
#                       Ubuntu/Debian: /etc/apt/sources.list.d/*.list, RHEL/Fedora/CentOS: /etc/yum.repos.d/*.repo
# 2018-12-14, jw v1.26  Better diagnostics, in case createrepo was never run.
# 2019-04-03, jw v1.27  Merge Linux_Mint into Ubuntu.
# 2019-04-16, jw v1.28  Support repo without arch subdirectories (as built by gitea.int.owncloud.com/client/build-linux)
#                       Added option --insecure to downgrade DownloadUrlHttps and DownloadUrlHttpsCred to http:// only.
#                       Added fixup_install_files() for INSTALL.sh url updates.
# 2019-04-17, jw v1.29  specialcase install_script_html: kill that var, when there is no INSTALL.sh
#                       Added support for concatenated allplatforms.html to write_platform_html()
# 2019-05-22, jw v1.30  Forked from administration-internal/obs-integration/download-page/repo-admin.py
# 2019-05-23, jw v1.31  python3 compat++ while maintaining python2 compatibility, sh example.sh instead of bash.
# 2019-07-25, jw v1.32  improved error message, when called on a repo for a different package.
# 2019-11-26, jw v1.33  Prefix dir, when complaining about no match in primary.xml
# 2019-12-10, jw v1.34  allow openSUSE to begin their release number with letters, e.g. NAME-10.3.2-lp1.1.1.noarch.rpm
# 2020-02-07, jw v1.35  print SUSE versions with 'lp' as 2.5.4-lp151.2719 instead of 2.5.4-lp151
#                       print fat WARNING about unparseable version number syntax (instead of silently skipping).
#
# TODO:
# * bring INSTALL.sh instructions in sync with assets/repo.cfg
# * Find out, when xml:base is present in repomd.xml -- we have to flag it as an error, as this is not relocatable.
# * nicer folding, so that we only show the full script block, when clicked.
# * Check Packages / Packages.gz for consistency. https://github.com/owncloud/core/issues/24887
#
# CAUTION: Keep in sync with gitea.owncloud.services/client/build-linux/download-page
# CAUTION: Keep in sync with gitea.owncloud.services/ownbrander/scripting/client-linux/genbranding/download-page
# CAUTION: Keep in sync with github/owncloud/administration-internal/obs_integration/download-page

from __future__ import print_function

from argparse import ArgumentParser, RawDescriptionHelpFormatter
import ast, sys, os, re, time, tempfile
import subprocess, base64
import shutil, errno, stat
import json


try:
  import ConfigParser
except:
  import configparser as ConfigParser    # python 3

try:
  import sha
except:
  from hashlib import sha1               # python 3
  class sha:
    def new(x): return sha1(x)

# for parsing meta files.
import gzip
import xml.etree.cElementTree as ET

_version_ = '1.35'

enable_gpg_check = True                 # caution: we cannot re-sign so we must not have any (changeable!) URLs in signed files.

# FIXME: The Linux Mint hack in write_platform_html() below should be a buttonAlias = {} redirect here.
buttonList=["CentOS","Debian","Fedora","openSUSE","SL","SLE","Ubuntu","Univention","RHEL","Arch","Other" ]
hidden = ['Arch', 'SL', 'Other' ]       # FIXME: hidden platforms are hardcoded here. Should by dynamic: hide when empty.

https_slash_slash = 'https://'          # used in DownloadUrlHttps and DownloadUrlHttpsCred. Downgrade to http:// with --no-https

RepoTemplate = """
      <repository recommended="true">
        <name>{repo_name}</name>
        <summary>{repo_summary}</summary>
        <description>{repo_description}</description>
        <url>{repo_url}</url>
      </repository>
"""
# usage: repo_templates is at least one RepoTemplate filled in with the repo itself. Typically we would also add
# a second repo there pointing to the respective opensuse project repo to help with dependencies...
# Stefan has a list of these adtional repos in ymp-mapping.txt.
YmpTemplate = """<metapackage xmlns:os="http://opensuse.org/Standards/One_Click_Install" xmlns="http://opensuse.org/Standards/One_Click_Install">
  <group>
    <repositories>
{pack_repos}
    </repositories>
    <software>
      <item>
        <name>{pack_name}</name>
        <summary>{pack_summary}</summary>
        <description>{pack_description}</description>
      </item>
    </software>
  </group>
</metapackage>
"""

ympPath="./ymp/"
pack_name_re=['.*']                                # derived from tar name, or -p or --packname
foldername="download"                              # option --download-dir -d
indexfile="index.html"                             # option --indexfile -i
download_url='http://USER:PASS@www.example.com/download'        # option --url -u
project_reponame=None                              # default via project_from_meta_l()
del_project_reponame=''                            # option --delrepofile -D

confdir=os.path.dirname(sys.argv[0])
if confdir =="": confdir="."
if not os.path.exists(confdir+'/assets'):
  confdir=confdir+'/client'                        # try the github layout
  if not os.path.exists(confdir+'/assets'):
    confdir=os.path.dirname(sys.argv[0])           # try the download/{bin,assets} layout done by --example.
    if confdir =="": confdir="."
    confdir=confdir+'/..'
    if not os.path.exists(confdir+'/assets'):
      confdir='/usr/share/obs-download-page'       # try installed package layout


# Keep in sync with internal_tar2obs.py obs_docker_install.py
def run(args, input=None, redirect=None, redirect_stdout=True, redirect_stderr=True, return_tuple=False, return_code=False, tee=False):
  """
     make the subprocess monster usable
  """

  # be prepared. I have seen overwritten lines in the log when subprocess docker build errors out.
  sys.stdout.flush()
  sys.stderr.flush()

  if redirect is not None:
    redirect_stderr = redirect
    redirect_stdout = redirect

  if redirect_stderr:
    redirect_stderr=subprocess.PIPE
  else:
    redirect_stderr=sys.stderr

  if redirect_stdout:
    redirect_stdout=subprocess.PIPE
  else:
    redirect_stdout=sys.stdout

  in_redirect=""
  in_fd=None
  if input is not None:
    in_fd = subprocess.PIPE
    if run.verbose > 1: in_redirect=" (<< '%s')" % input
    input = input.encode()              # bytes needed for python3

  if run.verbose: print("+ %s%s" % (args, in_redirect))
  p = subprocess.Popen(args, stdin=in_fd, stdout=redirect_stdout, stderr=redirect_stderr)

  (out,err) = p.communicate(input=input)

  if tee:
    if tee == True: tee=sys.stdout
    if out: print >>tee, " "+ out
    if err: print >>tee, " STDERROR: " + err

  if return_code:  return p.returncode
  if return_tuple: return (out,err,p.returncode)
  if err and out:  return out + "\nSTDERROR: " + err.decode()
  if err:          return "STDERROR: " + err.decode()
  return out
run.verbose=0


def FindPackagesList(path, pkg_re_list):
  meta_l = []
  for pkg_re in pkg_re_list:
    (dic,meta) = FindPackages(path, pkg_re)
    meta_l.append({'meta':meta, 'dic':dic, 'pkg_re':pkg_re})
  return meta_l

def FindPackages(path, pkg_re):
  """ looks for matching packages in the tree found at path.
      Toplevel directories there are expected to be distribution names.
      These should contain download repo contents as populated by obs.
      We parse package file names for DEB and RPM names to fill in dic.
      We parse the DEB Release files and the RPM .repo files to fill in meta.
  """
  dic = {}
  meta = {}
  subdirs = 0
  repodata_dirs = 0             # for RPM
  release_files = 0             # for DEB
  for dir in os.listdir(path):
      if not os.path.isdir(path+'/'+dir): continue
      subdirs += 1
      distribution = re.match(r"(([^_]+)_(.*))", dir)   #CentOS_6_PHP54/ --> CentOS & CentOS6_PHP54
      if not distribution: continue
      d_full = distribution.group(1)                    #CentOS_6_PHP54         Ubuntu_14.04
      d_base = distribution.group(2)                    #CentOS                 Ubuntu
      d_vers = distribution.group(3)                    #6_PHP54                14.04
      if FindPackages.verbose: print("seen d_full=%s, d_base=%s, d_vers=%s" % (d_full, d_base, d_vers))

      if not d_full in meta: meta[d_full] = { 'base': d_base }

      primary=None
      if os.path.exists(path+'/'+dir+'/repodata'):
        repodata_dirs += 1
        for file in os.listdir(path+'/'+dir+'/repodata'):
          if re.match('(.*-)?primary\.xml\.gz$', file):
            primary = 'repodata/'+file
      # else:
      #   print("no repodata in "+dir)        # repodata only in RPM

      if primary:
        if not 'primary.xml' in meta[d_full]: meta[d_full]['primary.xml'] = { 'name':primary }
        it = ET.iterparse(gzip.open(path+'/'+dir+'/'+primary, 'rb'))
        for _, el in it: el.tag = el.tag.split('}', 1)[-1] # strip all namespaces
        root = it.root
        all_pkg = []
        for el in root.iter('package'):
          all_pkg.append(el.find('name').text)
          if (re.match(r''+pkg_re+'$', el.find('name').text)):
            vers = el.find('version')
            vend = el.find('vendor')
            if vend is not None: meta[d_full]['primary.xml']['vendor'] = vend.text
            if vers is not None: meta[d_full]['primary.xml']['version'] = vers.attrib
            break
        else:
          print(dir+": no package in primary.xml matches '"+pkg_re+"': ", all_pkg)

      if os.path.exists(path+'/'+dir+'/repodata/repomd.xml'):
        if not 'repomd.xml' in meta[d_full]: meta[d_full]['repomd.xml'] = {}
        it = ET.iterparse(open(path+'/'+dir+'/repodata/repomd.xml', 'rb'))
        for _, el in it: el.tag = el.tag.split('}', 1)[-1] # strip all namespaces
        root = it.root
        for el in root.iter('repo'):
          meta[d_full]['repomd.xml']['repo'] = el.text
          break

      if os.path.exists( path+'/'+dir+'/Release'):
        release_files += 1
        for line in open(path+'/'+dir+'/Release', 'rb').readlines():
          if not 'Release' in meta[d_full]: meta[d_full]['Release'] = {}
          m = re.match(r'(\w+):\s+(.*)', line.decode())
          if (m):
            # Origin: obs://obs.int.owncloud.com/ownbrander:PACKAGENAME/Ubuntu_12.04
            meta[d_full]['Release'][m.group(1)] = m.group(2)

      for metafile in os.listdir(path+'/'+dir):
        # print(path+'/'+dir,metafile)
        if not os.path.isdir(path+'/'+dir+'/'+metafile):
          if (re.match(r".*\.ymp$", metafile)):
            meta[d_full]['ymp'] = dir+'/'+metafile
          if (re.match(r".*\.repo$", metafile)):
            meta[d_full]['.repo'] = dir+'/'+metafile

      # we expect arch subdirectories. But we also accept arch dependant files diretly in dir (in case only one architecture is supported)
      for arch in os.listdir(path+'/'+dir)+['.']:
        if arch in ('repodata', 'src'): continue
        if not os.path.isdir(path+'/'+dir+'/'+arch):
          if FindPackages.verbose: print("Not a dir: arch="+arch)
          continue

        for pkg in sorted(os.listdir(path+'/'+dir+'/'+arch), reverse=True):
          # reverse sort due to https://github.com/owncloud/administration-internal/issues/10
          # the first one that parses correctly is taken.
          # good: /space/tmp/surfdrive-2.0.2.506-linux/Ubuntu_14.04/amd64/surfdrive-client_2.0.2-1.oc20151119_amd64.deb
          # bad:  /space/tmp/surfdrive-2.0.2.506-linux/Ubuntu_14.04/all/surfdrive-client-doc_2.0.2-1.oc20151119_all.deb
          #
          if FindPackages.verbose: print(path+'/'+dir+'/'+arch+" has package "+pkg)
          version=re.match(r"("+pkg_re+")_(\d[^_]*)-(\d[^_]*)_[^-]+$",pkg)    #DEB: PACKAGENAME-8.0.2-6_all.deb -> 8.0.2 & 6
          if not version:
            #RPM: PACKAGENAME-8.0.2-28.1.src.rpm -> 8.0.2 & 28.1
            version=re.match(r"("+pkg_re+")-(\d[^-]*)-(\d[^\.]*)\.[^-]+$",pkg)
          if not version:
            #RPM: PACKAGENAME-10.3.2-lp151.1.1.noarch.rpm -> 10.3.2 & lp151.1.1
            version=re.match(r"("+pkg_re+")-(\d[^-]*)-(\w*\.\d[^\.]*)\.[^-]+$",pkg)
          if version:
            nam = version.group(1)
            ver = version.group(2)
            rel = version.group(3)
            if not d_base in dic: dic[d_base] = {}

            # dic= { 'CentOS': { 'CentOS_7':[8.0.2,6,'CentOS_7/all/PACKAGENAME-8.0.2-6.src.rpm'] } }
            dic[d_base][d_full] = [ver,rel, dir+"/"+arch+"/"+pkg, nam]
            # print(pkg+": growing dic ", d_base, d_full, dic[d_base][d_full])
            break
          else:
            # this is how we weed out all the meta files, that are not packages
            if FindPackages.verbose: print(pkg+": could not parse version number")
          if not version:
            if re.match(r"("+pkg_re+")-(\d[^-]*)", pkg):
              print("\nWARNING: FindPackages: packages ignored. Could not parse version number: ", '/'.join([path,dir,arch,pkg]))


  if not dic:
    print("Destination path needs to point to an unpacked tree with")
    print(" * packages matching '"+pkg_re+"'")
    print(" * repodata subdirectories for RPM based systems")
    print(" * Release files for DEB based systems")
    print("ERROR: packages or metadata not found in "+path+"/*/")
    print("INFO: seen %d subdirs, %d repodata folders (RPM), %d Release files (DEB)." % (subdirs, repodata_dirs, release_files))
    if subdirs > 0 and ( repodata_dirs + release_files ) == 0:
      print("HINT: run /usr/bin/createrepo first to add the missing metadata")
    sys.exit(1)

  if 'RedHat' in dic.keys():
    for z in dic['RedHat'].keys():
      znew = re.sub('^RedHat','RHEL',z)
      if not 'RHEL' in dic: dic['RHEL'] = {}
      if not znew in dic['RHEL']:
        print("RedHat fallback seen",z, dic['RedHat'][z])
        dic['RHEL'][znew] = dic['RedHat'][z]
        del(dic['RedHat'])
  if 'xUbuntu' in dic.keys():
    for z in dic['xUbuntu'].keys():
      znew = re.sub('^x','',z)
      if not 'Ubuntu' in dic: dic['Ubuntu'] = {}
      if not znew in dic['Ubuntu']:
        print("xUbuntu fallback seen",z, dic['xUbuntu'][z])
        dic['Ubuntu'][znew] = dic['xUbuntu'][z]
    del(dic['xUbuntu'])

  return dic,meta
FindPackages.verbose = False



def replace_commented_html(file, dic):
   """ for each KEY,VAL in dic, search through file, and
       replace all occurences of <!-- @@KEY@@ -->xxxxx<!----> with
       <!-- @@KEY@@ -->VAL<!---->. Note that the comment that anchors the key
       remains unchanged, so that the resulting file works fine for a subsequent replace.

       Alternative syntax:
       <!-- @@packageName@@cdata[2] --><title>Install package someword</title><!---->
       changes the second word of the cdata inside the container. 'someword'

       The named file is changed inplace. The number of substitutions is returned.
   """
   txt = open(file,'rb').read()
   total_subst = [ 0 ]

   def replace_commented_html_cb(m):
     total_subst[0] += 1
     k = m.group(1).decode()
     v = "UNKNOWN_SUBST(@@"+k+"@@)"
     if k in dic: v = dic[k]
     q = ''
     if m.group(3) is not None:
       q = m.group(2).decode()
       container = re.split(r'[<>]', m.group(4).decode())
       # ['', 'title', 'Install package someword', '/title', '']
       cdata = container[2].split()
       cdata[int(m.group(3))] = v
       v='<'+container[1]+'>'+' '.join(cdata)+'<'+container[3]+'>'
     r = '<!-- @@'+k+'@@'+q+' -->'+v+'<!'
     # print("replace_commented_html_cb: "+r)
     return r.encode()

   txt = re.sub(br'<!--\s*@@([^@]+)@@(cdata\[(\d+)\])?\s*-->(.*?)<!', replace_commented_html_cb, txt)

   f = open(file, "wb")
   f.write(txt)
   f.close()
   return total_subst[0]


def merge_dict(meta_l):
  dict = {}
  # owncloud {'CentOS': {'CentOS_7': ['9.0.0', '1', 'CentOS_7/noarch/owncloud-9.0.0-1.1.noarch.rpm', 'owncloud']}, 'openSUSE': {'openSUSE_Leap_42.1': ['9.0.0', '1', 'openSUSE_Leap_42.1/noarch/owncloud-9.0.0-1.1.noarch.rpm', 'owncloud'],
  # owncloud-files {'CentOS': {'CentOS_7': ['9.0.0', '1', 'CentOS_7/noarch/owncloud-files-9.0.0-1.1.noarch.rpm', 'owncloud-files']}, 'openSUSE': {'openSUSE_Leap_42.1': ['9.0.0', '1', 'openSUSE_Leap_42.1/noarch/owncloud-files-9.0.0-1.1.noarch.rpm', 'owncloud-files'],
  # merge the dict entries to
  # {
  #   'CentOS':
  #     {
  #       'CentOS_7':
  #         [
  #              ['9.0.0', '1', 'CentOS_7/noarch/owncloud-9.0.0-1.1.noarch.rpm', 'owncloud']
  #              ['9.0.0', '1', 'CentOS_7/noarch/owncloud-files-9.0.0-1.1.noarch.rpm', 'owncloud-files']
  #         }
  #     },
  #  .....
  for m in meta_l:
    for d_base in m['dic']:
      if not d_base in dict: dict[d_base] = {}
      for dist in m['dic'][d_base]:
        if not dist in dict[d_base]: dict[d_base][dist] = []
        dict[d_base][dist].append(m['dic'][d_base][dist])
  return dict


def write_ymp_html(path, meta_l):
  """ create ymp.html files like this:
 <a class="soo_ymplink soo_distro soo_distro_openSUSE soo_distro_openSUSE_13.1" href="./ymp/openSUSE_13.1/PACKAGENAME.ymp">openSUSE_13.1</a>
 <a class="soo_ymplink soo_distro soo_distro_openSUSE soo_distro_openSUSE_13.2" href="./ymp/openSUSE_13.2/PACKAGENAME.ymp">openSUSE_13.2</a>
  """
  dict = merge_dict(meta_l)
  for d_base in dict:
    if not re.match('(openSUSE|SLE)', d_base): continue
    fname = path+'/'+foldername+'/ymp/'+d_base+'_ymp.html'
    f = open(fname, "w")
    for dist in dict[d_base]:
      # [ ['1.7.2~beta1', '2.1', 'openSUSE_Factory/x86_64/PACKAGENAME-1.7.2~beta1-2.1.x86_64.rpm', 'PACKAGENAME'], [...], ... ]
      for pkg in dict[d_base][dist]:        # merged dict has a list of lists here.
        packname = pkg[3]
        f.write('<a class="soo_ymplink soo_distro soo_distro_%s soo_distro_%s" href="./ymp/%s/%s.ymp">%s</a>\n' % (d_base, dist, dist, packname, dist))
    f.close()

def config_load_expand(config_file):
  ## config is ini syntax
  ini = ConfigParser.ConfigParser()
  ini.read(config_file)
  cfg = {}
  for sect in ini.sections():
    cfg[sect] = {}
    for (k,v) in ini.items(sect): cfg[sect][k] = v

  ## if config is plain python syntax
  # cfg = ast.literal_eval(open(config_file).read())

  for k in cfg.keys():
    t = cfg[k]
    base_seen = []
    for depth in range(5):        # may be needed, if a base has anotherbase, we a parsing them in random order.
      if 'base' in t:
        t_base = t['base']
        del(t['base'])
        if type(t_base) == type(''): t_base = t_base.split()        # allow space delimited or list
        for b in t_base:
          if not b in base_seen:
            for bk in cfg[b].keys():
              if not bk in t:
                t[bk] = cfg[b][bk]
          base_seen.append(b)
  return cfg


## obsolete
def yaml_load_expand(yaml_file, top='platform'):
  yfp = open(yaml_file)
  y = yaml.load(yfp)
  for k in y[top].keys():
    t = y[top][k]
    base_seen = []
    for depth in range(5):        # may be needed, if a base has anotherbase, we a parsing them in random order.
      if 'base' in t:
        t_base = t['base']
        del(t['base'])
        for b in t_base:
          if not b in base_seen:
            for bk in y[top][b].keys():
              if not bk in t:
                t[bk] = y[top][b][bk]
          base_seen.append(b)
  return y[top]

def project_from_meta_l(meta_l, plat):
  """
  meta_l[0]['meta'][plat] = { 'primary.xml': {'version': { 'epoch': '0', 'ver': '1.7.2', 'rel': '0.2.1.beta1'}, 'vendor': 'obs://obs.int.owncloud.com/oem'},
                'base': 'RHEL',
                'repomd.xml': {'repo': 'obsrepository://obs.int.owncloud.com/ownbrander:PACKAGENAME/RHEL_6'}, '.repo': 'RHEL_6/ownbrander:PACKAGENAME.repo'}
  """
  for m in meta_l:
    if plat in m['meta']:
      meta_plat = m['meta'][plat]
      if '.repo' in meta_plat:
        proj = meta_plat['.repo']
        proj = re.sub(r'^.*/','',proj)                # strip prefix
        return re.sub(r'\.repo$','',proj)                # strip suffix

  for m in meta_l:
    if plat in m['meta']:
      meta_plat = m['meta'][plat]
      if 'repomd.xml' in meta_plat:
        if 'repo' in meta_plat['repomd.xml']:
          # obsrepository://obs.int.owncloud.com/ownbrander:PACKAGENAME/openSUSE_13.2
          proj = meta_plat['repomd.xml']['repo']
          proj = re.sub(r'/[^/]+$','',proj)                # strip suffix
          return re.sub(r'^.*/','',proj)                # strip prefix

  for m in meta_l:
    if plat in m['meta']:
      meta_plat = m['meta'][plat]
      if 'primary.xml' in meta_plat:
        if 'vendor' in meta_plat['primary.xml']:        # fake a project name. something moderatly unique
          proj = meta_plat['primary.xml']['vendor']
          return re.sub(r'[:/]+',':',proj)                # clean path

  return 'owncloud'                                # fake a project name. We have nothing. sorry.


def expand_repo_vars(dict, vars):
  vars2 = vars.copy()
  for var in dict.keys():
    vars2[var] = dict[var].format(**vars)
  # don't show help texts without commands.
  if vars2['key_sh'] == '': vars2['key_help'] = ''
  if vars2['repo_sh'] == '': vars2['repo_help'] = ''
  return vars2


def write_download_json(path, meta_l, u):
  dict = merge_dict(meta_l)
  destdir = path+'/'+foldername
  # CAUTION: keep in sync with mk_download_json.py
  url = u.type+u.chost+'/'+u.path
  tree = {}
  for d_base in sorted(dict):
    for plat in reversed(sorted(dict[d_base])):
      repo = url + '/' + plat
      tree[plat] = {}
      tree[plat]['flavor'] = d_base
      tree[plat]['repo'] = repo
      tree[plat]['packages'] = {}
      for dic in dict[d_base][plat]:
        # dic=['9.1.1', '1.2', 'Univention_4.1/all/owncloud_9.1.1-1.2_all.deb', 'owncloud']
        # d_base='Univention'
        # plat='Univention_4.1'
        name = re.sub('.*/+', '', dic[2])
        tree[plat]['packages'][name] = repo + '/' + dic[2]
        if os.path.exists(path+'/'+plat+'/'+dic[3]+'.ymp'):
          tree[plat]['ymp'] = repo+'/'+dic[3]+'.ymp'

  f=open(destdir+'/download.json', 'wb')
  f.write(json.dumps(tree, sort_keys=True, indent=2).encode())
  f.close()


def write_platform_html(path, meta_l, u):
  dict = merge_dict(meta_l)
  # FIXME: this hack should be a buttonAlias = {} above.
  if 'Linux' in dict and 'Ubuntu' in dict:
    print("Merging Linux_Mint into Ubuntu:")
    for mint in dict['Linux']:
      print(" - ", mint)
      dict['Ubuntu'][mint] = dict['Linux'][mint]
    del dict['Linux']
  srcdir = confdir+'/assets'
  destdir = path+'/'+foldername
  repo_config = config_load_expand(srcdir+"/repo.cfg")
  allplatforms_html_file = destdir + '/allplatforms.html'
  fcat=open(allplatforms_html_file, 'wb')
  fcat.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n'.encode())
  fcat.write('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n'.encode())
  for d_base in sorted(dict):
    platform_html = "<!-- CAUTION: Do not edit. Run repo-admin.py to update this file -->\n"
    platform_html_file = destdir + '/'+ d_base + '.html'
    ru_base = None
    if d_base in repo_config:
      ru_base = repo_config[d_base]
    else:
      print("WARNING: no repo_config known for d_base "+d_base+"  -- hoping for platform")

    for plat in reversed(sorted(dict[d_base])):
      for dic in dict[d_base][plat]:
        # dic=['9.1.1', '1.2', 'Univention_4.1/all/owncloud_9.1.1-1.2_all.deb', 'owncloud']
        # d_base='Univention'
        # plat='Univention_4.1'
        if ru_base is None: print(dic, d_base, plat)
        ru = None
        if ru_base:
          ru = ru_base.copy()                # .copy() here, as we del 'entry_template' and/or install_script_html below.
        if plat in repo_config: ru = repo_config[plat].copy()
        if ru is None:
          print("ERROR: no repo_config known for platform "+plat)
          print("       repo_config = config_load_expand(\""+srcdir+"/repo.cfg\")")
          print("       New d_base names need to be added in 4 places of client/assets/download.html")
          sys.exit(0)

        if project_reponame:
          proj = project_reponame
        else:
          proj = project_from_meta_l(meta_l, plat)
        vars = { 'Package': dic[3], 'Version': dic[0], 'VersionRel': dic[0] + '-' + dic[1],
                 'DownloadUrl': u.type+u.host+'/'+u.path,
                 'DownloadUrlCred': u.type+u.chost+'/'+u.path,
                 'DownloadUrlHttps': https_slash_slash+u.host+'/'+u.path,
                 'DownloadUrlHttpsCred': https_slash_slash+u.chost+'/'+u.path,
                 'Project':proj, 'Platform':plat, 'BasePlatform':d_base, 'DelRepoFile':del_project_reponame }

        ######
        # A little template engine ahead:
        # It is small, yet powerful. So beware.
        # We do three distinct rounds:
        # 1st) CamelCase variables from vars replaced in the lower_case fields from config
        #      saved into vars2.
        # 2nd) lower_case variables (now in vars2) replaced into 'entry_template'.
        # 3rd) paste together entries to form the platform_html_file.
        ######
        if not 'entry_template' in ru:
          print("Error: no 'entry_template' in ru: ", ru.keys())
          print("Error: no 'entry_template' in ru_base: ", ru_base.keys())
        e = ru['entry_template']
        del ru['entry_template']
        vars2 = expand_repo_vars(ru, vars)
        if not del_project_reponame: vars2['del_repo_sh'] = ''   # HACK
        if not os.path.exists(path+'/'+plat+'/INSTALL.sh'): vars2['install_script_html'] = ''   # HACK
        # If you get KeyErrors here, pre-populate the key as an empty string in the Generic section.
        entry = e.format(**vars2)
        platform_html += re.sub(r'<pre></pre>','', entry)        # HACK: hide empty shell code blocks.

    f=open(platform_html_file, 'wb')
    f.write(platform_html.encode())
    f.close()
    fcat.write(platform_html.encode())
  fcat.write("</body>\n</html>\n".encode())
  fcat.close()


def packagename(dic,meta,target):
    d_base = meta[target]['base']
    if not d_base in dic:
      return None
    if not target in dic[d_base]:
      return None                                                # happens with disabled builds.
    if len(dic[d_base][target]) > 3:
      return dic[d_base][target][3]
    else:
      print("packagename() not implemented for "+target+" Please FIX\n")
      return None

def merge_packnames(meta_l):
  packnames = []
  for m in meta_l:
    p = list_packagenames(m['dic'], m['meta'])
    packnames.append(p[0])                                       # one representitive per list.
  return packnames

def list_packagenames(dict, meta):
  """ walk through meta data and collect all package names.
      FIXME: does not use meta. should operate on merge_dict() result.
  """
  packnames = {}
  for b in dict.keys():
    for p in dict[b].keys():
      a = dict[b][p]
      if (len(a) > 3):
        if (not a[3] in packnames): packnames[a[3]] = True
  return sorted(packnames.keys())

def fillup_destdir(srcdir, destdir, entrypoint_html):
  """ install the main index.html if missing.
      install the assets if missing.
  """
  if not os.path.exists(destdir): os.makedirs(destdir)

  index_html = destdir+"/"+entrypoint_html
  if not os.path.exists(index_html):
    shutil.copyfile(srcdir+'/download.html', index_html)

  destdir = destdir+'/assets'
  if not os.path.exists(destdir): os.makedirs(destdir)
  for a in os.listdir(srcdir):
     if not os.path.exists(destdir+'/'+a): shutil.copyfile(srcdir+'/'+a, destdir+'/'+a)

def update_html(path, entrypoint_html, meta_l, u):
  """ install the main index.html if missing.
      install the assets if missing.
      update the main index.html and add ymp and platform html files.
  """
  fillup_destdir(confdir+'/assets', path+'/'+foldername, entrypoint_html)
  for e in meta_l:
     if 'Ubuntu'     in e['dic']: print(e['dic']['Ubuntu'].keys())
     if 'Debian'     in e['dic']: print(e['dic']['Debian'].keys())
     if 'Univention' in e['dic']: print(e['dic']['Univention'].keys())

  ## FIXME: this ignores all packages except the first...
  packnames = merge_packnames(meta_l)

  hidden = []
  dict = merge_dict(meta_l)
  for m in meta_l:
    print("meta_l[]:", m['pkg_re'], m['dic'].keys())
  print("dict:", dict.keys())
  for d_base in buttonList:
    if not d_base in dict:
      print("hidden.append('%s')" % d_base)
      hidden.append(d_base)

  # <!-- @@Hide_Buttons_CSS@@ --><style type="text/css"> #soo_button_SL, #soo_button_Arch, #soo_button_Other { display: none; } </style>
  HideButtonsCSS = ", ".join(["#soo_button_"+x for x in hidden])
  HideButtonsCSS = '<style type="text/css"> ' + HideButtonsCSS + " { display: none; } </style>"

  index_html = path+"/"+foldername+"/"+entrypoint_html
  n = replace_commented_html(index_html, { 'HideButtonsCSS': HideButtonsCSS, 'packageName': ', '.join(packnames) })
  # print("replace_commented_html " + str(n))
  write_ymp_html(path, meta_l)
  write_platform_html(path, meta_l, u)
  write_download_json(path, meta_l, u)


class ParseUrl:
  def __init__(self, url):
    urlMatch=re.match(r"([\w]*://)([^/]*)/(.*)",url)
    if not urlMatch:
      print("Url doesnt Match the pattern: http://[username:password@]download.example.com/path")
      sys.exit(1)

    self.chost = urlMatch.group(2)
    urlMatch2=re.match(r"(([^:@]+)(:([^@]*))?@)?(.*)",self.chost)
    if not urlMatch2:
      print("Cant Match"+urlMatch.group(2)+" for Username & Password")
    # print(urlMatch2.groups())  # ('USERNAME:PASSWORD@', 'USERNAME', ':PASSWORD', 'PASSWORD', 'SERVER.EXAMPLE.COM')

    self.type     =urlMatch.group(1)   #ht = https or http
    self.username =urlMatch2.group(2)  #username is None if its missing
    self.password =urlMatch2.group(4)  #password is None if its missing
    self.host     =urlMatch2.group(5)
    self.path     =urlMatch.group(3)

def check_primary_xml_location(path, meta, u):
  """ walk through all primary.xml files
     and fix/remove the xml.base attribute in location elements.
     and check for xml.base attributes in location elements.
     There should be none!

     If there are some, we could change them, but this invalidates the signature.

     There is only one primary.xml file per target, but
     we call this check once per package and target to be sure we get all targets.
  """
  for target in meta.keys():
    if 'primary.xml' in meta[target]:
      primary=target+'/'+meta[target]['primary.xml']['name']
      primary_path=path+'/'+primary
      # print(meta[target],target)
      it = ET.iterparse(gzip.open(primary_path, 'rb'))
      for _, el in it: el.tag = el.tag.split('}', 1)[-1] # strip all namespaces
      root = it.root
      for el in root.iter('package'):
        # <location ... xml:base="..."
        loc = el.find('location')
        for k in loc.attrib.keys():
          if re.match('^(.*[}:])?base$', k):
            print("WARNING: "+primary+" contains an xml:base attribute:")
            print("WARNING:    "+loc.attrib['xml:base'])
            print("WARNING:    This is not portable.")

        ## FIXME: it is an error to have xml:base here. primary files must be without!
        ## Otherwise they are not relocatable.
        # loc.attrib['xml:base'] = u.type+u.chost+'/'+u.path+'/'+target
      # f=gzip.open(primary_path, 'wb')
      # ET.ElementTree(root).write(f, encoding="utf-8", xml_declaration=True)
      # print("%s refreshed ..." % (primary))
      # f.write("\n")
      # f.close()

def check_matching_ymp_url(path, meta, u):
  """
      One *.ymp file per package and target
  """
  for target in meta.keys():
    url = u.type+u.chost+'/'+u.path+'/'+target+'/'
    if 'ymp' in meta[target]:
      ymp = meta[target]['ymp']
      ymp_path = path+'/'+meta[target]['ymp']
      xml = open(ymp_path, 'rb').read()
      xml = re.sub(br'<url>[^<]*', ('<url>'+url).encode(), xml, count=1)
      f = open(ymp_path, 'wb')
      f.write(xml)
      f.close()
      print("%s refreshed ..." % (ymp))


def sign_repomd_file(repomdfile):
  """
      We should compare repomdfile.key with the output of
      gpg -a --export SIGN_KEY_ID
      If it does not match, we don't have the right SIGN_KEY_ID.
      If it matches: We should create repomdfile.asc with the output of
      gpg -a --detach-sign repomdfile

      TODO: grab the secret key from the build service.
            or give instructions how to generate a key.
  """
  print("signing repomd.xml not impl.")


def write_repomd_xml(path, u):
  """
     Go through all files in repodata and write an appropriate entry in repomd.
     Also rename files that have a hex checksum in their name to have none.

     CAUTION: do not use. This invalidates the signature and we cannot resign.
  """
  for target in os.listdir(path):
    if os.path.exists(path+'/'+target+'/repodata/'):
      repodata=[]
      url = u.type+u.chost+'/'+u.path+'/'+target+'/'
      mdfile=target+'/repodata/repomd.xml'
      for file in os.listdir(path+'/'+target+'/repodata'):
        if not re.match('repomd', file):
          file_path = path+'/'+target+'/repodata/'+file
          z = open(file_path).read()
          o = gzip.open(file_path).read()
          a = { 'name': file, 'size': len(z), 'size-open': len(o),
                'sha': sha.new(z).hexdigest(),
                'sha-open': sha.new(o).hexdigest(),
                'timestamp': int(os.stat(file_path).st_mtime)
              }
          repodata.append(a)
      # print(repodata)

      for f in repodata:
        nohex = re.sub('^[0-9a-f]{32,128}-','', f['name'])        # strip 64 digit hex checksum
        if nohex != f['name']:
          print("%s -> %s" % (f['name'], nohex))
          os.rename(path+'/'+target+'/repodata/'+f['name'], path+'/'+target+'/repodata/'+nohex)
          f['name'] = nohex

      xml="""<?xml version="1.0" encoding="UTF-8"?>
<repomd xmlns="http://linux.duke.edu/metadata/repo" xmlns:rpm="http://linux.duke.edu/metadata/rpm">
 <revision>1426078451</revision>
"""
      for f in repodata:
        type=re.sub('\..*','', f['name'])        # strip xml.gz suffix
        xml +=""" <data type="%s">
  <checksum type="sha">%s</checksum>
  <open-checksum type="sha">%s</open-checksum>
  <location href="repodata/%s"/>
  <timestamp>%s</timestamp>
  <size>%s</size>
  <open-size>%s</open-size>
 </data>
""" % (type, f['sha'], f['sha-open'], f['name'], f['timestamp'], f['size'], f['size-open'])
      xml +="""</repomd>
"""
      f=open(path+'/'+mdfile,"wb")
      f.write(xml)
      f.close()
      ## FIXME: must re-sign the file. better not rewrite at all!!
      print("%s rewritten ..." % (mdfile))

      if os.path.exists(path+'/'+mdfile+'.asc'): os.unlink(path+'/'+mdfile+'.asc')
      if enable_gpg_check:
          sign_repomd_file(path+'/'+mdfile)


def fixup_install_files(path, meta, u):
  """
     There can be one INSTALL.sh file per target.
  """
  for target in meta.keys():
    installfile=path+'/'+target+"/INSTALL.sh"
    if os.path.exists(installfile):
      # print("fixup_install_files: found ", installfile)
      target_re=re.sub('\.', '\\.', target)
      target_re=re.sub('-', '\\-', target_re)

      lines=[]
      for line in open(installfile, 'rb').readlines():
        line = line.decode()    # python3 compat: convert bytes to str.
        if re.search('https?://\S*/'+target_re+'/', line):
          # print("fixup_install_files: url seen ", line)
          line = re.sub('https?://\S*/'+target_re+'/', u.type+u.chost+'/'+u.path+'/'+target+'/', line)
          # print("fixup_install_files: url updated ", line)
        lines.append(line.encode())     # python3 compat: convert str to bytes.
      print("%s refreshed ..." % (installfile))
      open(installfile, 'wb').write(''.encode().join(lines))


def fixup_repo_files(path, meta, u):
  """
     There is one *.repo file per target, but we call this
     once per package and target to make sure we reach all targets.
     Caution: meta[target]['.repo'] may be changed as a sideeffect, if project_reponame is defined.
  """
  for target in meta.keys():
    if '.repo' in meta[target]:
      repofile=meta[target]['.repo']
      repofile_path=path+'/'+repofile
      if project_reponame:
        subdir = re.sub(r'/.*$', '', repofile)
        new_repofile = subdir+'/'+project_reponame+'.repo'
        if repofile != new_repofile:
          os.rename(repofile_path, path+'/'+new_repofile)
          repofile = new_repofile
          repofile_path = path+'/'+repofile
          meta[target]['.repo'] = repofile
      lines=[]
      for line in open(repofile_path, 'rb').readlines():
        line = line.decode()    # python3 compat: convert bytes to str.
        if re.match('baseurl\s*=', line):
          line = 'baseurl='+u.type+u.chost+'/'+u.path+'/'+target+'\n'
        if re.match('gpgkey\s*=', line):
          line = 'gpgkey='+u.type+u.chost+'/'+u.path+'/'+target+'/repodata/repomd.xml.key\n'
        if re.match('gpgcheck\s*=', line):
          if enable_gpg_check:
            line = 'gpgcheck=1\n'
          else:
            line = 'gpgcheck=0\n'
        if project_reponame and re.match('\[\S+\]', line):
          line = '['+re.sub(r'[\-\.]+', '_', project_reponame)+']\n'
        lines.append(line.encode())     # python3 compat: convert str to bytes.

      print("%s refreshed ..." % (repofile))
      open(repofile_path, 'wb').write(''.encode().join(lines))

def ymp_added_repos(target):
  f = open(confdir+'/assets/ymp-added-repos.txt','r')
  found = False
  for line in f.readlines():
    if found: return line
    if line.rstrip() == target: found = True
  return ''

def ymp_write(path, dict, meta, u):
  # We put the ymp file in both places: web-page tree and the repo itself.
  # FIXME: check if we need a content file where the ymp-url points to?
  #  - opensuse repos have a content file there, naming the suse subfolder as 'DATADIR'
  #  - we currently don't have a subfolder and no content file.
  #
  # Example: http://software.opensuse.org/ymp/isv:ownCloud:community:testing/openSUSE_13.2/testpilotcloud-client.ymp
  #
  for target in meta.keys():
    if not re.match('(openSUSE|SLE)', target): continue
    pkg_name = packagename(dict,meta,target)
    if pkg_name is None: continue
    d_base = meta[target]['base']
    dic = dict[d_base][target]
    pkg_vers = dic[0]+'-'+dic[1]                # we could also fetch that from meta['primary.xml']['ver']+'-'+...['rel']

    repo_name = pkg_name + ' for ' + target
    repo_desc = 'This repository includes dependencies for '+pkg_name+' maintained by ownCloud.'
    repos = RepoTemplate.format( repo_name = repo_name, repo_summary = repo_name, repo_description = repo_desc, repo_url = u.type+u.chost+'/'+u.path+'/'+target+'/')
    repos += ymp_added_repos(target)
    ymp = YmpTemplate.format( pack_name = pkg_name, pack_summary = pkg_name + '-' + pkg_vers, pack_description = '', pack_repos = repos)
    # print(meta[target], dic, ymp)
    if not os.path.exists(path): os.mkdir(path)
    if not os.path.exists(path+'/'+foldername): os.mkdir(path+'/'+foldername)
    if not os.path.exists(path+'/'+foldername+'/ymp'): os.mkdir(path+'/'+foldername+'/ymp')
    if not os.path.exists(path+'/'+foldername+'/ymp/'+target): os.mkdir(path+'/'+foldername+'/ymp/'+target)
    ympname=path+'/'+foldername+'/ymp/'+target+'/'+pkg_name+'.ymp'
    open(ympname, 'w').write(ymp)
    # print(ympname+" written.")
    ympname=path+'/'+target+'/'+pkg_name+'.ymp'
    open(ympname, 'w').write(ymp)
    # print(ympname+" written.")

def refresh_url(path, url):
  # url:
  # {'username': 'USERNAME', 'host': 'SERVER.EXAMPLE.COM', 'chost': 'USERNAME:PASSWORD@SERVER.EXAMPLE.COM', 'path': 'download/PACKAGENAME', 'password': 'PASSWORD', 'type': 'http://'}
  # print(u.__dict__)

  path=re.sub("/+$","",path)        # remove trailing slashes
  d = path+'/'+foldername
  if os.path.exists(d) and not foldername in ('', '.') and not args.force:
    print("Directory "+d+" already in place. Remove it or use -f")
    sys.exit(1)

  meta_l = FindPackagesList(path, pack_name_re)

  for m in meta_l:
    check_primary_xml_location(path, m['meta'], url)
    check_matching_ymp_url(path, m['meta'], url)
    # write_repomd_xml(path, url)
    fixup_repo_files(path, m['meta'], url)
    fixup_install_files(path, m['meta'], url)
  return meta_l


def main(path):
  url=re.sub("/+$","",download_url)        # remove trailing slashes
  u = ParseUrl(url)
  if args.insecure and u.type == 'https://':
    print("WARNING: You specified a URL with https:// but also specified option --no-https")
  meta_l = refresh_url(path,u)
  for m in meta_l:
    ymp_write(path, m['dic'], m['meta'], u)
  update_html(path, indexfile, meta_l, u)

  print("URL of the install instructions:\n\n  " + u.type+u.host+"/"+u.path + "/" + foldername + "/" + indexfile+"\n")


def populate_example(path, idx):
  destdir = path+'/'+foldername
  if not os.path.exists(destdir): os.makedirs(destdir)
  extra_opts=''
  if args.insecure: extra_opts='--insecure '

  example_sh = destdir+'/example.sh'
  # if not os.path.exists(example_sh):
  print("creating "+example_sh+" ...")
  f = open(example_sh, 'wb')
  f.write(("""#! /bin/sh
#
# This example demonstrates how to call repo-admin.py
# You will need to call repo-admin.py with your download url if the url shown below differs.
# Basic auth username and password is supported in the url.
#
# You can customitze the main html file and re-run repo-admin.py later.
#
cd "$(dirname "${0}")"
set -eux
python bin/repo-admin.py %s--url %s -d '%s' -p '%s' -i '%s' -f ..
""" % (extra_opts, download_url, foldername, ','.join(pack_name_re), idx)).encode())
  os.fchmod(f.fileno(), stat.S_IRWXU|stat.S_IRGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH)
  f.close()

  destdir += '/bin'
  if not os.path.exists(destdir): os.makedirs(destdir)

  if not os.path.exists(destdir+'/repo-admin.py'):
     try: shutil.copyfile(sys.argv[0], destdir+'/repo-admin.py')
     except: pass        # ignore shutil.Error: ... are the same file.

  fillup_destdir(confdir+'/assets', path+'/'+foldername, idx)
  run.verbose=1
  return_code = run(['/bin/sh', example_sh], redirect=False, return_code=True)
  if return_code != 0:
    raise Exception('ERROR: %s failed.' % (example_sh))

def print_script(plat, path):
  proj = 'PROJECT'
  pack = 'PACKAGE'
  m = re.match(r'(.*?)/(.*)', plat)
  if m: proj,plat = m.groups()
  m = re.match(r'(.*?)/(.*)', plat)
  if m: pack,plat = m.groups()
  d_base = re.sub(r'[-_].*','',plat)
  platform = plat
  repo_config = config_load_expand(confdir+"/assets/repo_config_data.py")
  if not plat in repo_config:
    if d_base in repo_config:
      plat = d_base
    else:
      and_base=''
      if d_base != plat: and_base = " and base '%s'" % d_base
      print("Platform '%s'%s not known. Please try one of these:\n %s" % (plat, and_base, repo_config.keys()))
      sys.exit(0)
  ru = repo_config[plat]
  u = ParseUrl(download_url)

  if project_reponame:
    proj = project_reponame

  if path:
    meta_l = FindPackagesList(path, pack_name_re)
    dic = meta_l[0]['dic']
    meta = meta_l[0]['meta']
    if (len(meta_l) > 1):
      print("# Warning, script for multipple packages not implemented. Picking first.")
    packnames = merge_packnames(meta_l)
    if pack == 'PACKAGE': pack = packnames[0]        # FIXME: expose all e.g. ','.join(packnames)
    if proj == 'PROJECT' and platform in meta: proj = project_from_meta_l(meta_l, platform)

  vars = { 'Package': pack, 'Version': 'VERSION', 'VersionRel': 'VERSION-RELEASE', 'DownloadUrl': u.type+u.host+'/'+u.path, 'DownloadUrlCred': u.type+u.chost+'/'+u.path, 'Project':proj, 'Platform':platform, 'BasePlatform':d_base, 'DelRepoFile':del_project_reponame }

  del ru['entry_template']
  cfg = expand_repo_vars(ru, vars)
  if cfg['key_help']: print( "# "+re.sub('\n','\n# ', cfg['key_help']))
  if cfg['key_sh']: print(cfg['key_sh'])
  if cfg['repo_help']: print("# "+re.sub('\n','\n# ', cfg['repo_help']))
  if del_project_reponame: print(cfg['del_repo_sh'])
  if cfg['repo_sh']: print(cfg['repo_sh'])
  # print(cfg, proj, pack, plat)


ap = ArgumentParser()
ap.add_argument("-f", "--force", default=False, action="store_true", help="Override everything in "+foldername+" and create")
ap.add_argument("-e", "--example", default=False, action="store_true", help="place a copy of this script and all its assets in "+foldername+", generate a wrapper shell script that demonstrates the usage for url=http://www.example.com")
ap.add_argument("-p", "--package", default=','.join(pack_name_re), dest="package", metavar="PACKAGE_REGEXP_LIST",help="Regular expression of a package to advertise in index.html -- can be a comma separated list to advertise multiple packages. Default: wildcard '.*' picks the alphapetically first if multiple matches.")
ap.add_argument("-P", "--project", default=None, dest="project", metavar="PROJECT",help="Name of the *.repo and *.list files. Default: derived from meta-data.")
ap.add_argument("-d", "--foldername", default=foldername, dest="foldername", metavar="FOLDERNAME",help="choose the subdirectory name. Use the package name here, if you want to advertrise multiple packages in one repository")
ap.add_argument("-c", "--confdir", default=confdir, dest="confdir", metavar="CONFDIR",help="Directory containing mappings and assets. Default: dirname(argv0) or dirname(argv0)/client, whichever contains an 'assets' subdir.")
ap.add_argument("-i", "--indexfile", default=indexfile, dest="indexfile", metavar="INDEXFILE",help="HTML entry point")
ap.add_argument("-r", "--refresh-url", metavar="URL",help="Refresh *.yum *.repo INSTALL.sh (repomd.xml primary.xml??) files to contain a new Url. Example: http://$username:$password@download.example.com/download/repositories/...")
ap.add_argument("-u", "--url", metavar="URL",help="Repository Url. Example: http://$username:$password@download.example.com/download/repositories/...")
ap.add_argument("-s", "--script", metavar="PROJ/PACK/PLATFORM", help="Print out a shell script for the given platform. The PROJ/PACK/ part is optional. Try '-s help' for a list of platforms.")
ap.add_argument("-D", "--delrepofile", default=None, dest="delproject", metavar="DELPROJECT",help="Name of a *.repo and *.list to remove (without a .repo or .list suffix).")
ap.add_argument("-S", "--insecure", "--no-https", default=False, action="store_true", help="Use only http for key and package transfers")
ap.add_argument("path", metavar="PATH", nargs="?", help="Current path")

args = ap.parse_args()
if args.package:    pack_name_re=args.package.split(',')
if args.project:    project_reponame=args.project
if args.delproject: del_project_reponame=args.delproject
if args.foldername: foldername=args.foldername
if args.indexfile:  indexfile=args.indexfile
if args.confdir:    confdir=args.confdir
if args.url:        download_url=args.url
if args.insecure:   https_slash_slash='http://'

if not os.path.exists(confdir+'/assets'):
  print("Error: confdir('"+confdir+"') has no subdirectory 'assets'.")
  sys.exit(1)

if args.script:
  print_script(args.script, args.path)
  sys.exit(0)

if args.example:
  if not args.path:
    print("Need a 'PATH' argument where to populate the code and examples to.")
    sys.exit(1)
  populate_example(args.path, indexfile)
  sys.exit(0)

if args.refresh_url:
  if not args.path:
    print("Need a 'PATH' argument where to update the URL.")
    sys.exit(1)
  # print("updating files in %s to refer to URL %s\n" % (args.path, args.refresh_url))
  meta_l = refresh_url(args.path, ParseUrl(args.refresh_url))
  sys.exit(0)

if args.path:
  main(args.path)
else:
  print("Need at least '--example', '--script TARGET', or 'PATH' arguments")


