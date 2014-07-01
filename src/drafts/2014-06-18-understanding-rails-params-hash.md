Title: Understanding Rails' params hash
Slug: understanding-rails-params-hash
Tags: gsoc, ruby, rails, webdev, params
Category: geek
Lang: en


Rails parameters

- How the params hash is formed?
- Where does it get its name?

POST

Taken from the view label forms

```
<%= form_for :article do |f| %>
  <p>
    <%= f.label :title %><br>
    <%= f.text_field :title %>
  </p>
 
  <p>
    <%= f.label :text %><br>
    <%= f.text_area :text %>
  </p>
 
  <p>
    <%= f.submit %>
  </p>
<% end %>
```

When you call form_for, you pass it an identifying object for this form. 
In this case, it's the symbol :article. This symbol will later get 
referenced by a controller and extract the params hash whose keys are the 
labels of the form.

Sudmitting a form sends by default POST requests.

When a form is submitted, the fields of the form are sent to Rails as parameters. 

The params method returns an `ActiveSupport::HashWithIndifferentAccess`
object, which allows you to access the keys of the hash using either
strings or symbols.