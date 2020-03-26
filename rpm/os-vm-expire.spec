%global uname root
Name:    os-vm-expire-osc
Version: 0.9.3
Release: 1%{?dist}
Summary: Openstack client project for VM auto expiration
License: Apache 2.0
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Olivier Sallou <olivier.sallou@irisa.fr>
Url: https://github.com/genouest/os-vm-expire-osc-plugin

Source0: os-vm-expire-osc-%{version}.tar.gz
BuildRequires:  python2-pbr
BuildRequires:  python-setuptools
BuildRequires:  sudo
BuildRequires:  systemd

Requires:  python2-pbr
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

OSC plugin to manage VM expiration and auto-deletion in an Openstack cloud.
This project is an unofficial Openstack project, but follows Openstack
projects architecture, with a Horizon plugin and associated services.

* Free software: Apache license
* Bugs: https://github.com/genouest/os-vm-expire-osc-plugin/issues

The Openstack VmExpiration Management service adds an expiration to VMs.
After expiration, VM is deleted.
User can extend the VM lifetime via API or Horizon.
Expiration extend is not limited, user can always extend a VM, but it will
be extended only for a configured duration.
User cannot extend it more than configured duration.

%prep
%setup -n %{name}-%{version}

%build
PBR_VERSION=%{version} python setup.py build

%install
PBR_VERSION=%{version} python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%license LICENSE

%changelog
* Thu Mar 26 2020 Olivier Sallou <olivier.sallou@irisa.fr> 0.9.3-1
- Add rpm packagign file
