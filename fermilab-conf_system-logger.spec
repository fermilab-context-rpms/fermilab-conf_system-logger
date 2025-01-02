Name:		fermilab-conf_system-logger
Version:	1.4
Release:	2%{?dist}
Summary:	Log your system logs to the Fermi central logger

Group:		Fermilab
License:	MIT
URL:		https://github.com/fermilab-context-rpms/fermilab-conf_system-logger

Source0:	000-rsyslog-use-clogger.conf

BuildRequires:	augeas coreutils /usr/bin/awk
BuildArch:	noarch

%if 0%{?rhel} < 10
Obsoletes:	zz_use_clogger
%endif

# You must log things per CS-doc-5590-v1
# so require a system logger for now
Requires: 	rsyslog

# Top level package should require software specific packages
Requires:	(%{name}-rsyslog == %{version}-%{release} if rsyslog)

%description
This package will change your syslog configuration that will
send all of your logs to the Fermilab central logger.

Requirement from: CS-doc-5590-v1


%package rsyslog
Summary:	Log your system logs to the Fermi central logger using rsyslog
Requires:	%{name} = %{version}-%{release}
Requires:	rsyslog-gnutls >= 8.2108.0
Requires(post):	rsyslog >= 8.0 systemd
Requires(postun):	rsyslog >= 8.0 systemd

%description rsyslog
This package will change your rsyslog configuration that will
send all of your logs to the Fermilab central logger.

Requirement from: CS-doc-5590-v1


%prep


%build


%install
%{__install} -D %{SOURCE0} %{buildroot}%{_sysconfdir}/rsyslog.d/000-use-clogger.conf


%check
# Run a quick syntax/sanity check of the config file
TMPFILE=$(mktemp)
cat > ${TMPFILE} <<EOF
rm /augeas/load/Rsyslog/incl
rm /augeas/load/Rsyslog/incl
rm /augeas/load/Rsyslog/incl
set /augeas/load/Rsyslog/incl %{SOURCE0}
load

get /files/%{SOURCE0}/entry/action/hostname
EOF
cat ${TMPFILE}
# Should error out if file cannot be parsed
FETCH_HOSTNAME=$(augtool --noload < ${TMPFILE} | awk '{print $3}')
rm -f ${TMPFILE}

%post rsyslog
systemctl condrestart rsyslog.service

%postun rsyslog
systemctl condrestart rsyslog.service

%files
%defattr(0644,root,root,0755)

%files rsyslog
%defattr(0644,root,root,0755)
%config %{_sysconfdir}/rsyslog.d/*

%changelog
* Thu Jan 2 2025 Pat Riehecky <riehecky@fnal.gov> 1.4-2
* Since we don't use the CA cert, don't ship it

* Mon May 20 2024 Pat Riehecky <riehecky@fnal.gov> 1.4-1
* Skip CA check to make CST cert rotation easier

* Mon May 6 2024 Pat Riehecky <riehecky@fnal.gov> 1.3-1
- Use newer rsyslog features
- Don't log certificate warnings to syslog (still in journald)

* Thu May 19 2022 Pat Riehecky <riehecky@fnal.gov> 1.2-4
- Use disk cache rather than dropping under load

* Thu Apr 28 2022 Pat Riehecky <riehecky@fnal.gov> 1.2-3
- Note requirements on streamDriver.CAFile

* Fri Apr 15 2022 Pat Riehecky <riehecky@fnal.gov> 1.2-2
- Leave default templates in place

* Wed Apr 13 2022 Pat Riehecky <riehecky@fnal.gov> 1.2-1.1
- Use rich boolean deps

* Wed Mar 16 2022 Pat Riehecky <riehecky@fnal.gov> 1.2-1
- Default to encrypted messages via RITM1289242

* Mon Jan 13 2020 Pat Riehecky <riehecky@fnal.gov> 1.1-5.2
- Support newer augeas

* Mon Nov 2 2015 Pat Riehecky <riehecky@fnal.gov> 1.1-5.1
- added postun to hup the daemon

* Fri Aug 7 2015 Pat Riehecky <riehecky@fnal.gov> 1.1-5
- Updated for EL7

* Wed Jan 30 2013 Pat Riehecky <riehecky@fnal.gov> 1.1-4
- now using /etc/rsyslog.d/000-use-clogger.conf rather than
  editing /etc/rsyslog.conf

* Mon May 16 2011 Troy Dawson <dawson@fnal.gov> 1.1-3
- Changed the mispelled rsyslogd to rsyslog

* Mon May 16 2011 Troy Dawson <dawson@fnal.gov> 1.1-2
- Changed the mispelled sysklog to rsyslogd

* Wed Apr 20 2011 Troy Dawson <dawson@fnal.gov> 1.1-1
- Rebuilt to work with SLF6
- Converted everything from syslog to rsyslog

* Mon Apr 20 2009 Troy Dawson <dawson@fnal.gov> 1.0-1
- First go round
