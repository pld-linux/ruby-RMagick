%define		ruby_archdir	%(ruby -r rbconfig -e 'print Config::CONFIG["archdir"]')
%define		ruby_rubylibdir	%(ruby -r rbconfig -e 'print Config::CONFIG["rubylibdir"]')
%define		ruby_ridir	%(ruby -r rbconfig -e 'include Config; print File.join(CONFIG["datadir"], "ri", CONFIG["ruby_version"], "system")')
%define		ruby_version	%(ruby -r rbconfig -e 'print Config::CONFIG["ruby_version"]')

%define         tarname		RMagick

Summary:	Graphics Processing library for Ruby.
Summary(pl):	Biblioteka przetwarzania grafiki dla Ruby
Name:		ruby-RMagick
Version:	1.6.0
Release:	1
License:	Ruby-alike
Group:		Development/Languages
Source0:	http://rubyforge.org/frs/download.php/1212/%{tarname}-%{version}.tar.bz2
# Source0-md5:	7970f3eda76a021d2d523befff31cda4
Source1:	setup.rb
URL:		http://rmagick.rubyforge.org/
BuildRequires:	ImageMagick-coder-dot
BuildRequires:	ImageMagick-coder-dps
BuildRequires:	ImageMagick-coder-fpx
BuildRequires:	ImageMagick-coder-jbig
BuildRequires:	ImageMagick-coder-jpeg2
BuildRequires:	ImageMagick-coder-miff
BuildRequires:	ImageMagick-coder-mpr
BuildRequires:	ImageMagick-coder-pdf
BuildRequires:	ImageMagick-coder-ps2
BuildRequires:	ImageMagick-coder-svg
BuildRequires:	ImageMagick-coder-tiff
BuildRequires:	ImageMagick-coder-url
BuildRequires:	ImageMagick-coder-wmf
BuildRequires:	autoconf
BuildRequires:	ruby-devel
Requires:	ruby
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An interface to the ImageMagick and GraphicsMagick image processing
libraries. Supports more than 80 image formats, including GIF, JPEG,
PNG. Includes 2D drawing API. Comprehensive HTML documentation.

%description
Jest to interfejs do bibliotek przetwarzania grafiki ImageMagick i
GraphicsMagick. Wspiera ponad 80 format�w graficznych, w��czaj�c w to
GIF, JPEG, PNG. Zawiera API dla dwuwymiarowego rysowania. Obszerna
dokumentacja w HTML-u.

%prep
%setup -q -n %{tarname}-%{version}

%build
%{__autoconf}
./configure # no macro!
cp %{SOURCE1} install.rb
rm post-install.rb
touch post-install.rb
ruby install.rb config \
	--rb-dir=%{ruby_rubylibdir} \
	--so-dir=%{ruby_archdir}

ruby install.rb setup

rdoc --ri --op ri ext/RMagick lib
rdoc --op rdoc ext/RMagick lib

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_rubylibdir},%{ruby_ridir},%{_examplesdir}/%{name}}

ruby install.rb install --prefix=$RPM_BUILD_ROOT

cp -a ri/ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc rdoc
%{ruby_rubylibdir}/RMagick*
%attr(755,root,root) %{ruby_archdir}/*.so
%{ruby_ridir}/Magick
%{ruby_ridir}/Class_*
%{_examplesdir}/%{name}
