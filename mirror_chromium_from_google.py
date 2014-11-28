#!/usr/bin/env python

# Copyright (c) 2014 mogoweb. All rights reserved.
# Use of this source code is governed by a Apache license that can be
# found in the LICENSE file.

import os
import subprocess

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
    
    def mirror_chromium_repository(self):
        for git in self.chromium_git_list:
            git_folder = os.path.dirname(self.local_repo_root + '/' + git)
            google_git = self.google_repo_root + git + '.git'
            print git_folder
    
            if not os.path.exists(git_folder):
                os.makedirs(git_folder)

            os.chdir(git_folder)
            # git clone with mirror
            subprocess.call(["git", "clone", "--mirror", google_git])
            
def main():
    home_dir = os.path.expanduser("~")
    google_repo_root = 'https://chromium.googlesource.com/'
    local_repo_root = home_dir + '/local_mirror/chromium'
    print local_repo_root
    mirror = RepoMirror(google_repo_root, local_repo_root)
    mirror.mirror_chromium_repository()

if __name__ == '__main__':
    main()