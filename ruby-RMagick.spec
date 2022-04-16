#
# Conditional build:
%bcond_with	tests	# unit tests
%bcond_without	doc	# ri/rdoc documentation

%define pkgname RMagick
Summary:	Graphics Processing library for Ruby
Summary(pl.UTF-8):	Biblioteka przetwarzania grafiki dla języka Ruby
Name:		ruby-%{pkgname}
Version:	4.1.0
Release:	2
License:	Ruby-alike
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/rmagick-%{version}.gem
# Source0-md5:	e22024f2c78088f101ff0acade179043
Patch0:		no-gem.patch
Patch1:		no-git.patch
URL:		https://github.com/gemhome/rmagick
BuildRequires:	ImageMagick-devel >= 1:7.0.0
BuildRequires:	ruby-test-unit
BuildRequires:	gmp-devel
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.484
BuildRequires:	ruby >= 1:1.8.6
BuildRequires:	ruby-devel
BuildRequires:	ruby-modules
BuildRequires:	ruby-rake
BuildRequires:	ruby-rake-compiler
BuildRequires:	ruby-simplecov
BuildRequires:	ruby-rspec-core
BuildRequires:	ruby-rspec-expectations
BuildRequires:	ruby-rspec-mocks
%if %{with tests}
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
%endif
%if %{with doc}
BuildRequires:	ruby-rdoc
%endif
BuildConflicts:	ruby-RMagick < 1.7.2
%requires_ge_to	ImageMagick-libs ImageMagick-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An interface to the ImageMagick and GraphicsMagick image processing
libraries. Supports more than 80 image formats, including GIF, JPEG,
PNG. Includes 2D drawing API. Comprehensive HTML documentation.

%description -l pl.UTF-8
Jest to interfejs do bibliotek przetwarzania grafiki ImageMagick i
GraphicsMagick. Obsługuje ponad 80 formatów graficznych, włączając w
to GIF, JPEG, PNG. Zawiera API dla dwuwymiarowego rysowania. Obszerna
dokumentacja w HTML-u.

%package rdoc
Summary:	HTML documentation for Ruby %{pkgname} module
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla modułu języka Ruby %{pkgname}
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4
BuildArch:	noarch

%description rdoc
HTML documentation for Ruby %{pkgname} module.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla modułu języka Ruby %{pkgname}.

%package ri
Summary:	ri documentation for Ruby %{pkgname} module
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla modułu języka Ruby %{pkgname}
Group:		Documentation
Requires:	ruby
BuildArch:	noarch

%description ri
ri documentation for Ruby %{pkgname} module.

%description ri -l pl.UTF-8
Dokumentacja w formacie ri dla modułu języka Ruby %{pkgname}.

%prep
%setup -q -n rmagick-%{version}
%patch0 -p1
%patch1 -p1

%build
# make gemspec self-contained
ruby -r rubygems -e 'spec = eval(File.read("rmagick-%{version}.gemspec"))
	File.open("%{pkgname}-%{version}.gemspec", "w") do |file|
	file.puts spec.to_ruby_for_cache
end' #'

rake compile \
	CC="%{__cc}" \
	LDFLAGS="%{rpmldflags}" \
	CFLAGS="%{rpmcflags} -fPIC"

%if %{with tests}
rake spec
rake test
%endif

%if %{with doc}
rdoc --ri --op ri ext/RMagick lib
rdoc --op rdoc ext/RMagick lib
%{__rm} ri/created.rid
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_vendorarchdir},%{ruby_ridir},%{ruby_specdir},%{ruby_rdocdir}/%{name}-%{version}}

cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
%{__rm} $RPM_BUILD_ROOT%{ruby_vendorlibdir}/RMagick2.so

# install ext
install -p lib/RMagick2.so $RPM_BUILD_ROOT%{ruby_vendorarchdir}

%if %{with doc}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a rdoc/* $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}
%endif

# install gemspec
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md CODE_OF_CONDUCT.md CONTRIBUTING.md LICENSE README.md
%{ruby_vendorlibdir}/rmagick
%{ruby_vendorlibdir}/rmagick*.rb
%{ruby_vendorlibdir}/rvg
%attr(755,root,root) %{ruby_vendorarchdir}/RMagick2.so
%{ruby_specdir}/%{pkgname}-%{version}.gemspec

%if %{with doc}
%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/Magick
%{ruby_ridir}/RMagick
%endif
