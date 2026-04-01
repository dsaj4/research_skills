import tempfile
import unittest
from pathlib import Path

import company_wechat_rss


FIXTURES = Path(__file__).resolve().parent / "fixtures"


class CompanyWechatRssTests(unittest.TestCase):
    def test_normalize_company_feeds_supports_feed_ids_shortcut(self):
        company = {
            "company": "Alibaba",
            "feed_ids": ["MP_ALIBABA_CLOUD", "MP_ALIBABA_RESEARCH"],
        }

        feeds = company_wechat_rss.normalize_company_feeds(company)

        self.assertEqual(
            [item.feed_id for item in feeds],
            ["MP_ALIBABA_CLOUD", "MP_ALIBABA_RESEARCH"],
        )
        self.assertTrue(all(item.company == "Alibaba" for item in feeds))

    def test_collect_company_articles_normalizes_json_feed_records(self):
        config = {
            "base_url": "http://127.0.0.1:4000",
            "default_limit": 20,
            "companies": [
                {
                    "company": "Tencent",
                    "feeds": [
                        {
                            "feed_id": "MP_TENCENT_RESEARCH",
                            "account_name": "Tencent Research Institute",
                        }
                    ],
                }
            ],
        }
        catalog = company_wechat_rss.read_json_file(FIXTURES / "sample_feed_catalog.json")
        feed_payload = company_wechat_rss.read_json_file(FIXTURES / "sample_feed_tencent.json")
        client = company_wechat_rss.WeWeRssClient()
        client.fetch_feed_catalog = lambda: catalog

        def fake_fetcher(company_feed, limit, page, update):
            self.assertEqual(company_feed.feed_id, "MP_TENCENT_RESEARCH")
            self.assertEqual(limit, 20)
            self.assertEqual(page, 1)
            self.assertFalse(update)
            return feed_payload

        records, feed_catalog = company_wechat_rss.collect_company_articles(
            config,
            client,
            exported_at="2026-04-01T00:00:00+00:00",
            feed_fetcher=fake_fetcher,
        )

        self.assertEqual(feed_catalog, catalog)
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["company"], "Tencent")
        self.assertEqual(records[0]["feed_id"], "MP_TENCENT_RESEARCH")
        self.assertEqual(records[0]["public_account"], "Tencent Research Institute")
        self.assertEqual(records[0]["title"], "AI Industry Outlook")
        self.assertEqual(
            records[0]["article_url"],
            "https://mp.weixin.qq.com/s/article-001",
        )
        self.assertEqual(
            records[0]["source_feed_url"],
            "http://127.0.0.1:4000/feeds/MP_TENCENT_RESEARCH.json",
        )

    def test_export_company_data_writes_json_csv_and_manifest(self):
        config_path = FIXTURES / "tmp_config.json"
        config_payload = {
            "base_url": "http://127.0.0.1:4000",
            "default_limit": 20,
            "companies": [
                {
                    "company": "Tencent",
                    "feed_ids": ["MP_TENCENT_RESEARCH"],
                }
            ],
        }
        company_wechat_rss.write_json_file(config_path, config_payload)

        catalog = company_wechat_rss.read_json_file(FIXTURES / "sample_feed_catalog.json")
        feed_payload = company_wechat_rss.read_json_file(FIXTURES / "sample_feed_tencent.json")

        original_collect = company_wechat_rss.collect_company_articles

        def fake_collect(config, client, update=False, exported_at=None, feed_fetcher=None):
            exported_at = exported_at or "2026-04-01T00:00:00+00:00"
            records = company_wechat_rss.normalize_article_record(
                company_feed=company_wechat_rss.CompanyFeed(
                    company="Tencent",
                    feed_id="MP_TENCENT_RESEARCH",
                    account_name="Tencent Research Institute",
                ),
                feed_payload=feed_payload,
                feed_catalog_index=company_wechat_rss.build_feed_catalog_index(catalog),
                exported_at=exported_at,
            )
            return records, catalog

        company_wechat_rss.collect_company_articles = fake_collect
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                output_paths = company_wechat_rss.export_company_data(
                    config_path=config_path,
                    output_root=Path(tmpdir),
                    run_label="test-run",
                )

                self.assertTrue(output_paths["json_path"].exists())
                self.assertTrue(output_paths["csv_path"].exists())
                self.assertTrue(output_paths["manifest_path"].exists())

                csv_text = output_paths["csv_path"].read_text(encoding="utf-8-sig")
                self.assertIn("company,feed_id,public_account", csv_text)

                manifest = company_wechat_rss.read_json_file(output_paths["manifest_path"])
                self.assertEqual(manifest["record_count"], 2)
                self.assertEqual(manifest["company_count"], 1)
        finally:
            company_wechat_rss.collect_company_articles = original_collect
            if config_path.exists():
                config_path.unlink()


if __name__ == "__main__":
    unittest.main()
