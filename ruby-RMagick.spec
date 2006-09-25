%define		tarname		RMagick
Summary:	Graphics Processing library for Ruby
Summary(pl):	Biblioteka przetwarzania grafiki dla Ruby
Name:		ruby-RMagick
Version:	1.13.0
Release:	1
License:	Ruby-alike
Group:		Development/Languages
Source0:	http://rubyforge.org/frs/download.php/11315/%{tarname}-%{version}.tar.bz2
# Source0-md5:	c12834576b7b979a567fe191ec502418
Patch0:		%{name}-evil.patch
URL:		http://rmagick.rubyforge.org/
BuildConflicts:	ruby-RMagick < 1.7.2
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
BuildRequires:	ImageMagick-devel >= 1:6.2.4.0
BuildRequires:	autoconf
BuildRequires:	rpmbuild(macros) >= 1.277
BuildRequires:	ruby-devel
BuildRequires:	setup.rb
%{?ruby_mod_ver_requires_eq}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An interface to the ImageMagick and GraphicsMagick image processing
libraries. Supports more than 80 image formats, including GIF, JPEG,
PNG. Includes 2D drawing API. Comprehensive HTML documentation.

%description
Jest to interfejs do bibliotek przetwarzania grafiki ImageMagick i
GraphicsMagick. Wspiera ponad 80 formatów graficznych, w³±czaj±c w to
GIF, JPEG, PNG. Zawiera API dla dwuwymiarowego rysowania. Obszerna
dokumentacja w HTML-u.

%prep
%setup -q -n %{tarname}-%{version}
%patch0 -p1
cp /usr/share/setup.rb install.rb

%build
%{__autoconf}
./configure # no macro!
> post-install.rb
ruby install.rb config \
	--siterubyver=%{ruby_rubylibdir} \
	--sodir=%{ruby_archdir}

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
%{ruby_rubylibdir}/rvg*
%attr(755,root,root) %{ruby_archdir}/*.so
%{ruby_ridir}/Magick
%{_examplesdir}/%{name}
