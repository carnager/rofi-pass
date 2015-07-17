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
Just run it with `addpass -name "My new Site" -user "zeltak" -branch "branch" -custom "foobar" -CustomOrder "branch :tab user :tab pass"`.
You can add as many fields as needed. fieldnames are defined with `-` and the actual value is defined inside the quotations.

Also included is an import script for keepass2 databases. It's the same script that can be downloaded from the pass homepage, with some minor modifications to match rofi-pass structure.
