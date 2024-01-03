%global modname assignment-list

Name:           python3-%{modname}
Version:        0.0.1
Release:        1%{?dist}
Summary:        Assignment List PyQt5

License:        Unlicense
URL:            https://github.com/lshprung/assignment-list-pyqt
Source0:        %{name}-%{version}.tar.gz

BuildArch: noarch

BuildRequires:  python36-devel
BuildRequires:  python3-setuptools
BuildRequires:  python36-rpm-macros
BuildRequires:  python3-qt5-devel

%?python_enable_dependency_generator

%description
Assignment List PyQt5

%prep
%autosetup -n %{modname}-%{version}


%build
%py3_build


%install
%py3_install
mkdir -p %{buildroot}%{_datadir}/pixmaps
install data/%{modname}.svg %{buildroot}%{_datadir}/pixmaps/%{modname}.svg
mkdir -p %{buildroot}%{_datadir}/applications
install data/%{modname}.desktop %{buildroot}%{_datadir}/applications/%{modname}.desktop
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/%{modname}.desktop


%check
%{__python3} setup.py test

%files -n python3-%{modname}
%{_bindir}/assignment-list
%{python3_sitelib}/assignment_list_pyqt
%{python3_sitelib}/assignment_list-%{version}*
%{_datadir}/applications/%{modname}.desktop
%{_datadir}/pixmaps/%{modname}.svg


%changelog
* Wed Jan 03 2024 Louie S <lshprung@tutanota.com> - 0.0.1
- Update src directory name to assignment_list_pyqt
* Thu Sep 21 2023 Louie S <louie@example.com>
- Initial spec version
