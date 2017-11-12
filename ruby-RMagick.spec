#
# Conditional build:
%bcond_with	tests		# build without tests
%bcond_without	doc			# don't build ri/rdoc

%define pkgname RMagick
Summary:	Graphics Processing library for Ruby
Summary(pl.UTF-8):	Biblioteka przetwarzania grafiki dla języka Ruby
Name:		ruby-%{pkgname}
Version:	2.16.0
Release:	4
License:	Ruby-alike
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/rmagick-%{version}.gem
# Source0-md5:	d03bb84d342b0a78f9c6262acb451dc8
Patch0:		no-gem.patch
Patch1:		disable-tests.patch
Patch2:		no-git.patch
Patch3:		magick6.patch
URL:		https://github.com/gemhome/rmagick
BuildRequires:	ImageMagick6-devel >= 1:6.7.0.7-2
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
BuildRequires:	ImageMagick6-coder-dot
BuildRequires:	ImageMagick6-coder-fpx
BuildRequires:	ImageMagick6-coder-jbig
BuildRequires:	ImageMagick6-coder-jpeg
BuildRequires:	ImageMagick6-coder-jpeg2
BuildRequires:	ImageMagick6-coder-miff
BuildRequires:	ImageMagick6-coder-mpr
BuildRequires:	ImageMagick6-coder-pdf
BuildRequires:	ImageMagick6-coder-png
BuildRequires:	ImageMagick6-coder-ps2
BuildRequires:	ImageMagick6-coder-svg
BuildRequires:	ImageMagick6-coder-tiff
BuildRequires:	ImageMagick6-coder-url
BuildRequires:	ImageMagick6-coder-wmf
%endif
%if %{with doc}
BuildRequires:	ruby-rdoc
%endif
BuildConflicts:	ruby-RMagick < 1.7.2
%requires_ge_to	ImageMagick6-libs ImageMagick6-devel
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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description rdoc
HTML documentation for Ruby %{pkgname} module.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla modułu języka Ruby %{pkgname}.

%package ri
Summary:	ri documentation for Ruby %{pkgname} module
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla modułu języka Ruby %{pkgname}
Group:		Documentation
Requires:	ruby
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description ri
ri documentation for Ruby %{pkgname} module.

%description ri -l pl.UTF-8
Dokumentacja w formacie ri dla modułu języka Ruby %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%{__rm} spec/rmagick/draw_spec.rb

%build
# write .gemspec
%__gem_helper spec

# make gemspec self-contained
ruby -r rubygems -e 'spec = eval(File.read("rmagick.gemspec"))
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
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_vendorarchdir},%{ruby_ridir},%{ruby_specdir},%{ruby_rdocdir}/%{name}-%{version},%{_examplesdir}/%{name}-%{version}}

cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
%{__rm} $RPM_BUILD_ROOT%{ruby_vendorlibdir}/RMagick2.so

# install ext
install -p lib/RMagick2.so $RPM_BUILD_ROOT%{ruby_vendorarchdir}

%if %{with doc}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a rdoc/* $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}
%endif

cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# install gemspec
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc CHANGELOG.md LICENSE README.textile
%{ruby_vendorlibdir}/rmagick
%{ruby_vendorlibdir}/rmagick*.rb
%{ruby_vendorlibdir}/rvg
%attr(755,root,root) %{ruby_vendorarchdir}/RMagick2.so
%{ruby_specdir}/%{pkgname}-%{version}.gemspec
%{_examplesdir}/%{name}-%{version}

%if %{with doc}
%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/Magick
%{ruby_ridir}/RMagick
%endif
