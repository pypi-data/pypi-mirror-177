from tickerdax.constants import KeyTypes
from tickerdax.config_base import ConfigBase
from tickerdax.formatting import truncate_datetime


class Downloader(ConfigBase):
    """
    Downloads data from the tickerdax.com data api using a provided config.
    """
    def __init__(self, config, client_kwargs=None, till_now=False):
        super(Downloader, self).__init__(config, client_kwargs)

        # forces the end to be now
        if till_now:
            self._end = truncate_datetime(self._now, self._timeframe)

        self.download()

    def _validate(self):
        super(Downloader, self)._validate()
        self.client.validate_api_key(KeyTypes.REST)

    def download(self):
        """
        Downloads data from the algo trading REST API base on the bot config files.
        """
        downloaded_items = 0
        cached_items = 0
        missing_items = 0

        routes = self._config.get('routes', {})
        if routes:
            for route, symbols in routes.items():
                self._logger.info(f'Downloading {route} history from "{self._start}" to "{self._end}"...')
                self.client.get_route(
                    route=route,
                    symbols=symbols,
                    start=self._start,
                    end=self._end,
                    timeframe=self._timeframe
                )
                self._logger.info(f'Completed {len(self.client.rest_values)} "{route}" downloads')
                cached_items += len(self.client.cached_values)
                downloaded_items += len(self.client.rest_values)
                missing_items += len(self.client.missing_values)

            # show summary
            print(
                f'\nDownload Summary:'
                f'\n\t- {cached_items} items were already cached.'
                f'\n\t- {downloaded_items} items were downloaded.'
                f'\n\t- {missing_items} items were missing.'
            )


if __name__ == '__main__':
    import os
    import logging
    logging.basicConfig(level=logging.INFO)
    Downloader(config=os.path.join(os.path.dirname(__file__), 'example_configs', 'config.yaml'))
