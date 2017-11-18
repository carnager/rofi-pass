# rofi-pass

A bash script to handle [Simple Password Store](http://www.passwordstore.org/)
in a convenient way using [rofi](https://github.com/DaveDavenport/rofi).

![rofi-pass](https://53280.de/rofi/rofi-pass.png "rofi-pass in action")

## Features

* Open URLs of entries with hotkey
* Add new Entries to Password Storage
* Edit existing Entries
* Generate new passwords for entries
* Inline view, which can copy/type individual entries
* Move/Delete existing entries
* Support for different password stores (roots), e.g. to separate passwords for
  work from private passwords
* Type any field from entry
* Auto-typing of user and/or password fields.
  The format for password files should look like:

  ```
  foobarmysecurepassword
  user: MyUser
  url: http://my.url.foo
  ```

* Auto-typing of more than one field, using the `autotype` entry:

  ```
  foobarmysecurepassword
  ---
  user: MyUser
  SomeField: foobar
  AnotherField: barfoo
  url: http://my.url.foo
  autotype: SomeField :tab UserName :tab AnotherField :tab pass
  ```

  You can use `:tab`, `:enter`, or `:space` here to type <kbd>Tab</kbd>,
  <kbd>Enter</kbd>, or <kbd>Space</kbd> (useful for toggling checkboxes)
  respectively.
  `:delay` will trigger a delay (2 seconds by default).
* All hotkeys are configurable in the config file
* The field names for `user`, `url` and `autotype` are configurable
* Bookmarks mode (open stored URLs in browser, default: Alt+x)
* Share common used passwords between several entries (with different URLs, usernames etc)

## Requirements

* pass (http://www.passwordstore.org/)
* sed
* rofi (https://github.com/DaveDavenport/rofi)
* xdotool
* gawk
* bash
* pwgen

### BSD

* gnugrep
* gawk

## Configuration

rofi-pass may read its configuration values from `/etc/rofi-pass` and/or `$HOME/.config/rofi-pass/config`.
For an example configuration please take a look at the included `config.example` file.

## Extras

rofi-pass comes with a tiny helper script, which makes it easier to create new pass entries.
Just run it with

```
addpass --name "My new Site" +user "zeltak" +branch "branch" +custom "foobar" +autotype "branch :tab user :tab pass"
```

* First argument `--name` is mandatory. This will be the filename of the new password entry.
* Second argument can be `--root` followed by absolute path to your password-store. addpass also uses root config setting from rofi-pass config file. If both are not found, PASSWORD_STORE_DIR variable is checked. If none of the above are found, the default location `$HOME/.password-store` is used.
* `--root` can also be a colon separated list of directories, in which case you can navigate between them on the main menu with Shift+Left and Shift+Right.
* Fieldnames are defined with `+` and the actual value is defined inside the quotations. You can add as many fields as you like

Also included is an import script for keepass2 databases. It's the same script that can be downloaded from the pass homepage, with some minor modifications to match rofi-pass structure.

## Sharing passwords

Rofi-pass allows you to easily share common used passwords across multiple entries.
For example, if you have an academic account which includes several services (such as a library, Salary, Student portal etc),  all with different URL's, login forms etc. you can share one password across all of them. This is very handy when the passwords change annually.
To use this function you need to add the following line instead of the password, referencing a pass file which holds the password.

```
#FILE=PATH/to/filename
```
where PATH is relative to your password-store.

*And yes, you should slap your service provider for forcing you to share passwords across services.*

## FAQ

### rofi pass prints garbage instead of my actual passes

Make sure to run `setxkbmap <language> <variant>` at the start of your Xorg
session.

## Alternative

jreinert has written the roughly compatible tool
[autopass](https://github.com/jreinert/autopass). It has less features, but
definately saner code.
Also he provided a nice little script called `passed` to change your
fieldnames. [link](https://github.com/jreinert/passed)
It includes a script "pass2csv.py" to export your password store as CSV.
