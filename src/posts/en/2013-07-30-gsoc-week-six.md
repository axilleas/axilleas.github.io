Title: GSoC - Weekly update 6
Tags: gsoc, fedora, gitlab, packaging
Category: opensource

Here is what I have been doing the past week.

[TOC]

## Packages

### charlock_holmes

[Pending review][charlock]

This one gave me some headaches as it is a gem with c extensions and as it turned
out I didn't ship the soname in the right directory. It took me some time but I
finally understood how that works. Here are the steps I follow when packaging gems
with c extensions.

1. From the initial spec file that gem2rpm creates, comment the line below:

        ::bash
        mv %{buildroot}%{gem_instdir}/lib/shared_object.so %{buildroot}%{gem_extdir_mri}/lib/

2. Run `rpmbuild -bi rubygem-charlock_holmes.spec` in order not to remove the
  *BUILDROOT* directory.
  
3. Find the soname files that get created:

        ::bash
        find ~/rpmbuild/BUILDROOT/rubygem-charlock_holmes-0.6.9.4-1.fc19.x86_64/ -name '*.so'
        
        Output
        ------
        ~/rpmbuild/BUILDROOT/rubygem-charlock_holmes-0.6.9.4-1.fc19.x86_64/usr/share/gems/gems/charlock_holmes-0.6.9.4/ext/charlock_holmes/charlock_holmes.so
        ~/rpmbuild/BUILDROOT/rubygem-charlock_holmes-0.6.9.4-1.fc19.x86_64/usr/share/gems/gems/charlock_holmes-0.6.9.4/lib/charlock_holmes/charlock_holmes.so

    There are 2 files, one in `lib/` dir and one in `ext/` dir. We should ship the one in
    `lib/` dir, so in our spec file we replace the line that we commented before with:
  
        ::bash
        mkdir -p %{buildroot}%{gem_extdir_mri}/lib/%{gem_name}/
        mv %{buildroot}%{gem_libdir}/%{gem_name}/%{gem_name}.so %{buildroot}%{gem_extdir_mri}/lib/%{gem_name}/

        # Remove the binary extension sources and build leftovers.
        rm -rf %{buildroot}/%{gem_instdir}/ext/

    See what I did there? The lib dir when I used find was:
  
        ~/rpmbuild/BUILDROOT/rubygem-charlock_holmes-0.6.9.4-1.fc19.x86_64/usr/share/gems/gems/charlock_holmes-0.6.9.4/lib/charlock_holmes/charlock_holmes.so

    which when written with macros translates to:
  
        %{buildroot}%{gem_libdir}/%{gem_name}/%{gem_name}.so

    which in turn gets copied to:
  
        ::bash
        %{buildroot}%{gem_extdir_mri}/lib/%{gem_name}/

Tl;dr;
Follow the directory structure of `lib/` where the soname resides and remove the
`ext/`.

Beware that there are cases where this structure is not the same and the soname
is found right in `lib/` dir and not in `lib/%{gem_name}/`.

Take for example [rubygem-pg][] compared to [rubygem-charlock_holmes][].

### omniauth

[Pending review][omniauth]

I had some hard time with this too as it was failing the test suite. It turned out
I was missing a BuildRequires dependency. A huge thanks to [Ken Dreyer][] who
pointed me out to the right direction in the [mailing list][] as well as giving
some nice tips about the packaging workflow.

### sanitize

This was an easy one and was immediately accepted when [reviewed][sanitize].

### orm_adapter

This is pending a [review][orm].

## Update to GitLab 5.4

I updated the dependencies to version 5.4. Overall nothing changed except for the
addition of unicorn, which is already submitted for [review][unicorn].


[rubygem-pg]: http://pkgs.fedoraproject.org/cgit/rubygem-pg.git/tree/rubygem-pg.spec#n61
[rubygem-charlock_holmes]: https://github.com/axilleas/fedora/blob/master/packages/rubygem-charlock_holmes/rubygem-charlock_holmes.spec#L54
[mailing list]: https://lists.fedoraproject.org/pipermail/ruby-sig/2013-July/001393.html
[Ken Dreyer]: https://fedoraproject.org/wiki/User:Ktdreyer
[unicorn]: https://bugzilla.redhat.com/show_bug.cgi?id=786636
[sanitize]: https://bugzilla.redhat.com/show_bug.cgi?id=989132
[orm]: https://bugzilla.redhat.com/show_bug.cgi?id=988938
[charlock]: https://bugzilla.redhat.com/show_bug.cgi?id=989143
[omniauth]: https://bugzilla.redhat.com/show_bug.cgi?id=989775
