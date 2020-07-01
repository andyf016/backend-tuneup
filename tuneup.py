#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tuneup assignment

Use the timeit and cProfile libraries to find bad code.
"""

__author__ = "Andrew Fillenwarth, special thanks to \
              Sebastiaan Mathot and Corey Schafer on youtube"

import cProfile
import pstats
# import functools
import timeit
import io


def profile(func):
    """A cProfile decorator function that can be used to
    measure performance.
    """
    # This profiling decorator was adapted from the Python 3.6 Docs
    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = func(*args, **kwargs)
        pr.disable()
        ps = pstats.Stats(pr).strip_dirs().sort_stats('cumulative')
        ps.print_stats(5)
        #string = io.StringIO()
        #sortby = 'cumulative'
        #ps = pstats.Stats(pr, stream=string).sort_stats(sortby)
        #ps.print_stats()
        #print(string.getvalue())
        return retval

    return inner


def read_movies(src):
    """Returns a list of movie titles."""
    print(f'Reading file: {src}')
    with open(src, 'r') as f:
        return f.read().splitlines()


@profile
def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list."""
    movies = read_movies(src)
    movies = [movie.lower() for movie in movies]
    movies.sort()
    duplicates = [movie1 for movie1, movie2 in zip(movies[:-1],
                  movies[1:]) if movie1 == movie2]  # Sebastiaan Mathot
    return duplicates


def timeit_helper():
    """Part A: Obtain some profiling measurements using timeit."""
    t = timeit.Timer(stmt='find_duplicate_movies("movies.txt")', setup='from __main__ import find_duplicate_movies')
    result = t.repeat(repeat=7, number=3)
    best_time = min(result) / float(3)
    print('Best time across 7 repeats of 3 runs per repeat: {} sec '.format(best_time))
    


def main():
    """Computes a list of duplicate movie entries."""
    result = find_duplicate_movies('movies.txt')
    timeit_helper()
    print(f'Found {len(result)} duplicate movies:')
    print('\n'.join(result))
    


if __name__ == '__main__':
    main()
