from __future__ import annotations

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.providers.google.cloud.transfers.gdrive_to_local import GoogleDriveToLocalOperator
from typing import TYPE_CHECKING, Sequence
from airflow.models import BaseOperator
from airflow.providers.google.suite.hooks.drive import GoogleDriveHook

if TYPE_CHECKING:
    from airflow.utils.context import Context

class GoogleDriveToLocalOperator(BaseOperator):
    """
    Writes a Google Drive file into local Storage.

    .. seealso::
        For more information on how to use this operator, take a look at the guide:
        :ref:`howto/operator:GoogleDriveToLocalOperator`

    :param output_file: Path to downloaded file
    :param folder_id: The folder id of the folder in which the Google Drive file resides
    :param file_name: The name of the file residing in Google Drive
    :param gcp_conn_id: The GCP connection ID to use when fetching connection info.
    :param drive_id: Optional. The id of the shared Google Drive in which the file resides.
    :param impersonation_chain: Optional service account to impersonate using short-term
        credentials, or chained list of accounts required to get the access_token
        of the last account in the list, which will be impersonated in the request.
        If set as a string, the account must grant the originating account
        the Service Account Token Creator IAM role.
        If set as a sequence, the identities from the list must grant
        Service Account Token Creator IAM role to the directly preceding identity, with first
        account from the list granting this role to the originating account (templated).
    """

    template_fields: Sequence[str] = (
        "output_file",
        "folder_id",
        "file_name",
        "drive_id",
        "impersonation_chain",
    )

    def __init__(
        self,
        *,
        task_id: str,
        output_file: str,
        file_name: str,
        folder_id: str,
        drive_id: str | None = None,
        gcp_conn_id: str = "google_cloud_default",
        impersonation_chain: str | Sequence[str] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(task_id=task_id, **kwargs)
        self.output_file = output_file
        self.folder_id = folder_id
        self.drive_id = drive_id
        self.file_name = file_name
        self.gcp_conn_id = gcp_conn_id
        self.impersonation_chain = impersonation_chain

    def execute(self, context: Context):
        self.log.info("Executing download: %s into %s", self.file_name, self.output_file)
        gdrive_hook = GoogleDriveHook(
            gcp_conn_id=self.gcp_conn_id,
            impersonation_chain=self.impersonation_chain,
        )
        file_metadata = gdrive_hook.get_file_id(
            folder_id=self.folder_id, file_name=self.file_name, drive_id=self.drive_id
        )

        with open(self.output_file, "wb") as file:
            gdrive_hook.download_file(file_id=file_metadata["id"], file_handle=file)

MY_FILE_NAME = None
MY_OUTPUT_FILE = None
MY_FOLDER_ID = None

f = GoogleDriveToLocalOperator(
    task_id="download_file",
    output_file=MY_OUTPUT_FILE,
    file_name=MY_FILE_NAME,
    folder_id=MY_FOLDER_ID,
    drive_id=None,
    gcp_conn_id="google_cloud_default",
    impersonation_chain=None,
)

# Define the DAG
with DAG('drive_dag', start_date=datetime(2024, 1, 1),
         tags=['google_drive', 'example'],
         schedule_interval='@daily', catchup=False) as dag:

    start_task = PythonOperator(
        task_id='start_task',
        python_callable=lambda: print('hi')
    )

    download_task = GoogleDriveToLocalOperator(
        task_id='download_file',
        output_file='/path/to/local/file',
        file_name='my_file_name',
        folder_id='my_folder_id',
        drive_id=None,
        gcp_conn_id='google_cloud_default',
        impersonation_chain=None
    )

    stop_task = PythonOperator(
        task_id='stop_task',
        python_callable=lambda: print('bye')
    )

    start_task >> download_task >> stop_task