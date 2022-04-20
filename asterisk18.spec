#%%global _rc 1
#%%global _beta 3

%global           pjsip_version   2.12
%global           jansson_version 2.12
%global           bundledjansson 0

%global           optflags        %{optflags} -Werror-implicit-function-declaration -DLUA_COMPAT_MODULE -fPIC
%ifarch s390 %{arm} aarch64 %{mips}
%global           ldflags         -Wl,--as-needed,--library-path=%{_libdir} %{__global_ldflags}
%else
%global           ldflags         -m%{__isa_bits} -Wl,--as-needed,--library-path=%{_libdir} %{__global_ldflags}
%endif

%global           astvarrundir     /run/asterisk

%global           alsa       1
%global           apidoc     0
%global           bluetooth  1
%global           mysql      1
%global           odbc       1
%global           postgresql 1
%global           radius     0
%global           snmp       1
%global           misdn      0
%global           ldap       1
%global           gmime      0
%global           corosync   1
%global           imap       0
%global           jack       0
%global           phone      0
%global           xmpp       0
%global           ices       0
%global           meetme     1
%global           ooh323     1
%global           freepbx    1
%global           _datadir   /var/lib
%global           _datarootdir %{_datadir}
%global           makeargs        DEBUG= OPTIMIZE= DESTDIR=%{buildroot} ASTVARRUNDIR=%{astvarrundir} ASTDATADIR=%{_datadir}/asterisk ASTVARLIBDIR=%{_datadir}/asterisk ASTDBDIR=%{_localstatedir}/spool/asterisk NOISY_BUILD=1

Summary:          The Open Source PBX
Name:             asterisk18
Version:          18.11.1
Release:          1%{?dist}
License:          GPLv2
URL:              http://www.asterisk.org/
Group: Utilities/System
Source0:          http://downloads.asterisk.org/pub/telephony/asterisk/releases/asterisk-%{version}%{?_rc:-rc%{_rc}}%{?_beta:-beta%{_beta}}.tar.gz
Source1:          http://downloads.asterisk.org/pub/telephony/asterisk/releases/asterisk-%{version}%{?_rc:-rc%{_rc}}%{?_beta:-beta%{_beta}}.tar.gz.asc
Source2:          asterisk.logrotate
Source3:          menuselect.makedeps
Source4:          menuselect.makeopts
# GPG keyring with Asterisk developer signatures
# Created by running:
#gpg2 --no-default-keyring --keyring ./asterisk-gpgkeys.gpg \
#--keyserver=hkp://pool.sks-keyservers.net --recv-keys \
#0x21A91EB1F012252993E9BF4A368AB332B59975F3 \
#0x80CEBC345EC9FF529B4B7B808438CBA18D0CAA72 \
#0xCDBEE4CC699E200EB4D46BB79E76E3A42341CE04 \
#0x639D932D5170532F8C200CCD9C59F000777DCC45 \
#0x551F29104B2106080C6C2851073B0C1FC9B2E352 \
#0x57E769BC37906C091E7F641F6CB44E557BD982D8 \
#0x0F77FB5D216A02390B4C51DB7C2C8A8BCB3F61BD \
#0xF2FC93DB7587BD1FB49E045A5D984BE337191CE7
Source7:          asterisk-gpgkeys.gpg

# Now building Asterisk with bundled pjproject, because they apply custom patches to it
Source8:          https://raw.githubusercontent.com/asterisk/third-party/master/pjproject/%{pjsip_version}/pjproject-%{pjsip_version}.tar.bz2

# Bundling jansson on EL7 and EL8, because the version in CentOS is too old
Source9:          http://www.digip.org/jansson/releases/jansson-%{jansson_version}.tar.bz2

Source11:         http://downloads.digium.com/pub/telephony/codec_opus/asterisk-18.0/x86-64/codec_opus-18.0_current-x86_64.tar.gz
Source12:         http://downloads.digium.com/pub/telephony/codec_silk/asterisk-18.0/x86-64/codec_silk-18.0_current-x86_64.tar.gz
Source13:         http://downloads.digium.com/pub/telephony/codec_siren7/asterisk-18.0/x86-64/codec_siren7-18.0_current-x86_64.tar.gz
Source14:         http://downloads.digium.com/pub/telephony/codec_siren14/asterisk-18.0/x86-64/codec_siren14-18.0_current-x86_64.tar.gz
Source15:         modules.conf

Patch1016: asterisk-18-mp3.patch

Patch2: lazymembers.patch
# Asterisk now builds against a bundled copy of pjproject, as they apply some patches
# directly to pjproject before the build against it
Provides:         bundled(pjproject) = %{pjsip_version}

BuildRequires:    autoconf
BuildRequires:    automake
BuildRequires:    gcc
BuildRequires:    gcc-c++
BuildRequires:    ncurses
BuildRequires:    perl

# core build requirements
BuildRequires:    openssl-devel
BuildRequires:    newt-devel
BuildRequires:    ncurses-devel
BuildRequires:    libcap-devel
%if 0%{?gmime}
BuildRequires:    gtk2-devel
%endif
BuildRequires:    libsrtp23-devel
BuildRequires:    perl-interpreter
BuildRequires:    perl-generators
BuildRequires:    popt-devel
%{?systemd_requires}
BuildRequires:    systemd
BuildRequires:    kernel-headers

# for res_http_post
%if 0%{?gmime}
BuildRequires:    gmime-devel
%endif

# for building docs
BuildRequires:    doxygen
BuildRequires:    graphviz
BuildRequires:    libxml2-devel
BuildRequires:    latex2html

# for building res_calendar_caldav
BuildRequires:    neon-devel
BuildRequires:    libical-devel
BuildRequires:    libxml2-devel

# for codec_speex
BuildRequires:    speex-devel >= 1.2
%if (0%{?fedora} > 21 || 0%{?rhel} > 7)
BuildRequires:    speexdsp-devel >= 1.2
%endif

# for format_ogg_vorbis
BuildRequires:    libogg-devel
BuildRequires:    libvorbis-devel

# codec_gsm
BuildRequires:    gsm-devel

# additional dependencies
BuildRequires:    SDL-devel
BuildRequires:    SDL_image-devel

# cli
BuildRequires:    libedit-devel

# codec_ilbc
BuildRequires:    ilbc-devel

# res_rtp_asterisk
BuildRequires:    libuuid-devel

# res_resolver_unbound
BuildRequires:    unbound-devel

%if 0%{?corosync}
BuildRequires:    corosynclib-devel
%endif

BuildRequires:    alsa-lib-devel
BuildRequires:    libcurl-devel
BuildRequires:    dahdi-tools-devel >= 2.0.0
BuildRequires:    dahdi-tools-libs >= 2.0.0
BuildRequires:    libpri-devel >= 1.4.12
BuildRequires:    libss7-devel >= 1.0.1
BuildRequires:    spandsp-devel >= 0.0.5-0.1.pre4
BuildRequires:    libtiff-devel
BuildRequires:    libjpeg-turbo-devel
BuildRequires:    lua-devel
%if 0%{?jack}
BuildRequires:    jack-audio-connection-kit-devel
%endif
BuildRequires:    libresample-devel
BuildRequires:    bluez-libs-devel
BuildRequires:    libtool-ltdl-devel
BuildRequires:    portaudio-devel >= 19
BuildRequires:    sqlite-devel
BuildRequires:    freetds-devel

%if 0%{?misdn}
BuildRequires:    mISDN-devel
%endif

%if 0%{?ldap}
BuildRequires:    openldap-devel
%endif

%if 0%{?mysql}
BuildRequires:    mariadb-devel
%endif

%if 0%{?odbc}
BuildRequires:    libtool-ltdl-devel
BuildRequires:    unixODBC-devel
%endif

%if 0%{?postgresql}
%if 0%{?rhel}
BuildRequires:    postgresql-devel
%else
BuildRequires:    libpq-devel
%endif
%endif

%if 0%{?radius}
%if 0%{?fedora} || 0%{?rhel} < 7
BuildRequires:    freeradius-client-devel
%else
BuildRequires:    radcli-compat-devel
%endif
%endif

%if 0%{?snmp}
BuildRequires:    net-snmp-devel
BuildRequires:    lm_sensors-devel
%endif

%if 0%{?imap}
BuildRequires:    uw-imap-devel
%endif

%if 0%{bundledjansson}
BuildRequires:    jansson-devel
Requires:         jansson
%else
Provides:         bundled(jansson) = 2.11
%endif

# for gpg to be able to verify the signature
BuildRequires:    libgcrypt
BuildRequires:    make

Requires(pre):    %{_sbindir}/useradd
Requires(pre):    %{_sbindir}/groupadd

Requires(post):   systemd-units
Requires(post):   systemd-sysv
Requires(preun):  systemd-units
Requires(postun): systemd-units

# chan_phone headers no longer in kernel headers
Obsoletes:        asterisk-phone < %{version}

%description
Asterisk is a complete PBX in software. It runs on Linux and provides
all of the features you would expect from a PBX and more. Asterisk
does voice over IP in three protocols, and can interoperate with
almost all standards-based telephony equipment using relatively
inexpensive hardware.

%package core
Summary: Asterisk core package without any "extras".
Group: Utilities/System
Provides: asterisk13-speex = 13.38.3-2
Obsoletes: asterisk13-speex < 13.38.3-2
Provides: asterisk13-resample = 13.38.3-2
Obsoletes: asterisk13-resample < 13.38.3-2
Provides: asterisk13-addons-core = 13.38.3-2
Obsoletes: asterisk13-addons-core < 13.38.3-2
Provides: asterisk13-ogg = 13.38.3-2
Obsoletes: asterisk13-ogg < 13.38.3-2
Conflicts: asterisk14-core
Conflicts: asterisk16-core
Conflicts: asterisk10-core
Conflicts: asterisk11-core
Conflicts: asterisk12-core
Provides: asterisk13-core = 13.38.3-2
Obsoletes: asterisk13-core < 13.38.3-2
Requires: openssl
Requires: libxml2
Requires: libsrtp23
Requires(pre): %{_sbindir}/groupadd
Requires(pre): %{_sbindir}/useradd

%description core
This package contains a base install of Asterisk without any "extras".

%package addons
Summary: Asterisk-addons package.
Group: Utilities/System
Requires: %{name}-addons-core = %{version}-%{release}
Provides: %{name}-addons
Provides: asterisk-13-addons

%if 0%{?mysql}
Requires: %{name}-addons-mysql = %{version}-%{release}
Requires: mysql
%endif

%if 0%{?ooh323}
Requires: %{name}-addons-ooh323 = %{version}-%{release}
%endif

%description addons
This package contains a base install of Asterisk-addons without any "extras".

%package addons-core
Summary: Asterisk-addons core package.
Group: Utilities/System
Requires: %{name}-core = %{version}-%{release}
Provides: %{name}-addons-core
Provides: asterisk13-addons-core

%description addons-core
This package contains a base install of Asterisk-addons without any "extras".

%if 0%{?bluetooth}
%package addons-bluetooth
Summary: bluetooth modules for Asterisk
Group: Utilities/System
BuildRequires: bluez-libs-devel
Requires: bluez-libs
Requires: %{name}-core = %{version}-%{release}
Provides: %{name}-addons-bluetooth
Provides: asterisk13-addons-bluetooth = 13.38.3-2
Obsoletes: asterisk13-addons-bluetooth < 13.38.3-2

%description addons-bluetooth
bluetooth modules for Asterisk
%endif

%if 0%{?mysql}
%package addons-mysql
Summary: Applications for Asterisk that use MySQL
Group: Utilities/System
BuildRequires: mysql-devel
Requires: %{name}-core = %{version}-%{release}
Requires: mysql
Requires: %{name}-addons-core = %{version}-%{release}
Provides: %{name}-addons-mysql
Provides: asterisk13-addons-mysql = 13.38.3-2
Obsoletes: asterisk13-addons-mysql < 13.38.3-2

%description addons-mysql
Applications for Asterisk that use MySQL.
%endif

%if 0%{?ooh323}
%package addons-ooh323
Summary: H.323 channel for Asterisk using the Objective Systems Open H.323 for C library
Group: Utilities/System
Requires: %{name}-core = %{version}-%{release}
Provides: %{name}-addons-ooh323
Provides: asterisk13-addons-ooh = 13.38.3-2323
Obsoletes: asterisk13-addons-ooh < 13.38.3-2323

%description addons-ooh323
H.323 channel for Asterisk using the Objective Systems Open H.323 for C library.
%endif

%package ael
Summary: AEL (Asterisk Extension Logic) modules for Asterisk
Requires: %{name}-core = %{version}-%{release}

%description ael
AEL (Asterisk Extension Logic) mdoules for Asterisk

%package alembic
Summary: Alembic scripts for the Asterisk DB (realtime)
Requires: %{name}-core = %{version}-%{release}

%description alembic
Alembic scripts for the Asterisk DB

%if 0%{?alsa}
%package alsa
Summary: Alsa channel driver for Asterisk
Group: Utilities/System
BuildRequires: alsa-lib-devel
Requires: alsa-lib
Requires: %{name}-core = %{version}-%{release}
Provides: asterisk13-alsa = 13.38.3-2
Obsoletes: asterisk13-alsa < 13.38.3-2

%description alsa
Alsa channel driver for Asterisk
%endif

%if 0%{?apidoc}
%package apidoc
Summary: API documentation for Asterisk
Requires: asterisk = %{version}-%{release}

%description apidoc
API documentation for Asterisk.
%endif

%package calendar
Summary: Calendar applications for Asterisk
Requires: %{name}-core = %{version}-%{release}

%description calendar
Calendar applications for Asterisk.

%package configs
Summary: Basic configuration files for Asterisk
Group: Utilities/System
Requires: %{name}-core = %{version}
Provides: asterisk13-configs = 13.38.3-2
Obsoletes: asterisk13-configs < 13.38.3-2

%description configs
The sample configuration files for Asterisk

%if 0%{?corosync}
%package corosync
Summary: Modules for Asterisk that use Corosync
Requires: %{name}-core = %{version}-%{release}

%description corosync
Modules for Asterisk that use Corosync.
%endif

%package curl
Summary: Modules for Asterisk that use cURL
Requires: %{name}-core = %{version}-%{release}

%description curl
Modules for Asterisk that use cURL.

%package dahdi
Summary: Modules for Asterisk that use DAHDI
Requires: %{name}-core = %{version}-%{release}
Requires: dahdi-tools >= 2.0.0
Requires: libtonezone
Requires(pre): %{_sbindir}/usermod
Provides: asterisk-zaptel = %{version}-%{release}
Provides: asterisk13-dahdi = 13.38.3-2
Obsoletes: asterisk13-dahdi < 13.38.3-2

%description dahdi
Modules for Asterisk that use DAHDI.

%package devel
Summary: Development files for Asterisk
Requires: %{name}-core = %{version}-%{release}
Provides: asterisk13-devel = 13.38.3-2
Obsoletes: asterisk13-devel < 13.38.3-2

%description devel
Development files for Asterisk.

%package doc
Summary: The Documentation files for Asterisk
Group: Development/Libraries
Requires: %{name}-core = %{version}-%{release}
Provides: asterisk13-doc = 13.38.3-2
Obsoletes: asterisk13-doc < 13.38.3-2

%description doc
API documentation for Asterisk.

%package fax
Summary: FAX applications for Asterisk
Requires: %{name}-core = %{version}-%{release}

%description fax
FAX applications for Asterisk

%package festival
Summary: Festival application for Asterisk
Requires: %{name}-core = %{version}-%{release}
Requires: festival

%description festival
Application for the Asterisk PBX that uses Festival to convert text to speech.

%package hep
Summary: Modules for capturing SIP traffic using Homer (HEPv3)
Requires: %{name}-core = %{version}-%{release}

%description hep
Modules for capturing SIP traffic using Homer (HEPv3)

%if 0%{?ices}
%package ices
Summary: Stream audio from Asterisk to an IceCast server
Requires: %{name}-core = %{version}-%{release}
Requires: ices

%description ices
Stream audio from Asterisk to an IceCast server.
%endif

%if 0%{?jack}
%package jack
Summary: JACK resources for Asterisk
Requires: %{name}-core = %{version}-%{release}

%description jack
JACK resources for Asterisk.
%endif

%if 0%{?ldap}
%package ldap
Summary: LDAP resources for Asterisk
Requires: %{name}-core = %{version}-%{release}

%description ldap
LDAP resources for Asterisk.
%endif

%package lua
Summary: Lua resources for Asterisk
Requires: %{name}-core = %{version}-%{release}

%description lua
Lua resources for Asterisk.

%package mgcp
Summary: MGCP channel driver for Asterisk
Requires: %{name}-core = %{version}-%{release}

%description mgcp
MGCP channel driver for Asterisk

%package minivm
Summary: MiniVM applicaton for Asterisk
Requires: %{name}-core = %{version}-%{release}

%description minivm
MiniVM application for Asterisk.

%if 0%{?misdn}
%package misdn
Summary: mISDN channel for Asterisk
Requires: %{name}-core = %{version}-%{release}
Requires(pre): %{_sbindir}/usermod
Provides: asterisk13-misdn = 13.38.3-2
Obsoletes: asterisk13-misdn < 13.38.3-2

%description misdn
mISDN channel for Asterisk.
%endif

%package mwi-external
Summary: Support for developing external voicemail applications
Requires: %{name}-core = %{version}-%{release}
Conflicts: asterisk-voicemail = %{version}-%{release}
Conflicts: asterisk-voicemail-implementation = %{version}-%{release}

%description mwi-external
Support for developing external voicemail applications

%if 0%{?odbc}
%package odbc
Summary: Applications for Asterisk that use ODBC (except voicemail)
Requires: %{name}-core = %{version}-%{release}
Provides: asterisk13-odbc = 13.38.3-2
Obsoletes: asterisk13-odbc < 13.38.3-2

%description odbc
Applications for Asterisk that use ODBC (except voicemail)
%endif

%package oss
Summary: Modules for Asterisk that use OSS sound drivers
Requires: %{name}-core = %{version}-%{release}

%description oss
Modules for Asterisk that use OSS sound drivers.

%if 0%{?postgresql}
%package pgsql
Summary: Applications for Asterisk that use PostgreSQL
Requires: %{name}-core = %{version}-%{release}
Provides: asterisk13-pgsql = 13.38.3-2
Obsoletes: asterisk13-pgsql < 13.38.3-2

%description pgsql
Applications for Asterisk that use PostgreSQL.
%endif

%package phone
Summary: Channel driver for Quicknet Technologies, Inc.'s Telephony cards
Requires: %{name}-core = %{version}-%{release}

%description phone
Quicknet Technologies, Inc.'s Telephony cards including the Internet
PhoneJACK, Internet PhoneJACK Lite, Internet PhoneJACK PCI, Internet
LineJACK, Internet PhoneCARD and SmartCABLE.

%package portaudio
Summary: Modules for Asterisk that use the portaudio library
Requires: %{name}-core = %{version}-%{release}

%description portaudio
Modules for Asterisk that use the portaudio library.

%if 0%{?radius}
%package radius
Summary: Applications for Asterisk that use RADIUS
Requires: %{name}-core = %{version}-%{release}

%description radius
Applications for Asterisk that use RADIUS.
%endif

%package skinny
Summary: Modules for Asterisk that support the SCCP/Skinny protocol
Requires: %{name}-core = %{version}-%{release}

%description skinny
Modules for Asterisk that support the SCCP/Skinny protocol.

%if 0%{?snmp}
%package snmp
Summary: Module that enables SNMP monitoring of Asterisk
Requires: %{name}-core = %{version}-%{release}
# This subpackage depends on perl-libs, this Requires tracks versioning.
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Provides: asterisk13-snmp = 13.38.3-2
Obsoletes: asterisk13-snmp < 13.38.3-2

%description snmp
Module that enables SNMP monitoring of Asterisk.
%endif

%package sqlite3
Summary: Sqlite modules for Asterisk
Requires: %{name}-core = %{version}-%{release}
Provides: asterisk13-sqlite = 13.38.3-23
Obsoletes: asterisk13-sqlite < 13.38.3-23

%description sqlite3
Sqlite modules for Asterisk.

%package tds
Summary: Modules for Asterisk that use FreeTDS
Requires: %{name}-core = %{version}-%{release}
Provides: asterisk13-tds = 13.38.3-2
Obsoletes: asterisk13-tds < 13.38.3-2

%description tds
Modules for Asterisk that use FreeTDS.

%package unistim
Summary: Unistim channel for Asterisk
Requires: %{name}-core = %{version}-%{release}

%description unistim
Unistim channel for Asterisk

%package voicemail
Summary: Common Voicemail Modules for Asterisk
Requires: %{name}-core = %{version}-%{release}
Requires: %{name}-voicemail-implementation = %{version}-%{release}
Requires: /usr/bin/sox
Requires: /usr/sbin/sendmail
Conflicts: asterisk-mwi-external <= %{version}-%{release}
Provides: asterisk13-voicemail = 13.38.3-2
Obsoletes: asterisk13-voicemail < 13.38.3-2

%description voicemail
Common Voicemail Modules for Asterisk.

%if 0%{?imap}
%package voicemail-imapstorage
Summary: Store voicemail on an IMAP server
Requires: %{name}-core = %{version}-%{release}
Requires: %{name}-voicemail = %{version}-%{release}
Provides: %{name}-voicemail-implementation = %{version}-%{release}
Conflicts: %{name}-voicemail-odbcstorage <= %{version}-%{release}
Conflicts: %{name}-voicemail-plain <= %{version}-%{release}
Provides: asterisk13-voicemail-imapstorage = 13.38.3-2
Obsoletes: asterisk13-voicemail-imapstorage < 13.38.3-2

%description voicemail-imapstorage
Voicemail implementation for Asterisk that stores voicemail on an IMAP
server.
%endif

%package voicemail-odbcstorage
Summary: Store voicemail in a database using ODBC
Requires: %{name}-core = %{version}-%{release}
Requires: %{name}-voicemail = %{version}-%{release}
Provides: %{name}-voicemail-implementation = %{version}-%{release}
Conflicts: %{name}-voicemail-imapstorage <= %{version}-%{release}
Conflicts: %{name}-voicemail-plain <= %{version}-%{release}
Provides: asterisk13-voicemail-odbcstorage = 13.38.3-2
Obsoletes: asterisk13-voicemail-odbcstorage < 13.38.3-2

%description voicemail-odbcstorage
Voicemail implementation for Asterisk that uses ODBC to store
voicemail in a database.

%package voicemail-plain
Summary: Store voicemail on the local filesystem
Requires: %{name}-core = %{version}-%{release}
Requires: %{name}-voicemail = %{version}-%{release}
Provides: %{name}-voicemail-implementation = %{version}-%{release}
Conflicts: %{name}-voicemail-imapstorage <= %{version}-%{release}
Conflicts: %{name}-voicemail-odbcstorage <= %{version}-%{release}

%description voicemail-plain
Voicemail implementation for Asterisk that stores voicemail on the
local filesystem.

%if 0%{?xmpp}
%package xmpp
Summary: Jabber/XMPP resources for Asterisk
Requires: %{name}-core = %{version}-%{release}

%description xmpp
Jabber/XMPP resources for Asterisk.
%endif

%prep
%if 0%{?fedora} || 0%{?rhel} >=8
# only verifying on Fedora and RHEL >=8 due to version of gpg
rpm -q libgcrypt
gpgv2 --keyring %{SOURCE7} %{SOURCE1} %{SOURCE0}
%endif
%setup -q -n asterisk-%{version}%{?_rc:-rc%{_rc}}%{?_beta:-beta%{_beta}}


# copy the pjproject tarball to the cache/ directory
mkdir cache
cp %{SOURCE8} cache/

%if 0%{?rhel} >= 7
cp %{SOURCE9} cache/
%endif

echo '*************************************************************************'
ls -altr cache/
pwd
echo '*************************************************************************'

%patch1016 -p1

%patch2 -p1

cp %{S:3} menuselect.makedeps
cp %{S:4} menuselect.makeopts



# Fixup makefile so sound archives aren't downloaded/installed
%{__perl} -pi -e 's/^all:.*$/all:/' sounds/Makefile
%{__perl} -pi -e 's/^install:.*$/install:/' sounds/Makefile

# convert comments in one file to UTF-8
mv main/fskmodem.c main/fskmodem.c.old
iconv -f iso-8859-1 -t utf-8 -o main/fskmodem.c main/fskmodem.c.old
touch -r main/fskmodem.c.old main/fskmodem.c
rm main/fskmodem.c.old

chmod -x contrib/scripts/dbsep.cgi

%if ! 0%{?corosync}
%{__perl} -pi -e 's/^MENUSELECT_RES=(.*)$/MENUSELECT_RES=\1 res_corosync/g' menuselect.makeopts
%endif

%if ! 0%{?mysql}
%{__perl} -pi -e 's/^MENUSELECT_ADDONS=(.*)$/MENUSELECT_ADDONS=\1 res_config_mysql app_mysql cdr_mysql/g' menuselect.makeopts
%endif

%if ! 0%{?postgresql}
%{__perl} -pi -e 's/^MENUSELECT_RES=(.*)$/MENUSELECT_RES=\1 res_config_pgsql/g' menuselect.makeopts
%{__perl} -pi -e 's/^MENUSELECT_CDR=(.*)$/MENUSELECT_CDR=\1 cdr_pgsql/g' menuselect.makeopts
%{__perl} -pi -e 's/^MENUSELECT_CEL=(.*)$/MENUSELECT_CEL=\1 cel_pgsql/g' menuselect.makeopts
%endif

%if ! 0%{?radius}
%{__perl} -pi -e 's/^MENUSELECT_CDR=(.*)$/MENUSELECT_CDR=\1 cdr_radius/g' menuselect.makeopts
%{__perl} -pi -e 's/^MENUSELECT_CEL=(.*)$/MENUSELECT_CEL=\1 cel_radius/g' menuselect.makeopts
%endif

%if ! 0%{?snmp}
%{__perl} -pi -e 's/^MENUSELECT_RES=(.*)$/MENUSELECT_RES=\1 res_snmp/g' menuselect.makeopts
%endif

%if ! 0%{?misdn}
%{__perl} -pi -e 's/^MENUSELECT_CHANNELS=(.*)$/MENUSELECT_CHANNELS=\1 chan_misdn/g' menuselect.makeopts
%endif

%if ! 0%{?ices}
%{__perl} -pi -e 's/^MENUSELECT_APPS=(.*)$/MENUSELECT_APPS=\1 app_ices/g' menuselect.makeopts
%endif

%if ! 0%{?jack}
%{__perl} -pi -e 's/^MENUSELECT_APPS=(.*)$/MENUSELECT_APPS=\1 app_jack/g' menuselect.makeopts
%endif

%if ! 0%{?ldap}
%{__perl} -pi -e 's/^MENUSELECT_RES=(.*)$/MENUSELECT_RES=\1 res_config_ldap/g' menuselect.makeopts
%endif

%if ! 0%{?gmime}
%{__perl} -pi -e 's/^MENUSELECT_RES=(.*)$/MENUSELECT_RES=\1 res_http_post/g' menuselect.makeopts
%endif

%if ! 0%{xmpp}
%{__perl} -pi -e 's/^MENUSELECT_RES=(.*)$/MENUSELECT_RES=\1 res_xmpp/g' menuselect.makeopts
%{__perl} -pi -e 's/^MENUSELECT_CHANNELS=(.*)$/MENUSELECT_CHANNELS=\1 chan_motif/g' menuselect.makeopts
%endif

%if ! 0%{meetme}
%{__perl} -pi -e 's/^MENUSELECT_APPS=(.*)$/MENUSELECT_APPS=\1 app_meetme/g' menuselect.makeopts
%endif

%if ! 0%{ooh323}
%{__perl} -pi -e 's/^MENUSELECT_ADDONS=(.*)$/MENUSELECT_ADDONS=\1 chan_ooh323/g' menuselect.makeopts
%endif

%if ! 0%{imap}
%{__perl} -pi -e 's/^MENUSELECT_APPS=(.*)$/MENUSELECT_APPS=\1 app_voicemail_imap/g' menuselect.makeopts
%endif

%build

export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export FFLAGS="%{optflags}"
export LDFLAGS="%{ldflags}"
export ASTCFLAGS=" "

sed -i '1s/env python/python3/' contrib/scripts/refcounter.py

./bootstrap.sh

pushd menuselect
%configure
popd


%if 0%{?fedora}
%if 0%{?imap}
%configure --with-imap=system --with-gsm=/usr --with-ilbc=/usr --with-libedit=yes --with-srtp --with-pjproject-bundled --with-externals-cache=%{_builddir}/asterisk-%{version}%{?_rc:-rc%{_rc}}%{?_beta:-beta%{_beta}}/cache LDFLAGS="%{ldflags}" NOISY_BUILD=1 CPPFLAGS="-fPIC"
%else
%configure --without-imap --with-gsm=/usr --with-ilbc=/usr --with-libedit=yes --with-srtp --with-pjproject-bundled --with-externals-cache=%{_builddir}/asterisk-%{version}%{?_rc:-rc%{_rc}}%{?_beta:-beta%{_beta}}/cache LDFLAGS="%{ldflags}" NOISY_BUILD=1 CPPFLAGS="-fPIC"
%endif
%else
%if 0%{?imap}
%configure --with-imap=system --with-gsm=/usr --with-ilbc=/usr --with-libedit=yes --with-srtp --with-jansson-bundled --with-pjproject-bundled --with-externals-cache=%{_builddir}/asterisk-%{version}%{?_rc:-rc%{_rc}}%{?_beta:-beta%{_beta}}/cache LDFLAGS="%{ldflags}" NOISY_BUILD=1 CPPFLAGS="-fPIC"
%else
%configure --without-imap --with-gsm=/usr --with-ilbc=/usr --with-libedit=yes --with-srtp --with-jansson-bundled --with-pjproject-bundled --with-externals-cache=%{_builddir}/asterisk-%{version}%{?_rc:-rc%{_rc}}%{?_beta:-beta%{_beta}}/cache LDFLAGS="%{ldflags}" NOISY_BUILD=1 CPPFLAGS="-fPIC"
%endif
%endif

%make_build menuselect-tree NOISY_BUILD=1
%{__perl} -n -i -e 'print unless /openr2/i' menuselect-tree

%{__perl} -pi -e'/^MENUSELECT_ADDONS=/ and s,format_mp3,,' menuselect.makeopts
%{__perl} -pi -e'/^MENUSELECT_APPS=/ and s,app_mp3,,' menuselect.makeopts

# Build with plain voicemail and directory
echo "### Building with plain voicemail and directory"
%make_build %{makeargs}

rm apps/app_voicemail.o apps/app_directory.o
mv apps/app_voicemail.so apps/app_voicemail_plain.so
mv apps/app_directory.so apps/app_directory_plain.so

%if 0%{?imap}
# Now build with IMAP storage for voicemail and directory
sed -i -e 's/^MENUSELECT_OPTS_app_voicemail=.*$/MENUSELECT_OPTS_app_voicemail=IMAP_STORAGE/' menuselect.makeopts

echo "### Building with IMAP voicemail and directory"
%make_build %{makeargs}

rm apps/app_voicemail.o apps/app_directory.o
mv apps/app_voicemail.so apps/app_voicemail_imap.so
mv apps/app_directory.so apps/app_directory_imap.so
%endif

# Now build with ODBC storage for voicemail and directory
sed -i -e 's/^MENUSELECT_OPTS_app_voicemail=.*$/MENUSELECT_OPTS_app_voicemail=ODBC_STORAGE/' menuselect.makeopts
echo "### Building with ODBC voicemail and directory"
%make_build %{makeargs}

rm apps/app_voicemail.o apps/app_directory.o
mv apps/app_voicemail.so apps/app_voicemail_odbc.so
mv apps/app_directory.so apps/app_directory_odbc.so

# so that these modules don't get built again
touch apps/app_voicemail.o apps/app_directory.o
touch apps/app_voicemail.so apps/app_directory.so

sed -i -e 's/^MENUSELECT_RES=\(.*\)\bres_mwi_external\b\(.*\)$/MENUSELECT_RES=\1 \2/g' menuselect.makeopts
sed -i -e 's/^MENUSELECT_RES=\(.*\)\bres_mwi_external_ami\b\(.*\)$/MENUSELECT_RES=\1 \2/g' menuselect.makeopts
sed -i -e 's/^MENUSELECT_RES=\(.*\)\bres_stasis_mailbox\b\(.*\)$/MENUSELECT_RES=\1 \2/g' menuselect.makeopts
sed -i -e 's/^MENUSELECT_RES=\(.*\)\bres_ari_mailboxes\b\(.*\)$/MENUSELECT_RES=\1 \2/g' menuselect.makeopts
sed -i -e 's/^MENUSELECT_APP=\(.*\)$/MENUSELECT_RES=\1 app_voicemail/g' menuselect.makeopts

%make_build %{makeargs}

%if 0%{?apidoc}
%make_build progdocs %{makeargs}
# fix dates so that we don't get multilib conflicts
#find doc/api/html -type f -print0 | xargs --null touch -r ChangeLog
%endif

%install
rm -rf %{buildroot}

export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export FFLAGS="%{optflags}"
export LDFLAGS="%{ldflags}"
export ASTCFLAGS="%{optflags}"

make install %{makeargs}
make samples %{makeargs}
# Let's include the headers in the devel package, just as it used to be. We may use them to build the g.723 and g.729 codecs
make install-headers %{makeargs}

rm -f %{buildroot}%{_sbindir}/safe_asterisk
install -D -p -m 0644 %{S:2} %{buildroot}%{_sysconfdir}/logrotate.d/asterisk

rm %{buildroot}%{_libdir}/asterisk/modules/app_directory.so
rm %{buildroot}%{_libdir}/asterisk/modules/app_voicemail.so

%if 0%{?imap}
install -D -p -m 0755 apps/app_directory_imap.so %{buildroot}%{_libdir}/asterisk/modules/app_directory_imap.so
install -D -p -m 0755 apps/app_voicemail_imap.so %{buildroot}%{_libdir}/asterisk/modules/app_voicemail_imap.so
%endif
install -D -p -m 0755 apps/app_directory_odbc.so %{buildroot}%{_libdir}/asterisk/modules/app_directory_odbc.so
install -D -p -m 0755 apps/app_voicemail_odbc.so %{buildroot}%{_libdir}/asterisk/modules/app_voicemail_odbc.so
install -D -p -m 0755 apps/app_directory_plain.so %{buildroot}%{_libdir}/asterisk/modules/app_directory_plain.so
install -D -p -m 0755 apps/app_voicemail_plain.so %{buildroot}%{_libdir}/asterisk/modules/app_voicemail_plain.so

# create some directories that need to be packaged
mkdir -p %{buildroot}%{_datadir}/asterisk/sounds
mkdir -p %{buildroot}%{_datadir}/asterisk/ast-db-manage
mkdir -p %{buildroot}%{_localstatedir}/lib/asterisk
mkdir -p %{buildroot}%{_localstatedir}/log/asterisk/cdr-custom
mkdir -p %{buildroot}%{_localstatedir}/spool/asterisk/festival
mkdir -p %{buildroot}%{_localstatedir}/spool/asterisk/monitor
mkdir -p %{buildroot}%{_localstatedir}/spool/asterisk/outgoing
mkdir -p %{buildroot}%{_localstatedir}/spool/asterisk/uploads

# Don't package the sample voicemail user
rm -rf %{buildroot}%{_localstatedir}/spool/asterisk/voicemail/default

# Don't package example phone provision configs
rm -rf %{buildroot}%{_datadir}/asterisk/phoneprov/*

# these are compiled with -O0 and thus include unfortified code.
rm -rf %{buildroot}%{_sbindir}/hashtest
rm -rf %{buildroot}%{_sbindir}/hashtest2

rm -rf %{buildroot}%{_sysconfdir}/asterisk/app_skel.conf
rm -rf %{buildroot}%{_sysconfdir}/asterisk/config_test.conf
rm -rf %{buildroot}%{_sysconfdir}/asterisk/test_sorcery.conf

rm -rf %{buildroot}%{_libdir}/libasteriskssl.so
ln -s libasterisk.so.1 %{buildroot}%{_libdir}/libasteriskssl.so

%if 0%{?apidoc}
find doc/api/html -name \*.map -size 0 -delete
%endif

# copy the alembic scripts
cp -rp contrib/ast-db-manage %{buildroot}%{_datadir}/asterisk/ast-db-manage

%if ! 0%{?mysql}
rm -f %{buildroot}%{_sysconfdir}/asterisk/*_mysql.conf
%endif

%if ! 0%{?postgresql}
rm -f %{buildroot}%{_sysconfdir}/asterisk/*_pgsql.conf
%endif

%if ! 0%{?misdn}
rm -f %{buildroot}%{_sysconfdir}/asterisk/misdn.conf
%endif

%if ! 0%{?snmp}
rm -f %{buildroot}%{_sysconfdir}/asterisk/res_snmp.conf
%endif

%if ! 0%{?ldap}
rm -f %{buildroot}%{_sysconfdir}/asterisk/res_ldap.conf
%endif

%if ! 0%{?corosync}
rm -f %{buildroot}%{_sysconfdir}/asterisk/res_corosync.conf
%endif

%if ! 0%{?phone}
rm -f %{buildroot}%{_sysconfdir}/asterisk/phone.conf
%endif

%if ! 0%{xmpp}
rm -f %{buildroot}%{_sysconfdir}/asterisk/xmpp.conf
rm -f %{buildroot}%{_sysconfdir}/asterisk/motif.conf
%endif

%if ! 0%{ooh323}
rm -f %{buildroot}%{_sysconfdir}/asterisk/ooh323.conf
%endif

# move the asterisk sample files to /etc/asterisk/asterisk-*_samples
mkdir -p %{buildroot}/%{_sysconfdir}/samples-%{version}
%{__mv} -v %{buildroot}/%{_sysconfdir}/asterisk/* %{buildroot}/%{_sysconfdir}/samples-%{version}
%{__mv} -v %{buildroot}/%{_sysconfdir}/samples-%{version} %{buildroot}/%{_sysconfdir}/asterisk/

%if 0%{?freepbx}
# copy some really needed stuff (mainly for freepbx)
#%{__cp} -v %{buildroot}/%{_sysconfdir}/asterisk/samples-%{version}/asterisk.conf	%{buildroot}/%{_sysconfdir}/asterisk
#%{__cp} -v %{buildroot}/%{_sysconfdir}/asterisk/samples-%{version}/cdr_tds.conf	%{buildroot}/%{_sysconfdir}/asterisk
%{__cp} -v %{buildroot}/%{_sysconfdir}/asterisk/samples-%{version}/chan_dahdi.conf	%{buildroot}/%{_sysconfdir}/asterisk
%{__cp} -v %{buildroot}/%{_sysconfdir}/asterisk/samples-%{version}/dundi.conf		%{buildroot}/%{_sysconfdir}/asterisk
#%{__cp} -v %{buildroot}/%{_sysconfdir}/asterisk/samples-%{version}/gtalk.conf		%{buildroot}/%{_sysconfdir}/asterisk
#%{__cp} -v %{buildroot}/%{_sysconfdir}/asterisk/samples-%{version}/iax.conf		%{buildroot}/%{_sysconfdir}/asterisk
#%{__cp} -v %{buildroot}/%{_sysconfdir}/asterisk/samples-%{version}/jingle.conf		%{buildroot}/%{_sysconfdir}/asterisk
%{__cp} -v %{buildroot}/%{_sysconfdir}/asterisk/samples-%{version}/logger.conf		%{buildroot}/%{_sysconfdir}/asterisk
%{__cp} -v %{buildroot}/%{_sysconfdir}/asterisk/samples-%{version}/mgcp.conf		%{buildroot}/%{_sysconfdir}/asterisk
%{__cp} -v %{buildroot}/%{_sysconfdir}/asterisk/samples-%{version}/phoneprov.conf	%{buildroot}/%{_sysconfdir}/asterisk
#%{__cp} -v %{buildroot}/%{_sysconfdir}/asterisk/samples-%{version}/sip.conf		%{buildroot}/%{_sysconfdir}/asterisk
#%{__cp} -v %{buildroot}/%{_sysconfdir}/asterisk/samples-%{version}/pjsip.conf		%{buildroot}/%{_sysconfdir}/asterisk
%{__cp} -v %{buildroot}/%{_sysconfdir}/asterisk/samples-%{version}/skinny.conf		%{buildroot}/%{_sysconfdir}/asterisk
%{__cp} -v %{buildroot}/%{_sysconfdir}/asterisk/samples-%{version}/smdi.conf		%{buildroot}/%{_sysconfdir}/asterisk
%{__cp} -v %{buildroot}/%{_sysconfdir}/asterisk/samples-%{version}/unistim.conf		%{buildroot}/%{_sysconfdir}/asterisk
%{__cp} -v %{S:15} %{buildroot}/%{_sysconfdir}/asterisk
%endif

# Additional codecs
tar xzvvf %{S:11} --strip-components=1
tar xzvvf %{S:12} --strip-components=1
tar xzvvf %{S:13} --strip-components=1
tar xzvvf %{S:14} --strip-components=1
%{__cp} *.so %{buildroot}/%{_libdir}/asterisk/modules/
%{__cp} codec_opus_config-en_US.xml %{buildroot}/%{_datadir}/asterisk/documentation/thirdparty/

%pre
%{_sbindir}/groupadd -r asterisk &>/dev/null || :
%{_sbindir}/useradd  -r -s /sbin/nologin -d /var/lib/asterisk -M \
                               -c 'Asterisk User' -g asterisk asterisk &>/dev/null || :

%post
if [ $1 -eq 1 ] ; then
	/bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi


%preun
if [ "$1" -eq "0" ]; then
	# Package removal, not upgrade
	/bin/systemctl --no-reload disable asterisk.service > /dev/null 2>&1 || :
	/bin/systemctl stop asterisk.service > /dev/null 2>&1 || :
fi


%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart asterisk.service >/dev/null 2>&1 || :
fi

%pre dahdi
%{_sbindir}/usermod -a -G dahdi asterisk

%if 0%{?misdn}
%pre misdn
%{_sbindir}/usermod -a -G misdn asterisk
%endif

%files core
%defattr(-, root, root)
%license LICENSE

%{_libdir}/libasteriskssl.so.1
%{_libdir}/libasteriskpj.so
%{_libdir}/libasteriskpj.so.2
%dir %{_libdir}/asterisk
%dir %{_libdir}/asterisk/modules
%{_libdir}/asterisk/modules/app_agent_pool.so
%{_libdir}/asterisk/modules/app_adsiprog.so
%{_libdir}/asterisk/modules/app_alarmreceiver.so
%{_libdir}/asterisk/modules/app_amd.so
%{_libdir}/asterisk/modules/app_attended_transfer.so
%{_libdir}/asterisk/modules/app_audiosocket.so
%{_libdir}/asterisk/modules/app_authenticate.so
%{_libdir}/asterisk/modules/app_blind_transfer.so
%{_libdir}/asterisk/modules/app_bridgeaddchan.so
%{_libdir}/asterisk/modules/app_bridgewait.so
%{_libdir}/asterisk/modules/app_cdr.so
%{_libdir}/asterisk/modules/app_celgenuserevent.so
%{_libdir}/asterisk/modules/app_chanisavail.so
%{_libdir}/asterisk/modules/app_channelredirect.so
%{_libdir}/asterisk/modules/app_chanspy.so
%{_libdir}/asterisk/modules/app_confbridge.so
%{_libdir}/asterisk/modules/app_controlplayback.so
%{_libdir}/asterisk/modules/app_db.so
%{_libdir}/asterisk/modules/app_dial.so
%{_libdir}/asterisk/modules/app_dictate.so
%{_libdir}/asterisk/modules/app_directed_pickup.so
%{_libdir}/asterisk/modules/app_disa.so
%{_libdir}/asterisk/modules/app_dumpchan.so
%{_libdir}/asterisk/modules/app_echo.so
%{_libdir}/asterisk/modules/app_exec.so
%{_libdir}/asterisk/modules/app_externalivr.so
%{_libdir}/asterisk/modules/app_followme.so
%{_libdir}/asterisk/modules/app_forkcdr.so
%{_libdir}/asterisk/modules/app_getcpeid.so
%{_libdir}/asterisk/modules/app_image.so
%{_libdir}/asterisk/modules/app_macro.so
%{_libdir}/asterisk/modules/app_mp3.so
%{_libdir}/asterisk/modules/app_milliwatt.so
%{_libdir}/asterisk/modules/app_mixmonitor.so
%{_libdir}/asterisk/modules/app_morsecode.so
%{_libdir}/asterisk/modules/app_nbscat.so
%{_libdir}/asterisk/modules/app_originate.so
%{_libdir}/asterisk/modules/app_page.so
%{_libdir}/asterisk/modules/app_playback.so
%{_libdir}/asterisk/modules/app_playtones.so
%{_libdir}/asterisk/modules/app_privacy.so
%{_libdir}/asterisk/modules/app_queue.so
%{_libdir}/asterisk/modules/app_readexten.so
%{_libdir}/asterisk/modules/app_read.so
%{_libdir}/asterisk/modules/app_record.so
%{_libdir}/asterisk/modules/app_saycounted.so
%{_libdir}/asterisk/modules/app_sayunixtime.so
%{_libdir}/asterisk/modules/app_senddtmf.so
%{_libdir}/asterisk/modules/app_sendtext.so
%{_libdir}/asterisk/modules/app_sms.so
%{_libdir}/asterisk/modules/app_softhangup.so
%{_libdir}/asterisk/modules/app_speech_utils.so
%{_libdir}/asterisk/modules/app_stack.so
%{_libdir}/asterisk/modules/app_stasis.so
%{_libdir}/asterisk/modules/app_statsd.so
%{_libdir}/asterisk/modules/app_stream_echo.so
%{_libdir}/asterisk/modules/app_system.so
%{_libdir}/asterisk/modules/app_talkdetect.so
%{_libdir}/asterisk/modules/app_test.so
%{_libdir}/asterisk/modules/app_transfer.so
%{_libdir}/asterisk/modules/app_url.so
%{_libdir}/asterisk/modules/app_userevent.so
%{_libdir}/asterisk/modules/app_verbose.so
%{_libdir}/asterisk/modules/app_waitforring.so
%{_libdir}/asterisk/modules/app_waitforsilence.so
%{_libdir}/asterisk/modules/app_waituntil.so
%{_libdir}/asterisk/modules/app_while.so
%{_libdir}/asterisk/modules/app_zapateller.so
%{_libdir}/asterisk/modules/bridge_builtin_features.so
%{_libdir}/asterisk/modules/bridge_builtin_interval_features.so
%{_libdir}/asterisk/modules/bridge_holding.so
%{_libdir}/asterisk/modules/bridge_native_rtp.so
%{_libdir}/asterisk/modules/bridge_simple.so
%{_libdir}/asterisk/modules/bridge_softmix.so
%{_libdir}/asterisk/modules/cdr_csv.so
%{_libdir}/asterisk/modules/cdr_custom.so
%{_libdir}/asterisk/modules/cdr_manager.so
%{_libdir}/asterisk/modules/cdr_syslog.so
%{_libdir}/asterisk/modules/cel_custom.so
%{_libdir}/asterisk/modules/cel_manager.so
%{_libdir}/asterisk/modules/chan_audiosocket.so
%{_libdir}/asterisk/modules/chan_bridge_media.so
%{_libdir}/asterisk/modules/chan_rtp.so
%{_libdir}/asterisk/modules/codec_adpcm.so
%{_libdir}/asterisk/modules/codec_alaw.so
%{_libdir}/asterisk/modules/codec_a_mu.so
%{_libdir}/asterisk/modules/codec_g722.so
%{_libdir}/asterisk/modules/codec_g726.so
%{_libdir}/asterisk/modules/codec_gsm.so
%{_libdir}/asterisk/modules/codec_ilbc.so
%{_libdir}/asterisk/modules/codec_lpc10.so
%{_libdir}/asterisk/modules/codec_resample.so
%{_libdir}/asterisk/modules/codec_speex.so
%{_libdir}/asterisk/modules/codec_ulaw.so
%{_libdir}/asterisk/modules/codec_opus.so
%{_libdir}/asterisk/modules/format_ogg_opus.so
%{_libdir}/asterisk/modules/codec_silk.so
%{_libdir}/asterisk/modules/codec_siren14.so
%{_libdir}/asterisk/modules/codec_siren7.so
%{_libdir}/asterisk/modules/format_g719.so
%{_libdir}/asterisk/modules/format_g723.so
%{_libdir}/asterisk/modules/format_g726.so
%{_libdir}/asterisk/modules/format_g729.so
%{_libdir}/asterisk/modules/format_gsm.so
%{_libdir}/asterisk/modules/format_h263.so
%{_libdir}/asterisk/modules/format_h264.so
%{_libdir}/asterisk/modules/format_ilbc.so

%{_libdir}/asterisk/modules/format_mp3.so
%{_libdir}/asterisk/modules/format_ogg_speex.so
%{_libdir}/asterisk/modules/format_ogg_vorbis.so
%{_libdir}/asterisk/modules/format_pcm.so
%{_libdir}/asterisk/modules/format_siren14.so
%{_libdir}/asterisk/modules/format_siren7.so
%{_libdir}/asterisk/modules/format_sln.so
%{_libdir}/asterisk/modules/format_vox.so
%{_libdir}/asterisk/modules/format_wav_gsm.so
%{_libdir}/asterisk/modules/format_wav.so
%{_libdir}/asterisk/modules/func_aes.so
%{_libdir}/asterisk/modules/func_base64.so
%{_libdir}/asterisk/modules/func_blacklist.so
%{_libdir}/asterisk/modules/func_callcompletion.so
%{_libdir}/asterisk/modules/func_callerid.so
%{_libdir}/asterisk/modules/func_cdr.so
%{_libdir}/asterisk/modules/func_channel.so
%{_libdir}/asterisk/modules/func_config.so
%{_libdir}/asterisk/modules/func_cut.so
%{_libdir}/asterisk/modules/func_db.so
%{_libdir}/asterisk/modules/func_devstate.so
%{_libdir}/asterisk/modules/func_dialgroup.so
%{_libdir}/asterisk/modules/func_dialplan.so
%{_libdir}/asterisk/modules/func_enum.so
%{_libdir}/asterisk/modules/func_env.so
%{_libdir}/asterisk/modules/func_extstate.so
%{_libdir}/asterisk/modules/func_frame_trace.so
%{_libdir}/asterisk/modules/func_global.so
%{_libdir}/asterisk/modules/func_groupcount.so
%{_libdir}/asterisk/modules/func_hangupcause.so
%{_libdir}/asterisk/modules/func_holdintercept.so
%{_libdir}/asterisk/modules/func_iconv.so
%{_libdir}/asterisk/modules/func_jitterbuffer.so
%{_libdir}/asterisk/modules/func_lock.so
%{_libdir}/asterisk/modules/func_logic.so
%{_libdir}/asterisk/modules/func_math.so
%{_libdir}/asterisk/modules/func_md5.so
%{_libdir}/asterisk/modules/func_module.so
%{_libdir}/asterisk/modules/func_periodic_hook.so
%{_libdir}/asterisk/modules/func_pitchshift.so
%{_libdir}/asterisk/modules/func_presencestate.so
%{_libdir}/asterisk/modules/func_rand.so
%{_libdir}/asterisk/modules/func_realtime.so
%{_libdir}/asterisk/modules/func_sha1.so
%{_libdir}/asterisk/modules/func_shell.so
%{_libdir}/asterisk/modules/func_sorcery.so
%{_libdir}/asterisk/modules/func_speex.so
%{_libdir}/asterisk/modules/func_sprintf.so
%{_libdir}/asterisk/modules/func_srv.so
%{_libdir}/asterisk/modules/func_strings.so
%{_libdir}/asterisk/modules/func_sysinfo.so
%{_libdir}/asterisk/modules/func_talkdetect.so
%{_libdir}/asterisk/modules/func_timeout.so
%{_libdir}/asterisk/modules/func_uri.so
%{_libdir}/asterisk/modules/func_version.so
%{_libdir}/asterisk/modules/func_volume.so
%{_libdir}/asterisk/modules/pbx_config.so
%{_libdir}/asterisk/modules/pbx_dundi.so
%{_libdir}/asterisk/modules/pbx_loopback.so
%{_libdir}/asterisk/modules/pbx_realtime.so
%{_libdir}/asterisk/modules/pbx_spool.so
%{_libdir}/asterisk/modules/res_adsi.so
%{_libdir}/asterisk/modules/res_agi.so
%{_libdir}/asterisk/modules/res_ari.so
%{_libdir}/asterisk/modules/res_ari_applications.so
%{_libdir}/asterisk/modules/res_ari_asterisk.so
%{_libdir}/asterisk/modules/res_ari_bridges.so
%{_libdir}/asterisk/modules/res_ari_channels.so
%{_libdir}/asterisk/modules/res_ari_device_states.so
%{_libdir}/asterisk/modules/res_ari_endpoints.so
%{_libdir}/asterisk/modules/res_ari_events.so
%{_libdir}/asterisk/modules/res_ari_mailboxes.so
%{_libdir}/asterisk/modules/res_ari_model.so
%{_libdir}/asterisk/modules/res_ari_playbacks.so
%{_libdir}/asterisk/modules/res_ari_recordings.so
%{_libdir}/asterisk/modules/res_ari_sounds.so
%{_libdir}/asterisk/modules/res_audiosocket.so
%{_libdir}/asterisk/modules/res_chan_stats.so
%{_libdir}/asterisk/modules/res_clialiases.so
%{_libdir}/asterisk/modules/res_clioriginate.so
%{_libdir}/asterisk/modules/res_convert.so
%{_libdir}/asterisk/modules/res_crypto.so
%{_libdir}/asterisk/modules/res_endpoint_stats.so
%{_libdir}/asterisk/modules/res_format_attr_celt.so
%{_libdir}/asterisk/modules/res_format_attr_g729.so
%{_libdir}/asterisk/modules/res_format_attr_h263.so
%{_libdir}/asterisk/modules/res_format_attr_h264.so
%{_libdir}/asterisk/modules/res_format_attr_ilbc.so
%{_libdir}/asterisk/modules/res_format_attr_opus.so
%{_libdir}/asterisk/modules/res_format_attr_silk.so
%{_libdir}/asterisk/modules/res_format_attr_siren14.so
%{_libdir}/asterisk/modules/res_format_attr_siren7.so
%{_libdir}/asterisk/modules/res_format_attr_vp8.so
%{_libdir}/asterisk/modules/res_http_media_cache.so
%if 0%{?gmime}
%{_libdir}/asterisk/modules/res_http_post.so
%endif
%{_libdir}/asterisk/modules/res_http_websocket.so
%{_libdir}/asterisk/modules/res_limit.so
%{_libdir}/asterisk/modules/res_manager_devicestate.so
%{_libdir}/asterisk/modules/res_manager_presencestate.so
%{_libdir}/asterisk/modules/res_monitor.so
%{_libdir}/asterisk/modules/res_musiconhold.so
%{_libdir}/asterisk/modules/res_mutestream.so
%{_libdir}/asterisk/modules/res_mwi_devstate.so
%{_libdir}/asterisk/modules/res_parking.so
%{_libdir}/asterisk/modules/res_phoneprov.so
%{_libdir}/asterisk/modules/res_pjproject.so
%{_libdir}/asterisk/modules/res_prometheus.so
%{_libdir}/asterisk/modules/res_realtime.so
%{_libdir}/asterisk/modules/res_remb_modifier.so
%{_libdir}/asterisk/modules/res_resolver_unbound.so
%{_libdir}/asterisk/modules/res_rtp_asterisk.so
%{_libdir}/asterisk/modules/res_rtp_multicast.so
%{_libdir}/asterisk/modules/res_security_log.so
%{_libdir}/asterisk/modules/res_smdi.so
%{_libdir}/asterisk/modules/res_sorcery_astdb.so
%{_libdir}/asterisk/modules/res_sorcery_config.so
%{_libdir}/asterisk/modules/res_sorcery_memory.so
%{_libdir}/asterisk/modules/res_sorcery_memory_cache.so
%{_libdir}/asterisk/modules/res_sorcery_realtime.so
%{_libdir}/asterisk/modules/res_speech.so
%{_libdir}/asterisk/modules/res_srtp.so
%{_libdir}/asterisk/modules/res_stasis.so
%{_libdir}/asterisk/modules/res_stasis_answer.so
%{_libdir}/asterisk/modules/res_stasis_device_state.so
%{_libdir}/asterisk/modules/res_stasis_playback.so
%{_libdir}/asterisk/modules/res_stasis_recording.so
%{_libdir}/asterisk/modules/res_stasis_snoop.so
%{_libdir}/asterisk/modules/res_statsd.so
%{_libdir}/asterisk/modules/res_stir_shaken.so
%{_libdir}/asterisk/modules/res_stun_monitor.so
%{_libdir}/asterisk/modules/res_timing_pthread.so
%{_libdir}/asterisk/modules/res_timing_timerfd.so
%{_libdir}/asterisk/modules/app_dtmfstore.so
%{_libdir}/asterisk/modules/app_mf.so
%{_libdir}/asterisk/modules/app_reload.so
%{_libdir}/asterisk/modules/app_sf.so
%{_libdir}/asterisk/modules/app_waitforcond.so
%{_libdir}/asterisk/modules/func_frame_drop.so
%{_libdir}/asterisk/modules/func_json.so
%{_libdir}/asterisk/modules/func_sayfiles.so
%{_libdir}/asterisk/modules/func_scramble.so
%{_libdir}/asterisk/modules/res_tonedetect.so
%{_sbindir}/astcanary
%{_sbindir}/astdb2sqlite3
%{_sbindir}/asterisk
%{_sbindir}/astgenkey
%{_sbindir}/astman
%{_sbindir}/astversion
%{_sbindir}/autosupport
%{_sbindir}/muted
%{_sbindir}/rasterisk
%{_sbindir}/smsq
%{_sbindir}/stereorize
%{_sbindir}/streamplayer

# iax2
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/iax.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/iaxprov.conf
%dir %{_datadir}/asterisk/firmware
%dir %{_datadir}/asterisk/firmware/iax
%{_libdir}/asterisk/modules/chan_iax2.so

# pjsip
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/pjsip.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/pjproject.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/pjsip_notify.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/pjsip_wizard.conf
%{_libdir}/asterisk/modules/chan_pjsip.so
%{_libdir}/asterisk/modules/func_pjsip_aor.so
%{_libdir}/asterisk/modules/func_pjsip_contact.so
%{_libdir}/asterisk/modules/func_pjsip_endpoint.so
%{_libdir}/asterisk/modules/res_pjsip.so
%{_libdir}/asterisk/modules/res_pjsip_acl.so
%{_libdir}/asterisk/modules/res_pjsip_authenticator_digest.so
%{_libdir}/asterisk/modules/res_pjsip_caller_id.so
%{_libdir}/asterisk/modules/res_pjsip_config_wizard.so
%{_libdir}/asterisk/modules/res_pjsip_dialog_info_body_generator.so
%{_libdir}/asterisk/modules/res_pjsip_dlg_options.so
%{_libdir}/asterisk/modules/res_pjsip_diversion.so
%{_libdir}/asterisk/modules/res_pjsip_dtmf_info.so
%{_libdir}/asterisk/modules/res_pjsip_empty_info.so
%{_libdir}/asterisk/modules/res_pjsip_endpoint_identifier_anonymous.so
%{_libdir}/asterisk/modules/res_pjsip_endpoint_identifier_ip.so
%{_libdir}/asterisk/modules/res_pjsip_endpoint_identifier_user.so
%{_libdir}/asterisk/modules/res_pjsip_exten_state.so
%{_libdir}/asterisk/modules/res_pjsip_header_funcs.so
%{_libdir}/asterisk/modules/res_pjsip_history.so
%{_libdir}/asterisk/modules/res_pjsip_logger.so
%{_libdir}/asterisk/modules/res_pjsip_messaging.so
%{_libdir}/asterisk/modules/res_pjsip_mwi.so
%{_libdir}/asterisk/modules/res_pjsip_mwi_body_generator.so
%{_libdir}/asterisk/modules/res_pjsip_nat.so
%{_libdir}/asterisk/modules/res_pjsip_notify.so
%{_libdir}/asterisk/modules/res_pjsip_one_touch_record_info.so
%{_libdir}/asterisk/modules/res_pjsip_outbound_authenticator_digest.so
%{_libdir}/asterisk/modules/res_pjsip_outbound_publish.so
%{_libdir}/asterisk/modules/res_pjsip_outbound_registration.so
%{_libdir}/asterisk/modules/res_pjsip_path.so
%{_libdir}/asterisk/modules/res_pjsip_phoneprov_provider.so
%{_libdir}/asterisk/modules/res_pjsip_pidf_body_generator.so
%{_libdir}/asterisk/modules/res_pjsip_pidf_digium_body_supplement.so
%{_libdir}/asterisk/modules/res_pjsip_pidf_eyebeam_body_supplement.so
%{_libdir}/asterisk/modules/res_pjsip_publish_asterisk.so
%{_libdir}/asterisk/modules/res_pjsip_pubsub.so
%{_libdir}/asterisk/modules/res_pjsip_refer.so
%{_libdir}/asterisk/modules/res_pjsip_registrar.so
%{_libdir}/asterisk/modules/res_pjsip_rfc3326.so
%{_libdir}/asterisk/modules/res_pjsip_sdp_rtp.so
%{_libdir}/asterisk/modules/res_pjsip_send_to_voicemail.so
%{_libdir}/asterisk/modules/res_pjsip_session.so
%{_libdir}/asterisk/modules/res_pjsip_sips_contact.so
%{_libdir}/asterisk/modules/res_pjsip_stir_shaken.so
%{_libdir}/asterisk/modules/res_pjsip_t38.so
%{_libdir}/asterisk/modules/res_pjsip_transport_websocket.so
%{_libdir}/asterisk/modules/res_pjsip_xpidf_body_generator.so

# legacy sip
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/sip.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/sip_notify.conf
%{_libdir}/asterisk/modules/chan_sip.so

%{_mandir}/man8/astdb2bdb.8*
%{_mandir}/man8/astdb2sqlite3.8*
%{_mandir}/man8/asterisk.8*
%{_mandir}/man8/astgenkey.8*
%{_mandir}/man8/autosupport.8*
%{_mandir}/man8/safe_asterisk.8*

%attr(0775,asterisk,asterisk) %dir %{_sysconfdir}/asterisk
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/acl.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/adsi.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/agents.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/alarmreceiver.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/amd.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/ari.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/ast_debug_tools.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/asterisk.adsi
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/asterisk.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/ccss.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/cdr.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/cdr_beanstalkd.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/cdr_custom.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/cdr_manager.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/cdr_syslog.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/cel.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/cel_beanstalkd.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/cel_custom.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/cli.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/cli_aliases.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/cli_permissions.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/codecs.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/confbridge.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/dnsmgr.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/dsp.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/dundi.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/enum.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/extconfig.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/extensions.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/features.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/followme.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/http.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/indications.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/logger.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/manager.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/modules.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/musiconhold.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/muted.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/osp.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/phoneprov.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/prometheus.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/queuerules.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/queues.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/res_parking.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/res_stun_monitor.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/resolver_unbound.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/rtp.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/say.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/sla.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/smdi.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/sorcery.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/stasis.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/statsd.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/stir_shaken.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/telcordia-1.adsi
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/udptl.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/users.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/vpb.conf

%config(noreplace) %{_sysconfdir}/logrotate.d/asterisk
%if 0%{?freepbx}
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/modules.conf
%endif

%attr(0775,asterisk,asterisk) %dir %{_datadir}/asterisk
%attr(0775,asterisk,asterisk) %dir %{_datadir}/asterisk/agi-bin
%{_datadir}/asterisk/documentation
%{_datadir}/asterisk/images
%attr(0750,asterisk,asterisk) %{_datadir}/asterisk/keys
%{_datadir}/asterisk/phoneprov
%{_datadir}/asterisk/static-http
%{_datadir}/asterisk/rest-api
%attr(0775,asterisk,asterisk) %dir %{_datadir}/asterisk/sounds

%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/log/asterisk
%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/log/asterisk/cdr-csv
%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/log/asterisk/cdr-custom

%attr(0775,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk
%attr(0775,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/monitor
%attr(0775,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/outgoing
%attr(0775,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/tmp
%attr(0775,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/uploads
%attr(0775,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/voicemail

%attr(0775,asterisk,asterisk) %dir %{astvarrundir}
%{_datarootdir}/asterisk/scripts/

%files addons
%defattr(-, root, root)

%if 0%{bluetooth}
%files addons-bluetooth
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/chan_mobile.conf
%{_libdir}/asterisk/modules/chan_mobile.so
%endif

%files addons-core
%defattr(-, root, root)

%if 0%{mysql}
%files addons-mysql
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/app_mysql.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/cdr_mysql.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/res_config_mysql.conf
%doc contrib/realtime/mysql/*.sql
%{_libdir}/asterisk/modules/app_mysql.so
%{_libdir}/asterisk/modules/cdr_mysql.so
%{_libdir}/asterisk/modules/res_config_mysql.so
%endif

%if 0%{?ooh323}
%files addons-ooh323
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/ooh323.conf
%{_libdir}/asterisk/modules/chan_ooh323.so
%endif

%files ael
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/extensions.ael
%{_sbindir}/aelparse
#%%{_sbindir}/conf2ael
%{_libdir}/asterisk/modules/pbx_ael.so
%{_libdir}/asterisk/modules/res_ael_share.so

%files alembic
%{_datadir}/asterisk/ast-db-manage/

%files alsa
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/alsa.conf
%{_libdir}/asterisk/modules/chan_alsa.so

%if %{?apidoc}
%files apidoc
%doc doc/api/html/*
%endif

%files calendar
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/calendar.conf
%{_libdir}/asterisk/modules/res_calendar.so
%{_libdir}/asterisk/modules/res_calendar_caldav.so
%{_libdir}/asterisk/modules/res_calendar_ews.so
%{_libdir}/asterisk/modules/res_calendar_icalendar.so

%if 0%{?freepbx}
%files configs
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/chan_dahdi.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/dundi.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/logger.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/mgcp.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/phoneprov.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/skinny.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/smdi.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/unistim.conf
%endif

%if 0%{?corosync}
%files corosync
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/res_corosync.conf
%{_libdir}/asterisk/modules/res_corosync.so
%endif

%files curl
%doc contrib/scripts/dbsep.cgi
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/dbsep.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/res_curl.conf
%{_libdir}/asterisk/modules/func_curl.so
%{_libdir}/asterisk/modules/res_config_curl.so
%{_libdir}/asterisk/modules/res_curl.so

%files dahdi
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/meetme.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/chan_dahdi.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/ss7.timers
%{_libdir}/asterisk/modules/app_flash.so
%if 0%{?meetme} 
%{_libdir}/asterisk/modules/app_meetme.so
%endif
%{_libdir}/asterisk/modules/app_dahdiras.so
%{_libdir}/asterisk/modules/chan_dahdi.so
%{_libdir}/asterisk/modules/codec_dahdi.so
%{_libdir}/asterisk/modules/res_timing_dahdi.so
/usr/share/dahdi/span_config.d/40-asterisk

%files devel
%{_libdir}/libasteriskssl.so
%dir %{_includedir}/asterisk
%dir %{_includedir}/asterisk/doxygen
%{_includedir}/asterisk.h
%{_includedir}/asterisk/*.h
%{_includedir}/asterisk/doxygen/*.h

%files doc
%doc *.txt ChangeLog BUGS CREDITS configs
#%doc doc/configs/*


%files fax
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/res_fax.conf
%{_libdir}/asterisk/modules/res_fax.so
%{_libdir}/asterisk/modules/res_fax_spandsp.so

%files festival
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/festival.conf
%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/festival
%{_libdir}/asterisk/modules/app_festival.so

%files hep
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/hep.conf
%{_libdir}/asterisk/modules/res_hep.so
%{_libdir}/asterisk/modules/res_hep_rtcp.so
%{_libdir}/asterisk/modules/res_hep_pjsip.so

%if 0%{?ices}
%files ices
%doc contrib/asterisk-ices.xml
%{_libdir}/asterisk/modules/app_ices.so
%endif

%if 0%{?jack}
%files jack
%{_libdir}/asterisk/modules/app_jack.so
%endif

%if 0%{?ldap}
%files ldap
#doc doc/ldap.txt
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/res_ldap.conf
%{_libdir}/asterisk/modules/res_config_ldap.so
%endif

%files lua
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/extensions.lua
%{_libdir}/asterisk/modules/pbx_lua.so

%files mgcp
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/mgcp.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/res_pktccops.conf
%{_libdir}/asterisk/modules/chan_mgcp.so
%{_libdir}/asterisk/modules/res_pktccops.so

%files minivm
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/extensions_minivm.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/minivm.conf
%{_libdir}/asterisk/modules/app_minivm.so

%if 0%{misdn}
%files misdn
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/misdn.conf
%{_libdir}/asterisk/modules/chan_misdn.so
%endif

%files mwi-external
%{_libdir}/asterisk/modules/res_mwi_external.so
%{_libdir}/asterisk/modules/res_mwi_external_ami.so
%{_libdir}/asterisk/modules/res_stasis_mailbox.so

%if 0%{odbc}
%files odbc
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/cdr_adaptive_odbc.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/cdr_odbc.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/cel_odbc.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/func_odbc.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/res_odbc.conf
%{_libdir}/asterisk/modules/cdr_adaptive_odbc.so
%{_libdir}/asterisk/modules/cdr_odbc.so
%{_libdir}/asterisk/modules/cel_odbc.so
%{_libdir}/asterisk/modules/func_odbc.so
%{_libdir}/asterisk/modules/res_config_odbc.so
%{_libdir}/asterisk/modules/res_odbc.so
%{_libdir}/asterisk/modules/res_odbc_transaction.so
%endif

%files oss
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/oss.conf
%{_libdir}/asterisk/modules/chan_oss.so

%if 0%{postgresql}
%files pgsql
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/cdr_pgsql.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/cel_pgsql.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/res_pgsql.conf
%doc contrib/realtime/postgresql/*.sql
%{_libdir}/asterisk/modules/cdr_pgsql.so
%{_libdir}/asterisk/modules/cel_pgsql.so
%{_libdir}/asterisk/modules/res_config_pgsql.so
%endif

%if 0%{phone}
%files phone
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/phone.conf
%{_libdir}/asterisk/modules/chan_phone.so
%endif

%files portaudio
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/console.conf
%{_libdir}/asterisk/modules/chan_console.so

%if 0%{radius}
%files radius
%{_libdir}/asterisk/modules/cdr_radius.so
%{_libdir}/asterisk/modules/cel_radius.so
%endif

%files skinny
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/skinny.conf
%{_libdir}/asterisk/modules/chan_skinny.so

%if 0%{snmp}
%files snmp
#doc doc/asterisk-mib.txt
#doc doc/digium-mib.txt
#doc doc/snmp.txt
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/res_snmp.conf
#%%{_datadir}/snmp/mibs/DIGIUM-MIB.txt
%{_libdir}/asterisk/modules/res_snmp.so
%endif

%files sqlite3
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/cdr_sqlite3_custom.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/cel_sqlite3_custom.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/res_config_sqlite.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/res_config_sqlite3.conf
%{_libdir}/asterisk/modules/cdr_sqlite3_custom.so
%{_libdir}/asterisk/modules/cel_sqlite3_custom.so
%{_libdir}/asterisk/modules/res_config_sqlite3.so

%files tds
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/cdr_tds.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/cel_tds.conf
%{_libdir}/asterisk/modules/cdr_tds.so
%{_libdir}/asterisk/modules/cel_tds.so

%files unistim
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/unistim.conf
%{_libdir}/asterisk/modules/chan_unistim.so

%files voicemail
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/voicemail.conf
%{_libdir}/asterisk/modules/func_vmcount.so

%if 0%{?imap}
%files voicemail-imapstorage
%{_libdir}/asterisk/modules/app_directory_imap.so
%{_libdir}/asterisk/modules/app_voicemail_imap.so
%endif

%files voicemail-odbcstorage
#doc doc/voicemail_odbc_postgresql.txt
%{_libdir}/asterisk/modules/app_directory_odbc.so
%{_libdir}/asterisk/modules/app_voicemail_odbc.so

%files voicemail-plain
%{_libdir}/asterisk/modules/app_directory_plain.so
%{_libdir}/asterisk/modules/app_voicemail_plain.so

%if 0%{?xmpp}
%files xmpp
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/motif.conf
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/samples-%{version}/xmpp.conf
%{_libdir}/asterisk/modules/chan_motif.so
%{_libdir}/asterisk/modules/res_xmpp.so
%endif

%changelog
* Thu Sep 16 2021 Stefano Fancello <stefano.fancello@nethesis.it> - 13.38.3-1
- Update Asterisk to 13.38.3 - NethServer/dev#6550

* Fri Feb 26 2021 Stefano Fancello <stefano.fancello@nethesis.it> - 13.38.2-1
- Update Asterisk to 13.38.2 - NethServer/dev#6433

* Wed Jan 20 2021 Stefano Fancello <stefano.fancello@nethesis.it> - 13.38.1-1
- Update Asterisk to 13.38.1 - NethServer/dev#6386

* Tue Nov 17 2020 Stefano Fancello <stefano.fancello@nethesis.it> - 13.37.1-1
- Update Asterisk to 13.37.1 - NethServer/dev#6325

* Thu Nov 05 2020 Stefano Fancello <stefano.fancello@nethesis.it> - 13.37.0-1
- Update Asterisk to 13.37.0 - NethServer/dev#6315

* Tue Sep 29 2020 Stefano Fancello <stefano.fancello@nethesis.it> - 13.35.0-1
- Asterisk 13.35.0 (2020-07-16) - NethServer/dev#6260

* Mon Aug 31 2020 Stefano Fancello <stefano.fancello@nethesis.it> - 13.34.0-1
- Asterisk 13: update to 13.34.0 - NethServer/dev#6223

* Fri May 29 2020 Stefano Fancello <stefano.fancello@nethesis.it> - 13.29.2-2
- Use libresample from EPEL - Bug NethServer/dev#6187
- Build requires dahdi-tools-devel instead of libtonezone-devel - Bug NethServer/dev#6172

* Mon Dec 02 2019 Stefano Fancello <stefano.fancello@nethesis.it> - 13.29.2-1
- Asterisk 13: update to 13.29.2 - Bug NethServer/dev#5948

* Tue Sep 17 2019 Stefano Fancello <stefano.fancello@nethesis.it> - 13.28.1-1
- Asterisk 13: update to 13.28.1 for security reasons - Bug NethServer/dev#5828

* Mon Sep 02 2019 Stefano Fancello <stefano.fancello@nethesis.it> - 13.28.0-1
- Update Asterisk to 13.28.0 - NethServer/dev#5787
- Remove increase-max-stack.patch Patch no more needed since 512 is now default unless Asterisk is compiled with LOW_MEMORY flag

* Mon Apr 01 2019 Stefano Fancello <stefano.fancello@nethesis.it> - 13.25.0-1
- Asterisk13: update from 13.19 to 13.25 - NethServer/dev#5739
- Update from 13.24 to 13.25
- Release 13.24.0

* Thu Mar 05 2019 Stefano Fancello <stefano.fancello@nethesis.it> - 13.25.0-1
- Update from 13.24 to 13.25
* Wed Jan 23 2019 Stefano Fancello <stefano.fancello@nethesis.it> - 13.24.0-1
- Update from 13.19 to 13.24

* Thu Jul 26 2018 Stefano Fancello <stefano.fancello@nethesis.it> - 13.19.1-1
- Asterisk 13: update from 13.17 to 13.19 - NethServer/dev#5524
- Remove iksemel requires since it's no more maintained on epel NethServer/dev#5524
- Update lazymember patch
- Removed unbuilt docs
- Add increase-max-stack patch

* Thu Jan 25 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 13.17.2-3-1
- PBX: Asterisk logs aren't rotated - Bug NethServer/dev#5411

* Wed Nov 15 2017 Stefano Fancello <stefano.fancello@nethesis.it> 13.17.2-2
- Change Asterisk user home from /var/lib/asterisk to /home/asterisk

* Wed Nov 08 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> 13.17.2-1
- Update Asterisk 13 packages - NethServer/dev#5375
- Security fix: http://downloads.asterisk.org/pub/security/AST-2017-008.html

* Fri Jun 13 2014 Derek Carter <derek.carter@schmoozecom.com> 12.3.2-1
- Version Bump

* Wed Jun 11 2014 Derek Carter <derek.carter@schmoozecom.com> 12.3.1-1
- New SHMZ common build system

* Fri Oct 07 2011 Jason Parker <jparker@digium.com> - 1.8.7.0-1
- Update to 1.8.7.0

* Thu Sep 01 2011 Jason Parker <jparker@digium.com> - 1.8.6.0-1
- Update to 1.8.6.0

* Mon Jul 11 2011 Jason Parker <jparker@digium.com> - 1.8.5.0-1
- Update to 1.8.5.0

* Tue Jun 28 2011 Jason Parker <jparker@digium.com> - 1.8.4.4-1
- Update to 1.8.4.4

* Thu Jun 23 2011 Jason Parker <jparker@digium.com> - 1.8.4.3-1
- Update to 1.8.4.3

* Thu Jun 02 2011 Jason Parker <jparker@digium.com> - 1.8.4.2-1
- Update to 1.8.4.2

* Fri May 20 2011 Jason Parker <jparker@digium.com> - 1.8.4.1-1
- Update to 1.8.4.1

* Fri May 13 2011 Jason Parker <jparker@digium.com> - 1.8.4-1
- Update to 1.8.4

* Thu Apr 21 2011 Jason Parker <jparker@digium.com> - 1.8.3.3-1
- Update to 1.8.3.3

* Thu Mar 17 2011 Jason Parker <jparker@digium.com> - 1.8.3.2-1
- Update to 1.8.3.2

* Wed Mar 16 2011 Jason Parker <jparker@digium.com> - 1.8.3.1-1
- Update to 1.8.3.1

* Mon Feb 28 2011 Jason Parker <jparker@digium.com> - 1.8.3-1
- Update to 1.8.3

* Mon Feb 21 2011 Jason Parker <jparker@digium.com> - 1.8.2.4-1
- Update to 1.8.2.4

* Thu Jan 20 2011 Jason Parker <jparker@digium.com> - 1.8.2.2-1
- Update to 1.8.2.2

* Tue Jan 18 2011 Jason Parker <jparker@digium.com> - 1.8.2.1-1
- Update to 1.8.2.1

* Fri Jan 14 2011 Jason Parker <jparker@digium.com> - 1.8.2-1
- Update to 1.8.2

* Mon Dec 13 2010 Jason Parker <jparker@digium.com> - 1.8.1.1-1
- Update to 1.8.1.1

* Fri Oct 22 2010 Jason Parker <jparker@digium.com> - 1.8.0-1
- Update to 1.8.0

* Mon Oct 18 2010 Jason Parker <jparker@digium.com> - 1.8.0-rc5-1
- Update to 1.8.0-rc5

* Mon Oct 18 2010 Jason Parker <jparker@digium.com> - 1.8.0-rc4-1
- Update to 1.8.0-rc4

* Fri Oct 08 2010 Jason Parker <jparker@digium.com> - 1.8.0-rc3-1
- Update to 1.8.0-rc3

* Thu Sep 23 2010 Jason Parker <jparker@digium.com> - 1.8.0-rc2-1
- Update to 1.8.0-rc2

* Tue Sep 21 2010 Jason Parker <jparker@digium.com> - 1.8.0-beta5-1
- Initial 1.8 build.
