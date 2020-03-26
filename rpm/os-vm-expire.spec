%global uname root
Name:    python-osvmexpire
Version: 0.9.3
Release: 1%{?dist}
Summary: Openstack project for VM auto expiration
License: Apache 2.0
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Olivier Sallou <olivier.sallou@irisa.fr>
Url: https://github.com/genouest/os-vm-expire

Source0: os-vm-expire-%{version}.tar.gz
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  sudo
BuildRequires:  systemd

Requires:  python-pbr
Requires:  python-paste
Requires:  python-paste-deploy
Requires:  python-oslo-config
Requires:  python2-oslo-context
Requires:  python2-oslo-db
Requires:  python-oslo-policy
Requires:  python-oslo-messaging
Requires:  python-oslo-log
Requires:  python2-oslo-utils
Requires:  python2-oslo-middleware
Requires:  python-oslo-i18n
Requires:  python-oslo-service
Requires:  python-webob
Requires:  python-keystonemiddleware
Requires:  python-pecan
Requires:  python-six
Requires:  python-sqlalchemy
Requires:  python-alembic
Requires:  python-prettytable
Requires(post): systemd
Requires(postun): systemd
Requires(preun): systemd



%description

Manage VM expiration and auto-deletion in an Openstack cloud.
This project is an unofficial Openstack project, but follows Openstack projects architecture, with a Horizon plugin and associated services.

* Free software: Apache license
* Documentation: http://os-vm-expire.readthedocs.io/
* Bugs: https://github.com/genouest/os-vm-expire/issues
* Horizon plugin: https://github.com/genouest/os-vm-expire-horizon-plugin

The Openstack VmExpiration Management service adds an expiration to VMs.
After expiration, VM is deleted.
User can extend the VM lifetime via API or Horizon.
Expiration extend is not limited, user can always extend a VM, but it will be extended only for a configured duration.
User cannot extend it more than configured duration.

%prep
%setup -n os-vm-expire-%{version}

%build
PBR_VERSION=%{version} python setup.py build

%install
PBR_VERSION=%{version} python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
mkdir -p $RPM_BUILD_ROOT/etc/os-vm-expire
cp -r etc/os-vm-expire/* $RPM_BUILD_ROOT/etc/os-vm-expire/
install -p -D -m 640 etc/oslo-config-generator/policy.json.sample $RPM_BUILD_ROOT/etc/os-vm-expire/policy.json
install -p -D -m 640 etc/oslo-config-generator/osvmexpire.conf.sample $RPM_BUILD_ROOT/etc/os-vm-expire/osvmexpire.conf
install -p -D -m 644 etc/systemd/system/osvmexpire-cleaner.service %{buildroot}%{_unitdir}/osvmexpire-cleaner.service
install -p -D -m 644 etc/systemd/system/osvmexpire-worker.service %{buildroot}%{_unitdir}/osvmexpire-worker.service
install -p -D -m 644 etc/systemd/system/osvmexpire-api.service %{buildroot}%{_unitdir}/osvmexpire-api.service
install -p -D -m 644 etc/logrotate.d/osvmexpire-api %{buildroot}%{_sysconfdir}/logrotate.d/osvmexpire-api.logrotate

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%license LICENSE
%config(noreplace) %attr(0640, root, %{uname}) /etc/os-vm-expire/policy.json
%config(noreplace) %attr(0640, root, %{uname}) /etc/os-vm-expire/osvmexpire.conf
%config(noreplace) %attr(0640, root, %{uname}) /etc/os-vm-expire/osvmexpire-api-paste.ini
%config(noreplace) %attr(0640, root, %{uname}) /etc/os-vm-expire/vassals/osvmexpire-api.ini
%dir %{_sysconfdir}/os-vm-expire
%config(noreplace) %{_sysconfdir}/logrotate.d/*
%{_unitdir}/osvmexpire-cleaner.service
%{_unitdir}/osvmexpire-worker.service
%{_unitdir}/osvmexpire-api.service

%post
%systemd_post osvmexpire-cleaner.service
%systemd_post osvmexpire-worker.service
%systemd_post osvmexpire-api.service


%preun
%systemd_preun osvmexpire-cleaner.service
%systemd_preun osvmexpire-worker.service
%systemd_preun osvmexpire-api.service

%postun
%systemd_postun_with_restart osvmexpire-cleaner.service
%systemd_postun_with_restart osvmexpire-worker.service
%systemd_postun_with_restart osvmexpire-api.service


%changelog
* Thu Mar 26 2020 Olivier Sallou <olivier.sallou@irisa.fr> 0.9-1
- Add rpm packagign file