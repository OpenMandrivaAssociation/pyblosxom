Summary:	Python clone of Blosxom, a blogging system
Name:		pyblosxom
Version:	1.4.3
Release:	4
License:	GPL
Group:		Networking/WWW
Url:        http://pyblosxom.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/pyblosxom/%{name}-%{version}.tar.bz2
Patch0:     %{name}.config.patch
BuildRequires:	python-devel >= 2.2
Requires:   webserver
BuildArch:	noarch

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

%files
%defattr(0644,root,root,0755)
%doc  INSTALL  LICENSE docs/* README
%{_datadir}/%{name}-%{version}/
/var/www/%{name}/*.tac
%attr(0755,root,root) /var/www/%{name}/*.cgi
%dir /var/%{name}/
%config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/config.py
%dir  %{_sysconfdir}/%{name}/
%{py_puresitedir}/%{name}-%{version}-py%{py_ver}.egg-info
%{_bindir}/pyblcmd
%{py_puresitedir}/Pyblosxom/*


%changelog
* Sun Feb 07 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.4.3-3mdv2010.1
+ Revision: 501735
- use herein document for apache configuration
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise

* Tue Sep 15 2009 Thierry Vignaud <tv@mandriva.org> 1.4.3-2mdv2010.0
+ Revision: 441982
- rebuild

* Tue Jan 06 2009 Funda Wang <fwang@mandriva.org> 1.4.3-1mdv2009.1
+ Revision: 325979
- fix file list
- rediff config patch

* Thu Sep 04 2008 Jérôme Soyer <saispo@mandriva.org> 1.4.3-1mdv2009.0
+ Revision: 280730
- Fix 64bits compiling
- Fix files section
- New release
- Change python macro
- Fix python macros
- New release

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - fix file list
    - rebuild
    - fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot


* Sat Aug 13 2005 Michael Scherer <misc@mandriva.org> 1.2.1-1mdk
- 1.2.1
- fix apache config file location
- mkrel

* Sat Dec 04 2004 Michael Scherer <misc@mandrake.org> 1.0.0-3mdk
- Rebuild for new python

* Fri May 28 2004 Michael Scherer <misc@mandrake.org> 1.0.0-2mdk 
- [DIRM]

* Tue May 25 2004 Michael Scherer <misc@mandrake.org> 1.0.0-1mdk
- New release 1.0.0
- rpmbuildupdate aware

* Mon Mar 22 2004 Michael Scherer <misc@mandrake.org> 0.9-2mdk
- fix perm on files

* Fri Mar 19 2004 Michael Scherer <misc@mandrake.org> 0.9-1mdk
- 0.9

* Mon Jan 26 2004 Michael Scherer <misc@mandrake.org> 0.8.1-1mdk
- First mandrake package

