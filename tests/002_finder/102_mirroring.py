# -*- coding: utf-8 -*-
import os


def test_relative_001(settings, finder):
    """
    Mirror all compilable sources in relative mode
    """
    result = finder.mirror_sources(
        os.path.join(settings.sample_path, 'components')
    )

    assert result == [
        ('twin_2.scss', 'twin_2.css'),
        ('twin_3.scss', 'twin_3.css'),
    ]


def test_absolute_002(settings, finder):
    """
    Mirror all compilable sources in absolute mode
    """
    result = finder.mirror_sources(
        os.path.join(settings.sample_path, 'components'),
        targetdir=settings.tests_path
    )

    assert result == [
        (
            os.path.join(settings.sample_path, 'components', 'twin_2.scss'),
            os.path.join(settings.tests_path, 'twin_2.css')
        ),
        (
            os.path.join(settings.sample_path, 'components', 'twin_3.scss'),
            os.path.join(settings.tests_path, 'twin_3.css')
        ),
    ]


def test_relative_recursive_003(settings, finder):
    """
    Mirror all compilable sources in relative mode
    """
    result = finder.mirror_sources(settings.sample_path)

    assert result == [
        ('main_basic.scss', 'main_basic.css'),
        ('main_circular_0.scss', 'main_circular_0.css'),
        ('main_circular_1.scss', 'main_circular_1.css'),
        ('main_circular_2.scss', 'main_circular_2.css'),
        ('main_circular_3.scss', 'main_circular_3.css'),
        ('main_circular_4.scss', 'main_circular_4.css'),
        ('main_circular_5.scss', 'main_circular_5.css'),
        ('main_circular_bridge.scss', 'main_circular_bridge.css'),
        ('main_commented.scss', 'main_commented.css'),
        ('main_depth_import-1.scss', 'main_depth_import-1.css'),
        ('main_depth_import-2.scss', 'main_depth_import-2.css'),
        ('main_depth_import-3.scss', 'main_depth_import-3.css'),
        ('main_encoding.scss', 'main_encoding.css'),
        ('main_error.scss', 'main_error.css'),
        ('main_syntax.scss', 'main_syntax.css'),
        ('main_twins_1.scss', 'main_twins_1.css'),
        ('main_twins_2.scss', 'main_twins_2.css'),
        ('main_twins_3.scss', 'main_twins_3.css'),
        ('main_using_libs.scss', 'main_using_libs.css'),
        ('main_with_subimports.scss', 'main_with_subimports.css'),
        ('components/twin_2.scss', 'components/twin_2.css'),
        ('components/twin_3.scss', 'components/twin_3.css'),
    ]


def test_absolute_recursive_004(settings, finder):
    """
    Mirror all compilable sources in absolute mode
    """
    # To avoid to write every os path join
    absolutize = lambda x, y: (  # noqa: E731
        os.path.join(settings.sample_path, x),
        os.path.join(settings.tests_path, y)
    )

    result = finder.mirror_sources(
        settings.sample_path,
        targetdir=settings.tests_path
    )

    assert result == [
        absolutize('main_basic.scss', 'main_basic.css'),
        absolutize('main_circular_0.scss', 'main_circular_0.css'),
        absolutize('main_circular_1.scss', 'main_circular_1.css'),
        absolutize('main_circular_2.scss', 'main_circular_2.css'),
        absolutize('main_circular_3.scss', 'main_circular_3.css'),
        absolutize('main_circular_4.scss', 'main_circular_4.css'),
        absolutize('main_circular_5.scss', 'main_circular_5.css'),
        absolutize('main_circular_bridge.scss', 'main_circular_bridge.css'),
        absolutize('main_commented.scss', 'main_commented.css'),
        absolutize('main_depth_import-1.scss', 'main_depth_import-1.css'),
        absolutize('main_depth_import-2.scss', 'main_depth_import-2.css'),
        absolutize('main_depth_import-3.scss', 'main_depth_import-3.css'),
        absolutize('main_encoding.scss', 'main_encoding.css'),
        absolutize('main_error.scss', 'main_error.css'),
        absolutize('main_syntax.scss', 'main_syntax.css'),
        absolutize('main_twins_1.scss', 'main_twins_1.css'),
        absolutize('main_twins_2.scss', 'main_twins_2.css'),
        absolutize('main_twins_3.scss', 'main_twins_3.css'),
        absolutize('main_using_libs.scss', 'main_using_libs.css'),
        absolutize('main_with_subimports.scss', 'main_with_subimports.css'),
        absolutize('components/twin_2.scss', 'components/twin_2.css'),
        absolutize('components/twin_3.scss', 'components/twin_3.css'),
    ]


def test_relative_excludes_005(settings, finder):
    """
    Mirror allowed compilable sources in relative mode
    """
    excludes = [
        'main_error.scss',
        'main_circular_5.scss',
        'main_circular_0.scss',
        'main_circular_4.scss',
        'main_circular_3.scss',
        'main_circular_1.scss',
        'main_circular_2.scss',
        'main_circular_bridge.scss',
        "main_twins_*.scss",
        '*/twin_*.scss',
    ]

    result = finder.mirror_sources(settings.sample_path, excludes=excludes)

    assert result == [
        ('main_basic.scss', 'main_basic.css'),
        ('main_commented.scss', 'main_commented.css'),
        ('main_depth_import-1.scss', 'main_depth_import-1.css'),
        ('main_depth_import-2.scss', 'main_depth_import-2.css'),
        ('main_depth_import-3.scss', 'main_depth_import-3.css'),
        ('main_encoding.scss', 'main_encoding.css'),
        ('main_syntax.scss', 'main_syntax.css'),
        ('main_using_libs.scss', 'main_using_libs.css'),
        ('main_with_subimports.scss', 'main_with_subimports.css'),
    ]
