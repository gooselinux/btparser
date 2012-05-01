Name: btparser
Version: 0.13
Release: 1%{?dist}
Summary: Parser and analyzer for backtraces produced by GDB
Group: Development/Libraries
License: GPLv2+
URL: http://fedorahosted.org/btparser
Source0: https://fedorahosted.org/released/btparser/btparser-%{version}.tar.xz

%description
Btparser is a backtrace parser and analyzer, which works with
backtraces produced by the GNU Project Debugger. It can parse a text
file with a backtrace to a tree of C structures, allowing to analyze
the threads and frames of the backtrace and work with them.

Btparser also contains some backtrace manipulation and extraction
routines:
- it can find a frame in the crash-time backtrace where the program
  most likely crashed (a chance is that the function described in that
  frame is buggy)
- it can produce a duplication hash of the backtrace, which helps to
  discover that two crash-time backtraces are duplicates, triggered by
  the same flaw of the code
- it can "rate" the backtrace quality, which depends on the number of
  frames with and without the function name known (missing function
  name is caused by missing debugging symbols)

%package devel
Summary: Development libraries for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries and headers for %{name}.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

# Remove all libtool archives (*.la) from modules directory.
find %{buildroot} -regex ".*\.la$" | xargs rm -f --

%check
make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README NEWS COPYING TODO ChangeLog
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz
%{_libdir}/lib*.so.*

%files devel
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*

%changelog
* Mon May 16 2011 Karel Klíč <kklic@redhat.com> - 0.13-1
- Initial packaging
