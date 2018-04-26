%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%global modname otcextensions
# disable docs
%global with_doc 0

%global commit 923e90b7ffb1ab8797a4922392ffb105bc2f408c
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:             python-otcextensions
Version:          0.2.0
Release:          1%{?dist}
Summary:          OpenTelekomCloud Extensions to the OpenStack Command-line Client and the SDK
License:          ASL 2.0
URL:              https://github.com/OpenTelekomCloud/%{name}
BuildArch:        noarch
Source0:          https://github.com/OpenTelekomCloud/%{name}/archive/%{upstream_version}.tar.gz

%global _description \
Adds OpenTelekomCloud services into the OpenStackSDK and the OpenStackCLI

BuildRequires:  git

%description %{_description}

%package -n python2-%{modname}
Summary: %{summary}
%{?python_provide:%python_provide python2-%{modname}}
BuildRequires: python2-devel
BuildRequires: python2-openstacksdk
BuildRequires: python2-openstacksdk-tests
BuildRequires: python2-openstackclient
BuildRequires: python2-boto3
BuildRequires: python2-pbr >= 2.0.0
BuildRequires: python2-sphinx
BuildRequires: python2-openstackdocstheme
BuildRequires: python2-keystoneauth1
BuildRequires: python2-appdirs
BuildRequires: python2-requestsexceptions
BuildRequires: python-munch
BuildRequires: python2-jmespath
BuildRequires: python2-futures
BuildRequires: python2-jsonschema
BuildRequires: python2-os-service-types
# Test requirements
BuildRequires: python2-deprecation
BuildRequires: python2-iso8601 >= 0.1.11
BuildRequires: python2-jsonpatch >= 1.6
BuildRequires: python2-subunit
BuildRequires: python2-oslotest
BuildRequires: python2-mock
BuildRequires: python-testrepository
BuildRequires: python-testscenarios
BuildRequires: python2-testtools
BuildRequires: python2-glanceclient
%if 0%{?fedora} || 0%{?rhel} > 7
%if 0%{?fedora} == 27
BuildRequires: PyYAML
BuildRequires: python-requests-mock
BuildRequires: python-ipaddress
%else
BuildRequires: python2-pyyaml
BuildRequires: python2-requests-mock
BuildRequires: python2-ipaddress
%endif
BuildRequires: python2-decorator
BuildRequires: python2-dogpile-cache
BuildRequires: python2-netifaces
%else
BuildRequires: python-requests-mock
BuildRequires: python-decorator
BuildRequires: python-dogpile-cache
BuildRequires: python-ipaddress
BuildRequires: python-netifaces
%endif

Requires:      python2-openstacksdk >= 0.11.0
Requires:      python2-openstackclient >= 3.12.0
Requires:      python2-boto3 >= 1.4.6

%description -n python2-%{modname} %{_description}

Python 2 version.

%if 0%{?with_python3}
%package -n python3-%{modname}
Summary: %{summary}
%{?python_provide:%python_provide python3-%{modname}}
BuildRequires: python3-devel
BuildRequires: python3-openstacksdk
BuildRequires: python3-openstacksdk-tests
BuildRequires: python3-openstackclient
BuildRequires: python3-boto3
BuildRequires: python3-devel
BuildRequires: python3-pbr >= 2.0.0
BuildRequires: python3-keystoneauth1
BuildRequires: python3-dogpile-cache
BuildRequires: python3-appdirs
BuildRequires: python3-requestsexceptions
BuildRequires: python3-munch
BuildRequires: python3-decorator
BuildRequires: python3-jmespath
BuildRequires: python3-netifaces
BuildRequires: python3-jsonschema
BuildRequires: python3-os-service-types
# Test requirements
BuildRequires: python3-deprecation
BuildRequires: python3-iso8601 >= 0.1.11
BuildRequires: python3-jsonpatch >= 1.6
BuildRequires: python3-subunit
BuildRequires: python3-oslotest
BuildRequires: python3-stestr
BuildRequires: python3-mock
BuildRequires: python3-requests-mock
BuildRequires: python3-testrepository
BuildRequires: python3-testscenarios
BuildRequires: python3-testtools

Requires:      python3-openstacksdk >= 0.11.0
Requires:      python3-openstackclient >= 3.12.0
Requires:      python3-boto3 >= 1.4.6

%description -n python3-%{modname} %{_description}

Python 3 version.
%endif

%if 0%{?with_doc}
%package -n python-%{modname}-doc
Summary:        An SDK for building applications to work with OpenStack - documentation
BuildRequires: python2-sphinx
BuildRequires: python2-openstackdocstheme
%description -n python-%{modname}-doc
A collection of libraries for building applications to work with OTC cloud - documentation.
%endif

%prep
%autosetup -n %{name}-%{upstream_version} -S git

# We handle requirements ourselves
rm -rf requirements.txt test-requirements.txt

%build
%py2_build

%if 0%{?with_python3}
%py3_build
%endif

%if 0%{?with_doc}
# generate html docs
sphinx-build -b html doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%py2_install

%if 0%{?with_python3}
%py3_install
%endif

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo

# No tests, since SDK tests are missing
%check
#% {__python2} setup.py test
%if 0%{?with_python3}
# %{__python3} setup.py test
stestr-3 --test-path ./%{modname}/tests/unit run
%endif

%files -n python2-%{modname}
%license LICENSE
%doc LICENSE README.rst
%{python2_sitelib}/*.egg-info
%{python2_sitelib}/%{modname}
%exclude %{python2_sitelib}/%{modname}/tests
# %doc docs

%if 0%{?with_python3}
%files -n python3-%{modname}
%license LICENSE
%doc LICENSE README.rst
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/%{modname}
%exclude %{python3_sitelib}/%{modname}/tests
# %doc docs
%endif

%changelog
* Thu Apr 26 2018 Artem Goncharov <artem.goncharov@gmail.com> - 0.2.0-1
- Release 0.2.0

* Mon Apr 23 2018 Artem Goncharov <artem.goncharov@gmail.com> - 0.1.0-1
- Release 0.1.0

* Tue Mar 27 2018 Artem Goncharov <artem.goncharov@gmail.com> - 0.0.1-0
- Initial version
