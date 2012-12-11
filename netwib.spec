%define name	netwib
%define version	5.39.0
%define release	1

%define major	5
%define libname %mklibname %{name} %major
%define develname %mklibname -d %{name}
%define develnamest %mklibname -d -s %{name}

Summary:	A network library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		Networking/Other
URL:		http://www.laurentconstantin.com/fr/netw/netwib/
Source0:	http://www.laurentconstantin.com/common/netw/netwib/download/v5/%{name}-%{version}-src.tgz
Source1:	http://www.laurentconstantin.com/common/netw/netwib/download/v5/%{name}-%{version}-doc_html.tgz
Patch0:		netwib-5.39.0-genemake.patch
BuildRequires:	libpcap-devel >= 0.7.2
BuildRequires:	net-devel >= 1.1.3

%description
Netwib is a network library for network administrator and hackers.
She provides:
  + address translation
  + client/server udp/tcp
  + paquets creation and annalyze
  + etc.

With Netwib, you can easily create a network application.

%package -n	%{libname}
Summary:	A network library
Group:		Networking/Other
Provides:	%{name}
Provides:	lib%{name} = %{version}-%{release}

%description -n	%{libname}
Netwib is a network library for network administrator and hackers.
She provides:
  + address translation
  + client/server udp/tcp
  + paquets creation and annalyze
  + etc.

With Netwib, you can easily create a network application.

%package -n	%{develname}
Summary:	A network library
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel
Obsoletes:	%{name}-devel
Obsoletes:	%{libname}-devel

%description -n	%{develname}
Netwib is a network library for network administrator and hackers.
She provides:
  + address translation
  + client/server udp/tcp
  + paquets creation and annalyze
  + etc.

With Netwib, you can easily create a network application.



%package -n	%{develnamest}
Summary:	A network library
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Requires:	%{develname} = %{version}-%{release}
Provides:	lib%{name}-devel-static = %{version}-%{release}
Provides:	%{name}-devel-static

%description -n	%{develnamest}
Netwib is a network library for network administrator and hackers.
She provides:
  + address translation
  + client/server udp/tcp
  + paquets creation and annalyze
  + etc.

With Netwib, you can easily create a network application.



%package -n	%{name}-doc
Summary:	Netwib html documentation
Group:		Networking/Other

%description -n	%{name}-doc
The netwib documention in html format.

Netwib is a network library for network administrator and hackers.
She provides:
  + address translation
  + client/server udp/tcp
  + paquets creation and annalyze
  + etc.

With Netwib, you can easily create a network application.

%prep

%setup -q -n %{name}-%{version}-src
%setup -q -D -T -a1 -n %{name}-%{version}-src
%patch0 -p1

perl -pi -e 's!^NETWIBDEF_INSTPREFIX=.*!NETWIBDEF_INSTPREFIX=%{_prefix}!' src/config.dat
# Hacking for lib64
perl -pi -e 's!^NETWIBDEF_INSTLIB=.*!NETWIBDEF_INSTLIB=%{_libdir}!' src/config.dat
perl -pi -e 's!^NETWIBDEF_INSTMAN=.*!NETWIBDEF_INSTMAN=%{_mandir}!' src/config.dat
perl -pi -e 's!^NETWIBDEF_SYSARCH=.*!NETWIBDEF_SYSARCH=%{_arch}!' src/config.dat

%build
cd src

./genemake

%make \
    GCCOPT="%{optflags} -Wall -fPIC -D_BSD_SOURCE -D__BSD_SOURCE -D__FAVOR_BSD -DHAVE_NET_ETHERNET_H" \
    GCCOPTL="$GCCOPT" GCCOPTP="$GCCOPT" libnetwib.so libnetwib.a

%install
cd src
%makeinstall_std
%make installso DESTDIR=%{buildroot}

%files -n %{libname}
%doc INSTALLUNIX.TXT INSTALLWINDOWS.TXT README.TXT
%{_libdir}/libnetwib.so.*
%{_libdir}/libnetwib539.so.5.39.0
#% {_libdir}/libnetwib*.so.*

%files -n %{develname}
%doc INSTALLUNIX.TXT INSTALLWINDOWS.TXT README.TXT
%{_bindir}/netwib*-config
%{_includedir}/netwib*
%{_libdir}/libnetwib*.so
%{_mandir}/man3/netwib*

%files -n %{develnamest}
%{_libdir}/libnetwib*.a

%files -n %{name}-doc
%doc doc/*.txt %{name}-%{version}-doc_html/* 


%changelog
* Mon Jul 09 2012 Alexander Khrukin <akhrukin@mandriva.org> 5.39.0-1
+ Revision: 808565
- version update 5.39

  + Oden Eriksson <oeriksson@mandriva.com>
    - the mass rebuild of 2010.0 packages

* Thu Jun 04 2009 Oden Eriksson <oeriksson@mandriva.com> 5.35.0-5mdv2010.0
+ Revision: 382729
- rebuilt against libnet 1.1.3

* Wed Oct 29 2008 Oden Eriksson <oeriksson@mandriva.com> 5.35.0-4mdv2009.1
+ Revision: 298321
- rebuilt against libpcap-1.0.0

* Wed Jul 23 2008 Thierry Vignaud <tv@mandriva.org> 5.35.0-3mdv2009.0
+ Revision: 241094
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Tue Jul 03 2007 Funda Wang <fwang@mandriva.org> 5.35.0-1mdv2008.0
+ Revision: 47385
- New version
  Rediff patch0
- bunzip2 the patch
- new devel package policy
- Import netwib

