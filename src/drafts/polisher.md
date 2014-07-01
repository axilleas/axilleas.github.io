polisher: a set of tools for easy Fedora rubygem packaging

# Dependencies:

libcurl-devel

curb
colored
activesupport
json
gem2rpm
rake
pkgwat
awesome_spawn
versionomy

# Binaries

## gem_dependency_checker

Currently, the commands supported are the ones below:

```
    -h, --help                       Display this help screen
        --format val                 Format which to render output
        --gemfile file               Location of the gemfile to parse
        --group gemfile_groups       Gemfile groups (may be specified multiple times)
        --gemspec file               Location of the gemspec to parse
        --gem name                   Name of the rubygem to check
        --[no-]devel                 Include development dependencies
    -m, --[no-]missing               Highlight missing packages
    -f, --[no-]fedora                Check fedora for packages
    -g, --git [url]                  Check git for packages
    -k, --koji [url]                 Check koji for packages
    -t, --koji-tag tag               Koji tag to query
        --bodhi [url]                Check Bodhi for packages
        --rhn [url]                  Check RHN for packages
    -y, --yum                        Check yum for packages
    -b, --bugzilla                   Check bugzilla for bugs filed against package
    -e, --errata [url]               Check packages filed in errata
```

