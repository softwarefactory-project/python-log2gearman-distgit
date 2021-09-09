%global         commit0 89bfe00dda0b9761bd79b0aa1ac2092940f0f11d
%global         shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global         checkout 20201022git%{shortcommit0}
%global         uname puppet-log_processor

Name:           python-log2gearman
Version:        0.1
Release:        6.%{checkout}%{dist}
Summary:        Python tools for writing/consuming log export tasks from Jenkins to Logstash

License:        ASL 2.0
URL:            https://opendev.org/opendev/${uname}
Source0:        https://opendev.org/opendev/%{uname}/archive/%{commit0}.tar.gz
Source1:        log-gearman-client.service
Source2:        log-gearman-worker.service

Patch0:         0001-SF-compatibility.patch
Patch1:         0001-Do-not-import-daemon-in-forground.patch
Patch2:         0001-Add-capability-with-python3-added-log-request-cert-v.patch

BuildArch:      noarch

Buildrequires:  python3-devel
BuildRequires:  systemd

%description
Python tools for writing/consuming log export tasks from Jenkins to Logstash

%package client
Summary: Python tools for writing log export tasks from Jenkins to Logstash
Requires:       python3-gear
Requires:       python3-pbr
Requires:       python3-extras
Requires:       PyYAML
Requires:       python3-zmq

%description client
Python tools for writing log export tasks from Jenkins to Logstash

%package worker
Summary: Python tools for consuming log export tasks from Jenkins to Logstash
Requires:       python3-gear
Requires:       python3-pbr
Requires:       python3-extras
Requires:       PyYAML
Requires:       python3-zmq
Requires:       python3-paho-mqtt

%description worker
Python tools for consuming log export tasks from Jenkins to Logstash

%prep
%autosetup -n %{uname} -p1

%build

%install
install -p -d %{buildroot}%{_bindir}/
install -p -d -m 0755 %{buildroot}%{_sysconfdir}/log-gearman-client
install -p -d -m 0755 %{buildroot}%{_sysconfdir}/log-gearman-worker
install -p -d -m 0700 %{buildroot}%{_var}/log/log-gearman-client
install -p -d -m 0700 %{buildroot}%{_var}/log/log-gearman-worker
install -p -D -m 0755 files/log-gearman-client.py %{buildroot}%{_bindir}/
install -p -D -m 0755 files/log-gearman-worker.py %{buildroot}%{_bindir}/
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/log-gearman-client.service
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/log-gearman-worker.service

%files client
%{_bindir}/log-gearman-client.py
%dir %attr(0750, joblogsclient, joblogsclient) %{_var}/log/log-gearman-client
%{_unitdir}/log-gearman-client.service
%config(noreplace) %{_sysconfdir}/log-gearman-client

%files worker
%{_bindir}/log-gearman-worker.py
%dir %attr(0750, joblogsworker, joblogsworker) %{_var}/log/log-gearman-worker
%{_unitdir}/log-gearman-worker.service
%config(noreplace) %{_sysconfdir}/log-gearman-worker

%pre client
getent group joblogsclient >/dev/null || groupadd -r joblogsclient
if ! getent passwd joblogsclient >/dev/null; then
  useradd -r -g joblogsclient -G joblogsclient -d %{_sharedstatedir}/joblogsclient -s /sbin/nologin -c "Job logs gearman client Daemon" joblogsclient
fi

%post client
%systemd_post log-gearman-client.service

%preun client
%systemd_preun log-gearman-client.service

%postun client
%systemd_postun log-gearman-client.service

%pre worker
getent group joblogsworker >/dev/null || groupadd -r joblogsworker
if ! getent passwd joblogsworker >/dev/null; then
  useradd -r -g joblogsworker -G joblogsworker -d %{_sharedstatedir}/joblogsworker -s /sbin/nologin -c "Job logs gearman client Daemon" joblogsworker
fi
exit 0

%post worker
%systemd_post log-gearman-worker.service

%preun worker
%systemd_preun log-gearman-worker.service

%postun worker
%systemd_postun log-gearman-worker.service

%changelog
* Thu Sep 09 2021 Daniel Pawlik <dpawlik@redhat.com> - 0.1-6
- Bump to commit 89bfe00dda0b9761bd79b0aa1ac2092940f0f11d
- Add requirements
- Change interpreter to python3

* Tue Dec 11 2018 Tristan Cacqueray <tdecacqu@redhat.com> - 0.1-5
- Remove python-daemon

* Thu Aug 23 2018 Tristan Cacqueray <tdecacqu@redhat.com> - 0.1-4
- Add missing paho-mqtt worker requirement

* Mon Jun 25 2018 Tristan Cacqueray <tdecacqu@redhat.com> - 0.1-3
- Bump version

* Mon May 15 2017 Tristan Cacqueray <tdecacqu@redhat.com> - 0.1-2.20170317git3aa0ef4
- Update SF compatibility patch

* Fri Mar 17 2017 Fabien Boucher <fboucher@redhat.com> - 0.1-1.20170317git3aa0ef4
- Initial packaging
