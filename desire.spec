Summary:	DESIRE - statistics access library
Summary(pl):	DESIRE - biblioteka, statysytyka dostepu 
Name:		desire
Version:	3.1
Release:	0.5
License:	???
Group:		Libraries
Group(de):	Libraries
Group(fr):	Librairies
Group(pl):	Biblioteki
Source0:	http://www.spelio.net.ru/soft/desire-3.1.tar.gz
Patch0:		%{name}-QnD.patch
Patch1:		%{name}-DESTDIR.patch
BuildRequires:	autoconf
BuildRequires:	gd-devel >= 2.0.1
BuildRequires:	gd-static >= 2.0.1
BuildRequires:	libstrfunc-devel
BuildRequires:	db3-devel

BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_cgidir		/home/httpd/cgi-bin
%define		_logdir		/var/log/desire

%description
Package includes:
    1. The library, libdesire, with header files
    2. Display library, libddraw, customizable at run time
    3. The set of dependent programs:
	+ Proxy (Squid, OOPS) accounting convertor and graphics
	  generator
	+ Cisco ip accounting converter and graphics generator
	+ Helper utilities

%package devel
Summary:	Development part of the desire library
Summary(pl):	Czê¶æ biblioteki desire przeznaczona dla developerów
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
This package contains the files needed for development of programs
linked against desire.

%package static
Summary:	Static desire library
Summary(pl):	Statyczna biblioteka desire
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description static
This package contains static desire library.

%package progs
Summary:	Utility programs that use desire
Summary(pl):	Narzêdzia które u¿ywaj± desire
Group:		Applications
Group(de):	Applikationen
Group(pl):	Aplikacje
Requires:	%{name} = %{version}
Requires:	apache

%description progs
These are utility programs supplied with desire.

%prep
%setup -q 
%patch0 -p1 
%patch1 -p1

%build
rm -f ltmain.sh aclocal.m4
libtoolize --copy --force
aclocal
autoconf
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
        DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_cgidir}/{cistat,proxy_stats}
install -d $RPM_BUILD_ROOT%{_logdir}/{calls,traffic,dialup/Usres,proxy/Domains}

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
