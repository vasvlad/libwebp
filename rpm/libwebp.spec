Name:          libwebp
Version:       0.6.1
Release:       1
URL:           http://webmproject.org/
Summary:       Library and tools for the WebP graphics format
License:       BSD
Source0:       http://downloads.webmproject.org/releases/webp/%{name}-%{version}.tar.gz

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

%package tools
Summary:       The WebP command line tools

%description tools
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

%prep
%setup -q -n %{name}-%{version}/%{name}

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
%{__make} %{?_smp_mflags}

%install
%make_install
find "%{buildroot}/%{_libdir}" -type f -name "*.la" -delete

%post -n %{name} -p /sbin/ldconfig

%postun -n %{name} -p /sbin/ldconfig

%files tools
%{_bindir}/cwebp
%{_bindir}/dwebp
%{_bindir}/gif2webp
%{_bindir}/img2webp
%{_bindir}/webpinfo
%{_bindir}/webpmux
%{_mandir}/man*/*

%files
%doc PATENTS NEWS COPYING
%{_libdir}/%{name}.so.7*
%{_libdir}/%{name}decoder.so.3*
%{_libdir}/%{name}demux.so.2*
%{_libdir}/%{name}mux.so.3*

%files devel
%doc README AUTHORS COPYING
%{_libdir}/%{name}*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*

