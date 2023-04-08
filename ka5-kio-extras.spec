#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	22.12.3
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		kio-extras
Summary:	kio-extras
Name:		ka5-%{kaname}
Version:	22.12.3
Release:	2
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	db4f869ea037adec53e87e890933c1fc
URL:		http://www.kde.org/
BuildRequires:	OpenEXR-devel >= 3.0.5
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= 5.4.0
BuildRequires:	Qt5Widgets-devel >= 5.4.0
BuildRequires:	cmake >= 2.8.12
BuildRequires:	gettext-devel
BuildRequires:	kdsoap-devel >= 1.9.0
BuildRequires:	kf5-extra-cmake-modules >= %{kframever}
BuildRequires:	libsmbclient-devel
BuildRequires:	libtirpc-devel > 1.3.2
BuildRequires:	ninja
BuildRequires:	qt5-build >= %{qtver}
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
install -d build
cd build
%cmake \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	..
%ninja_build

%if %{with tests}
ctest
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
%ghost %{_libdir}/libkioarchive.so.5
%attr(755,root,root) %{_libdir}/libkioarchive.so.5.*.*
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kded/filenamesearchmodule.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kded/recentdocumentsnotifier.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kded/smbwatcher.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kfileitemaction/kactivitymanagerd_fileitem_linking_plugin.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kio/about.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kio/activities.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kio/archive.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kio/bookmarks.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kio/filter.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kio/fish.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kio/info.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kio/man.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kio/mtp.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kio/nfs.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kio/recentdocuments.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kio/recentlyused.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kio/sftp.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kio/smb.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kio/thumbnail.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kio/kio_filenamesearch.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kiod/kmtpd.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kfileaudiopreview.so
%attr(755,root,root) %{_prefix}/libexec/kf5/smbnotifier
%{_datadir}/config.kcfg/jpegcreatorsettings5.kcfg
%dir %{_datadir}/kio_bookmarks
%{_datadir}/kio_bookmarks/kio_bookmarks.css
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
%{_datadir}/kservicetypes5/thumbcreator.desktop
%{_datadir}/qlogging-categories5/kio-extras.categories
%{_datadir}/qlogging-categories5/kio-extras.renamecategories
%{_datadir}/remoteview/mtp-network.desktop
%{_datadir}/remoteview/smb-network.desktop
%{_datadir}/dbus-1/services/org.kde.kmtpd5.service
%{_datadir}/solid/actions/solid_mtp.desktop
%dir %{_libdir}/qt5/plugins/kf5/thumbcreator
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/thumbcreator/audiothumbnail.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/thumbcreator/comicbookthumbnail.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/thumbcreator/cursorthumbnail.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/thumbcreator/djvuthumbnail.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/thumbcreator/ebookthumbnail.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/thumbcreator/exrthumbnail.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/thumbcreator/imagethumbnail.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/thumbcreator/jpegthumbnail.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/thumbcreator/kritathumbnail.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/thumbcreator/opendocumentthumbnail.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/thumbcreator/svgthumbnail.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/thumbcreator/textthumbnail.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/thumbcreator/windowsexethumbnail.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/thumbcreator/windowsimagethumbnail.so
%{_datadir}/kservices5/directorythumbnail.desktop
%{_datadir}/mime/packages/org.kde.kio.smb.xml
%dir %{_libdir}/qt5/plugins/kf5/kfileitemaction
%{_libdir}/qt5/plugins/kf5/kfileitemaction/forgetfileitemaction.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/kio_archivebase.h
%{_includedir}/KF5/libkioarchive_export.h
%{_libdir}/cmake/KioArchive
