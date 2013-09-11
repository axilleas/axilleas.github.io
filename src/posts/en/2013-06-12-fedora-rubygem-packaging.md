Title: New in Fedora: How to package a Ruby gem
Category: geek
Tags: fedora, rubygem, ruby, packaging
Status: draft

TODO: dude cookies -> dude lines :p

Ok, this is going to be a really long post so bare with me, there are cookies along
the way :)

It's been almost three months that I have been dealing with packaging in Fedora
and especially with Ruby gems. In this article I'll talk about the things I learned
these past months, the difficulties I encountered and how I got past them. 
Hopefully, this is going to be a good starting point for all those wanting to
contribute in Fedora Ruby gem packaging and have a hard time understanding 
the process (like I used to).

To be honest, there is a ton of information one has to process and this might be
a little overwhelming in the beginning. I'll try to guide you through what to read
first and not get lost. At the end of this article I have compiled a list of helpful
links.

There are bits and pieces that I took from discussion on irc or questions in [Ruby-sig][]
mailing list.
 
I am focusing on `ruby >= 1.9.1` and Fedora >= 19. [Different][wiki-old] guidelines
apply to previous versions. Maybe I will dedicate a section of how to build on older
versions or EPEL, but that is not my priority for now.

[TOC]

# Where to begin

If you are completely new to packaging then [How to create an RPM package](https://fedoraproject.org/wiki/How_to_create_an_RPM_package)
is a good starting point. The next step is to read [Packaging Ruby](https://fedoraproject.org/wiki/Packaging:Ruby)
for specific Ruby guidelines.

In short you should do 



# Anatomy of a spec file

http://www.rpm.org/max-rpm/ch-rpm-inside.html

## prep
## build
## install
## check

- Running tests
if they are bundled in gem, they goes into -doc subpackage, if they are not included, I typically unpack them in %check section and don't have to care about them anymore
it is very important to execute the test suites, if possible
it is the only way how we can check if the gem works or not, if we upgrade Ruby in Fedora, etc. It is not possible to go and test manually every gem during the rebuild

for example, as in here http://pkgs.fedoraproject.org/cgit/rubygem-gem2rpm.git/tree/rubygem-gem2rpm.spec

Generally, if there's a spec dir, run "rspec spec/" and if there's a test dir, run "testrb -Ilib /test/<path>"?

generally yes ... but that are just the most common testing frameworks ... also, if the testrb is tricky sometimes the -Ilib is optional and it depends how the test files are structured under the test directory

it also sometimes happens that the test passes although no test was executed at all, so one needs to be careful


- What to do with tests, spec directories.

generally, we apply https://fedoraproject.org/wiki/Packaging:Guidelines?rd=Packaging/Guidelines#PackageDocumentation on them

Normally tests are only run at package buildtime. They should not be included in the binary rpms that users install on their systems. You may make an exception for this if the package makes public use of the test suite at runtime (for instance, an application package that has a --selftest command line switch that runs its testsuite.) 

i.e. they are not essential, therefore they go to -doc subpackage and there is also this remark: Do not ship tests

- By "not ship tests" does it mean the tests shouldn't be in the main package but can be in the doc subpackage?

the original meaning was to %exclude them, or rm -rf them ... but keeping in -doc subpackage is good as well
A couple of packages do rm -rf them: each maintainer has a bit different preference.

%check
pushd %{buildroot}%{gem_instdir}
ruby -I. -e "Dir.glob('test/**/*_test.rb').each {|t| require t}"
popd

## files

- LICENSE files **always** go under `%files` macro and is marked as `%doc`
- We exclude all files beginning with a dot (one can remove them as well durging `%install`)
- All files that the gem can live without, meaning they are not needed during runtime, go under `%files doc`
- Anything that seems like documentation is marked with the `%doc` macro. For example
if you see something like Changelog, Readme, Contributing or History mark it as `%doc`.
- If you want to include tests in shipped package, do it in the doc subpackage.
In our example I shipped the `spec/` folder.
- Other files like Gemfile, Rakefile, Guardfile, could be placed under `%files doc`
but NOT marked as `%doc` as they clearly are not documentation. Again, someone can
exclude/rm all those files and not ship them, but I prefer to include them.
- `hashie.gemspec` is interpreted as `%{gem_name}.gemspec`. In general it is good practice to use macros wherever possible.

- Which files would go in %files doc?
%files doc README CHANGELOG
%files LICENSE
the rest, it depends what is it good for

- Manual pages

In theory, you should not keep them, since they will be installed among other man pages

Example: http://pkgs.fedoraproject.org/cgit/rubygem-bundler.git/tree/rubygem-bundler.spec#n72

This is how it is in bundler, however, bundler need the man pages internally.

In case of other Gem, they get installed in eg " /usr/share/gems/gems/guard-1.8.0/man/guard.1{,html}", I would say that once the "real" man pages are created, we can drop their source

But it is more or less up to you, they should go into -doc subpackage anyway, if you like to keep them in the package

-- Do I need to find out the man section number manually?
Should be man1, it is already in its name, and probably in its content

Hidden files

- I normally put the .travis.yml, .irbrc, .document etc in %files doc. But since they are hidden, what is the suggested way around it (rpmlint complains)?
Use %exclude .*, you should always exclude hidden files unless there is some special need

- Or rm {%buildroot}{%gem_instdir}/.*?

Ideally, such files should not be included in gem

- Suppose there was a dot file that was actually being used, that would be caught during running the test? I just include them to be on a safe side.

There might be some test configurations, but I do not remember any case, where the test would fail without it
Please exclude them all.

rpmlint message:
'hidden-file-or-dir',
'''The file or directory is hidden. You should see if this is normal, and delete it from the package if not.''',


- What if someone excludes Gemfile, Rakefile and the gemspec?

Non of them are super important, you can point it in review, that you would keep them and your reasons.
The submitter tells you his reasons and you decide together.

# Know thy tools

## gem2rpm

- Previously the gem2rpm used to create a variable rubyabi = 1.9.1 and call ruby(abi) = %{rubyabi}, which is now done by "ruby(release)"?
Those two are functionally same, right?

More or less the ruby(release) is typically used without version and if the version is used, it should be MRI version, not ABI version.
Prefer to put %check after %install

1) it is optional section, so it is nice to see %prep, %build and %install all in one look not disturbed by any other section
2) it depends on implementation, but the %check section might be executable only on installed package. If that is the case, then it is natural to see it after the %install section
3) during the build, the %check is executed after %install section, so it is just convenient to follow the order in .spec file as well.

## rpmlint is your friend

- rpmlint gives this: rubygem-{gem-name}.noarch: E: script-without-shebang /usr/share/gems/gems/{gem-name}-1.1.0/lib/
Choose one: add shebang or remove executable permission. (I was told on #fedora-devel, that this happens if files are set executable without shebang)
eg specfile : https://bugzilla.redhat.com/show_bug.cgi?id=839650 | http://v3.sk/~hexo/rpm/rubygem-awesome_print.spec

## mock

## koji

## Difficulties

### Test suites

koji / mock builds will not have a live running instance of mysql just to perform that check.
If a test requires a running instance of mysql, it will not work regardless.
Any fedora build system will fail the test, and the package will not finish.

- So should I just try the tests locally and comment them out if I ever have to use the build system?

koji and mock will not have a running dbms.  so yes, you can ifdef them out or comment them - but they will not run properly.
If there are tests that do not require a running dbms, by all means- yes you should run them.

- The best bet is to try them out locally during rpmbuild -ba, and comment them afterwards, isn't it?

Or build your spec so that it only runs %check when you pass "--with checks" or somesuch define.
koji builds wont pass any --with/--without params, so the default should work
Example of a package with --with checks parameters : http://www.rpm.org/wiki/PackagerDocs/ConditionalBuilds
That should let you have a single .spec file that works with checks (outside of mock) and without checks for koji/mock builds.
Above, the word "checks" is not reserved, just seemed fitting.  use whatever you think fits best to describe it.

- If I have a gem that provides a configuration.yml.example for rspec, and expects me to rename the file to configuration.yml with my details in it, how do I go about it? Or can I just skip it? (eg. mysql2-0.3.12b6)

#### sed is your friend

You will encounter many times failing tests due to some gems not yet packaged
in Fedora or bugs inside the test suite. Fear not. These tests can probably pass
if you comment or remove the sections that mess with your build. Below are some
examples.

1. [coveralls][] is not packaged yet for Fedora, nor is a dependency

    sed -i '/[Cc]overalls/d' spec/helper.rb (omniauth)
    
    sed -i -e '/^#!\/usr\/bin\/env/d' Rakefile http://pkgs.fedoraproject.org/cgit/rubygem-pg.git/tree/rubygem-pg.spec#n67

**Note:** It is a good practice to include a comment of your own explaining why you
did such change. It's even better practice to include a link to a discussion with
upstream mentioning the bug you encountered or a fix to be released soon.

### Shebangs and executables

```
# Fix anything executable that does not have a shebang
for file in `find ./%{gem_instdir} -type f -perm /a+x`; do
    [ -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 644 $file
done

# Find files with a shebang that do not have executable permissions
for file in `find ./%{gem_instdir} -type f ! -perm /a+x -name "*.rb"`; do
    [ ! -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 755 $file
done
```

### Relax dependencies

example: http://pkgs.fedoraproject.org/cgit/rubygem-actionpack.git/tree/?h=f19

Under `%prep`

```
pushd .%{gem_dir}
%patch1 -p0
%patch2 -p1
popd
```

Patching gemspec workflow:

```
rpmbuild -bc foo.spec
cd ~/rpmbuild/BUILD/foo/usr/share/gems/
cp specifications/foo.{gemspec,.old}
edit specification/foo.gemspec
diff -rupN specifications/foo.gemspec.old specifications/foo.gemspec  > ~/rpmbuild/SOURCES/rubygem-foo-relax-bar-dependency.patch
```

where foo the name of upstream gem we are packaging and bar the name of the gem
that foo depends on and we want to use a greater version.


%{gem_dir} => /usr/share/gems/

path => specifications/foo.gemspec => use `-p0`:

    specifications/foo.gemspec.orig
    specifications/foo.gemspec

path => dir/specifications/foo.gemspec => use `-p1`:

    a/specifications/foo.gemspec
    b/specifications/foo.gemspec

## My workflow

Let's take hashie gem for example.

0. (Use screen)
1. Run `gget hashie`
2. `vim rubygem-hashie.spec` and complete license tag or edit summary/description
3. `:w` and `:!rpmbuild -ba %`
4. Write down any errors to a temp file (I have a geany sheet open next to my terminal)

Running rpmbuild on `rubygem-hashie.spec` as it was generated by gem2rpm,
gives these errors:

    error: Installed (but unpackaged) file(s) found:
    /usr/share/gems/gems/hashie-2.0.5/.document
    /usr/share/gems/gems/hashie-2.0.5/.gitignore
    /usr/share/gems/gems/hashie-2.0.5/.rspec
    /usr/share/gems/gems/hashie-2.0.5/.travis.yml
    /usr/share/gems/gems/hashie-2.0.5/.yardopts
    /usr/share/gems/gems/hashie-2.0.5/CHANGELOG.md
    /usr/share/gems/gems/hashie-2.0.5/CONTRIBUTING.md
    /usr/share/gems/gems/hashie-2.0.5/Gemfile
    /usr/share/gems/gems/hashie-2.0.5/Guardfile
    /usr/share/gems/gems/hashie-2.0.5/LICENSE
    /usr/share/gems/gems/hashie-2.0.5/README.markdown
    /usr/share/gems/gems/hashie-2.0.5/Rakefile
    /usr/share/gems/gems/hashie-2.0.5/hashie.gemspec
    /usr/share/gems/gems/hashie-2.0.5/spec/hashie/clash_spec.rb
    /usr/share/gems/gems/hashie-2.0.5/spec/hashie/dash_spec.rb
    /usr/share/gems/gems/hashie-2.0.5/spec/hashie/extensions/coercion_spec.rb
    /usr/share/gems/gems/hashie-2.0.5/spec/hashie/extensions/deep_merge_spec.rb
    /usr/share/gems/gems/hashie-2.0.5/spec/hashie/extensions/indifferent_access_spec.rb
    /usr/share/gems/gems/hashie-2.0.5/spec/hashie/extensions/key_conversion_spec.rb
    /usr/share/gems/gems/hashie-2.0.5/spec/hashie/extensions/merge_initializer_spec.rb
    /usr/share/gems/gems/hashie-2.0.5/spec/hashie/extensions/method_access_spec.rb
    /usr/share/gems/gems/hashie-2.0.5/spec/hashie/hash_spec.rb
    /usr/share/gems/gems/hashie-2.0.5/spec/hashie/mash_spec.rb
    /usr/share/gems/gems/hashie-2.0.5/spec/hashie/trash_spec.rb
    /usr/share/gems/gems/hashie-2.0.5/spec/spec.opts
    /usr/share/gems/gems/hashie-2.0.5/spec/spec_helper.rb

5. Make the appropriate changes to the `%files` and `%files doc` macro:

Before:

    %files
    %dir %{gem_instdir}
    %{gem_libdir}
    %exclude %{gem_cache}
    %{gem_spec}

    %files doc
    %doc %{gem_docdir}
    
After:

    %files
    %dir %{gem_instdir}
    %{gem_libdir}
    %doc %{gem_instdir}/LICENSE
    %exclude %{gem_cache}
    %exclude %{gem_instdir}/.*
    %{gem_spec}

    %files doc
    %doc %{gem_docdir}
    %doc %{gem_instdir}/CHANGELOG.md
    %doc %{gem_instdir}/CONTRIBUTING.md
    %doc %{gem_instdir}/README.markdown
    %{gem_instdir}/Gemfile
    %{gem_instdir}/Guardfile
    %{gem_instdir}/Rakefile
    %{gem_instdir}/%{gem_name}.gemspec
    %{gem_instdir}/spec/
  
Explanation:

Anatomy of a spec file -> files

6. Save our changes and run rpmbuild again: `:w` and `:!rpmbuild -ba %`
If everything builds fine, the last you should see is:

    Executing(%clean): /bin/sh -e /var/tmp/rpm-tmp.dq5r4c
    + umask 022
    + cd /home/axil/rpmbuild/BUILD
    + cd hashie-2.0.5
    + /usr/bin/rm -rf /home/axil/rpmbuild/BUILDROOT/rubygem-hashie-2.0.5-1.fc19.x86_64
    + exit 0


7. Next, check produced packages with rpmlint.

    rpmlint ../SRPMS/rubygem-hashie-2.0.5-1.fc19.src.rpm ../RPMS/noarch/rubygem-hashie*
    
    Output:
    3 packages and 0 specfiles checked; 0 errors, 0 warnings.

Cool, so far so good.

8. Time to include the test suite.

Under `%install` and above `%files` include the following:

    %check
    pushd .%{gem_instdir}
    rspec spec/
    popd

Save it and run rpmbuild -ba on the spec file again.
If this is the first time you are building a gem that requires rspec, the build
will fail during check with:

    /usr/share/rubygems/rubygems/core_ext/kernel_require.rb:45:in 'require': cannot load such file -- rspec (LoadError)

which means you are missing the rspec gem. 
Install it with `yum install rubygem-rspec` and add a `BuildRequires` line to your spec:

    BuildRequires: rubygem(rspec)

Save it and run rpmbuild again, it should now pass. Running rpmlint again shows
no errors as well. 

9. Now that rpmbuild finishes with no errors, we run mock against the generated src.rpm.

For Fedora 19:

    mock -v -r fedora-19-x86_64 ../SRPMS/rubygem-hashie-2.0.5-1.fc19.src.rpm

or for rawhide:

    mock -v -r fedora-rawhide-x86_64 ../SRPMS/rubygem-hashie-2.0.5-1.fc19.src.rpm

10. Finally we run rpmlint again on the mock generated packages.

    rpmlint /var/lib/mock/fedora-rawhide-x86_64/result/*rpm
  
  Optionally you can run a koji build for a final test that everything builds fine:

    koji build --scratch rawhide ../SRPMS/rubygem-hashie-2.0.5-1.fc19.src.rpm

### Additional to consider

This was an easy package. Other gems are more difficult to package, for example:

- gem with c extensions

1. run rpmbuild and let it fail
2. check where is the soname. In general `ls BUILDROOT/gem-name/lib`.
if in lib ..

- gem that doesn't ship its tests
- gem that is missing packages needed for building and are not in Fedora's repos
- gem that includes non executable scripts

## FAQ

- Another question is about runtime dependencies and development dependencies. Wouldn't the development dependencies be important for the test suite to run successfully?

Of course for running test suite, you have to specify correct BuildRequires.
On the other hand they are not 100% the same as development dependencies specified by the gem.
There is cases like activerecord, where in ideal world, you would like to run its test suite against every DB adapter.
In reality, it is hard to setup PG to be able to run the test suite against it.
So now, the test suite does not run against PG, therefore you dont have to specify BR: rubygem(pg).
There are cases like tilt, where it can work with plenty of markup gems.
Not every of them is in Fedora yet, but tilt is useful even with one of them.
It is always good to document such cases, like "test suite could run against PG, 
but it his hard to setup", "tilt supports markaby, but we don't have it in Fedora yet".

- So what you are saying is that rubygems.org might list several dev dependencies, but not all might be necessary.

Yes. For example, rake is listed as a development dependency, but we are trying to avoid the BR on rake.
Rake is example of hurting of extra gems. It tends to bring in a lot of cruft, such as hoe, etc.
These are really needed just for development, not for packaging or running test suite.

- While this can reduce the packaging job, how do I find out these gems that can be ignored?

bundler .... any time you see bundler needed for development, please get rid of it

DM(datamapper) is not needed, I am pretty sure
Actually, you see, the orm_adapter, that is exactly the thing I was speaking about
It is obvious from the name, that it tries to hide differencies between several ORMs in Ruby
We have activerecord, so you run at least the AR test suite part
If we get DM into fedora, that would be good time to add the DM dependency and run the DM part of test suite as well
And there is dependency on sqlite3, I am pretty sure that you should be able to run the test suite also against other DB engines with proper setup, but it would be hard probably
So its about trade-offs you can learn this just by experimenting I am afraid ... hard to document



- How do you know if a new version of a gem has come out? It could happen that you packaged a gem, and it works fine for years.
https://fedoraproject.org/wiki/Upstream_release_monitoring


- Where do I check if packages are being reviewed/built by Koji?
https://admin.fedoraproject.org/pkgdb/ or https://apps.fedoraproject.org/packages/
Each provides a bit different information. For a review, you need to check BZ or you can use isitfedoraruby.com.
But for the review, only the BZ, or fedora-package-review ML

Tip: you can package the gem you are going to review yourself and then you can do just diff ;) ... something like competition


Errors while running a test suite: 

 - "fatal: Not a git repository (or any parent up to mount point /home)
Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set)."

 - Answer Looks like the tests would only work if they were run over the Git repository: 
 http://pkgs.fedoraproject.org/cgit/rubygem-bundler.git/tree/rubygem-bundler.spec#n96


If there's a package A that has a BuildRequires: B, and A and B are both being packaged by me, how do I ask mock to include package B (it is not in the repos) while testing package A?

With the --installdeps flag and also, the dependency chains can get pretty large... so you might want to look into creating 
your own local repository, either on a web server or on the filesystem with file:///
It is easier to just dump them in a local repo, run createrepo, and let yum do its job.
https://fedoraproject.org/wiki/Using_Mock_to_test_package_builds#Building_packages_that_depend_on_packages_not_in_a_repository

mockchain was suggested as a solution on #fedora-devel.

"buildroot overrides" is suggested for Koji or just wait for the packages to get into stable
When you file your review bugs, make sure you set the "depends on" items properly, so reviewers can see what should be reviewed first

- what's the difference between rubygem-foo and rubygem(foo) in BuildRequires? 

rubygem(foo) is virtual provide ... the original idea was, that the content inside of the
brackets should correspond with file name, which can be required.



## Link references

### Package maintainers

- [Category:Package Maintainers](https://fedoraproject.org/wiki/Category:Package_Maintainers)

### Guidelines
- [Packaging](https://fedoraproject.org/wiki/Packaging:Guidelines)
- [Licensing](https://fedoraproject.org/wiki/Packaging:LicensingGuidelines)
- [Naming](https://fedoraproject.org/wiki/Packaging:NamingGuidelines)
- [Dist Tag](https://fedoraproject.org/wiki/Packaging:DistTag)
- [Review](https://fedoraproject.org/wiki/Packaging:ReviewGuidelines)

### Packaging Guides

- [Packaging Ruby](https://fedoraproject.org/wiki/Packaging:Ruby)
- [How to create an RPM package](https://fedoraproject.org/wiki/How_to_create_an_RPM_package)
- [Packaging tricks](https://fedoraproject.org/wiki/Packaging_tricks)
- [Scriptlet Snippets](https://fedoraproject.org/wiki/Packaging:ScriptletSnippets)
- [Scripts for package maintainers](https://fedoraproject.org/wiki/Scripts_for_package_maintainers)
- [Package update HOWTO](https://fedoraproject.org/wiki/Package_update_HOWTO)
- [Packagers Guide](http://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/Packagers_Guide/)

### Git
- [Using Fedora GIT](https://fedoraproject.org/wiki/Using_Fedora_GIT)
- [Using git FAQ for package maintainers](https://fedoraproject.org/wiki/Using_git_FAQ_for_package_maintainers)


### Testing spec/srpm/rpm
- [Common Rpmlint issues](https://fedoraproject.org/wiki/Common_Rpmlint_issues)
- [Using Mock to test package builds](https://fedoraproject.org/wiki/Using_Mock_to_test_package_builds)
- [Using the Koji build system](https://fedoraproject.org/wiki/Using_the_Koji_build_system)
- [Test Machine Resources For Package_Maintainers](https://fedoraproject.org/wiki/Test_Machine_Resources_For_Package_Maintainers)


### Policy
- [Package maintainer policy](https://fedoraproject.org/wiki/Package_maintainer_policy)
- [Package maintainer responsibilities](https://fedoraproject.org/wiki/Package_maintainer_responsibilities)


### Review
- [Package Review Process](https://fedoraproject.org/wiki/Package_Review_Process)
- [Policy for stalled package reviews](https://fedoraproject.org/wiki/Policy_for_stalled_package_reviews)

### Misc
- [Fedorapeople Repos](https://fedoraproject.org/wiki/Fedorapeople_Repos)


----------------

NOTES

1) don't forget to rpmlint on doc packages as well.
2) test cases: cp -r test .%{gem_instdir} before pushd.

---
[wiki-old]: https://fedoraproject.org/w/index.php?title=Packaging:Ruby&oldid=306009
