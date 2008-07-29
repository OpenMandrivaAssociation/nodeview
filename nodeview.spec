Summary:	OpenKiosk central server containing the client information database 
Name:		nodeview
Version:	2.0.3
Release:	%mkrel 5
License:	GPL
Group:		Networking/Other
URL:		http://openkiosk.sourceforge.net			
Source0:	http://prdownloads.sourceforge.net/openkiosk/%{name}-%{version}.tar.bz2
Source1:	nodeview-48x48.png
BuildRequires:	db4.2-devel
BuildRequires:	qt3-devel
BuildRequires:	ImageMagick dos2unix
BuildRequires:	kdelibs-devel
BuildRoot:	%{_tmppath}/%{name}-buildroot-%{version}
	
%description
The Openkiosk system is basically composed of two parts. The first program 
is called NodeView. It acts as the OpenKiosk central server containing the 
client information database. It is responsible for administering all the 
clients on the network either automatically or manually. Monitoring and 
controlling the workstations can be done locally via the graphical user 
interfaces or remotely from a Java Applet in a browser.

The client application that goes with nodeview is call kdex11client.

%prep

%setup -q

%build
sed -i 's|usr/local|usr|g' configure
sed -i 's|${PREFIX:22}|4.2|' configure
sed -i 's|read VER||' configure

export QTDIR=/usr/lib/qt3
%configure
%make

%install
rm -rf $RPM_BUILD_ROOT

export QTDIR=/usr/lib/qt3
%makeinstall_std INSTALL_ROOT=$RPM_BUILD_ROOT

install -d %{buildroot}%{_liconsdir}
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_miconsdir}

cp %{SOURCE1} .

install -m0644 nodeview-48x48.png %{buildroot}%{_liconsdir}/%{name}.png
convert -size 32x32 nodeview-48x48.png %{buildroot}%{_iconsdir}/%{name}.png
convert -size 16x16 nodeview-48x48.png %{buildroot}%{_miconsdir}/%{name}.png


mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=NodeView
Comment=The central control program of the OpenKiosk system
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-System-Configuration-Networking;Settings;Network;
EOF

#(sb) get rid of these old docs/make rpmlint happier
rm -fr docs/oldversion
dos2unix docs/doc.css
dos2unix docs/update.htm

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-,root,root)
%doc AUTHORS BUGS COPYING ChangeLog README* docs/*
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

