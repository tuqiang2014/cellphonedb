import json

import pandas as pd
from flask import request, Response

from cellphonedb import extensions
from cellphonedb.api_endpoints.web_api.web_api_endpoint_base import WebApiEndpointBase
from utils import utils


class WebEndpointClusterStatisticalAnalysis(WebApiEndpointBase):
    def post(self):
        counts = utils.read_data_from_content_type(request.files['counts_file'], index_column_first=True)
        meta = utils.read_data_from_content_type(request.files['meta_file'], index_column_first=True)
        parameters = json.loads(request.form['parameters'])

        iterations = parameters['iterations']
        threshold = int(parameters['threshold']) / 100

        if not isinstance(counts, pd.DataFrame):
            self.attach_error(
                {'code': 'parsing_error', 'title': 'Error parsing counts file', 'detail': 'Error parsing counts file'})

        if not isinstance(meta, pd.DataFrame):
            self.attach_error(
                {'code': 'parsing_error', 'title': 'Error parsing meta file', 'detail': 'Error parsing meta file'})

        iterations = int(iterations)

        max_iterations = 1000
        min_iterations = 10
        iterations = max_iterations if iterations > max_iterations else iterations
        iterations = min_iterations if iterations < min_iterations else iterations

        if not self._errors:
            pvalues, means, significant_means, mean_pvalue, deconvoluted = \
                extensions.cellphonedb_flask.cellphonedb.method.cluster_statistical_analysis(meta,
                                                                                             counts,
                                                                                             iterations=iterations,
                                                                                             threshold=threshold,
                                                                                             threads=-1,
                                                                                             debug_seed=-1)

            self._attach_csv(pvalues.to_csv(index=False), 'pvalues.csv')
            self._attach_csv(means.to_csv(index=False), 'means.csv')
            self._attach_csv(significant_means.to_csv(index=False), 'significant_means.csv')
            self._attach_csv(mean_pvalue.to_csv(index=False), 'mean_pvalue.csv')
            self._attach_csv(deconvoluted.to_csv(index=False), 'deconvoluted.csv')

        self._commit_attachments()

        return Response(self._msg.as_string(), mimetype='multipart/form-data; boundary="%s"' % self._msg.get_boundary())
