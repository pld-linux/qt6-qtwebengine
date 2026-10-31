#
# TODO:
#	- clenup BRs post split from qt6.spec
#
# Conditional build:
# -- build targets
%bcond_without	doc				# Documentation
# -- SIMD CPU instructions
%bcond_with	sse2				# use SSE2 instructions
%bcond_with	sse3				# use SSE3 instructions (since: Intel middle Pentium4, AMD Athlon64)
%bcond_with	ssse3				# use SSSE3 instructions (Intel since Core2, Via Nano)
%bcond_with	sse41				# use SSE4.1 instructions (Intel since middle Core2)
%bcond_with	sse42				# use SSE4.2 instructions (the same)
%bcond_with	avx				# use AVX instructions (Intel since Sandy Bridge, AMD since Bulldozer)
%bcond_with	avx2				# use AVX2 instructions (Intel since Haswell)
# -- system libraries
%bcond_without	system_ffmpeg	# use system FFmpeg
%bcond_without	system_libvpx	# use system libvpx (build fails QTBUG-129955)
# -- build system
%bcond_without	samurai				# use ninja instead of samurai

%define		orgname		qtwebengine
%define		base_version	6.11

%ifarch	athlon
%define		with_3dnow	1
%endif
%ifarch athlon pentium3 pentium4 %{x8664} x32
%define		with_mmx	1
%endif
%ifarch pentium4 %{x8664} x32
%define		with_sse2	1
%endif
# QTBUG-36129
%ifnarch %{arm} aarch64
%define		with_red_reloc	1
%endif
%ifarch %{x86_with_sse} %{arm_with_neon}
%define		with_simd	1
%endif
%define		specflags	%{!?with_simd:-DDISABLE_SIMD -DPFFFT_SIMD_DISABLE}

# cmake autogen (moc/uic/rcc) spawns many threads per job; on high-core
# machines this exhausts RLIMIT_NPROC and aborts the build. Cap to 16.
%define		_smp_ncpus_max	16

%define		icu_abi		78
%define		next_icu_abi	%(echo $((%{icu_abi} + 1)))

Summary:	The Qt6 WebEngine library
Summary(pl.UTF-8):	Biblioteka Qt6 WebEngine
Name:		qt6-%{orgname}
Version:	%{base_version}.2
Release:	5
License:	LGPL v3 or GPL v2 or GPL v3 or commercial
Group:		X11/Libraries
Source0:	https://download.qt.io/official_releases/qt/%{base_version}/%{version}/submodules/%{orgname}-everywhere-src-%{version}.tar.xz
# Source0-md5:	a33984478c690295f2b7a3d153c5772d
Patch1:		ninja-program.patch
Patch2:		arm-no-xnnpack.patch
Patch3:		chromium-107-proprietary-codecs.patch
Patch4:		chromium-112-ffmpeg-first_dts.patch
Patch5:		qtwebengine-cmake-build-type.patch
Patch9:		header-dep.patch
Patch10:	qtwebengine-v8-gc.patch
URL:		https://www.qt.io/
BuildRequires:	EGL-devel
BuildRequires:	GConf2-devel
BuildRequires:	Mesa-libgbm-devel
BuildRequires:	OpenGL-devel
BuildRequires:	Qt6Core-devel = %{version}
BuildRequires:	Qt6Gui-devel = %{version}
BuildRequires:	Qt6Network-devel = %{version}
BuildRequires:	Qt6Qml-devel = %{version}
BuildRequires:	Qt6Quick-devel = %{version}
BuildRequires:	Qt6WebChannel-devel = %{version}
BuildRequires:	Vulkan-Loader-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	at-spi2-core-devel
BuildRequires:	bison
BuildRequires:	bluez-libs-devel
# qdoc
BuildRequires:	clang-devel
BuildRequires:	cmake >= 3.22
BuildRequires:	dbus-devel >= 1.2
BuildRequires:	double-conversion-devel
BuildRequires:	ffmpeg-devel
%if %{with system_ffmpeg}
BuildRequires:	ffmpeg-devel >= 6.0
%endif
BuildRequires:	flex
BuildRequires:	flite-devel
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 2.2.0
BuildRequires:	gdb
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	glibc-headers >= 6:2.16
BuildRequires:	gperf
BuildRequires:	grpc-devel
BuildRequires:	gstreamer-devel >= 1.0
BuildRequires:	gstreamer-gl-devel >= 1.0
BuildRequires:	gstreamer-plugins-bad-devel >= 1.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0
BuildRequires:	gypsy-devel
BuildRequires:	harfbuzz-devel >= 4.3.0
BuildRequires:	harfbuzz-subset-devel >= 4.3.0
BuildRequires:	hunspell-devel
BuildRequires:	jasper-devel
BuildRequires:	khrplatform-devel
BuildRequires:	lcms2-devel
BuildRequires:	libb2-devel
BuildRequires:	libdrm-devel
# see dependency on libicu version below
BuildRequires:	libicu-devel < %{next_icu_abi}
BuildRequires:	libicu-devel >= %{icu_abi}
BuildRequires:	libjpeg-devel
BuildRequires:	libmng-devel
BuildRequires:	libpng-devel >= 2:1.6.0
BuildRequires:	libstdc++-devel >= 6:10
BuildRequires:	libtiff-devel >= 4.5.0
BuildRequires:	liburing-devel
BuildRequires:	libva-devel
%{?with_system_libvpx:BuildRequires:	libvpx-devel >= 1.10.0}
BuildRequires:	libwebp-devel
BuildRequires:	libxcb-devel >= 1.12
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	minizip-devel
BuildRequires:	mtdev-devel
%{!?with_samurai:BuildRequires:	ninja >= 1.7.2}
BuildRequires:	nodejs >= 20.0
BuildRequires:	nss-devel >= 3.26
BuildRequires:	openjpeg2-devel
BuildRequires:	openssl-devel >= 1.1.1
BuildRequires:	opus-devel >= 1.3.1
BuildRequires:	pciutils-devel
BuildRequires:	pcre2-16-devel >= 10.20
BuildRequires:	pcsc-lite-devel
BuildRequires:	pipewire-devel >= 0.3
BuildRequires:	pkgconfig
BuildRequires:	poppler-cpp-devel
BuildRequires:	protobuf-c-devel
BuildRequires:	protobuf-devel
BuildRequires:	pulseaudio-devel
BuildRequires:	python3 >= 1:3.8
BuildRequires:	python3-devel-tools
BuildRequires:	python3-html5lib
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	qt6-assistant
BuildRequires:	qt6-doc-common
BuildRequires:	re2-devel >=  20230601
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.047
%{?with_samurai:BuildRequires:	samurai}
BuildRequires:	sed >= 4.0
BuildRequires:	snappy-devel
BuildRequires:	speech-dispatcher-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel
BuildRequires:	wayland-devel >= 1.15
BuildRequires:	xcb-util-cursor-devel >= 0.1.1
BuildRequires:	xcb-util-devel >= 0.1.1
BuildRequires:	xcb-util-image-devel >= 0.3.9
BuildRequires:	xcb-util-keysyms-devel >= 0.3.9
BuildRequires:	xcb-util-renderutil-devel >= 0.3.9
BuildRequires:	xcb-util-wm-devel >= 0.3.9
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXcomposite-devel
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXrender-devel >= 0.6
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xorg-lib-libxkbcommon-devel >= 0.9.0
BuildRequires:	xorg-lib-libxkbcommon-x11-devel >= 0.9.0
BuildRequires:	xorg-lib-libxkbfile-devel
BuildRequires:	xorg-lib-libxshmfence-devel
BuildRequires:	xorg-proto-glproto-devel
BuildRequires:	xz
BuildRequires:	zlib-devel >= 1.0.8
BuildRequires:	zstd-devel >= 1.3
ExclusiveArch:	%{x8664} aarch64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages	0

%define		filterout	-flto

%define		qt6dir		%{_libdir}/qt6

%description
Qt6 WebEngine library provides seamless integration of C++ and QML
applications with HTML/JavaScript clients.

%description -l pl.UTF-8
Biblioteka Qt6 WebEngine udostępnia integrację aplikacji C++ i QML z
klientami w HTML-u/JavaScripcie.

%package -n Qt6WebEngine
Summary:	The Qt6 WebEngine library
Summary(pl.UTF-8):	Biblioteka Qt6 WebEngine
Group:		Libraries
%requires_ge_to	Qt6Core Qt6Core-devel
%requires_ge_to	Qt6Gui Qt6Gui-devel
%requires_ge_to	Qt6Network Qt6Network-devel
%requires_ge_to	Qt6Qml Qt6Qml-devel
%requires_ge_to	Qt6Quick Qt6Quick-devel
%requires_ge_to	Qt6WebChannel Qt6WebChannel-devel
Requires:	alsa-lib >= 1.0.10
Requires:	freetype >= 1:2.4.2
Requires:	harfbuzz >= 3.0.0
Requires:	harfbuzz-subset >= 3.0.0
%requires_ge_to	libicu libicu-devel
Requires:	libpng >= 2:1.6.0
Requires:	libtiff >= 4.5.0
%{?with_system_libvpx:Requires:	libvpx >= 1.10.0}
Requires:	nss >= 3.26
Requires:	opus >= 1.3.1
Requires:	pulseaudio-libs >= 0.9.10
Requires:	re2 >=  20230601

%description -n Qt6WebEngine
Qt6 WebEngine library provides seamless integration of C++ and QML
applications with HTML/JavaScript clients.

%description -n Qt6WebEngine -l pl.UTF-8
Biblioteka Qt6 WebEngine udostępnia integrację aplikacji C++ i QML z
klientami w HTML-u/JavaScripcie.

%package -n Qt6WebEngine-devel
Summary:	Qt6 WebEngine library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 WebEngine - pliki programistyczne
Group:		Development/Libraries
%requires_ge_to	Qt6Core-devel Qt6Core-devel-devel
%requires_ge_to	Qt6Gui-devel Qt6Gui-devel-devel
%requires_ge_to	Qt6Network-devel Qt6Network-devel-devel
%requires_ge_to	Qt6PrintSupport-devel Qt6PrintSupport-devel-devel
%requires_ge_to	Qt6Qml-devel Qt6Qml-devel-devel
%requires_ge_to	Qt6Quick-devel Qt6Quick-devel-devel
%requires_ge_to	Qt6WebChannel-devel Qt6WebChannel-devel-devel
%requires_ge_to	Qt6Widgets-devel Qt6Widgets-devel-devel
Requires:	Qt6WebEngine = %{version}

%description -n Qt6WebEngine-devel
Qt6 WebEngine library - development files.

%description -n Qt6WebEngine-devel -l pl.UTF-8
Biblioteka Qt6 WebEngine - pliki programistyczne.

%package -n Qt6WebEngine-doc
Summary:	Qt6 WebEngine documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 WebEngine w formacie HTML
License:	FDL v1.3
Group:		Documentation
%requires_ge	qt6-doc-common
BuildArch:	noarch

%description -n Qt6WebEngine-doc
Qt6 WebEngine documentation in HTML format.

%description -n Qt6WebEngine-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 WebEngine w formacie HTML.

%package -n Qt6WebEngine-doc-qch
Summary:	Qt6 WebEngine documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 WebEngine w formacie QCH
License:	FDL v1.3
Group:		Documentation
%requires_ge	qt6-doc-common
BuildArch:	noarch

%description -n Qt6WebEngine-doc-qch
Qt6 WebEngine documentation in QCH format.

%description -n Qt6WebEngine-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 WebEngine w formacie QCH.

%package -n Qt6Designer-plugin-qwebengineview
Summary:	QWebEngineView plugin for Qt6 Designer
Summary(pl.UTF-8):	Wtyczka QWebEngineView dla Qt6 Designera
Group:		X11/Libraries
%requires_ge_to	Qt6Core Qt6Core-devel
%requires_ge_to	Qt6Designer Qt6Designer-devel
%requires_ge_to	Qt6Gui Qt6Gui-devel
%requires_ge_to	Qt6Widgets Qt6Widgets-devel
Requires:	Qt6WebEngine = %{version}

%description -n Qt6Designer-plugin-qwebengineview
QWebEngineView plugin for Qt6 Designer.

%description -n Qt6Designer-plugin-qwebengineview -l pl.UTF-8
Wtyczka QWebEngineView dla Qt6 Designera.

%package -n Qt6WebView-plugin-webengine
Summary:	Qt6 WebView library WebEngine plugin
Summary(pl.UTF-8):	Wtyczka WebEngine do biblioteki Qt6 WebView
Group:		X11/Libraries
%requires_ge_to	Qt6WebView Qt6WebView-devel
Requires:	Qt6WebEngine = %{version}

%description -n Qt6WebView-plugin-webengine
Qt6 WebView library WebEngine plugin.

%description -n Qt6WebView-plugin-webengine -l pl.UTF-8
Wtyczka WebEngine do biblioteki Qt6 WebView.

%package -n Qt6Pdf
Summary:	The Qt6 Pdf library
Summary(pl.UTF-8):	Biblioteka Qt6 Pdf
Group:		Libraries
%requires_ge_to	Qt6Core Qt6Core-devel
%requires_ge_to	Qt6Gui Qt6Gui-devel
%requires_ge_to	Qt6Network Qt6Network-devel
%requires_ge_to	Qt6Qml Qt6Qml-devel
%requires_ge_to	Qt6Quick Qt6Quick-devel
%requires_ge_to	Qt6Widgets Qt6Widgets-devel

%description -n Qt6Pdf
Qt6 Pdf module contains classes and functions for rendering PDF
documents.

%description -n Qt6Pdf -l pl.UTF-8
Moduł Qt6 Pdf zawiera klasy i funkcje do renderowania dokumentów PDF.

%package -n Qt6Pdf-devel
Summary:	Qt6 Pdf library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Pdf - pliki programistyczne
Group:		Development/Libraries
%requires_ge_to	Qt6Core-devel Qt6Core-devel-devel
%requires_ge_to	Qt6Gui-devel Qt6Gui-devel-devel
%requires_ge_to	Qt6Widgets-devel Qt6Widgets-devel-devel
Requires:	Qt6Pdf = %{version}

%description -n Qt6Pdf-devel
Qt6 Pdf library - development files.

%description -n Qt6Pdf-devel -l pl.UTF-8
Biblioteka Qt6 Pdf - pliki programistyczne.

%package -n Qt6Pdf-doc
Summary:	Qt6 Pdf documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Pdf w formacie HTML
License:	FDL v1.3
Group:		Documentation
%requires_ge	qt6-doc-common
BuildArch:	noarch

%description -n Qt6Pdf-doc
Qt6 Pdf documentation in HTML format.

%description -n Qt6Pdf-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Pdf w formacie HTML.

%package -n Qt6Pdf-doc-qch
Summary:	Qt6 Pdf documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Pdf w formacie QCH
License:	FDL v1.3
Group:		Documentation
%requires_ge	qt6-doc-common
BuildArch:	noarch

%description -n Qt6Pdf-doc-qch
Qt6 Pdf documentation in QCH format.

%description -n Qt6Pdf-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Pdf w formacie QCH.

%prep
%setup -q -n %{orgname}-everywhere-src-%{version}
%patch -P1 -p2
%patch -P2 -p1
%patch -P3 -p1 -d src/3rdparty/chromium
%patch -P4 -p1 -d src/3rdparty/chromium
%patch -P5 -p2
%patch -P9 -p1
%patch -P10 -p1 -d src/3rdparty

%if %(echo %{cxx_version} | cut -d. -f1) < 9
# available since gcc 9
%{__sed} -i -e '/-Wdeprecated-copy/d' \
	qtwebengine/src/3rdparty/chromium/third_party/{angle,dawn/src/common,pdfium,skia/gn/skia}/BUILD.gn \
	qtwebengine/src/3rdparty/chromium/third_party/swiftshader/CMakeLists.txt
%endif

%build
# We're using samurai instead of ninja because the latter
# cannot be told what command line flags to use globally
%cmake -B build \
	-GNinja \
	-DBUILD_SHARED_LIBS=ON \
	-DBUILD_WITH_PCH=%{__ON_OFF pch} \
	%{?with_samurai:-DCMAKE_MAKE_PROGRAM:FILEPATH=/usr/bin/samu} \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DINSTALL_ARCHDATADIR=%{qt6dir} \
	-DINSTALL_BINDIR=%{qt6dir}/bin \
	-DINSTALL_LIBDIR=%{_libdir} \
	-DINSTALL_LIBEXECDIR=%{qt6dir}/libexec \
	-DINSTALL_DATADIR=%{_datadir}/qt6 \
	-DINSTALL_DOCDIR=%{_docdir}/qt6-doc \
	-DINSTALL_INCLUDEDIR=%{_includedir}/qt6 \
	-DINSTALL_EXAMPLESDIR=%{_examplesdir}/qt6 \
	-DINSTALL_MKSPECSDIR=%{qt6dir}/mkspecs \
	-DINSTALL_PLUGINSDIR=%{qt6dir}/plugins \
	-DINSTALL_QMLDIR=%{qt6dir}/qml \
	-DINSTALL_SYSCONFDIR=%{_sysconfdir}/qt6 \
	-DINSTALL_TRANSLATIONSDIR=%{_datadir}/qt6/translations \
	%{?with_samurai:-DNinja_EXECUTABLE:FILEPATH=/usr/bin/samu} \
	-DQT_BUILD_EXAMPLES=OFF \
	-DQT_DISABLE_RPATH=TRUE \
	-DQT_FEATURE_accessibility=ON \
	-DQT_FEATURE_avx2=%{__ON_OFF avx2} \
	-DQT_FEATURE_avx=%{__ON_OFF avx} \
	-DQT_FEATURE_cups=%{__ON_OFF cups} \
	-DQT_FEATURE_dbus_linked=ON \
	-DQT_FEATURE_directfb=%{__ON_OFF directfb} \
	-DQT_FEATURE_eglfs=%{__ON_OFF egl} \
	-DQT_FEATURE_enable_new_dtags=ON \
	-DQT_FEATURE_fontconfig=ON \
	-DQT_FEATURE_glib=ON \
	-DQT_FEATURE_gtk3=%{__ON_OFF gtk} \
	-DQT_FEATURE_icu=ON \
	-DQT_FEATURE_journald=%{__ON_OFF systemd} \
	-DQT_FEATURE_kms=%{__ON_OFF kms} \
	-DQT_FEATURE_libinput=%{__ON_OFF libinput} \
	-DQT_FEATURE_opengles2=%{__ON_OFF gles} \
	-DQT_FEATURE_openssl_linked=ON \
	-DQT_FEATURE_qml_jit=%{__ON_OFF qml_jit} \
	-DQT_FEATURE_reduce_relocations=%{__ON_OFF red_reloc} \
	-DQT_FEATURE_relocatable=OFF \
	-DQT_FEATURE_rpath=OFF \
	-DQT_FEATURE_separate_debug_info=OFF \
	-DQT_FEATURE_sse2=%{__ON_OFF sse2} \
	-DQT_FEATURE_sse3=%{__ON_OFF sse3} \
	-DQT_FEATURE_sse4_1=%{__ON_OFF sse41} \
	-DQT_FEATURE_sse4_2=%{__ON_OFF sse42} \
	-DQT_FEATURE_ssse3=%{__ON_OFF ssse3} \
	-DQT_FEATURE_system_doubleconversion=ON \
	-DQT_FEATURE_system_freetype=ON \
	-DQT_FEATURE_system_harfbuzz=ON \
	-DQT_FEATURE_system_jpeg=ON \
	-DQT_FEATURE_system_pcre2=ON \
	-DQT_FEATURE_system_png=ON \
	-DQT_FEATURE_system_zlib=ON \
	-DQT_FEATURE_tslib=%{__ON_OFF tslib} \
	-DQT_FEATURE_use_gold_linker=ON \
	-DQT_FEATURE_webengine_proprietary_codecs=ON \
	-DQT_FEATURE_webengine_system_alsa=ON \
	-DQT_FEATURE_webengine_system_ffmpeg=%{__ON_OFF system_ffmpeg} \
	-DQT_FEATURE_webengine_system_freetype=ON \
	-DQT_FEATURE_webengine_system_glib=ON \
	-DQT_FEATURE_webengine_system_harfbuzz=ON \
	-DQT_FEATURE_webengine_system_icu=ON \
	-DQT_FEATURE_webengine_system_lcms2=ON \
	-DQT_FEATURE_webengine_system_libjpeg=ON \
	-DQT_FEATURE_webengine_system_libopenjpeg2=ON \
	-DQT_FEATURE_webengine_system_libpci=ON \
	-DQT_FEATURE_webengine_system_libpng=ON \
	-DQT_FEATURE_webengine_system_libtiff=ON \
	-DQT_FEATURE_webengine_system_libvpx=%{__ON_OFF system_libvpx} \
	-DQT_FEATURE_webengine_system_libwebp=ON \
	-DQT_FEATURE_webengine_system_libxml=ON \
	-DQT_FEATURE_webengine_system_minizip=ON \
	-DQT_FEATURE_webengine_system_opus=ON \
	-DQT_FEATURE_webengine_system_pulseaudio=ON \
	-DQT_FEATURE_webengine_system_re2=ON \
	-DQT_FEATURE_webengine_system_snappy=ON \
	-DQT_FEATURE_webengine_system_zlib=ON \
	-DQT_FEATURE_xcb=ON \
	-DQT_FEATURE_xcb_sm=ON \
	-DQT_FEATURE_xkbcommon=ON \
	-DQT_GENERATE_SBOM:BOOL=OFF

# Make sure arg-less sub-invocations will follow our parallel build setting
export CMAKE_BUILD_PARALLEL_LEVEL="%__jobs"
%{?with_samurai:export SAMUFLAGS="%{_smp_mflags}"}
export VERBOSE=1
export CFLAGS="%{rpmcflags}"
export CXXFLAGS="%{rpmcxxflags}"
export LDFLAGS="%{rpmldflags}"

%{__cmake} --build build --verbose %{_smp_mflags}

%if %{with doc}
%{__cmake} --build build --target docs --verbose %{_smp_mflags}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/qt6,%{_bindir},%{_pkgconfigdir},%{qt6dir}/libexec}

# for QtSolutions (qtlockedfile, qtsingleapplication, etc)
install -d $RPM_BUILD_ROOT%{_includedir}/qt6/QtSolutions

DESTDIR=$RPM_BUILD_ROOT %{__cmake} --install build/

%if %{with doc}
DESTDIR=$RPM_BUILD_ROOT %{__cmake} --build build/ --target install_docs
%endif

# we have system gn package, available on all archs
%{__rm} $RPM_BUILD_ROOT%{qt6dir}/libexec/gn

# kill unnecessary -L%{_libdir} from *.prl, *.pc
%{__sed} -i -e "s,-L%{_libdir} \?,,g" \
	$RPM_BUILD_ROOT%{_libdir}/*.prl \
	$RPM_BUILD_ROOT%{_pkgconfigdir}/*.pc

# find_lang --with-qm supports only PLD qt3/qt4 specific %{_localedir}/*/LC_MESSAGES layout
find_qt6_qm()
{
	name="$1"
	find $RPM_BUILD_ROOT%{_datadir}/qt6/translations -name "${name}_*.qm" | \
		sed -e "s:^$RPM_BUILD_ROOT::" \
		    -ne 's:\(.*/'$name'_\)\([a-z][a-z][a-z]\?\)\(_[A-Z][A-Z]\)\?\(\.qm\)$:%lang(\2\3) \1\2\3\4:p'
}

echo '%defattr(644,root,root,755)' > qtwebengine.lang
%if %{with doc}
find_qt6_qm qtwebengine >> qtwebengine.lang
%endif

install -d $RPM_BUILD_ROOT%{qt6dir}/plugins/styles

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt6WebEngine -p /sbin/ldconfig
%postun	-n Qt6WebEngine -p /sbin/ldconfig

%post	-n Qt6Pdf -p /sbin/ldconfig
%postun	-n Qt6Pdf -p /sbin/ldconfig

%files -n Qt6WebEngine -f qtwebengine.lang
%defattr(644,root,root,755)
%{_libdir}/libQt6WebEngineCore.so.*.*.*
%ghost %{_libdir}/libQt6WebEngineCore.so.6
%{_libdir}/libQt6WebEngineQuick.so.*.*.*
%ghost %{_libdir}/libQt6WebEngineQuick.so.6
%{_libdir}/libQt6WebEngineQuickDelegatesQml.so.*.*.*
%ghost %{_libdir}/libQt6WebEngineQuickDelegatesQml.so.6
%{_libdir}/libQt6WebEngineWidgets.so.*.*.*
%ghost %{_libdir}/libQt6WebEngineWidgets.so.6
%dir %{qt6dir}/qml/QtWebEngine
%{qt6dir}/qml/QtWebEngine/plugins.qmltypes
%{qt6dir}/qml/QtWebEngine/qmldir
%{qt6dir}/qml/QtWebEngine/ControlsDelegates
%{qt6dir}/qml/QtWebEngine/libqtwebenginequickplugin.so
%dir %{_datadir}/qt6/resources
%{_datadir}/qt6/resources/qtwebengine*.pak
%{_datadir}/qt6/resources/v8_context_snapshot.bin
%dir %{_datadir}/qt6/translations/qtwebengine_locales
%lang(am) %{_datadir}/qt6/translations/qtwebengine_locales/am.pak
%lang(ar) %{_datadir}/qt6/translations/qtwebengine_locales/ar.pak
%lang(bg) %{_datadir}/qt6/translations/qtwebengine_locales/bg.pak
%lang(bn) %{_datadir}/qt6/translations/qtwebengine_locales/bn.pak
%lang(ca) %{_datadir}/qt6/translations/qtwebengine_locales/ca.pak
%lang(cs) %{_datadir}/qt6/translations/qtwebengine_locales/cs.pak
%lang(da) %{_datadir}/qt6/translations/qtwebengine_locales/da.pak
%lang(de) %{_datadir}/qt6/translations/qtwebengine_locales/de.pak
%lang(el) %{_datadir}/qt6/translations/qtwebengine_locales/el.pak
%lang(en) %{_datadir}/qt6/translations/qtwebengine_locales/en-GB.pak
%lang(en) %{_datadir}/qt6/translations/qtwebengine_locales/en-US.pak
%lang(es) %{_datadir}/qt6/translations/qtwebengine_locales/es.pak
%lang(es_AR,es_BO,es_CL,es_CO,es_CR,es_CU,es_DO,es_EC,es_GT,es_HN,es_MX,es_NI,es_PA,es_PE,es_PR,es_PY,es_SV,es_UY,es_VE) %{_datadir}/qt6/translations/qtwebengine_locales/es-419.pak
%lang(et) %{_datadir}/qt6/translations/qtwebengine_locales/et.pak
%lang(fa) %{_datadir}/qt6/translations/qtwebengine_locales/fa.pak
%lang(fi) %{_datadir}/qt6/translations/qtwebengine_locales/fi.pak
%lang(fil) %{_datadir}/qt6/translations/qtwebengine_locales/fil.pak
%lang(fr) %{_datadir}/qt6/translations/qtwebengine_locales/fr.pak
%lang(gu) %{_datadir}/qt6/translations/qtwebengine_locales/gu.pak
%lang(he) %{_datadir}/qt6/translations/qtwebengine_locales/he.pak
%lang(hi) %{_datadir}/qt6/translations/qtwebengine_locales/hi.pak
%lang(hr) %{_datadir}/qt6/translations/qtwebengine_locales/hr.pak
%lang(hu) %{_datadir}/qt6/translations/qtwebengine_locales/hu.pak
%lang(id) %{_datadir}/qt6/translations/qtwebengine_locales/id.pak
%lang(it) %{_datadir}/qt6/translations/qtwebengine_locales/it.pak
%lang(ja) %{_datadir}/qt6/translations/qtwebengine_locales/ja.pak
%lang(kn) %{_datadir}/qt6/translations/qtwebengine_locales/kn.pak
%lang(ko) %{_datadir}/qt6/translations/qtwebengine_locales/ko.pak
%lang(lt) %{_datadir}/qt6/translations/qtwebengine_locales/lt.pak
%lang(lv) %{_datadir}/qt6/translations/qtwebengine_locales/lv.pak
%lang(ml) %{_datadir}/qt6/translations/qtwebengine_locales/ml.pak
%lang(mr) %{_datadir}/qt6/translations/qtwebengine_locales/mr.pak
%lang(ms) %{_datadir}/qt6/translations/qtwebengine_locales/ms.pak
%lang(nb) %{_datadir}/qt6/translations/qtwebengine_locales/nb.pak
%lang(nl) %{_datadir}/qt6/translations/qtwebengine_locales/nl.pak
%lang(pl) %{_datadir}/qt6/translations/qtwebengine_locales/pl.pak
%lang(pt_BR) %{_datadir}/qt6/translations/qtwebengine_locales/pt-BR.pak
%lang(pt) %{_datadir}/qt6/translations/qtwebengine_locales/pt-PT.pak
%lang(ro) %{_datadir}/qt6/translations/qtwebengine_locales/ro.pak
%lang(ru) %{_datadir}/qt6/translations/qtwebengine_locales/ru.pak
%lang(sk) %{_datadir}/qt6/translations/qtwebengine_locales/sk.pak
%lang(sl) %{_datadir}/qt6/translations/qtwebengine_locales/sl.pak
%lang(sr) %{_datadir}/qt6/translations/qtwebengine_locales/sr.pak
%lang(sv) %{_datadir}/qt6/translations/qtwebengine_locales/sv.pak
%lang(sw) %{_datadir}/qt6/translations/qtwebengine_locales/sw.pak
%lang(ta) %{_datadir}/qt6/translations/qtwebengine_locales/ta.pak
%lang(te) %{_datadir}/qt6/translations/qtwebengine_locales/te.pak
%lang(th) %{_datadir}/qt6/translations/qtwebengine_locales/th.pak
%lang(tr) %{_datadir}/qt6/translations/qtwebengine_locales/tr.pak
%lang(uk) %{_datadir}/qt6/translations/qtwebengine_locales/uk.pak
%lang(vi) %{_datadir}/qt6/translations/qtwebengine_locales/vi.pak
%lang(zh_CN) %{_datadir}/qt6/translations/qtwebengine_locales/zh-CN.pak
%lang(zh_TW) %{_datadir}/qt6/translations/qtwebengine_locales/zh-TW.pak
%attr(755,root,root) %{_libdir}/qt6/libexec/QtWebEngineProcess
%attr(755,root,root) %{_libdir}/qt6/libexec/qwebengine_convert_dict
%attr(755,root,root) %{_libdir}/qt6/libexec/webenginedriver

%files -n Qt6WebEngine-devel
%defattr(644,root,root,755)
%{_libdir}/libQt6WebEngineCore.so
%{_libdir}/libQt6WebEngineQuick.so
%{_libdir}/libQt6WebEngineQuickDelegatesQml.so
%{_libdir}/libQt6WebEngineWidgets.so
%{_libdir}/libQt6WebEngineCore.prl
%{_libdir}/libQt6WebEngineQuick.prl
%{_libdir}/libQt6WebEngineQuickDelegatesQml.prl
%{_libdir}/libQt6WebEngineWidgets.prl
%{_includedir}/qt6/QtWebEngineCore
%{_includedir}/qt6/QtWebEngineQuick
%{_includedir}/qt6/QtWebEngineWidgets
%{_pkgconfigdir}/Qt6WebEngineCore.pc
%{_pkgconfigdir}/Qt6WebEngineQuick.pc
%{_pkgconfigdir}/Qt6WebEngineQuickDelegatesQml.pc
%{_pkgconfigdir}/Qt6WebEngineWidgets.pc
%{_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtWebEngineTestsConfig.cmake
%{_libdir}/cmake/Qt6Qml/QmlPlugins/Qt6qtwebenginequick*.cmake
%{_libdir}/cmake/Qt6WebEngineCore
%{_libdir}/cmake/Qt6WebEngineCorePrivate
%{_libdir}/cmake/Qt6WebEngineCoreTools
%{_libdir}/cmake/Qt6WebEngineQuick
%{_libdir}/cmake/Qt6WebEngineQuickPrivate
%{_libdir}/cmake/Qt6WebEngineQuickDelegatesQml
%{_libdir}/cmake/Qt6WebEngineWidgets
%{_libdir}/cmake/Qt6WebEngineWidgetsPrivate
%{qt6dir}/metatypes/qt6webenginecore_metatypes.json
%{qt6dir}/metatypes/qt6webenginequick_metatypes.json
%{qt6dir}/metatypes/qt6webenginequickdelegatesqml_metatypes.json
%{qt6dir}/metatypes/qt6webenginewidgets_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_webenginecore.pri
%{qt6dir}/mkspecs/modules/qt_lib_webenginecore_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_webenginequickdelegatesqml.pri
%{qt6dir}/mkspecs/modules/qt_lib_webenginequick.pri
%{qt6dir}/mkspecs/modules/qt_lib_webenginequick_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_webenginewidgets.pri
%{qt6dir}/mkspecs/modules/qt_lib_webenginewidgets_private.pri
%{qt6dir}/modules/WebEngineCore.json
%{qt6dir}/modules/WebEngineQuick.json
%{qt6dir}/modules/WebEngineQuickDelegatesQml.json
%{qt6dir}/modules/WebEngineWidgets.json

%if %{with doc}
%files -n Qt6WebEngine-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtwebengine

%files -n Qt6WebEngine-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtwebengine.qch
%endif

%files -n Qt6Designer-plugin-qwebengineview
%defattr(644,root,root,755)
%{_libdir}/qt6/plugins/designer/libqwebengineview.so
%{_libdir}/cmake/Qt6Designer/Qt6QWebEngineViewPlugin*.cmake

# webengine will include this
%if 0
%files -n Qt6WebView-plugin-webengine
%defattr(644,root,root,755)
%{qt6dir}/plugins/webview/libqtwebview_webengine.so
%{_libdir}/cmake/Qt6WebView/Qt6QWebEngineWebViewPlugin*.cmake
%endif

%files -n Qt6Pdf
%defattr(644,root,root,755)
%{_libdir}/libQt6Pdf.so.*.*.*
%ghost %{_libdir}/libQt6Pdf.so.6
%{_libdir}/libQt6PdfQuick.so.*.*.*
%ghost %{_libdir}/libQt6PdfQuick.so.6
%{_libdir}/libQt6PdfWidgets.so.*.*.*
%ghost %{_libdir}/libQt6PdfWidgets.so.6
%dir %{qt6dir}/qml/QtQuick/Pdf
%{qt6dir}/qml/QtQuick/Pdf/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Pdf/qmldir
%{qt6dir}/qml/QtQuick/Pdf/*.qml
%{qt6dir}/qml/QtQuick/Pdf/libpdfquickplugin.so
%dir %{qt6dir}/qml/QtQuick/Pdf/+Material
%{qt6dir}/qml/QtQuick/Pdf/+Material/*.qml
%dir %{qt6dir}/qml/QtQuick/Pdf/+Universal
%{qt6dir}/qml/QtQuick/Pdf/+Universal/*.qml
%{_libdir}/qt6/plugins/imageformats/libqpdf.so

%files -n Qt6Pdf-devel
%defattr(644,root,root,755)
%{_libdir}/libQt6Pdf.so
%{_libdir}/libQt6PdfQuick.so
%{_libdir}/libQt6PdfWidgets.so
%{_libdir}/libQt6Pdf.prl
%{_libdir}/libQt6PdfQuick.prl
%{_libdir}/libQt6PdfWidgets.prl
%{_includedir}/qt6/QtPdf
%{_includedir}/qt6/QtPdfQuick
%{_includedir}/qt6/QtPdfWidgets
%{_pkgconfigdir}/Qt6Pdf.pc
%{_pkgconfigdir}/Qt6PdfQuick.pc
%{_pkgconfigdir}/Qt6PdfWidgets.pc
%{_libdir}/cmake/Qt6Gui/Qt6QPdfPlugin*.cmake
%{_libdir}/cmake/Qt6Qml/QmlPlugins/Qt6PdfQuickplugin*.cmake
%{_libdir}/cmake/Qt6Pdf
%{_libdir}/cmake/Qt6PdfPrivate
%{_libdir}/cmake/Qt6PdfQuick
%{_libdir}/cmake/Qt6PdfQuickPrivate
%{_libdir}/cmake/Qt6PdfWidgets
%{_libdir}/cmake/Qt6PdfWidgetsPrivate
%{qt6dir}/mkspecs/modules/qt_lib_pdf.pri
%{qt6dir}/mkspecs/modules/qt_lib_pdf_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_pdfquick.pri
%{qt6dir}/mkspecs/modules/qt_lib_pdfquick_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_pdfwidgets.pri
%{qt6dir}/mkspecs/modules/qt_lib_pdfwidgets_private.pri
%{qt6dir}/modules/Pdf.json
%{qt6dir}/modules/PdfQuick.json
%{qt6dir}/modules/PdfWidgets.json
%{qt6dir}/metatypes/qt6pdf_metatypes.json
%{qt6dir}/metatypes/qt6pdfquick_metatypes.json
%{qt6dir}/metatypes/qt6pdfwidgets_metatypes.json

%if %{with doc}
%files -n Qt6Pdf-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtpdf

%files -n Qt6Pdf-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtpdf.qch
%endif
