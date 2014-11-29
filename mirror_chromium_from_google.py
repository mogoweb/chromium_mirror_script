#!/usr/bin/env python

# Copyright (c) 2014 mogoweb. All rights reserved.
# Use of this source code is governed by a Apache license that can be
# found in the LICENSE file.

import optparse
import os
import subprocess
import sys
from numpy.version import git_revision

class RepoMirror:
    '''mirror chromium repository to local'''
    def __init__(self, google_repo_root, local_repo_root):
        self.google_repo_root = google_repo_root
        self.local_repo_root = local_repo_root
        self.chromium_git_list = []
        self.read_git_list()
    
    def read_git_list(self):
        ''' read chromium git list from file '''
        f = file('chromium_git_list.txt')
        for line in f:
            self.chromium_git_list.append(line.strip())
        print self.chromium_git_list
    
    def check_if_git(self, local_git_folder):
        try:
            os.chdir(local_git_folder)
            subprocess.check_output(["git", "remote", "-v"])
        except Exception, error:
            print error
            return False
        
        return True
    
    def mirror_chromium_repository(self):
        for git in self.chromium_git_list:
            git_folder = self.local_repo_root + '/' + git
            git_parent_folder = os.path.dirname(git_folder)
            
            google_git = self.google_repo_root + git
    
            if not os.path.exists(git_parent_folder):
                os.makedirs(git_parent_folder)
            
            if (self.check_if_git(git_folder)):
                print "fetch from google remote repository %s" % google_git
                subprocess.call(["git", "fetch"])
            else:
                os.chdir(git_parent_folder)
                # git clone with mirror
                subprocess.call(["git", "clone", "--mirror", google_git])

def main(orig_args):
    home_dir = os.path.expanduser("~")
    default_local_root = home_dir + '/local_mirror/chromium'
    parser = optparse.OptionParser()  
    parser.add_option("--reference", dest="reference", default=default_local_root,
                  help="location of mirror directory", metavar="DIR")  

    (options, args) = parser.parse_args(orig_args)
    google_repo_root = 'https://chromium.googlesource.com/'
    local_repo_root = options.reference
    print "local chromium's repository: %s" % local_repo_root
    mirror = RepoMirror(google_repo_root, local_repo_root)
    mirror.mirror_chromium_repository()

if __name__ == '__main__':
    main(sys.argv[1:])