Summary: A GNU general-purpose parser generator
Name: bison
Version: 3.8.2
Release: 1
License: GPLv3+
Source: ftp://ftp.gnu.org/pub/gnu/bison/bison-%{version}.tar.xz
URL: https://github.com/sailfishos/bison
BuildRequires: m4 >= 1.4 
BuildRequires: help2man
# autopoint required during build.
BuildRequires: gettext-devel
BuildRequires: flex
# makeinfo required for build
BuildRequires: texinfo
BuildRequires: gperf
Requires: m4 >= 1.4

%description
Bison is a general purpose parser generator that converts a grammar
description for an LALR(1) context-free grammar into a C program to
parse that grammar. Bison can be used to develop a wide range of
language parsers, from ones used in simple desk calculators to complex
programming languages. Bison is upwardly compatible with Yacc, so any
correctly written Yacc grammar should work with Bison without any
changes. If you know Yacc, you shouldn't have any trouble using
Bison. You do need to be very proficient in C programming to be able
to use Bison. Bison is only needed on systems that are used for
development.

If your system will be used for C development, you should install
Bison.

%package devel
Summary: -ly library for development using Bison-generated parsers

%description devel
The bison-devel package contains the -ly library sometimes used by
programs using Bison-generated parsers.  If you are developing programs
using Bison, you might want to link with this library.  This library
is not required by all Bison-generated parsers, but may be employed by
simple programs to supply minimal support for the generated parsers.

# -ly is kept static.  It only contains two symbols: main and yyerror,
# and both of these are extremely simple (couple lines of C total).
# It doesn't really pay off to introduce a shared library for that.
#
# Therefore -devel subpackage could have been created as -static, but
# the split was done in Jan 2005, which predates current guidelines.
# Besides there is logic to that: the library is devel in the sense
# that the generated parser could be distributed together with other
# sources, and only bison-devel would be necessary to wrap the build.

%prep
%setup -q -n %{name}-%{version}/%{name}

%build
rm -rf submodules/autoconf
ln -s ../../autoconf submodules/autoconf
echo %{version} | cut -d '+' -f 1 > .tarball-version
cp .tarball-version .version

./bootstrap --skip-po --no-git --no-bootstrap-sync --gnulib-srcdir=../gnulib/
# this currently linked in git and not getting handled by bootstrap
rm -f build-aux/move-if-change
ln -s ../../gnulib/build-aux/move-if-change build-aux/move-if-change
%configure
%make_build

%install
%makeinstall

# Remove unpackaged files.
rm -f $RPM_BUILD_ROOT/%{_bindir}/yacc
rm -rf $RPM_BUILD_ROOT/%{_infodir}
rm -f $RPM_BUILD_ROOT/%{_mandir}/man1/yacc*
rm -rf $RPM_BUILD_ROOT/%{_docdir}/%{name}/examples/*
rm -f $RPM_BUILD_ROOT/%{_docdir}/%{name}/{AUTHORS,COPYING,NEWS,README,THANKS,TODO}

# The distribution contains also source files.  These are used by m4
# when the target parser file is generated.
%files
%defattr(-,root,root)
%license COPYING
%{_mandir}/*/bison*
%{_datadir}/bison
%{_bindir}/bison
%{_datadir}/aclocal/bison*.m4

%files devel
%license COPYING
%defattr(-,root,root)
%{_libdir}/liby.a
