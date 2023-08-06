Changelog
=========

Unreleased
8.0
----------

  * Examples are now included in the ``calliope_music`` distribution and
    installed as a separate ``calliope_examples`` package. The "Special Mix"
    example can now be executed directly after installation:

    .. code:: bash

        python3 -m calliope_examples.special_mix

  * Meson is now used as the project build system for Python package builds.
    All setuptools configuration has been removed. There should be no
    functional difference with this change.
    :mr:`211`

8.0
---

  * Multiple artists are now returned when you resolve or annotate via
    MusicBrainz and Spotify. This is a change in the data format for
    those subcommands: fields such as `artist_id` are replaced by a
    `artists` list.
    :mr:`205`
  * musicbrainz: The ``annotate --include`` option now supports all values that
    the `MusicBrainz API <https://musicbrainz.org/doc/MusicBrainz_API#Subqueries>`_
    supports.

       * See the full list of keys with ``cpe musicbrainz list-includes``
       * Use ``*`` to select many keys, e.g. ``--include=artist.*`` to select
         all data related to the artist.

    :mr:`200`
  * Other Musicbrainz improvements:

       * The ``annotate`` command no longer calls ``search()`` unless required.
       * More detailed artist data is returned.
         :mr:`201`
       * Fix crash if :func:`calliope.musicbrainz.annotate` is called
         without the ``select_fn`` parameter.

    :mr:`203`
  * Fix some implementation gaps around
    :class:`calliope.cache.CacheLookupResult`.
    :mr:`199`
  * Remove unneccessary reimplementation of SQLite's retry-on-busy handling.
    :mr:`202`
  * Bugfixes:

       * cli: Quiet 'unhandled attribute' warnings from 'musicbrainzngs' library
           when `-v 3`.
           :mr:`199`
       * lastfm-history: Fix database error
           :mr:`208`
       * listenbrainz: Fix import error of bundled pylistenbrainz package (it's bundled awaiting https://github.com/metabrainz/pylistenbrainz/pull/10)
       * listenbrainz-history: Fix error when artist-msid isn't returned
           :mr:`207`
       * More stuff not listed here.

7.1
---

  * Fix a bug in cache migration.
    :mr:`197`

7.0
---

  * Cache expiry is now supported in `calliope.cache` module.
      * The :meth:`calliope.cache.Cache.lookup()` method now
        returns ``(datetime, value)`` instead of ``(bool, value)``.
        Code calling this function may require changes.
      * The :meth:`calliope.cache.Cache.wrap()` method now accepts
        an ``expiry`` parameter.
  * bandcamp: Add `export-band` and `export-album` commands.
    :mr:`192`
  * bandcamp: Add `wishlist` command.
  * example: Fix `collectors/online-to-local.sh`.
    :bug:`96`
  * tests: Use `Tox <https://tox.wiki/>`_ to run tests in virtualenv.
    Minor improvements to Gitlab CI setup and PyPI packaging.

6.0
---

  * examples: Add `special-mix` example.
  * lastfm-history: Add `histogram` command
  * listenbrainz: Fix a bug in 'week' histogram generation

5.0
---

  * tracker: Support querying remote databases over HTTP.
  * listenbrainz: Add `cpe listenbrainz-history histogram` command.
  * musicbrainz: Documentation improvements and bugfixes.
  * select: Add named keyword arguments to all constraints.
  * Default Git branch renamed to 'main'.

4.0
---

 * New `cpe listenbrainz` command to export playlists from
   `Listenbrainz <https://listenbrainz.org/>`_.
   :mr:`178`
 * New `cpe listenbrainz-history` command to cache and query listening history
   from `Listenbrainz <https://listenbrainz.org/>`_.
   :mr:`176`
 * spotify: Export and Import tracks, albums or artists from/into the current
   users' spotify library
   By :user:`lackhove`.
   :mr:`168`
 * Bug fixes.

3.1
---

 * spotify: Fix breakage with Python 3.7.
   By :user:`lackhove`.
   :mr:`164`
 * spotify: Fix a broken testcase
   By :user:`lackhove`.
   :mr:`165`

3.0
---

 * spotify: Use the much improved resolver introduced in 2.0.0 and extend
   playlist import action to use spotify IDs and URIs and update existing
   playlists.
   By :user:`lackhove`.
   :mr:`155`.
 * spotify: Remove the ``--user`` flag, it did not do what it claimed to do.
   :mr:`158`.
 * Document how to get Spotify API keys.
   :mr:`161`.
 * lastfm-history: Move progress bar to stderr.
   :mr:`160`.
 * Other small fixes and documentation improvements.

2.0
---

 * Replace --debug with --verbosity CLI option.
   Thanks to :user:`lackhove`.
   :mr:`149`.
 * Skip tests if module requirements aren't installed.
   Thanks to :user:`lackhove`.
   :mr:`151`.
 * Update CI image with some follow-up fixes.
 * musicbrainz: Add a much improved resolver.
   Thanks to :user:`lackhove`.
   :mr:`148`.
 * spotify: Small improvements to resolver, add playlist import.
   :mr:`150`.
 * youtube: Fix mass playlist export
   :bug:`85`.
