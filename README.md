# rofi-pass

#### bash script to handle pass storages in a convenient way

![rofi-pass](screenshot.png "rofi-pass in action")

## rofi-pass has the following features:

* Open URLs of entries with hotkey
* Add new Entries to Password Storage
* Edit existing Entries
* Support for multiple roots for password-store (e.g. separate work from private passwords)
* Auto Type User and Password. Format of password files are expected to be like:
```
foobarmysecurepassword
UserName: MyUser
URL: http://my.url.foo
```
* Auto Typing of more than one field. This expects a autotype field in password file. (name of the field can be changed in config file - same for URL and Username)
```
foobarmysecurepassword
---
UserName: MyUser
SomeField: foobar
AnotherField: barfoo
URL: http://my.url.foo
autotype: SomeField :tab UserName :tab AnotherField :tab pass
```
The `:tab` field has a special meaning. this will hit the tab key, obviously.

## Requirements
* pass (https://github.com/zx2c4/password-store)
* sed
* rofi (https://github.com/DaveDavenport/rofi)
* wmctrl
* xprop
* xdotool
* awk
* bash

## Extras
rofi-pass comes with a tiny helper script, which makes it easier to create new pass entries.
Just run it with 

```
addpass --name "My new Site" +user "zeltak" +branch "branch" +custom "foobar" +autotype "branch :tab user :tab pass"`.
```

* First argument `--name` is mandatory. This will be the filename of the new password entry.
* Second argument can be `--root` followed by absolute filename. addpass also uses root config setting from rofi-pass config file. If both are not found, PASSWORD_STORE_DIR variable is checked. If none of the above are found, the default location `$HOME/.password-store` is used.

* Fieldnames are defined with `+` and the actual value is defined inside the quotations. You can add as many fields as you like

Also included is an import script for keepass2 databases. It's the same script that can be downloaded from the pass homepage, with some minor modifications to match rofi-pass structure.
