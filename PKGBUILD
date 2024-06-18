# Maintainer: iris snazzsinclair@gmail.com
pkgname=revhubinterface-git
_pkgname=RevHubInterface
pkgver=1.3.3.r33.g1f6409a
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
source=("$_pkgname::git+https://github.com/unofficial-rev-port/REVHubInterface")
b2sums=('SKIP')
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
    install -Dm644 -t "${pkgdir}/usr/share/pixmaps"  org.unofficialrevport.REVHubInterface.Devel.png
    install -Dm644 -t "${pkgdir}/usr/share/applications" revhubinterface.desktop
    install -Dm755 -t "${pkgdir}/usr/bin" dist/REVHubInterface
}
