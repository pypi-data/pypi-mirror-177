#  Copyright 2022 Collate
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""
Great Expectations plugin to send flattened validation results to
Oracle database storage.

This subpackage needs to be used in Great Expectations
checkpoints actions.
"""

import functools
import os
import json
from typing import Dict, Optional, Union
from flatten_json import flatten

from great_expectations.checkpoint.actions import ValidationAction
from great_expectations.core.batch import Batch
from great_expectations.core.expectation_validation_result import (
    ExpectationSuiteValidationResult,
)
from great_expectations.data_asset.data_asset import DataAsset
from great_expectations.data_context.data_context import DataContext
from great_expectations.data_context.types.resource_identifiers import (
    ExpectationSuiteIdentifier,
    GeCloudIdentifier,
    ValidationResultIdentifier,
)
from great_expectations.exceptions import StoreBackendError
from great_expectations.validator.validator import Validator

import logging

logger = logging.getLogger(__name__)

class OracleStoreValidationResultsAction(ValidationAction):
    """Oracle Store validation action. It inherits from
    great expection validation action class and implements the
    `_run` method.

    Attributes:
        data_context: great expectation data context
        container: Azure Storage Account container
        connection_string: To connect to the Storage Account. You can find this connection string in
        the Storage Account resource in your Azure account portal.
        prefix: The folder path in your container where the .json blob will be stored.
        account_url: Url for the Azure Storage Account
    """
    

    def __init__(
        self,
        data_context: DataContext,
        username=None,
        password=None,
        hostname=None,
        port=1521,
        service_name="ORCL",
        connection_string=None,
        table_name=None
    ):
        super().__init__(data_context)
        self.username = username or os.environ.get("USERNAME")
        self.password = password or os.environ.get("PASSWORD")
        self.connection_string = connection_string or os.environ.get(
            "ORACLE_DB_CONNECTION_STRING"
        )
        self.hostname = hostname or os.environ.get("HOSTNAME")
        self.port = port or os.environ.get("PORT")
        self.service_name = service_name or os.environ.get("SERVICE_NAME")
        self.table_name = table_name or os.environ.get("TABLE_NAME")

    # pylint: disable=arguments-differ,unused-argument
    def _run(
        self,
        validation_result_suite: ExpectationSuiteValidationResult,
        validation_result_suite_identifier: Union[
            ValidationResultIdentifier, GeCloudIdentifier
        ],
        data_asset: Union[Validator, DataAsset, Batch],
        payload=None,
        expectation_suite_identifier: Optional[ExpectationSuiteIdentifier] = None,
        checkpoint_identifier=None,
    ):
        """main function to implement great expectation hook

        Args:
            validation_result_suite: result suite returned when checkpoint is ran
            validation_result_suite_identifier: type of result suite
            data_asset:
            payload:
            expectation_suite_identifier: type of expectation suite
            checkpoint_identifier: identifier for the checkpoint
        """
        logger.debug("OracleStoreValidationResultsAction.run")

        if validation_result_suite is None:
            logger.warning(
                f"No validation_result_suite was passed to {type(self).__name__} action. Skipping action."
            )
            return

        if not isinstance(
            validation_result_suite_identifier,
            (ValidationResultIdentifier, GeCloudIdentifier),
        ):
            raise TypeError(
                "validation_result_id must be of type ValidationResultIdentifier or GeCloudIdentifier, not {}".format(
                    type(validation_result_suite_identifier)
                )
            )
        
        batch_id = validation_result_suite_identifier._batch_identifier
        run_name = validation_result_suite_identifier._run_id._run_name
        
        file_name = ''.join([batch_id,'_',run_name])

        ### UNCOMMENT THE FOLLOWING 2 LINES OF CODE TO TEST THIS PLUGIN IN YOUR LOCAL FILESYSTEM
        # os.makedirs("great_expectations/uncommitted/flat_json", exist_ok=True)
        # file_key = os.path.join("great_expectations/uncommitted/flat_json", file_name)
        
        results_json = validation_result_suite.to_json_dict()
        meta = json.dumps(flatten(results_json["meta"]))
        evaluation_parameters = json.dumps(flatten(results_json["evaluation_parameters"]))
        results = []
        for each in results_json["results"]:
            results.append(json.dumps(flatten(each)))
        print(type(results))
        print(results)
        statistics = json.dumps(flatten(results_json["statistics"]))
        success = results_json["success"]

        json_object = json.dumps(flatten(validation_result_suite.to_json_dict()), indent=2)
        ### UNCOMMENT THE FOLLOWING 2 LINES OF CODE TO TEST THIS PLUGIN IN YOUR LOCAL FILESYSTEM
        # with open(file_key, "w") as outfile:
        #     outfile.write(json_object)
        self.set(file_name, meta, evaluation_parameters, statistics, success, results)
    
    @property
    @functools.lru_cache()
    def _database_client(self):

        import oracledb

        if self.connection_string:
            connection =  oracledb.connect(
                user=self.username, 
                password=self.password, 
                dsn=self.connection_string
            )
        elif self.hostname:
            print(self.hostname)
            dsn = oracledb.makedsn(self.hostname, self.port, self.service_name)
            connection = oracledb.connect(
                user=self.username, 
                password=self.password, 
                dsn=dsn
            )
        else:
            raise StoreBackendError(
                "Unable to initialize oracleDBClient, ORACLE_DB_CONNECTION_STRING should be set"
            )

        print('Connection successful!')

        return connection

    def set(self, key, meta, eval, stat, succ, results, content_encoding="utf-8", **kwargs):

        import oracledb

        sql = ('insert into {t}(BATCH_KEY, META, EVALUATION_PARAMETERS, STATISTICS, SUCCESS, RESULT) '
            'values(:key, :value, :eval, :stat, :succ, :result)'.format(t=self.table_name))
        with self._database_client.cursor() as cursor:
            try:
                for result in results:
                    cursor.execute(
                        sql,
                        [key, meta, eval, stat, succ, result]
                    )
                self._database_client.commit()
            except oracledb.Error as error:
                print('Error occurred:')
                print(error)