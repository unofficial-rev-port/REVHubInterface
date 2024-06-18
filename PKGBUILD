# Maintainer: iris snazzsinclair@gmail.com
pkgname=revhubinterface-git
_name=RevHubInterface
pkgver=1.3.3dev
pkgrel=1
pkgdesc="Software for controling a REV Expansion Hub on a pc over USB"
arch=('any')
url="https://github.com/unofficial-rev-port/REVHubInterface"
license=('BSD3')
makedepends=(
			'git'
            'pyinstaller'
            'python>=3.7'
		    'python-pyserial'
            'tk'
)
source=("$_pkgname::https://github.com/unofficial-rev-port/REVHubInterface.git")
b2sums=('SKIP')
#It works till here
pkgver(){
    cd $_pkgname
	git describe --long --tags | sed 's/^v//;s/\([^-]*-g\)/r\1/;s/-/./g'    
}   
build(){
    cd $_pkgname
    pyinstaller REVHubInterface.spec
}
package(){
    cd $_pkgname
    mkdir /usr/bin/REVHubInterface
    mv dist/REVHubInterface /usr/bin/REVHubInterface
}

