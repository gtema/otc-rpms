%global pypi_name keystoneauth1

%global with_tests 0

%global common_desc \
Keystoneauth provides a standard way to do authentication and service requests \
within the OpenStack ecosystem. It is designed for use in conjunction with \
the existing OpenStack clients and for simplifying the process of writing \
new clients.

%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:       python-%{pypi_name}
Version:    3.4.0
Release:    1%{?dist}
Summary:    Authentication Library for OpenStack Clients
License:    ASL 2.0
URL:        https://pypi.io/pypi/%{pypi_name}
Source0:    https://tarballs.openstack.org/keystoneauth/keystoneauth1-%{upstream_version}.tar.gz

BuildArch:  noarch

%description
%{common_desc}

%package -n     python2-%{pypi_name}
Summary:        Authentication Libarary for OpenStack Identity
Provides:       python-%{pypi_name} = %{version}-%{release}
Provides:       python-keystoneauth = %{version}-%{release}

BuildRequires: git
BuildRequires: python2-devel
BuildRequires: python2-setuptools
BuildRequires: python2-six
BuildRequires: python2-pbr >= 2.0.0

# test requires
BuildRequires: python2-betamax >= 0.7.0
# BuildRequires: python2-fixtures >= 1.3.1
BuildRequires: python2-oslotest
BuildRequires: python2-oslo-utils
BuildRequires: python2-os-testr
%if 0%{?fedora} || 0%{?rhel} > 7
# F27 packages
%if 0%{?fedora} == 27
BuildRequires: PyYAML
BuildRequires: python-requests-mock >= 1.1
BuildRequires: python-fixtures >= 1.3.1
%else
BuildRequires: python2-pyyaml
BuildRequires: python2-requests-mock >= 1.1
BuildRequires: python2-fixtures >= 1.3.1
%endif
# BuildRequires: python2-pyyaml
# BuildRequires: python2-requests-mock >= 1.1
BuildRequires: python2-lxml
BuildRequires: python2-requests-kerberos
BuildRequires: python2-oauthlib
%else
# BuildRequires: PyYAML
BuildRequires: python-lxml
BuildRequires: python-requests-kerberos
# BuildRequires: python-requests-mock >= 1.1
BuildRequires: python-oauthlib
%endif

Requires:      python2-iso8601 >= 0.1.11
Requires:      python2-pbr >= 2.0.0
Requires:      python2-requests >= 2.14.2
Requires:      python2-six => 1.10.0
Requires:      python2-stevedore >= 1.20.0

%description -n python2-%{pypi_name}
%{common_desc}

%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        Authentication Libarary for OpenStack Identity
Provides:       python3-keystoneauth = %{version}-%{release}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr >= 2.0.0
BuildRequires: python3-sphinx

# test requres
BuildRequires: python3-betamax >= 0.7.0
BuildRequires: python3-fixtures >= 1.3.1
BuildRequires: python3-lxml
BuildRequires: python3-requests-mock >= 1.1
BuildRequires: python3-oslotest
BuildRequires: python3-oslo-utils
BuildRequires: python3-os-testr
BuildRequires: python3-oauthlib
BuildRequires: python3-PyYAML

Requires:      python3-iso8601 >= 0.1.11
Requires:      python3-pbr >= 2.0.0
Requires:      python3-requests >= 2.14.2
Requires:      python3-six => 1.10.0
Requires:      python3-stevedore >= 1.20.0

%description -n python3-%{pypi_name}
%{common_desc}
%endif

%if 0%{?fedora} == 0
%package doc
Summary:    Documentation for OpenStack Identity Authentication Library

BuildRequires: python2-sphinx
BuildRequires: python2-openstackdocstheme
BuildRequires: python2-mock
BuildRequires: python2-requests
BuildRequires: python2-mox3
BuildRequires: python2-oslo-config
BuildRequires: python2-stevedore
BuildRequires: python2-iso8601
BuildRequires: python2-fixtures
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires: python2-pep8
%else
BuildRequires: python-pep8
%endif

%description doc
Documentation for OpenStack Identity Authentication Library
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

sed -i '/sphinx.ext.intersphinx.*$/d'  doc/source/conf.py

# Let RPM handle the dependencies
rm -rf {test-,}requirements.txt
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

%if 0%{?fedora} == 0
# generate html docs
%{__python} setup.py build_sphinx -b html
rm -rf doc/build/html/.buildinfo
%endif

%check
# keystoneauth upstream switched to stestr
#%{__python2} /usr/bin/ostestr
#%if 0%{?with_python3}
# cleanup testrepository
#rm -rf .testrepository
#%{__python3} /usr/bin/ostestr
#%endif

%files -n python2-%{pypi_name}
%doc README.rst
%license LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/*.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/*.egg-info
%endif

%if 0%{?fedora} == 0
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Sat Feb 10 2018 RDO <dev@lists.rdoproject.org> 3.4.0-1
- Update to 3.4.0
