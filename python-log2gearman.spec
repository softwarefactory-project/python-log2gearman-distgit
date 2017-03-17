%global         commit0 3aa0ef430534c4d467d3e09f45333fea11f71b95
%global         shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global         checkout 20170317git%{shortcommit0}
%global         uname puppet-log_processor

Name:           python-log2gearman
Version:        0.1
Release:        1.%{checkout}%{dist}
Summary:        Python tools for writting/consuming log export tasks from Jenkins to Logstash

License:        ASL 2.0
URL:            https://github.com/openstack-infra/${uname}
Source0:        https://github.com/openstack-infra/%{uname}/archive/%{commit0}.tar.gz
Source1:        log-gearman-client.service
Source2:        log-gearman-worker.service

Patch0:         0001-SF-compatibility.patch

BuildArch:      noarch

Buildrequires:  python2-devel
BuildRequires:  systemd

%description
Python tools for writting/consuming log export tasks from Jenkins to Logstash

%package client
Summary: Python tools for writting log export tasks from Jenkins to Logstash
Requires:       python-gear
Requires:       PyYAML
Requires:       python-daemon
Requires:       python-zmq

%description client
Python tools for writting log export tasks from Jenkins to Logstash

%package worker
Summary: Python tools for consuming log export tasks from Jenkins to Logstash
Requires:       python-gear
Requires:       PyYAML
Requires:       python-daemon
Requires:       python-zmq

%description worker
Python tools for consuming log export tasks from Jenkins to Logstash

%prep
%autosetup -n %{uname}-%{commit0} -p1

%build

%install
install -p -d %{buildroot}%{_bindir}/
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

%files worker
%{_bindir}/log-gearman-worker.py
%dir %attr(0750, joblogsworker, joblogsworker) %{_var}/log/log-gearman-worker
%{_unitdir}/log-gearman-worker.service

%pre client
getent group joblogsclient >/dev/null || groupadd -r joblogsclient
if ! getent passwd joblogsclient >/dev/null; then
  useradd -r -g joblogsclient -G joblogsclient -d %{_sharedstatedir}/joblogsclient -s /sbin/nologin -c "Job logs gearman client Daemon" joblogsclient
fi

%pre worker
getent group joblogsworker >/dev/null || groupadd -r joblogsclient
if ! getent passwd joblogsworker >/dev/null; then
  useradd -r -g joblogsworker -G joblogsclient -d %{_sharedstatedir}/joblogsclient -s /sbin/nologin -c "Job logs gearman client Daemon" joblogsclient
fi
exit 0

%changelog
* Fri Mar 17 2017 Fabien Boucher <fboucher@redhat.com> - 0.1-1.20170317git3aa0ef4
- Initial packaging
