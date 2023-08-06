"""
A special example of Calliope playlist generation using the Python API.

Generates 60 minute playlists using a variety of different generators,
aiming to focus on a single factor each.
"""

import argparse
from datetime import date, datetime, timedelta
import logging
import os
import pathlib
import random
import sys

import calliope

log = logging.getLogger()


DURATION = 60 * 60


class ConfigError(Exception):
    pass


class Config(calliope.config.Configuration):
    """Config is stored in 'special_mix' section of calliope.conf"""

    def __init__(self, sync=True, tracker_http_endpoint=None):
        super(Config, self).__init__()
        self._sync = sync
        self._tracker_http_endpoint = tracker_http_endpoint

    def content_resolver(self):
        return calliope.tracker.TrackerClient(
            http_endpoint=self._tracker_http_endpoint
        )

    def listen_history_provider(self):
        provider = self.get('special-mix', 'listen-history-provider') or 'listenbrainz'

        user = self.get('special-mix', 'listen-history-user')
        if user is None:
            user = self.get('listenbrainz', 'user')
        if user is None:
            raise ConfigError(
                "No user defined. Please set special-mix.listen-history-user "
                "in calliope.conf.")

        if provider == 'listenbrainz' or provider is None:
            log.debug("Set up Listenbrainz provider with username %s", user)
            return calliope.listenbrainz.listens.load(user)
        elif provider == 'lastfm':
            log.debug("Set up Last.fm provider with username %s", user)
            return calliope.lastfm.history.load(user)
        else:
            raise ConfigError(f"Invalid listen history provider: {provider}")

    def sync(self):
        return self._sync


class PlaylistGenerator():
    def __init__(self, config: Config):
        self.config = config


class ListenHistoryMixin():
    def setup_listen_history(self):
        self.listen_history = self.config.listen_history_provider()

        if self.config.sync():
            log.info("Syncing from listen history provider")
            sync_op = self.listen_history.prepare_sync()
            for page in sync_op.pages():
                sync_op.process_page(page)


class DiscoveredInTimePeriod(PlaylistGenerator, ListenHistoryMixin):
    """
    Tracks where first play was in specified time period.
    """

    def __init__(self, config: Config, span='year', period=None, minimum_tracks=100):
        super(DiscoveredInTimePeriod, self).__init__(config)
        self.span = span
        self.period = None
        self.minimum_tracks = 100

    def _add_year(self, d):
        try:
            return d.replace(year = d.year + 1)
        except ValueError:
            return d + (date(d.year + 1, 1, 1) - date(d.year, 1, 1))

    def setup(self):
        self.setup_listen_history()

    def run(self):
        histogram = self.listen_history.histogram(bucket=self.span)

        if self.period is None:
            active_periods = list(sorted(
                entry.bucket
                for entry in histogram if entry.count > self.minimum_tracks
            ))
            self.period = random.choice(active_periods)

        period_start = datetime.fromisoformat(self.period)
        period_end = self._add_year(period_start)

        log.info("Query tracks for period %s -> %s", period_start, period_end)
        all_tracks = list(self.listen_history.tracks(
            first_play_since=period_start, first_play_before=period_end))
        log.info("Tracks: %i", len(all_tracks))

        tracker = self.config.content_resolver()
        resolved_tracks = list(calliope.tracker.resolve_content(tracker, all_tracks))

        tracks_with_durations = [
            t for t in resolved_tracks if 'duration' in t and 'location' in t
        ]
        log.info("Tracks with location and duration resolved: %i", len(tracks_with_durations))

        constraints = [
            calliope.select.constraints.PlaylistDurationConstraint(
                DURATION * 1000, DURATION * 1000
            )
        ]

        playlist = list(calliope.select.select(
            calliope.shuffle.shuffle(tracks_with_durations),
            constraints
        ))

        if len(playlist) == 0:
            raise RuntimeError("Empty playlist generated.")

        playlist[0]['playlist.title'] = f"Discoveries of {period_start.year}"
        playlist[0]['playlist.generator'] = "special_mix.DiscoveredInTimePeriod"

        return playlist


def argument_parser():
    parser = argparse.ArgumentParser(
        description="Special Mix: playlist generator using Listenbrainz/Last.fm history")
    parser.add_argument('--debug', dest='debug', action='store_true',
                        help="Enable detailed logging to stderr")
    parser.add_argument('--random-seed', '-r',
                        help="Use fixed random number seed.")
    parser.add_argument('--sync', dest='sync', action='store_true')
    parser.add_argument('--no-sync', dest='sync', action='store_false')
    parser.add_argument('--tracker-http-endpoint', metavar="URL", type=str,
                        help="Resolve content using remote Tracker database "
                             "(default is to use local database)")
    parser.add_argument('output', metavar='OUTPUT', type=argparse.FileType('w'),
                        help="Playlist output file (use '-' for stdout)")
    parser.set_defaults(sync=True)
    return parser


def main():
    args = argument_parser().parse_args()

    if args.debug:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    config = Config(sync=args.sync,
                    tracker_http_endpoint=args.tracker_http_endpoint)

    pl = DiscoveredInTimePeriod(config)
    pl.setup()
    playlist = list(pl.run())

    calliope.playlist.write(playlist, args.output)


try:
    main()
except RuntimeError as e:
    sys.stderr.write("ERROR: {}\n".format(e))
    sys.exit(1)
