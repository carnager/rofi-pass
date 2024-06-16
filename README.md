# !!! This script is unmaintained !!!

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

* Auto-typing username based on path.
  The structure of your password store must be like:

  ```
  foo/bar/site.com/username
  ```

  And you must set the `default-autotype` to `'path :tab pass'`.

* Auto-typing of more than one field, using the `autotype` entry:

  ```
  foobarmysecurepassword
  ---
  user: MyUser
  SomeField: foobar
  AnotherField: barfoo
  url: http://my.url.foo
  autotype: SomeField :tab user :tab AnotherField :tab pass
  ```

  You can use `:tab`, `:enter`, or `:space` here to type <kbd>Tab</kbd>,
  <kbd>Enter</kbd>, or <kbd>Space</kbd> (useful for toggling checkboxes)
  respectively.
  `:otp` will generate an OTP, either `pass-otp(1)` style, or according to the
  `otp_method:`, if it is defined.
* Generating OTPs.
  The format for OTPs should either compatible with `pass-otp(1)`:

  ```
  [...]
  otpauth://[...]
  ```

  Or it should define a method for generating OTPs:

  ```
  [...]
  otp_method: /opt/obscure-otp-generator/oog --some-option some args
  ```

  `:delay` will trigger a delay (2 seconds by default).
* All hotkeys are configurable in the config file
* The field names for `user`, `url` and `autotype` are configurable
* Bookmarks mode (open stored URLs in browser, default: Alt+x)
* Share common used passwords between several entries (with different URLs, usernames etc)
* Change backend with environment variable `ROFI_PASS_BACKEND`, valid
  backends are `xdotool` or `wtype`. For example use `rofi-pass` with
  [wtype](https://github.com/atx/wtype):

  ```
  ROFI_PASS_BACKEND=wtype rofi-pass
  ```

  or

  ```
  ROFI_PASS_BACKEND=wtype ROFI_PASS_CLIPBOARD_BACKEND=wl-clipboard rofi-pass
  ```

  Alternative change the backend in the config file using
  `backend=wtype` or `clibpoard_backend=wl-clipboard`.
## Requirements

* [pass](http://www.passwordstore.org/)
* sed
* [rofi](https://github.com/DaveDavenport/rofi)
* xdotool or wtype
* xclip or wl-clipboard
* gawk
* bash 4.x
* find
* pwgen
* [pass-otp](https://github.com/tadfisher/pass-otp) (optional: for OTPs)

### BSD

* gnugrep
* gawk

## Configuration

rofi-pass may read its configuration values from different locations in the following order:
* `ROFI_PASS_CONFIG` (environment variable)
* `$HOME/.config/rofi-pass/config`
* `/etc/rofi-pass.conf`

rofi-pass only loads the first existing file.
In case no config file exists, rofi-pass uses its internal default values.
You can set the environment variable like this:

```
ROFI_PASS_CONFIG="$HOME/path/to/config" rofi-pass
```

For an example configuration please take a look at the included `config.example` file.

## Extras

### addpass

rofi-pass comes with a tiny helper script, which makes it easier to create new pass entries.
Just run it with

```
addpass --name "My new Site" +user "zeltak" +branch "branch" +custom "foobar" +autotype "branch :tab user :tab pass"
```

* First argument `--name` is mandatory. This will be the filename of the new password entry.
* Second argument can be `--root` followed by absolute path to your password-store. addpass also uses root config setting from rofi-pass config file. If both are not found, PASSWORD_STORE_DIR variable is checked. If none of the above are found, the default location `$HOME/.password-store` is used.
* `--root` can also be a colon separated list of directories, in which case you can navigate between them on the main menu with Shift+Left and Shift+Right.
* Fieldnames are defined with `+` and the actual value is defined inside the quotations. You can add as many fields as you like

### keepass2 import script

Also included is an import script for keepass2 databases. It's the same script that can be downloaded from the pass homepage, with some minor modifications to match rofi-pass structure.

### csv exporter

Finally a script to export your pass database to csv is included. The resulting csv was tested in keepassxc.

## Sharing passwords

Rofi-pass allows you to easily share common used passwords across multiple entries.
For example, if you have an academic account which includes several services (such as a library, Salary, Student portal etc),  all with different URL's, login forms etc. you can share one password across all of them. This is very handy when the passwords change annually.
To use this function you need to add the following line instead of the password, referencing a pass file which holds the password:

```
#FILE=PATH/to/filename
```

where PATH is relative to your password-store.

*And yes, you should slap your service provider for forcing you to share passwords across services.*

## User filename as user

If your password file has no user field you can ask rofi-pass to use the filename instead.
For example with this password file path : `web/fsf.org/rms` rofi-pass will user `rms` as your username.
To get this, you need to set `default_user` to `:filename` in your configuration.

## FAQ

### rofi pass prints garbage instead of my actual passes

Make sure to run `setxkbmap <language> <variant>` at the start of your Xorg
session.

### rofi pass hangs after selecting password

To access passwords your GPG agent needs to have unlocked your secret key
you're using to encrypt your passwords with. If the secret key hasn't been
unlocked yet it will prompt for the secret key password using `pinentry`. If
`pinentry` is configured to read from a `tty` then `rofi-pass` will hang
indefinitely. To fix this you need to [configure gpg][gpg_pinentry_config] to
use a gui version of `pinentry`. E.g.
```
$ cat ~/.gnupg/gpg-agent.conf
pinentry-program /usr/bin/pinentry-qt
```
You may have to kill the GPG agent if it's still in a bad state:
```
killall -9 gpg-agent
```

## Alternative

jreinert has written the roughly compatible tool
[autopass](https://github.com/jreinert/autopass). It has less features, but
definately saner code.
Also he provided a nice little script called `passed` to change your
fieldnames. [link](https://github.com/jreinert/passed)

[gpg_pinentry_config][https://github.com/bfrg/gpg-guide/blob/master/gpg-agent.conf#L15]
