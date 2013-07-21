Title: GSoC - Weekly update 5
Tags: gsoc, fedora, gitlab, packaging, fedpkg, git
Category: tech
Status: draft



As you may know, I am in the process of writing an article on how to package Ruby
gems in Fedora. This is the only type of package I have been dealing with for the
past months, so I am far from an avid packager. But, as a structure and wiki freak I
like to have everything in order, even understandable by completely newbies, so
this is going to be very comprehensive. Progress is being made :)

[TOC]




# Packages

## hashie

## omniauth

## bootstrap-sass

Approved

## timers

Approved

## rugged

Approved?



# My workflow of maintaining unofficial repositories


## Create repos 

First, I created the directory structure for my [gitlab repository][] locally on
my machine:

    ::bash
    mkdir -pv ~/repos/gitlab/fedora-{19,rawhide}/{noarch,x86_64,i386,SRPMS}

Alternatively you can use the [script][repo-create] mentioned in the wiki.

## Process


- Run `mock -r fedora-19-x86_64 ../SRPMS/rubygem-foo-ver-real-dist.src.rpm`
- `rpmlint /var/lib/mock/**/result/*.rpm`
- Run `copytorepo rubygem-foo`
- Run updaterepo

gget:

    ::bash
    #!/usr/bin/env bash

    gem='$1'

    spec_dir=$HOME/rpmbuild/SPECS
    rpm_dir=$HOME/rpmbuild/RPMS
    srpm_dir=$HOME/rpmbuild/SRPMS
    src_dir=$HOME/rpmbuild/SOURCES

    pushd . >& /dev/null

    cd $src_dir

    echo "Fetching $1 from rubygems.org"
    gem2rpm --fetch $1 -o $spec_dir/rubygem-$1.spec
    echo "gem downloaded in : $src_dir"
    echo "spec file is in   : $spec_dir"

    popd >& /dev/null

copytorepo:

mock_dir='/var/lib/mock'
fedora_19='fedora-19-$basearch'
fedora_rawhide='fedora-rawhide-$basearch'
repo_19='$HOME/repos/gitlab/fedora-19'
repo_rawhide='$HOME/repos/gitlab/fedora-rawhide'



rsync -avr $mock_dir/**/result/*.rpm

updaterepo:



# How to package a Ruby gem - blog post status

https://trello.com/c/oGOKkvBn/6-weekly-blog-posts


# TODO next week

- google midterm evaluation
- more packages



[repo-create]: https://fedoraproject.org/wiki/Fedorapeople_Repos#Script_for_easy_create_tree_local_repo_directory
[gitlab repository]: http://repos.fedorapeople.org/repos/axilleas/gitlab/

