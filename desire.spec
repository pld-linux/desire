# TODO:
# - update to >= 4.0.2
# - switch to current db
# - kill gd-static BR
# - stop using hardcoded /srv subdir by default
Summary:	DESIRE - statistics access library
Summary(pl.UTF-8):	DESIRE - biblioteka, statystyka dostępu
Name:		desire
Version:	3.1
Release:	2
License:	BSD-like
Group:		Libraries
Source0:	http://lionet.info/soft/%{name}-%{version}.tar.gz
# Source0-md5:	86fde160bb54f868a6a9ba2bc2925ec2
Patch0:		%{name}-QnD.patch
Patch1:		%{name}-DESTDIR.patch
URL:		http://lionet.info/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	db3-devel
BuildRequires:	fhs-compliance
BuildRequires:	gd-devel >= 2.0.1
BuildRequires:	gd-static >= 2.0.1
BuildRequires:	libstrfunc-devel
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_cgidir		/srv/httpd/cgi-bin
%define		_logdir		/var/log/desire

%description
Package includes main library (libdesire) and display library,
libddraw, customizable at run time.

%description -l pl.UTF-8
Pakiet zawiera główną bibliotekę (libdesire) i bibliotekę do
rysowania, libddraw, konfigurowalną w locie.

%package devel
Summary:	Development part of the desire library
Summary(pl.UTF-8):	Część biblioteki desire przeznaczona dla developerów
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the files needed for development of programs
linked against desire.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki potrzebne do kompilowania programów z
biblioteką desire.

%package static
Summary:	Static desire library
Summary(pl.UTF-8):	Statyczna biblioteka desire
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains static desire library.

%description static -l pl.UTF-8
Ten pakiet zawiera statyczną bibliotekę desire.

%package progs
Summary:	Utility programs that use desire
Summary(pl.UTF-8):	Narzędzia które używają desire
Group:		Applications
Requires:	%{name} = %{version}-%{release}
Requires:	webserver = apache

%description progs
These are utility programs supplied with desire:
 - Proxy (Squid, OOPS) accounting convertor and graphics generator
 - Cisco ip accounting converter and graphics generator
 - Helper utilities

%description progs -l pl.UTF-8
Tutaj są programy dostarczone z desire:
 - Konwerter i generator graficznych statystyk z Proxy (Squid, OOPS)
 - Konwerter i generator grafik z Cisco
 - programy pomocnicze

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
rm -f ltmain.sh aclocal.m4
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_cgidir}/{cistat,proxy_stats} \
	$RPM_BUILD_ROOT%{_logdir}/{calls,traffic,dialup/Usres,proxy/Domains}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install depend/cistat/html/* $RPM_BUILD_ROOT%{_cgidir}/cistat
install depend/proxy_stats/html/* $RPM_BUILD_ROOT%{_cgidir}/proxy_stats
install conf/* $RPM_BUILD_ROOT%{_sysconfdir}
touch $RPM_BUILD_ROOT%{_sysconfdir}/DOMAINS

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog
%attr(755,root,root) %{_libdir}/*.so.*

%files devel
%defattr(644,root,root,755)
%{_libdir}/*.so
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files progs
%defattr(644,root,root,755)
%{_logdir}
%{_sysconfdir}/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_cgidir}/proxy_stats
%attr(755,root,root) %{_cgidir}/cistat
