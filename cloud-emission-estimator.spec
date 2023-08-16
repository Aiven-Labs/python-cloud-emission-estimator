Name:           python-cloud-emission-estimator
Version:        %{major_version}
Release:        %{minor_version}%{?dist}
Url:            https://aiven.io/
Summary:        Cloud Emission Estimator
License:        ASL 2.0
Source0:        rpm-src-cloud-emission-estimator.tar
BuildArch:      noarch
BuildRequires:  python3-devel

%global _description %{expand:
Cloud Emission Estimator is a Python based tool for calculating energy usage and carbon emissions based on cloud resource consumption.

The tool is based on Cloud Carbon Footprint project.}

%description %_description

%package -n python3-cloud-emission-estimator
Summary: %{summary}
BuildRequires:  python3-devel, python3-flake8, python3-mypy, python3-pytest

%description -n python3-cloud-emission-estimator %_description

%prep
%setup -q -n cloud-emission-estimator

%install
%{__mkdir_p} %{buildroot}%{_bindir}
%{__mkdir_p} %{buildroot}%{python3_sitelib}
cp -a cloud_emission_estimator %{buildroot}%{python3_sitelib}/

%check
make test

%files -n python3-cloud-emission-estimator
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{python3_sitelib}/cloud_emission_estimator


%changelog
* Wed Aug 9 2023 Aiven Support <support@aiven.io>
- Initial version
