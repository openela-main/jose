Name:           jose
Version:        10
Release:        2%{?dist}.3
Summary:        Tools for JSON Object Signing and Encryption (JOSE)

License:        ASL 2.0
URL:            https://github.com/latchset/%{name}
Source0:        https://github.com/latchset/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.bz2

Patch1: 0001-openssl-decode-private-exponent-when-converting-jwk-.patch
Patch2: 0002-Fix-potential-DoS-issue-with-p2c-header.patch
Patch3: 0003-Adapt-alg_comp-test-to-different-zlib-142.patch
Patch4: 0004-Avoid-potential-DoS-with-high-decompression-chunks.patch
Patch5: 0005-jwe-fix-the-case-when-we-have-zip-in-the-protected-h.patch

BuildRequires:  pkgconfig
BuildRequires:  jansson-devel >= 2.10
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  autoconf automake libtool
Requires: lib%{name}%{?_isa} = %{version}-%{release}

%description
José is a command line utility for performing various tasks on JSON
Object Signing and Encryption (JOSE) objects. José provides a full
crypto stack including key generation, signing and encryption.

%package -n lib%{name}
Summary:        Library implementing JSON Object Signing and Encryption
Conflicts:      jansson < 2.10
Provides:       lib%{name}-openssl = %{version}-%{release}
Obsoletes:      lib%{name}-openssl < %{version}-%{release}
Provides:       lib%{name}-zlib = %{version}-%{release}
Obsoletes:      lib%{name}-zlib < %{version}-%{release}

%description -n lib%{name}
This package contains a C library for performing JOSE operations.

%package -n lib%{name}-devel
Summary:        Development files for lib%{name}
Requires:       lib%{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
Requires:       jansson-devel
Provides:       lib%{name}-openssl-devel = %{version}-%{release}
Obsoletes:      lib%{name}-openssl-devel < %{version}-%{release}
Provides:       lib%{name}-zlib-devel = %{version}-%{release}
Obsoletes:      lib%{name}-zlib-devel < %{version}-%{release}

%description -n lib%{name}-devel
This package contains development files for lib%{name}.

%prep
%autosetup -p1
autoreconf -fv --install

%build
%if 0%{?rhel}
%__sed -i 's|libcrypto >= 1\.0\.2|libcrypto >= 1\.0\.1|' configure
%endif
%configure --disable-openmp
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install
rm -rf %{buildroot}/%{_libdir}/lib%{name}.la

%check
make %{?_smp_mflags} check

%post -n lib%{name} -p /sbin/ldconfig
%postun -n lib%{name} -p /sbin/ldconfig

%files
%{_bindir}/%{name}
%{_mandir}/man1/jose*.1*

%files -n lib%{name}
%license COPYING
%{_libdir}/lib%{name}.so.*

%files -n lib%{name}-devel
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/jose*.3*

%changelog
* Mon Jul 01 2024 Sergio Correia <scorreia@redhat.com> - 10-2.3
- Backport fix for CVE-2024-28176
  Resolves: RHEL-28719

* Mon Jul 01 2024 Sergio Correia <scorreia@redhat.com> - 10-2.2
- Fix tests on s390x
  Related: RHEL-29857

* Sun Jun 30 2024 Sergio Correia <scorreia@redhat.com> - 10-2.1
- Fixes CVE-2023-50967

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 29 2017 Nathaniel McCallum <npmccallum@redhat.com> - 10-1
- New upstream release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 16 2017 Nathaniel McCallum <npmccallum@redhat.com> - 9-1
- New upstream release

* Wed Jun 14 2017 Nathaniel McCallum <npmccallum@redhat.com> - 8-1
- New upstream release

* Fri Mar 17 2017 Nathaniel McCallum <npmccallum@redhat.com> - 7-1
- New upstream release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 18 2017 Nathaniel McCallum <npmccallum@redhat.com> - 6-4
- Add a conflicts on old versions of jansson

* Fri Nov 11 2016 Nathaniel McCallum <npmccallum@redhat.com> - 6-3
- Fix build on big-endian platforms (fix already upstream)

* Thu Nov 10 2016 Nathaniel McCallum <npmccallum@redhat.com> - 6-2
- Rebuild to pick up new architectures

* Tue Oct 25 2016 Nathaniel McCallum <npmccallum@redhat.com> - 6-1
- New upstream release

* Fri Oct 14 2016 Nathaniel McCallum <npmccallum@redhat.com> - 5-1
- New upstream release

* Fri Sep 23 2016 Nathaniel McCallum <npmccallum@redhat.com> - 4-1
- New upstream release

* Wed Sep 21 2016 Nathaniel McCallum <npmccallum@redhat.com> - 3-1
- Initial package
