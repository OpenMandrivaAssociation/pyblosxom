%define name    pyblosxom
%define version 1.3.2

Summary:	Pyblosxom is a python clone of Blosxom, a blogging system
Name:		%name
Version:	%version
Release:	%mkrel 1
License:	GPL
Group:		Networking/WWW
Url:        http://pyblosxom.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/pyblosxom/%{name}-%{version}.tar.bz2
Source1:    %{name}.apache.bz2
Patch0:     %{name}.config.patch
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	python-devel >= 2.2
Requires:   webserver
%description
Pyblogsxom is a clone of the original Bloxsom.
It is fully compatible with it , and allows you
to publish easily your weblog on your apache webserver.

%prep
%setup -q
%patch0 -p1

%build
CFLAGS="%{optflags}" python setup.py build


%install
rm -rf %buildroot
python setup.py install --root="%{buildroot}"

mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf/webapps.d
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}

bunzip2 -c %SOURCE1 > %{buildroot}/%{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf

mkdir -p %{buildroot}/var/www/%{name}
mv %{buildroot}/%{_datadir}/%{name}-%{version}/web/* %{buildroot}/var/www/%{name}

mkdir -p %{buildroot}/var/%{name}/

mv %{buildroot}/var/www/%{name}/config.py  %{buildroot}/%{_sysconfdir}/%{name}

perl -pi -e "s#py\['datadir'\].*#py['datadir'] = \"/var/pyblosxom/\"# "  %{buildroot}/%{_sysconfdir}/%{name}/config.py

%clean
rm -rf %buildroot


%post
%{_initrddir}/httpd reload

%postun
%{_initrddir}/httpd reload


%files
%defattr(0644,root,root,0755)
%doc  INSTALL  LICENSE docs/* README
%{py_pursitedir}/Pyblosxom
%{_datadir}/%{name}-%{version}/
/var/www/%{name}/
%attr(0755,root,root) /var/www/%{name}/*.cgi
%dir /var/%{name}/
%config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/config.py
%dir  %{_sysconfdir}/%{name}/
%{py_pursitedir}/%{name}-%{version}-py2.5.egg-info
