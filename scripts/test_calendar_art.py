from datetime import date, timedelta
import unittest
import xml.etree.ElementTree as ET

from calendar_art import blue_calendar


class CalendarArtworkTests(unittest.TestCase):
    def test_partial_final_week_has_inactive_tiles(self):
        start = date(2025, 11, 2)
        source = '<div data-to="2026-11-02"><h2>1 contributions in the last year</h2>'
        for index in range(366):
            level = 1 if index == 365 else 0
            source += f'<td data-date="{start + timedelta(days=index)}" data-level="{level}"></td>'
        source += '</div>'
        for mobile in [False, True]:
            for light in [False, True]:
                with self.subTest(mobile=mobile, light=light):
                    svg = ET.fromstring(blue_calendar(source, mobile=mobile, light=light))
                    tiles = list(svg.iter('{http://www.w3.org/2000/svg}rect'))
                    self.assertEqual(len(tiles), 371, 'The final week must contain all seven tiles')
                    self.assertEqual(sum(tile.get('class') == 'active' for tile in tiles), 1)
                    self.assertTrue(all(tile.get('class') is None for tile in tiles[-5:]))
                    self.assertEqual(len({tile.get('fill') for tile in tiles[-5:]}), 1)


if __name__ == '__main__':
    unittest.main()
