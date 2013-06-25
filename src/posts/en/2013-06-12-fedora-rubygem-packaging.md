Title: New in Fedora: How to package a Ruby gem
Status: draft
Category: geek
Tags: fedora, gsoc, rubygem, ruby, packaging

The GSoC period has officially started and since I will be dealing mainly with
Ruby gems
Ok this is going to be a really long post so bare with patience. There are bits
and pieces 
 

[TOC]

## Where to begin
### gem2rpm

- Previously the gem2rpm used to create a variable rubyabi = 1.9.1 and call ruby(abi) = %{rubyabi}, which is now done by "ruby(release)"?
Those two are functionally same, right?

More or less the ruby(release) is typically used without version and if the version is used, it should be MRI version, not ABI version.
Prefer to put %check after %install

1) it is optional section, so it is nice to see %prep, %build and %install all in one look not disturbed by any other section
2) it depends on implementation, but the %check section might be executable only on installed package. If that is the case, then it is natural to see it after the %install section
3) during the build, the %check is executed after %install section, so it is just convenient to follow the order in .spec file as well.


## Anatomy of a spec file
### prep
### build
### install
### check

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

### files

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


## Testing
### rpmlint is your friend

- rpmlint gives this: rubygem-{gem-name}.noarch: E: script-without-shebang /usr/share/gems/gems/{gem-name}-1.1.0/lib/
Choose one: add shebang or remove executable permission. (I was told on #fedora-devel, that this happens if files are set executable without shebang)
eg specfile : https://bugzilla.redhat.com/show_bug.cgi?id=839650 | http://v3.sk/~hexo/rpm/rubygem-awesome_print.spec

### mock

### koji

### Difficulties in running tests


koji / mock builds will not have a live running instance of mysql just to perform that check.
If a test requires a running instance of mysql, it will not work regardless.
Any fedora build system will fail the test, and the package will not finish.

- So should I just try the tests locally and comment them out if I ever have to use the build system?

koji and mock will not have a running dbms.  so yes, you can ifdef them out or comment them - but they will not run properly.
If there are tests that do not require a running dbms, by all means- yes you should run them.
The best bet is to try them out locally during rpmbuild -ba, and comment them afterwards, isn't it?
Or build your spec so that it only runs %check when you pass "--with checks" or somesuch define.
koji builds wont pass any --with/--without params, so the default should work
Example of a package with --with checks parameters : http://www.rpm.org/wiki/PackagerDocs/ConditionalBuilds
That should let you have a single .spec file that works with checks (outside of mock) and without checks for koji/mock builds.
Above, the word "checks" is not reserved, just seemed fitting.  use whatever you think fits best to describe it.

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


- If I have a gem that provides a configuration.yml.example for rspec, and expects me to rename the file to configuration.yml with my details in it, how do I go about it? Or can I just skip it? (eg. mysql2-0.3.12b6)


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


If there's a package A that has a BuildRequires: B, and A and B are both being packaged by me, how do I ask m
ock to include package B (it is not in the repos) while testing package A?
With the --installdeps flag and also, the dependency chains can get pretty large... so you might want to look into creating 
your own local repository, either on a web server or on the filesystem with file:///
It is easier to just dump them in a local repo, run createrepo, and let yum do its job.

mockchain was suggested as a solution on #fedora-devel.

"buildroot overrides" is suggested for Koji or just wait for the packages to get into stableW
When you file your review bugs, make sure you set the "depends on" items properly, so reviewers can see what should be reviewed first



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

