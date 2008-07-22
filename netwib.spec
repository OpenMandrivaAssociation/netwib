%define name	netwib
%define version	5.35.0
%define release	%mkrel 3

%define major	5
%define libname %mklibname %{name} %major
%define develname %mklibname -d %{name}

Summary:	A network library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		Networking/Other
URL:		http://www.laurentconstantin.com/fr/netw/netwib/
Source0:	http://www.laurentconstantin.com/common/netw/netwib/download/v5/%{name}-%{version}-src.tgz
Source1:	http://www.laurentconstantin.com/common/netw/netwib/download/v5/%{name}-%{version}-doc_html.tgz
Patch0:		netwib-5.35.0-genemake.patch
BuildRequires:	libpcap-devel >= 0.7.2
BuildRequires:	net2-devel => 1.1.2.1
BuildRoot:	%{_tmppath}/%{name}-buildroot

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
%patch0 -p0

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

cd src
%makeinstall_std
%make installso DESTDIR=%{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{develname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{develname} -p /sbin/ldconfig
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc INSTALLUNIX.TXT INSTALLWINDOWS.TXT README.TXT
%{_libdir}/libnetwib.so.*
%{_libdir}/libnetwib*.so.*

%files -n %{develname}
%defattr(-,root,root)
%doc INSTALLUNIX.TXT INSTALLWINDOWS.TXT README.TXT
%{_bindir}/netwib*-config
%{_includedir}/netwib*
%{_libdir}/libnetwib*.a
%{_libdir}/libnetwib*.so
%{_mandir}/man3/netwib*

%files -n %{name}-doc
%defattr(-,root,root)
%doc doc/*.txt %{name}-%{version}-doc_html/* 
