Title: GitLab gem install benchmarking with bundler 1.4
Category: opensource
Tag: gitlab, bundler, time

It appears that the new `bundler 1.4.0` will [support][] parallel gem installation. Thanks to [thoughtbot's post][post]
that brought that to my attention :)

Now, since I've been dealing daily with GitLab for the past four months, I thought it would be a good candidate for testing.

I tried it on my production server which is a QEMU VM machine. Here are the specs[^cpuinfo]:
```
Operating System  : Debian 7
Linux kernel      : 3.2.0-4-amd64
RAM               : 4GB
CPU               : 4-cores
```

On to the installation of bundler's `pre` version:
```
gem install bundler --pre
```

Next step the actual benchmarking. Make sure you either perform a new GitLab installation or
remove the `vendor/bundle/` directory. I used the same command the official installation suggests:
```
RAILS_ENV=production bundle install --without postgres development test aws
```

and I kept track of the output of four different numbers of jobs to run in parallel.
As you'll see, the recommended option is to use as many jobs as your cpu cores.

Next table depicts the difference in gem installation time which is pretty impressive.

|#jobs            | time                                                  | % difference  |
|-----------------|:------------------------------------------------------|:-------------:|
| 1 (default)     | 281.91s user 47.21s system 39% cpu **13:43.34** total |       -       |
| 4               | 286.28s user 48.60s system 104% cpu **5:20.65** total |      61 %     |
| 8               | 267.65s user 43.41s system 128% cpu **4:01.71** total |      71 %     |
| 12              | 262.71s user 42.90s system 136% cpu **3:43.31** total |      73 %     |
| 16              | 256.37s user 41.47s system 139% cpu **3:34.05** total |      74 %     |


[^cpuinfo]: See full `/proc/cpuinfo` in this [gist][].

[post]: http://robots.thoughtbot.com/post/59584648154/parallel-gem-installing-using-bundler
[gist]: https://gist.github.com/axilleas/6399274
[support]: https://github.com/bundler/bundler/pull/2481
