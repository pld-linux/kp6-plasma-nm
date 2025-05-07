#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.3.5
%define		qtver		6.6.0
%define		kpname		plasma-nm
%define		kf6ver		5.39.0

Summary:	plasma-nm
Name:		kp6-%{kpname}
Version:	6.3.5
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	fcbb0e9cfbab81cc66d73688b8861fc9
URL:		http://www.kde.org/
BuildRequires:	ModemManager-devel
BuildRequires:	NetworkManager-devel
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Network-devel >= %{qtver}
BuildRequires:	Qt6Qml-devel >= %{qtver}
BuildRequires:	Qt6Quick-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	Qt6Xml-devel >= %{qtver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	gettext-devel
BuildRequires:	kf6-kcompletion-devel
BuildRequires:	kf6-kconfigwidgets-devel
BuildRequires:	kf6-kcoreaddons-devel
BuildRequires:	kf6-kdbusaddons-devel
BuildRequires:	kf6-kdeclarative-devel
BuildRequires:	kf6-ki18n-devel
BuildRequires:	kf6-kiconthemes-devel
BuildRequires:	kf6-kio-devel
BuildRequires:	kf6-kitemviews-devel
BuildRequires:	kf6-knotifications-devel
BuildRequires:	kf6-kservice-devel
BuildRequires:	kf6-kwallet-devel
BuildRequires:	kf6-kwidgetsaddons-devel
BuildRequires:	kf6-kwindowsystem-devel
BuildRequires:	kf6-kxmlgui-devel
BuildRequires:	kf6-modemmanager-qt-devel
BuildRequires:	kf6-networkmanager-qt-devel
BuildRequires:	kf6-solid-devel
BuildRequires:	kp6-libplasma-devel >= %{version}
BuildRequires:	ninja
BuildRequires:	qcoro-qt6-devel
%ifnarch i686 x32
BuildRequires:	Qt6WebEngine-devel >= %{qtver}
BuildRequires:	openconnect-devel >= 3.99
%endif
BuildRequires:	pkgconfig
BuildRequires:	qca-qt6-devel >= 2.1.1
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
Obsoletes:	kp5-%{kpname} < 6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
Plasma applet written in QML for managing network connections.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	%ifarch i686 x32
		-DBUILD_OPENCONNECT=OFF
	%endif

%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database_post

%postun
/sbin/ldconfig
%update_desktop_database_postun

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libplasmanm_editor.so
%attr(755,root,root) %{_libdir}/libplasmanm_internal.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kded/networkmanagement.so
%dir %{_libdir}/qt6/qml/org/kde/plasma/networkmanagement
%{_libdir}/qt6/qml/org/kde/plasma/networkmanagement/qmldir
%{_datadir}/plasma/plasmoids/org.kde.plasma.networkmanagement
%dir %{_datadir}/kcm_networkmanagement
%dir %{_datadir}/kcm_networkmanagement/qml
%{_datadir}/kcm_networkmanagement/qml/ConnectionItem.qml
%{_datadir}/kcm_networkmanagement/qml/ListItem.qml
%{_datadir}/kcm_networkmanagement/qml/main.qml
%{_datadir}/metainfo/org.kde.plasma.networkmanagement.appdata.xml
%{_datadir}/kcm_networkmanagement/qml/AddConnectionDialog.qml
%{_datadir}/kcm_networkmanagement/qml/ConfigurationDialog.qml
%dir %{_libdir}/qt6/plugins/plasma/network
%dir %{_libdir}/qt6/plugins/plasma/network/vpn

%ifnarch i686 x32
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/network/vpn/plasmanetworkmanagement_openconnect_anyconnect.so
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/network/vpn/plasmanetworkmanagement_openconnect_globalprotectui.so
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/network/vpn/plasmanetworkmanagement_openconnect_juniperui.so
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/network/vpn/plasmanetworkmanagement_openconnect_pulseui.so
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/network/vpn/plasmanetworkmanagement_openconnect_arrayui.so
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/network/vpn/plasmanetworkmanagement_openconnect_f5ui.so
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/network/vpn/plasmanetworkmanagement_openconnect_fortinetui.so
%endif

%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/network/vpn/plasmanetworkmanagement_fortisslvpnui.so
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/network/vpn/plasmanetworkmanagement_iodineui.so
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/network/vpn/plasmanetworkmanagement_l2tpui.so
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/network/vpn/plasmanetworkmanagement_openvpnui.so
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/network/vpn/plasmanetworkmanagement_pptpui.so
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/network/vpn/plasmanetworkmanagement_sshui.so
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/network/vpn/plasmanetworkmanagement_sstpui.so
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/network/vpn/plasmanetworkmanagement_strongswanui.so
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/network/vpn/plasmanetworkmanagement_vpncui.so
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/kcms/systemsettings_qwidgets/kcm_networkmanagement.so
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/network/vpn/plasmanetworkmanagement_libreswanui.so
%{_desktopdir}/kcm_networkmanagement.desktop

%{_libdir}/qt6/qml/org/kde/plasma/networkmanagement/kde-qmlmodule.version
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/plasma/networkmanagement/libplasmanm_internalplugin.so
%{_libdir}/qt6/qml/org/kde/plasma/networkmanagement/plasmanm_internal.qmltypes
%{_datadir}/knotifications6/networkmanagement.notifyrc
%{_datadir}/qlogging-categories6/plasma-nm.categories
%{_desktopdir}/org.kde.vpnimport.desktop
