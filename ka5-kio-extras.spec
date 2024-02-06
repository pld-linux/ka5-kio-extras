#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	24.01.95
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		kio-extras
Summary:	kio-extras
Name:		ka5-%{kaname}
Version:	24.01.95
Release:	0.1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/unstable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	bed8ebf22e429dea72840a4ef6226d74
URL:		http://www.kde.org/
BuildRequires:	OpenEXR-devel >= 3.0.5
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= 5.4.0
BuildRequires:	Qt6Widgets-devel >= 5.4.0
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	kdsoap-qt6-devel >= 2.2.0
BuildRequires:	kdsoap-ws-discovery-client-qt6-devel >= 0.3.0
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-karchive-devel >= %{kframever}
BuildRequires:	kf6-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf6-kdnssd-devel >= %{kframever}
BuildRequires:	kf6-kguiaddons-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	kf6-solid-devel >= %{kframever}
BuildRequires:	kf6-syntax-highlighting-devel >= %{kframever}
BuildRequires:	kp5-plasma-activities-devel
BuildRequires:	kp5-plasma-activities-stats-devel
BuildRequires:	libsmbclient-devel
BuildRequires:	libtirpc-devel > 1.3.2
BuildRequires:	ninja
BuildRequires:	phonon-qt6-devel
BuildRequires:	qcoro-qt6-devel >= 0.10.0
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
kio-extras.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

# not supported by glibc yet
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kded/filenamesearchmodule.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kded/smbwatcher.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kfileitemaction/kactivitymanagerd_fileitem_linking_plugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kio/activities.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kio/archive.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kio/filter.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kio/fish.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kio/info.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kio/man.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kio/mtp.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kio/recentlyused.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kio/sftp.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kio/smb.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kio/thumbnail.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kio/kio_filenamesearch.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kiod/kmtpd.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kfileaudiopreview.so
%attr(755,root,root) %{_prefix}/libexec/kf6/smbnotifier
%{_datadir}/config.kcfg/jpegcreatorsettings5.kcfg
%dir %{_datadir}/kio_docfilter
%{_datadir}/kio_docfilter/kio_docfilter.css
%dir %{_datadir}/kio_info
%{_datadir}/kio_info/kde-info2html
%{_datadir}/kio_info/kde-info2html.conf
%dir %{_datadir}/konqueror
%dir %{_datadir}/konqueror/dirtree
%dir %{_datadir}/konqueror/dirtree/remote
%{_datadir}/konqueror/dirtree/remote/mtp-network.desktop
%{_datadir}/konqueror/dirtree/remote/smb-network.desktop
%{_datadir}/remoteview/mtp-network.desktop
%{_datadir}/remoteview/smb-network.desktop
%{_datadir}/dbus-1/services/org.kde.kmtpd5.service
%{_datadir}/solid/actions/solid_mtp.desktop
%dir %{_libdir}/qt6/plugins/kf6/thumbcreator
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/thumbcreator/audiothumbnail.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/thumbcreator/comicbookthumbnail.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/thumbcreator/cursorthumbnail.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/thumbcreator/djvuthumbnail.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/thumbcreator/ebookthumbnail.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/thumbcreator/exrthumbnail.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/thumbcreator/imagethumbnail.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/thumbcreator/jpegthumbnail.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/thumbcreator/opendocumentthumbnail.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/thumbcreator/svgthumbnail.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/thumbcreator/textthumbnail.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/thumbcreator/windowsexethumbnail.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/thumbcreator/windowsimagethumbnail.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/thumbcreator/kraorathumbnail.so
%{_datadir}/mime/packages/org.kde.kio.smb.xml
%dir %{_libdir}/qt6/plugins/kf6/kfileitemaction
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kfileitemaction/forgetfileitemaction.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kio/afc.so
%{_datadir}/remoteview/afc-network.desktop
%{_datadir}/solid/actions/solid_afc.desktop
%ghost %{_libdir}/libkioarchive6.so.6
%attr(755,root,root) %{_libdir}/libkioarchive6.so.*.*
%attr(755,root,root) %{_libdir}/qt6/plugins/kcm_trash.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/thumbcreator/directorythumbnail.so
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/kcms/systemsettings_qwidgets/kcm_netpref.so
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/kcms/systemsettings_qwidgets/kcm_proxy.so
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/kcms/systemsettings_qwidgets/kcm_webshortcuts.so
%{_desktopdir}/kcm_netpref.desktop
%{_desktopdir}/kcm_proxy.desktop
%{_desktopdir}/kcm_trash.desktop
%{_desktopdir}/kcm_webshortcuts.desktop
%{_datadir}/qlogging-categories6/kio-extras.categories
%{_datadir}/qlogging-categories6/kio-extras.renamecategories


%files devel
%defattr(644,root,root,755)
%{_includedir}/KioArchive6
%{_libdir}/cmake/KioArchive6
