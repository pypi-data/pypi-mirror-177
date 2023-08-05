"""Test repository classes
"""
from __future__ import annotations

import collections
import fnmatch
import re
from abc import ABC, abstractmethod
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Sequence, Set

from .cmake_builder import CmakeBuilder, PresetCollection
from .test import ConcreteTest, Test


class RepoException(Exception):
    """Base exception for repository errors"""


class TestConfigError(RepoException):
    """Error with test configuration"""


class TestRepositoryBase(ABC):
    """Base class for repositories of tests"""

    @property
    @abstractmethod
    def path(self) -> Path:
        """The path of the repository."""

    @abstractmethod
    def tests(self) -> Sequence[ConcreteTest]:
        """Returns the list of tests for this repository"""
        raise NotImplementedError

    @abstractmethod
    def all_tags(self, test: ConcreteTest) -> Sequence[str]:
        """Return set of tags for a given test."""
        raise NotImplementedError

    def presets(self) -> PresetCollection:
        """Return collection of presets for the tests of this repository"""
        return PresetCollection(*(test.build_preset for test in self.tests()))

    def print_tests(self) -> None:
        """Print out a list of this repository's tests to stdout"""
        for test in self.tests():
            print(test.name)
            print("   Desc:", test.description)
            print("   Tags:", ", ".join(self.all_tags(test)))
            print()


class TestRepository(TestRepositoryBase):
    """A repository of tests in the new format, relying on `test_config.py` files
    for test discovery and configuration.

    Tests are defined a subdirectories of `root_dir` that contain a `test_config.py` file.
    A test specification file named `<root_dir>/some/test/test_config.py`
    will define the test named `some/test`.

    Each test specification file must be a valid Python script,
    and is expected to define a variable `test` of the class `Test`,
    which encapsulates all the required information for this test.
    """

    def __init__(self, root_dir: Path, builder: CmakeBuilder):
        self.root_dir = root_dir
        self.builder = builder

    @property
    def path(self) -> Path:
        """Path to the directory of this repository"""
        return Path(self.root_dir)

    @lru_cache(maxsize=None)
    def all_tags(self, test: ConcreteTest) -> Sequence[str]:
        tags = set(self.builder.preset_tags(test.build_preset))
        tags.update(test.run.auto_tags(test.path), test.tags)

        is_word = re.compile(r"\w+")

        if not all(is_word.fullmatch(tag) for tag in tags):
            raise TestConfigError(f"All tags must be alphanumeric, found {tags}")

        return sorted(tags)

    def tests(self) -> Sequence[ConcreteTest]:
        def test_from_config(config_fname: Path) -> ConcreteTest:
            with config_fname.open("rb") as config_file:
                code = compile(config_file.read(), config_fname, "exec")
            variables: Dict[str, Any] = {}
            exec(code, variables)
            if "test" not in variables:
                raise TestConfigError(f"'{config_fname}': variable 'test' not defined")

            test = variables["test"]
            if not isinstance(test, Test):
                raise TestConfigError(
                    f"'{config_fname}': variable 'test' is not an instance of Test"
                )

            parent_dir = config_fname.parent
            return ConcreteTest(
                build_preset=test.build_preset,
                run=test.run,
                self_check=test.self_check,
                comparison_check=test.comparison_check,
                description=test.description,
                tags=test.tags,
                # Set name from relative path starting from root_dir
                name=str(parent_dir.relative_to(self.path)),
                path=parent_dir,
            )

        tests = [
            test_from_config(config_fname)
            for config_fname in sorted(self.path.glob("**/test_config.py"))
        ]

        # Check that tests have unique names;
        # should always be the case when named from filesystem locations,
        # but being careful can't hurt
        name_count = collections.Counter([test.name for test in tests])
        duplicate_names = [name for (name, count) in name_count.items() if count > 1]
        if duplicate_names:
            raise TestConfigError(
                f"repository {self.path}: "
                f"tests with duplicate names: {duplicate_names}"
            )
        return tests


class TestsMatchingPatterns(TestRepositoryBase):
    """
    Select tests from a parent test repository whenever their
    names match any of the provided `fnmatch` (glob-style) patterns.
    """

    def __init__(self, repo: TestRepositoryBase, patterns: Sequence[str]):
        self.repo = repo
        self.patterns = patterns

    @property
    def path(self) -> Path:
        return self.repo.path

    def all_tags(self, test: ConcreteTest) -> Sequence[str]:
        return self.repo.all_tags(test)

    def tests(self) -> Sequence[ConcreteTest]:
        return [
            test
            for test in self.repo.tests()
            if any(fnmatch.fnmatch(test.name, pattern) for pattern in self.patterns)
        ]


def _tag_matches(tag: str, tag_set: Set[str]) -> bool:
    if tag.startswith("~"):
        return tag[1:] not in tag_set
    return tag in tag_set


class TestsWithAnyTag(TestRepositoryBase):
    """Selects tests matching any of the tags"""

    def __init__(self, repo: TestRepositoryBase, tags: Sequence[str]):
        self.repo = repo
        self.tags = tags

    @property
    def path(self) -> Path:
        return self.repo.path

    def all_tags(self, test: ConcreteTest) -> Sequence[str]:
        return self.repo.all_tags(test)

    def tests(self) -> Sequence[ConcreteTest]:
        return [
            test
            for test in self.repo.tests()
            if any(_tag_matches(tag, set(self.all_tags(test))) for tag in self.tags)
        ]


class TestsWithAllTags(TestRepositoryBase):
    """Selects tests matching all of the tags"""

    def __init__(self, repo: TestRepositoryBase, tags: Sequence[str]):
        self.repo = repo
        self.tags = tags

    @property
    def path(self) -> Path:
        return self.repo.path

    def all_tags(self, test: ConcreteTest) -> Sequence[str]:
        return self.repo.all_tags(test)

    def tests(self) -> Sequence[ConcreteTest]:
        # Return tests whose tags are a superset of tag selection
        return [
            test
            for test in self.repo.tests()
            if all(_tag_matches(tag, set(self.all_tags(test))) for tag in self.tags)
        ]
