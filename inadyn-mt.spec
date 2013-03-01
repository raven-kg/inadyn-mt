Name:           inadyn-mt

Version:        2.24.38
Release:        1%{?dist}

Summary:        Dynamic DNS Client

Group:          System Environment/Daemons
License:        GPLv3
URL:            http://inadyn-mt.sourceforge.net
Source0:        http://prdownloads.sourceforge.net/inadyn-mt/inadyn-mt.v.0%{version}.tar.gz
Source1:        inadyn-mt.conf
Source2:        inadyn.init
Source3:        inadyn-nm-dispatcher

BuildRequires:  libao-devel

Obsoletes:      inadyn < %{version}
Provides:       inadyn = %{version}-%{release}

%description
INADYN-MT is a dynamic DNS client. It maintains the IP address of 
a host name. It periodically checks wheather the IP address stored
by the DSN server is the real current address of the machine that
is running INADYN-MT.

Before using inadyn-mt for the first time you must use the DynDNS
provider's web interface to create the entry for the hostname. You
should then fill in /etc/inadyn-mt.conf with the appropriate detail

%prep
%setup -q -n %name.v.0%{version}

%build
rm -rf bin/
%configure
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS"

%install
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
install -m 0755 src/inadyn-mt $RPM_BUILD_ROOT%{_sbindir}/inadyn

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man5
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8
install -p -m 0644 man/inadyn.8 $RPM_BUILD_ROOT%{_mandir}/man8
install -p -m 0644 man/inadyn.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
install -p -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/inadyn-mt/lang
cp lang/* $RPM_BUILD_ROOT%{_datadir}/inadyn-mt/lang

mkdir -p $RPM_BUILD_ROOT%{_datadir}/inadyn-mt/extra
cp -R extra/* $RPM_BUILD_ROOT%{_datadir}/inadyn-mt/extra

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/init.d
install -p %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/init.d/inadyn

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/NetworkManager/dispatcher.d
install -p -m 0755 %{SOURCE3} ${RPM_BUILD_ROOT}%{_sysconfdir}/NetworkManager/dispatcher.d/30-inadyn

%post 
/sbin/chkconfig --add inadyn

%preun 
if [ $1 -eq 0 ]; then
  /sbin/service inadyn stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del inadyn
fi

%postun 
if [ $1 -ge 1 ]; then
  /sbin/service inadyn condrestart >/dev/null
fi

%files 
%defattr(-,root,root,-)
%doc COPYING readme.html
%{_sbindir}/inadyn
%{_sysconfdir}/init.d/inadyn
%{_mandir}/man*/*
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/NetworkManager/dispatcher.d/30-inadyn
%{_datadir}/%{name}/

%changelog
* Fri Mar 01 2013 Raven <admin@sysadmins.el.kg> - 2.24.38-1
- Initial build for el6
