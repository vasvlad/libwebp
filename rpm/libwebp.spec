%global tools webp-tools

Name:          libwebp
Version:       1.3.1
Release:       1
URL:           https://github.com/sailfishos/libwebp
Summary:       Library and tools for the WebP graphics format
License:       BSD
Source0:       %{name}-%{version}.tar.gz

BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: giflib-devel
BuildRequires: libtiff-devel
BuildRequires: autoconf automake libtool

%description
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.

%package -n %{tools}
Summary:       The WebP command line tools
Requires:      %{name} = %{version}-%{release}

%description -n %{tools}
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.

%package devel
Summary:       Development files for libwebp, a library for the WebP format
Requires:      %{name} = %{version}-%{release}

%description devel
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.

%package doc
Summary:   Documentation for %{name} and %{tools}
Requires:  %{name} = %{version}-%{release}

%description doc
Man pages for %{name} and %{tools}.

%prep
%autosetup -n %{name}-%{version}/%{name}

%build
autoreconf -vfi
%ifarch aarch64
export CFLAGS="%{optflags} -frename-registers"
%endif
# Neon disabled due to resulting CFLAGS conflict resulting in
# inlining failed in call to always_inline '[...]': target specific option mismatch
%configure --disable-static --enable-libwebpmux \
           --enable-libwebpdemux --enable-libwebpdecoder \
           --disable-neon
%make_build

%install
%make_install
find "%{buildroot}/%{_libdir}" -type f -name "*.la" -delete

mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
install -m0644 -t %{buildroot}%{_docdir}/%{name}-%{version} \
        PATENTS NEWS README.md AUTHORS COPYING

%post -n %{name} -p /sbin/ldconfig

%postun -n %{name} -p /sbin/ldconfig

%files -n %{tools}
%{_bindir}/cwebp
%{_bindir}/dwebp
%{_bindir}/gif2webp
%{_bindir}/img2webp
%{_bindir}/webpinfo
%{_bindir}/webpmux

%files
%license COPYING
%{_libdir}/%{name}.so.7*
%{_libdir}/%{name}decoder.so.3*
%{_libdir}/%{name}demux.so.2*
%{_libdir}/%{name}mux.so.3*
%{_libdir}/libsharpyuv.so.0*

%files devel
%{_libdir}/%{name}*.so
%{_libdir}/libsharpyuv.so
%{_includedir}/*
%{_libdir}/pkgconfig/*

%files doc
%defattr(-,root,root,-)
%{_mandir}/man1/*webp*
%{_docdir}/%{name}-%{version}
