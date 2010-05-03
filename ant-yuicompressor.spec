# TODO:
# - pldize examples
%include	/usr/lib/rpm/macros.java
Summary:	Ant task for yuicompressor
Summary(pl.UTF-8):	Wtyczka programu ant do yuicompressor
Name:		ant-yuicompressor
Version:	0.5
Release:	1
License:	BSD
Group:		Development/Languages/Java
Source0:	http://github.com/n0ha/yui-compressor-ant-task/tarball/yui-compressor-ant-task-0.5/%{name}-%{version}.tar.gz
# Source0-md5:	895d08ada70ec00d48b9b008a1054a8f
Source1:	antlib.xml
URL:		http://github.com/n0ha/yui-compressor-ant-task/
BuildRequires:	ant
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.555
BuildRequires:	sed >= 4.0
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ant task for yuicompressor.

%description -l pl.UTF-8
Wtyczka programu ant do yuicompressor.

%package javadoc
Summary:	Online manual for %{name}
Summary(pl.UTF-8):	Dokumentacja online do %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Documentation for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja do %{name}.

%description javadoc -l fr.UTF-8
Javadoc pour %{name}.

%package examples
Summary:	Examples for %{name}
Summary(pl.UTF-8):	Przykłady użycia %{name}
Group:		Documentation
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description examples
Examples for %{name}.

%description examples -l pl.UTF-8
Przykłady dla pakietu %{name}.

%package source
Summary:	Source code of %{name}
Summary(pl.UTF-8):	Kod źródłowy %{name}
Group:		Documentation
Requires:	jpackage-utils >= 1.7.5-2

%description source
Source code of %{name}.

%description source -l pl.UTF-8
Kod źródłowy %{name}.

%prep
%setup -qc
mv n0ha-*/* .
%undos build.xml doc/example/build.xml

# name of second jar can not be substring of first jar. This part of code is
# from /usr/bin/jar:
#          for dep in `cat "$file"`; do
#            case "$OPT_JAR_LIST" in
#            *"$dep"*) ;;
#            *) OPT_JAR_LIST="$OPT_JAR_LIST${OPT_JAR_LIST:+ }$dep"
#            esac
#          done
# so if second name is contained in first it will be skipped.
echo "yuicompressor ant/ant-yuicompressor" > ant.conf

echo >> doc/CHANGELOG
echo >> doc/LICENSE

find -name '*jar' | xargs rm

%build
export JAVA_HOME="%{java_home}"

required_jars="yuicompressor"
CLASSPATH=$(build-classpath $required_jars)

%ant jar javadocs \
	-Dbuild.sysclasspath=first

install -d net/noha/tools/ant/yuicompressor/tasks/
cp -a %{SOURCE1} net/noha/tools/ant/yuicompressor/tasks/antlib.xml
%jar uf build/bin/yui-compressor-ant-task-%{version}.jar net/noha/tools/ant/yuicompressor/tasks/antlib.xml

%jar cf %{name}.src.jar -C src .

%install
rm -rf $RPM_BUILD_ROOT

# ant task
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/ant.d,%{_javadir}/ant}
cp -a build/bin/yui-compressor-ant-task-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/ant/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/ant/%{name}.jar
cp -a ant.conf $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/yuicompressor

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a build/doc/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

# examples
install -d $RPM_BUILD_ROOT%{_examplesdir}
cp -a doc/example $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# source
install -d $RPM_BUILD_ROOT%{_javasrcdir}
cp -a %{name}.src.jar $RPM_BUILD_ROOT%{_javasrcdir}/%{name}.src.jar

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc README doc/CHANGELOG doc/LICENSE
%{_sysconfdir}/ant.d/yuicompressor
%{_javadir}/ant/%{name}.jar
%{_javadir}/ant/%{name}-%{version}.jar

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}

%files source
%defattr(644,root,root,755)
%{_javasrcdir}/%{name}.src.jar
