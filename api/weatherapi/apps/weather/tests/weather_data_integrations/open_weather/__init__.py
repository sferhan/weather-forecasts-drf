from vcr_unittest import VCRMixin


class OpenWeatherGatewayVCRMixin(VCRMixin):
    # Called by vcr.py to configure options
    def _get_vcr_kwargs(self, **kwargs):
        return {
            'filter_query_parameters': ['appid'],
            # Change record_mode to preferable value when developing tests ie new_episodes
            'record_mode': 'once',
            **kwargs
        }