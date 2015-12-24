%define pkgname RMagick
Summary:	Graphics Processing library for Ruby
Summary(pl.UTF-8):	Biblioteka przetwarzania grafiki dla Ruby
Name:		ruby-%{pkgname}
Version:	2.13.4
Release:	3
License:	Ruby-alike
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/rmagick-%{version}.gem
# Source0-md5:	2be71aebd8050fdc0c09ae33a8590af7
Patch0:		format-security.patch
Patch1:		rubygems.patch
Patch2:		disable-hanging-handler.patch
Patch3:		disable-tests.patch
URL:		https://github.com/gemhome/rmagick
BuildRequires:	ImageMagick-coder-dot
BuildRequires:	ImageMagick-coder-fpx
BuildRequires:	ImageMagick-coder-jbig
BuildRequires:	ImageMagick-coder-jpeg
BuildRequires:	ImageMagick-coder-jpeg2
BuildRequires:	ImageMagick-coder-miff
BuildRequires:	ImageMagick-coder-mpr
BuildRequires:	ImageMagick-coder-pdf
BuildRequires:	ImageMagick-coder-png
BuildRequires:	ImageMagick-coder-ps2
BuildRequires:	ImageMagick-coder-svg
BuildRequires:	ImageMagick-coder-tiff
BuildRequires:	ImageMagick-coder-url
BuildRequires:	ImageMagick-coder-wmf
BuildRequires:	ImageMagick-devel >= 1:6.7.0.7-2
BuildRequires:	rpmbuild(macros) >= 1.484
BuildRequires:	ruby >= 1:1.8.6
BuildRequires:	ruby-devel
BuildRequires:	ruby-modules
BuildRequires:	ruby-rake
BuildRequires:	ruby-rake-compiler
BuildRequires:	ruby-rdoc
BuildConflicts:	ruby-RMagick < 1.7.2
%requires_eq_to	ImageMagick-libs ImageMagick-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An interface to the ImageMagick and GraphicsMagick image processing
libraries. Supports more than 80 image formats, including GIF, JPEG,
PNG. Includes 2D drawing API. Comprehensive HTML documentation.

%description -l pl.UTF-8
Jest to interfejs do bibliotek przetwarzania grafiki ImageMagick i
GraphicsMagick. Wspiera ponad 80 formatów graficznych, włączając w to
GIF, JPEG, PNG. Zawiera API dla dwuwymiarowego rysowania. Obszerna
dokumentacja w HTML-u.

%package rdoc
Summary:	HTML documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla %{pkgname}
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description rdoc
HTML documentation for %{pkgname}.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla %{pkgname}.

%package ri
Summary:	ri documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla %{pkgname}
Group:		Documentation
Requires:	ruby
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description ri
ri documentation for %{pkgname}.

%description ri -l pl.UTF-8
Dokumentacji w formacie ri dla %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
# write .gemspec
%__gem_helper spec

# make gemspec self-contained
ruby -r rubygems -e 'spec = eval(File.read("rmagick.gemspec"))
	File.open("%{pkgname}-%{version}.gemspec", "w") do |file|
	file.puts spec.to_ruby_for_cache
end'

rake \
	CC="%{__cc}" \
	LDFLAGS="%{rpmldflags}" \
	CFLAGS="%{rpmcflags} -fPIC"

rdoc --ri --op ri ext/RMagick lib
rdoc --op rdoc ext/RMagick lib
%{__rm} ri/created.rid

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_vendorarchdir},%{ruby_ridir},%{ruby_specdir},%{ruby_rdocdir}/%{name}-%{version},%{_examplesdir}/%{name}}

cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
%{__rm} $RPM_BUILD_ROOT%{ruby_vendorlibdir}/RMagick2.so

# install ext
install -p lib/RMagick2.so $RPM_BUILD_ROOT%{ruby_vendorarchdir}

cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a rdoc/* $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}

# install gemspec
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc ChangeLog README.textile CONTRIBUTING.md
%{ruby_vendorlibdir}/RMagick*
%{ruby_vendorlibdir}/rmagick*
%{ruby_vendorlibdir}/rvg*
%attr(755,root,root) %{ruby_vendorarchdir}/*.so
%{ruby_specdir}/%{pkgname}-%{version}.gemspec
%{_examplesdir}/%{name}

%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/Magick
