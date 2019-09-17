import os
import os.path
import pytest
import sh

from buddy.make_symlink import add_relative_symlink


class TestLinkMaker(object):
    def test_make_fresh_link(self, tmpdir):
        # - make a temp dir
        # - add a file
        # - use make_soft_link to make a link to that file from a previously
        # non-existing location
        target = "abc.txt"
        link = "abc.link"
        with sh.pushd(tmpdir):
            sh.touch(target)
            add_relative_symlink(target, link)
            assert os.path.islink(link)
            assert os.readlink(link) == target

    def test_dont_throw_error_if_link_points_to_target(self, tmpdir, mocker):
        # - make a temp dir
        # - add a file
        # - make a soft link to that file from a link-name
        # - use make_soft_link to make a link to that file from the same link-name
        # - check that the second call did not call os.symlink
        target = "abc.txt"
        link = "abc.link"
        with sh.pushd(tmpdir):
            sh.touch(target)
            add_relative_symlink(target, link)
            add_relative_symlink(target, link)
            assert os.path.islink(link)
            assert os.readlink(link) == target

    def test_throw_error_if_rewriting_link(self, tmpdir, mocker):
        # - make a temp dir
        # - add two files
        # - make a soft link to one file
        # - attempt to make the link point to the other file
        # - check that the second call throws an error
        target1 = "abc.txt"
        target2 = "def.txt"
        link = "abc.link"
        with sh.pushd(tmpdir):
            sh.touch(target1)
            sh.touch(target2)
            add_relative_symlink(target1, link)
            with pytest.raises(FileExistsError):
                add_relative_symlink(target2, link)

    def test_correct_relative_paths(self, tmpdir):
        # - make a tempdir
        # - add two directories A and B
        # - add a file to A
        # - make a link to A/the_file from in B using python
        # - make a link to A/the_file from in B using relative paths in sh
        # - test that the the two links have the same representation
        with sh.pushd(tmpdir):
            sh.mkdir("A")
            sh.mkdir("B")
            target = "A/some_file"
            sh.touch(target)
            link1 = "B/link1"
            link2 = "B/link2"
            add_relative_symlink(target, link1)
            sh.ln("--symbolic", "--relative", target, link2)
            assert os.readlink(link1) == os.readlink(link2)

    def test_error_if_linkloc_exists_but_is_not_a_link(self, tmpdir):
        # - make a tempdir
        # - add two files
        # - make a link from one file to the other
        # - making the link should fail since a (non-link) file exists at the
        # link location
        with sh.pushd(tmpdir):
            sh.touch("a.txt")
            sh.touch("b.txt")
            with pytest.raises(FileExistsError):
                add_relative_symlink("a.txt", "b.txt")

    def test_subdir_is_made_when_subdir_doesnt_exist(self, tmpdir):
        # - make a tempdir
        # - add a file
        # - make a link from a location in a non-existing subdir to the file
        with sh.pushd(tmpdir):
            sh.touch("a.txt")
            link = "subdir/b.txt"
            add_relative_symlink("a.txt", link)
            assert os.path.islink(link)
            assert os.readlink(link) == "../a.txt"

    def test_error_if_target_is_missing(self, tmpdir):
        # - make a tempdir
        # - attempt to make a link from a file to another (nonexisting) file
        # - error should be thrown
        with sh.pushd(tmpdir):
            with pytest.raises(FileNotFoundError):
                add_relative_symlink("doesnt_exist.txt", "some_link")
