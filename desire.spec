Summary:	DESIRE - statistics access library
Summary(pl):	DESIRE - biblioteka, statystyka dostêpu
Name:		desire
Version:	3.1
Release:	1
License:	BSD-like
Group:		Libraries
Source0:	http://www.spelio.net.ru/soft/%{name}-%{version}.tar.gz
# Source0-md5:	86fde160bb54f868a6a9ba2bc2925ec2
Patch0:		%{name}-QnD.patch
Patch1:		%{name}-DESTDIR.patch
URL:		http://www.spelio.net.ru/soft/#DESIRE
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	db3-devel
BuildRequires:	gd-devel >= 2.0.1
BuildRequires:	gd-static >= 2.0.1
BuildRequires:	libstrfunc-devel
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_cgidir		/home/services/httpd/cgi-bin
%define		_logdir		/var/log/desire

%description
Package includes main library (libdesire) and display library,
libddraw, customizable at run time.

%description -l pl
Pakiet zawiera g³ówn± bibliotekê (libdesire) i bibliotekê do
rysowania, libddraw, konfigurowaln± w locie.

%package devel
Summary:	Development part of the desire library
Summary(pl):	Czê¶æ biblioteki desire przeznaczona dla developerów
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
This package contains the files needed for development of programs
linked against desire.

%description devel -l pl
Ten pakiet zawiera pliki potrzebne do kompilowania programów z
bibliotek± desire.

%package static
Summary:	Static desire library
Summary(pl):	Statyczna biblioteka desire
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
This package contains static desire library.

%description static -l pl
Ten pakiet zawiera statyczn± bibliotekê desire.

%package progs
Summary:	Utility programs that use desire
Summary(pl):	Narzêdzia które u¿ywaj± desire
Group:		Applications
Requires:	%{name} = %{version}
Requires:	apache

%description progs
These are utility programs supplied with desire:
 - Proxy (Squid, OOPS) accounting convertor and graphics generator
 - Cisco ip accounting converter and graphics generator
 - Helper utilities

%description progs -l pl
Tutaj s± programy dostarczone z desire:
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
install conf/* $RPM_BUILD_ROOT/%{_sysconfdir}
touch $RPM_BUILD_ROOT/%{_sysconfdir}/DOMAINS

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
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
