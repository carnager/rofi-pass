# rofi-pass

#### bash script to handle pass storages in a convenient way

![rofi-pass](screenshot.png "rofi-pass in action")

## rofi-pass has the following features:

* Auto Type User and Password. Format of password files are expected to be like:
```
foobarmysecurepassword
UserName: MyUser
URL: http://my.url.foo
```
* Auto Typing of more than one field. This expects a CustomOrder field in password file:
```
foobarmysecurepassword
---
UserName: MyUser
SomeField: foobar
AnotherField: barfoo
URL: http://my.url.foo
CustomOrder: SomeField :tab UserName :tab AnotherField :tab password
```
The `:tab` field has a special meaning. this will hit the tab key, obviously.

* Open URLs of entries with hotkey
* Add new Entries to Password Storage
* Edit existing Entries
* Support for multiple roots for password-store (e.g. separate work from private passwords)

## Requirements
* pass (https://github.com/zx2c4/password-store)
* sed
* rofi (https://github.com/DaveDavenport/rofi)
* wmctrl
* xprop
* xdotool
* awk
* bash
