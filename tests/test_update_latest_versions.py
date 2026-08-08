import unittest

from scripts.update_latest_versions import update_latest_versions


class UpdateLatestVersionsTests(unittest.TestCase):
    def test_adds_missing_versions_and_updates_stale_versions(self) -> None:
        plugins: list[dict[str, object]] = [
            {"name": "missing-version"},
            {"name": "stale-version", "latest_version_available": "1.0.0"},
        ]
        versions = {"missing-version": "2.0.0", "stale-version": "1.1.0"}

        changed = update_latest_versions(plugins, versions.__getitem__)

        self.assertTrue(changed)
        self.assertEqual(plugins[0]["latest_version_available"], "2.0.0")
        self.assertEqual(plugins[1]["latest_version_available"], "1.1.0")

    def test_reports_no_change_when_versions_are_current(self) -> None:
        plugins: list[dict[str, object]] = [
            {"name": "current-version", "latest_version_available": "1.0.0"}
        ]

        changed = update_latest_versions(plugins, lambda _: "1.0.0")

        self.assertFalse(changed)

    def test_rejects_a_plugin_without_a_distribution_name(self) -> None:
        with self.assertRaisesRegex(ValueError, "non-empty string name"):
            update_latest_versions([{"name": ""}], lambda _: "1.0.0")


if __name__ == "__main__":
    unittest.main()
