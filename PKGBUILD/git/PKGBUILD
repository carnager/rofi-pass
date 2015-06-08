# Maintainer: Rasmus Steinke <rasi at xssn dot at>

pkgname=rofi-pass-git
_pkgname=rofi-pass
pkgver=5.f4255a9
pkgrel=1
pkgdesc="bash script to handle pass storages in a convenient way"
arch=('any')
url='https://github.com/carnager/rofi-pass'
license=('GPL')
depends=('xorg-xprop' 'wmctrl' 'rofi-git' 'pass' 'xdotool' 'xclip')

install=('rofi-pass.install')
makedepends=('git')
source=('git+http://git.53280.de/rofi-pass')

pkgver() {
	cd ${_pkgname}
	printf "%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

package() {
    cd ${_pkgname}
    make DESTDIR="$pkgdir/" \
       PREFIX='/usr' \
       install
}
md5sums=('SKIP')
