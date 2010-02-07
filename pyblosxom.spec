%define name    pyblosxom
%define version 1.4.3

Summary:	Python clone of Blosxom, a blogging system
Name:		%name
Version:	%version
Release:	%mkrel 3
License:	GPL
Group:		Networking/WWW
Url:        http://pyblosxom.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/pyblosxom/%{name}-%{version}.tar.bz2
Patch0:     %{name}.config.patch
BuildRequires:	python-devel >= 2.2
Requires:   webserver
%if %mdkversion < 201010
Requires(post):   rpm-helper
Requires(postun):   rpm-helper
%endif
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

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

# apache configuration
install -d -m 755 %{buildroot}%{webappconfdir}
cat > %{buildroot}%{webappconfdir}/%{name}.conf << EOF
Alias /pyblosxom /var/www/pyblosxom

<Directory /var/www/pyblosxom>
    Options +ExecCGI
    Order allow,deny
    Allow from all
    DirectoryIndex pyblosxom.cgi
</Directory>
EOF


mkdir -p %{buildroot}/var/www/%{name}
mv %{buildroot}/%{_datadir}/%{name}-%{version}/web/* %{buildroot}/var/www/%{name}

mkdir -p %{buildroot}/var/%{name}/

mv %{buildroot}/var/www/%{name}/config.py  %{buildroot}/%{_sysconfdir}/%{name}

perl -pi -e "s#py\['datadir'\].*#py['datadir'] = \"/var/pyblosxom/\"# "  %{buildroot}/%{_sysconfdir}/%{name}/config.py

%clean
rm -rf %buildroot

%post
%if %mdkversion < 201010
%_post_webapp
%endif

%postun
%if %mdkversion < 201010
%_postun_webapp
%endif


%files
%defattr(0644,root,root,0755)
%doc  INSTALL  LICENSE docs/* README
%{_datadir}/%{name}-%{version}/
/var/www/%{name}/
%attr(0755,root,root) /var/www/%{name}/*.cgi
%dir /var/%{name}/
%config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/config.py
%dir  %{_sysconfdir}/%{name}/
%{py_puresitedir}/%{name}-%{version}-py%{py_ver}.egg-info
%{_bindir}/pyblcmd
%{py_puresitedir}/Pyblosxom/*
