Title: GitLab - the story so far
Category: talks
Tags: gitlab, ruby, rails, git
Status: draft

### Milestones

  - 1.0.1 -> Gitosis
  - 2.0.0 -> Gitolite
  - 2.3.0 -> Fully open sourced under MIT
  - 5.0.0 -> From gitolite to gitlab-shell (easier development)

### Timeline

2 years before 09/2011: 
  - 1 member team

Now:
  - 11 members
  - large community
  - 10.000 organizations using it (images: michigan, brightbox, phusion, blackberry etc.)
  - Github top 50
  
  
## Built with

### Backend

  - rails 
  - sidekiq (process queue manager, creating background jobs, logging, system monitoring, scheduling, user notification)
  - puma (ruby webserver) (introduced in 5.1, previously unicorn) puma.io
  - redis (key-value store, data structure server)
  - gitlab-shell (replacemenet for gitolite in 5.0, manage authorized_keys, repositories)
  - mysql/postgresql
  
### Frontend

  - bootstrap (twitter)
  - coffescript (javascript)
    
## Features

 - enable/disable signup
 - login with ldap, pam (5.2), omni_auth(google, twitter, github)
 - repository access 5 access level, branch protection
 - merge requests (MR) - PR on github
 - Issue tracker
 - Code review (comments in diff)
 - team, group, gollum wiki (clonable)
 - snippets (like gists)
 - import existing repos (eg. github, bitbucket, gitweb)
 - commit timeline

## Comparison

  - gitorious
  - github enterprise
  
## Links

  - 
  
  
