Title: Fedora - maintaining unofficial repositories
Tags: fedora, packaging
Category: linux
Status: draft

## My workflow on maintaining unofficial repositories

Along with submitting package reviews, I crafted an [unofficial repo][] of packages
I am working on, not yet submitted for review due to many reasons. If you want to
try any of them give it a go.

### Create repos 

First, I created the directory structure for my [gitlab repository][] locally on
my machine:

    ::bash
    mkdir -pv ~/repos/gitlab/fedora-{19,rawhide}/{noarch,x86_64,i386,SRPMS}

Alternatively you can use the [script][repo-create] mentioned in the wiki.

### Process


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

