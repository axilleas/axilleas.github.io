Title: GSoC-2014 isitfedoraruby - Week 3
Slug: gsoc2014-week-three
Tags: fedora, isitfedoraruby, gsoc, ruby, rails, webdev
Category: geek
Lang: en

Testing, testing, testing.
Diving into BDD for the first time can be a little tedious but you sure learn
a lot. In the ruby/rails world there is a ton of excellent tools to help you
test your app. Some more popular than the others. I'm no exception so I
picked what the majority of the community dictated.

# Testing tools

## Rspec

The Rspec test suite is well established among ruby developers and has a big
community to support it. You can also find many good books about it. One that
I highly recommend is [Everyday Rails Testing with RSpec][rspec-book]. It
basically includes all the tools I'll be using, I'm a little biased I admit it
but it is really worth it.

Here are the specs that will be populated with tests over time.

```
models
├── bug_spec.rb
├── build_spec.rb
├── dependency_spec.rb
├── fedora_rpm_spec.rb
├── rpm_version_spec.rb
└── ruby_gem_spec.rb
```

Currently, I have worked only on `bug_spec.rb` which is finished for the time
being.

```ruby
# app/spec/models/bug_spec.rb
#
# == Schema Information
#
# Table name: bugs
#
#  id            :integer          not null, primary key
#  name          :string(255)
#  bz_id         :string(255)
#  fedora_rpm_id :integer
#  is_review     :boolean
#  created_at    :datetime
#  updated_at    :datetime
#  last_updated  :string(255)
#  is_open       :boolean
#
require 'rails_helper'

describe Bug do
  it 'has valid factory' do
    expect(create(:bug)).to be_valid
  end

  before(:all) do
    @bug = create(:bug)
    @bugzilla_url = 'https://bugzilla.redhat.com/show_bug.cgi?id='
  end

  it 'has valid bugzilla url' do
    expect(@bug.url).to match(/#{Regexp.quote(@bugzilla_url)}\d+/)
  end

  it 'is a Review Request' do
    expect(@bug.is_review).to eq true
  end

  it 'is open' do
    expect(@bug.is_open).to eq true
  end

  it 'is closed' do
    @bug.is_open = false
    expect(@bug.is_open).to eq false
  end

end
```

Here I'm using the new rspec method `expect(object).to` instead of the old one
`object.should`. 

In the validation of the bugzilla url I wanted to test against a regular
expression that would return the bug url and bug number. At first I used
`/#{@bugzilla_url}\d+/` but that was interpreted into
`/https:\/\/bugzilla.redhat.com\/show_bug.cgi?id=\d+/`. So, the slashes where
treated as regexp wildcards. The trick I [learned][stack-regexp] is to enclose
the string into `Regexp.quote(str)`. This method escapes any characters that
would otherwise have special meaning[^ruby-doc].

## FactoryGirl

FactoryGirl is a replacement for fixtures, Rails' default way of creating test
data. In my first attempt I used it to create a Bug object.

```ruby
# app/spec/factories/bugs.rb

FactoryGirl.define do
  factory :bug do |b|
    b.bz_id '12345'
    b.is_review true
    b.is_open true
  end 
end
```

So, when I call `create(:bug)` in my `bug_spec.rb` it automatically creates
a new Bug object in the database with the predefined attributes I gave it
in the factory file. I could probably use `build(:bug)` instead of `create`
and that would simply create the object but not save it in the database.
This could get a lot better since it takes 2.2 seconds to just run 5 tests.
Refactoring will come later, I'll primarily focus on making enough tests to
cover as many edge cases as I can find.

## Cucumber/capybara

So far I talked about unit testing. When it comes to integration testing,
that is how the application as a whole behaves, there is `cucumber` and `capybara`.
I haven't actually used any of these two yet. Cucumber is known for its
descriptive language and better used when one works with a non-programmer
product owner that doesn't want to look at a lot of code[^quote]. I'll probably
just go with capybara.

# Setting a Rails development environment

I spent quite a lot of time to find the proper gems and configuration to
have a nice setup. This will do for an article of its own so I won't go into
details.

# TODOs

Except for preparing the test suite, I'm also into cleaning the code where
possible and necessary. There are some functions that need removing, but I
have to do it carefully, don't want to break anything and without tests I
cannot be 100% sure. So far I have used the [rubocop][] gem with some
interesting findings (exactly 666 warnings/errors). I will talk about it next week.
Now go and watch the [Number of the beast][maiden].

[^ruby-doc]: <http://ruby-doc.org/core-2.1.2/Regexp.html#method-c-quote>
[^quote]: Quote taken from Everyday Rails Testing with RSpec

[rspec-book]: https://leanpub.com/everydayrailsrspec "Everyday Rails Testing with RSpec"
[stack-regexp]: http://stackoverflow.com/a/150598/2137281 "Interpolating a string into a regex"
[maiden]: https://www.youtube.com/watch?v=CamAhPeYoC8 "Six six six"
[rubocop]: https://github.com/bbatsov/rubocop "A Ruby static code analyzer, based on the community Ruby style guide"